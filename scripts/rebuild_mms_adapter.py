"""Rebuild an MMS adapter-only fine-tune (final/ dir) from the pinned base model + our backed-up adapter tensors.

Our MMS fine-tunes train only the language adapter + lm_head (`adapter_only`). The Colab watcher backs up just those
tensors (adapter_head.safetensors). Base + adapter are the whole model, so this restores it exactly:

    uv run python scripts/rebuild_mms_adapter.py <adapter_head.safetensors> <out_dir> --lang kat --train-manifest <runs/train_*/train_manifest.json>

The train manifest is copied in, so runs of the rebuilt model are labelled "ours" like the original.
"""

from __future__ import annotations

import argparse
import shutil

import torch
from safetensors.torch import load_file, save_file
from transformers import AutoModelForCTC, AutoProcessor

REV = "3d33597edbdaaba14a8e858e2c8caa76e3cec0cd"  # facebook/mms-1b-all, as pinned in every MMS config


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("adapter")
    ap.add_argument("out")
    ap.add_argument("--lang", required=True)
    ap.add_argument("--train-manifest", required=True)
    a = ap.parse_args()
    ours = load_file(a.adapter)
    model = AutoModelForCTC.from_pretrained("facebook/mms-1b-all", revision=REV, target_lang=a.lang,
                                            ignore_mismatched_sizes=True, layerdrop=0.0)
    _, unexpected = model.load_state_dict(ours, strict=False)
    assert not unexpected, unexpected
    sd = model.state_dict()
    assert all(torch.equal(sd[k], ours[k]) for k in ours)
    model.save_pretrained(a.out)
    # Where `load_adapter(target_lang)` looks (as asrbench train writes it), so run configs keep target_lang.
    save_file({k: v.contiguous() for k, v in ours.items()}, f"{a.out}/adapter.{a.lang}.safetensors")
    p = AutoProcessor.from_pretrained("facebook/mms-1b-all", revision=REV)
    p.tokenizer.set_target_lang(a.lang)
    p.save_pretrained(a.out)
    shutil.copy(a.train_manifest, f"{a.out}/train_manifest.json")
    print("rebuilt", a.out, len(ours), "adapter/head tensors")


if __name__ == "__main__":
    main()
