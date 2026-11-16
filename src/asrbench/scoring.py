"""`asrbench score` and `asrbench compare`.

score   -> <run>/scores.json, <run>/item_scores.jsonl, <run>/report.md
compare -> paired bootstrap on matched item IDs (S24, S77), printed as Markdown.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from .bootstrap import corpus_rate_ci, paired_delta_ci
from .metrics import ItemScore, corpus_metrics, score_item, silence_report, top_substitutions
from .normalize import PolicySet, load_policies


def read_predictions(run_dir: Path) -> list[dict]:
    path = Path(run_dir) / "predictions.jsonl"
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _cluster(p: dict) -> str:
    return p.get("session") or p.get("speaker") or p["id"]


def _score_all(preds: list[dict], policies: PolicySet) -> dict[str, list[tuple[dict, ItemScore]]]:
    by_lang: dict[str, list] = defaultdict(list)
    for p in preds:
        pol = policies.for_language(p["language"])
        by_lang[p["language"]].append((p, score_item(p["id"], p["reference"], p["hypothesis"], pol)))
    return by_lang


def _pct(x):
    return "—" if x is None else f"{100 * x:.2f}%"


def score(run_dir: str | Path, policy_path: str | None = None, n_boot: int = 2000) -> dict:
    run_dir = Path(run_dir)
    policies = load_policies(policy_path)
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    by_lang = _score_all(read_predictions(run_dir), policies)

    results = {"run": manifest.get("name"), "split": manifest.get("split"), "model": manifest.get("model"),
               "scoring_policy": policies.to_dict(), "policy_file": policy_path, "languages": {}}
    with (run_dir / "item_scores.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for lang, rows in sorted(by_lang.items()):
            scores = [s for _, s in rows]
            m = corpus_metrics(scores)
            speech = [(p, s) for p, s in rows if not s.is_silence]
            keys = [_cluster(p) for p, _ in speech]
            if speech and speech[0][1].words is not None:
                m["wer_ci"] = corpus_rate_ci(keys, [s.words.errors for _, s in speech],
                                             [s.words.n_ref for _, s in speech], n_boot=n_boot)
            m["cer_ci"] = corpus_rate_ci(keys, [s.chars.errors for _, s in speech],
                                         [s.chars.n_ref for _, s in speech], n_boot=n_boot)
            audio = sum(p["audio_sec"] for p, _ in rows)
            compute = sum(p["compute_sec"] for p, _ in rows)
            m["audio_sec"] = round(audio, 2)
            m["rtf"] = compute / audio if audio else None
            m["silence"] = silence_report(scores)
            m["top_substitutions"] = top_substitutions(scores)
            worst = sorted(speech, key=lambda r: -(r[1].words.errors if r[1].words else r[1].chars.errors))[:10]
            m["worst_items"] = [{"id": s.id, "ref": s.ref_norm, "hyp": s.hyp_norm,
                                 "errors": (s.words or s.chars).as_dict()} for _, s in worst]
            results["languages"][lang] = m
            for p, s in rows:
                f.write(json.dumps({"id": s.id, "language": lang, "ref_norm": s.ref_norm, "hyp_norm": s.hyp_norm,
                                    "words": s.words.as_dict() if s.words else None,
                                    "chars": s.chars.as_dict()}, ensure_ascii=False) + "\n")

    (run_dir / "scores.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    (run_dir / "report.md").write_text(render_report(results, manifest), encoding="utf-8")
    return results


def render_report(results: dict, manifest: dict) -> str:
    model = manifest.get("model", {})
    hw = manifest.get("env", {}).get("hardware", {})
    lines = [
        f"# {results['run']} ({results['split']})",
        "",
        f"- Model: `{model.get('model_id')}` @ `{model.get('revision_resolved') or model.get('revision_requested')}` "
        f"({model.get('family')}, {model.get('dtype')}, {model.get('device')})",
        f"- Hardware: {hw.get('gpu', 'CPU')}; batch size {manifest.get('batch_size')}",
        f"- Dataset: `{manifest['dataset']['path']}` sha256 `{manifest['dataset']['sha256'][:12]}`",
        f"- Timing boundary: {manifest.get('timing_boundary')}",
        "",
        "| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | MER | WIL | RTF | Silent clips w/ output |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for lang, m in results["languages"].items():
        wci, cci = m.get("wer_ci"), m.get("cer_ci")
        sil = m["silence"]
        lines.append("| " + " | ".join([
            lang, str(m["items"]), f"{m['audio_sec']:.0f}", _pct(m.get("wer")),
            f"{_pct(wci['low'])} – {_pct(wci['high'])}" if wci else "—", _pct(m.get("mean_clip_wer")),
            _pct(m.get("cer")), f"{_pct(cci['low'])} – {_pct(cci['high'])}" if cci else "—",
            _pct(m.get("mer")), _pct(m.get("wil")), f"{m['rtf']:.3f}" if m.get("rtf") else "—",
            f"{sil['items_with_output']}/{sil['silent_items']}",
        ]) + " |")
    lines += ["", "WER/CER are corpus rates (pooled edit counts / pooled reference units). CIs: cluster bootstrap "
              "over sessions/speakers. No cross-language average is shown on purpose (S19).", ""]
    for lang, m in results["languages"].items():
        lines += [f"## {lang}", "", f"Word counts: {m.get('word_counts')}  ", f"Char counts: {m['char_counts']}", "",
                  "Top substitutions (ref → hyp × n): " + ", ".join(f"{r}→{h}×{n}" for r, h, n in m["top_substitutions"][:10]),
                  "", "Worst items:", ""]
        for w in m["worst_items"][:5]:
            lines += [f"- `{w['id']}` {w['errors']}", f"  - ref: {w['ref']}", f"  - hyp: {w['hyp']}"]
        lines.append("")
    return "\n".join(lines)


def compare(run_a: str | Path, run_b: str | Path, policy_path: str | None = None, n_boot: int = 2000) -> str:
    policies = load_policies(policy_path)
    a = {p["id"]: p for p in read_predictions(Path(run_a))}
    b = {p["id"]: p for p in read_predictions(Path(run_b))}
    shared = sorted(set(a) & set(b))
    mismatched = [i for i in shared if a[i]["reference"] != b[i]["reference"]]
    if mismatched:
        raise ValueError(f"{len(mismatched)} shared IDs have different references, e.g. {mismatched[0]}")
    lines = [f"A = `{Path(run_a).name}`  ", f"B = `{Path(run_b).name}`  ",
             f"Matched items: {len(shared)} (A only: {len(set(a) - set(b))}, B only: {len(set(b) - set(a))})", "",
             "| Language | Items | WER A | WER B | Δ (A−B) | 95% CI | P(A better) | CER A | CER B | Δ CER | 95% CI |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    by_lang = defaultdict(list)
    for i in shared:
        by_lang[a[i]["language"]].append(i)
    for lang, ids in sorted(by_lang.items()):
        pol = policies.for_language(lang)
        sa = [score_item(i, a[i]["reference"], a[i]["hypothesis"], pol) for i in ids]
        sb = [score_item(i, b[i]["reference"], b[i]["hypothesis"], pol) for i in ids]
        keep = [k for k, s in enumerate(sa) if not s.is_silence]
        keys = [_cluster(a[ids[k]]) for k in keep]
        cells = [lang, str(len(keep))]
        if sa[0].words is not None:
            w = paired_delta_ci(keys, [sa[k].words.errors for k in keep], [sb[k].words.errors for k in keep],
                                [sa[k].words.n_ref for k in keep], n_boot=n_boot)
            ma, mb = corpus_metrics(sa), corpus_metrics(sb)
            cells += [_pct(ma["wer"]), _pct(mb["wer"]), _pct(w["delta"]), f"{_pct(w['low'])} – {_pct(w['high'])}",
                      f"{w['p_a_better']:.2f}"]
        else:
            ma, mb = corpus_metrics(sa), corpus_metrics(sb)
            cells += ["—"] * 5
        c = paired_delta_ci(keys, [sa[k].chars.errors for k in keep], [sb[k].chars.errors for k in keep],
                            [sa[k].chars.n_ref for k in keep], n_boot=n_boot)
        cells += [_pct(ma["cer"]), _pct(mb["cer"]), _pct(c["delta"]), f"{_pct(c['low'])} – {_pct(c['high'])}"]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"
