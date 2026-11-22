"""Short, graph-first Project 3 deck (5 slides, <= 2 minutes), clean white 16:9 Calibri aesthetic
with restrained red-pen accents and deep ASR technical content (paradigms, decoding math, A2/A3 audit,
3-seed variance, BPE truncation & dev decoder ablation).
Usage: python presentation/make_short.py
"""

import json
import math
import random
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Emu, Inches, Pt

HERE = Path(__file__).parent
FIG = HERE / "figures"
OUT = HERE / "project3-presentation-short.pptx"

BLACK = RGBColor(0x11, 0x11, 0x11)
GREY = RGBColor(0x55, 0x55, 0x55)
LIGHT = RGBColor(0xD9, 0xD9, 0xD9)
CARD_BG = RGBColor(0xFA, 0xFA, 0xFA)
BLUE = RGBColor(0x2A, 0x78, 0xD6)
ORANGE = RGBColor(0xEB, 0x68, 0x34)
TEAL = RGBColor(0x1B, 0xAF, 0x7A)
RED_DARK = RGBColor(0xC6, 0x28, 0x28)

W, H = Inches(13.333), Inches(7.5)

prs = Presentation()
prs.slide_width, prs.slide_height = W, H
BLANK = prs.slide_layouts[6]


def text(slide, x, y, w, h, s, size=18, bold=False, colour=BLACK, align=PP_ALIGN.LEFT):
    tf = slide.shapes.add_textbox(x, y, w, h).text_frame
    tf.word_wrap = True
    for i, line in enumerate(s.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line
        r.font.name, r.font.size, r.font.bold, r.font.color.rgb = "Calibri", Pt(size), bold, colour


def slide(heading, takeaway, note):
    s = prs.slides.add_slide(BLANK)
    text(s, Inches(0.45), Inches(0.24), Inches(12.4), Inches(0.72), heading, size=30, bold=True)
    if takeaway:
        text(s, Inches(0.35), Inches(6.66), Inches(12.63), Inches(0.62), takeaway, size=18, bold=True,
             align=PP_ALIGN.CENTER)
    s.notes_slide.notes_text_frame.text = note
    return s


def figure(s, name, x, y, max_w, max_h, centre=True):
    w, h = Image.open(FIG / f"{name}.png").size
    scale = min(max_w / w, max_h / h)
    pw, ph = int(w * scale), int(h * scale)
    left = x + (max_w - pw) // 2 if centre else x
    pic = s.shapes.add_picture(str(FIG / f"{name}.png"), Emu(left), Emu(y), Emu(pw), Emu(ph))
    pic.line.color.rgb, pic.line.width = LIGHT, Pt(1)
    return lambda px, py: (left + int(px * scale), y + int(py * scale))


# Restrained hand-drawn red-pen layer (max 2 callouts per figure for crispness)
PEN = RGBColor(0xE0, 0x2B, 0x2B)
WOBBLE = random.Random(3)


def pen_line(slide, points, arrow=False, weight=2.6):
    builder = slide.shapes.build_freeform(*points[0], scale=1.0)
    builder.add_line_segments(points[1:], close=False)
    shape = builder.convert_to_shape()
    shape.fill.background()
    shape.line.color.rgb, shape.line.width = PEN, Pt(weight)
    shape.shadow.inherit = False
    if arrow:
        end = OxmlElement("a:tailEnd")
        end.set("type", "arrow")
        end.set("w", "med")
        end.set("len", "med")
        shape.line._get_or_add_ln().append(end)


def circle(slide, at, cx, cy, w, h):
    points = []
    for i in range(46):
        a = -2.2 + i * (2 * math.pi * 1.12) / 45
        wob = 1 + WOBBLE.uniform(-0.03, 0.03) + 0.045 * i / 45
        points.append(at(cx + w / 2 * wob * math.cos(a), cy + h / 2 * wob * math.sin(a)))
    pen_line(slide, points)


def arrow(slide, at, start, end, bend=0.20):
    (x0, y0), (x1, y1) = start, end
    mx, my = (x0 + x1) / 2 - (y1 - y0) * bend, (y0 + y1) / 2 + (x1 - x0) * bend
    points = []
    for i in range(21):
        t = i / 20
        px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t ** 2 * x1
        py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t ** 2 * y1
        points.append(at(px + WOBBLE.uniform(-1.2, 1.2), py + WOBBLE.uniform(-1.2, 1.2)))
    pen_line(slide, points, arrow=True)


def scribble(slide, at, px, py, words, size=14.5, width=Inches(3.2), rotation=-1.2):
    x, y = at(px, py)
    box = slide.shapes.add_textbox(Emu(x), Emu(y), width, Inches(0.95))
    box.rotation = rotation
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(words.split("|")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = p.add_run()
        r.text = line
        r.font.name, r.font.size, r.font.bold, r.font.color.rgb = "Ink Free", Pt(size), True, PEN


def card(s, x, y, w, h, border=LIGHT, fill=CARD_BG):
    box = s.shapes.add_shape(1, x, y, w, h)
    box.fill.solid()
    box.fill.fore_color.rgb = fill
    box.line.color.rgb = border
    box.line.width = Pt(1)
    box.shadow.inherit = False
    return box


coords = json.loads((FIG / "coords.json").read_text(encoding="utf-8"))

# ==============================================================================
# 1. COVER + AUTHOR (merged — zero wasted slide click, clean photo space on right) (~5 s)
# ==============================================================================
s = prs.slides.add_slide(BLANK)
text(s, Inches(0.8), Inches(1.95), Inches(8.6), Inches(1.0),
     "Georgian speech recognition", size=42, bold=True)
text(s, Inches(0.8), Inches(3.00), Inches(8.6), Inches(1.25),
     "Low-resource ASR across four paradigms:\nclassical GMM-HMM, fine-tuned Enc-Dec & CTC + KenLM,\nand why Whisper cuts off long Georgian clips",
     size=20, colour=GREY)
text(s, Inches(0.8), Inches(4.85), Inches(8.6), Inches(0.90),
     "İsmet Efe Balık  ·  2509011061\nCOE025 Natural Language Processing  ·  Project 3  ·  group “stray” (solo)",
     size=16, bold=True, colour=BLACK)

# Subtle technical scope strip along bottom
card(s, Inches(0.8), Inches(6.05), Inches(11.73), Inches(0.72), border=LIGHT, fill=CARD_BG)
text(s, Inches(0.95), Inches(6.18), Inches(11.43), Inches(0.45),
     "147.5 h CV train  ·  3.1 h FLEURS test  ·  4 ASR paradigms  ·  3-seed variance  ·  95% cluster bootstrap  ·  pinned HF revisions",
     size=14.2, bold=True, colour=GREY, align=PP_ALIGN.CENTER)

s.notes_slide.notes_text_frame.text = (
    "~5 s (12 words).\n"
    "SAY: Georgian speech recognition — I'm İsmet Efe Balık, group stray, working solo.\n"
    "(Optional in Canva: drop your portrait photo in the open right space at x=9.8..12.4 in.)"
)

# ==============================================================================
# 2. THE TASK, REAL GEORGIAN EXAMPLE & FOUR ASR PARADIGMS (~22 s)
# ==============================================================================
s = slide(
    "the task: Georgian ASR across four paradigms",
    "Architecture ≠ checkpoint ≠ our contribution — all four lecture paradigms evaluated on the same two test sets.",
    "~22 s (49 words). WHAT LANGUAGE, ARCHITECTURE VS CHECKPOINT, OUR CONTRIBUTION.\n"
    "SAY: Georgian is low-resource: Canary, Parakeet and Qwen3-ASR don't support it. I benchmark all four "
    "lecture paradigms, separating architecture from checkpoints: a Kaldi GMM-HMM I trained myself, Whisper, "
    "wav2vec-2 CTC, and NVIDIA's transducer. My contribution is fine-tuning Whisper-turbo and a small MMS "
    "adapter, plus a 3-gram language-model decoder.\n\n"
    "IF ASKED:\n"
    "- Eligibility: non-English, eligibility confirmed, unique in class register (group 'stray').\n"
    "- Real example on top: in agglutinative Georgian, pretrained greedy MMS drops the 1-letter genitive suffix -s "
    "(საქართველოს → საქართველო, 30× on CV test; MMS FT+LM cuts dropped -s from 32 to 10 clips).\n"
    "- Unsupported baselines (A3, links in README): Canary v2 (25 EU), Parakeet v3 (25 EU), "
    "Qwen3-ASR (30 langs); no Georgian HuBERT+CTC ASR checkpoint found on HF Hub.\n"
    "- Shallow fusion equation: argmax_W [ log P_CTC(W|X) + α log P_LM(W) + β|W| ], with α=0.5, β=0 chosen on dev.\n"
    "- Fine-tuning setup: Whisper-turbo full FT (809M, 6,000 steps × 16, ≈1 epoch, A100); MMS kat adapter-only FT "
    "(2.3M adapter + head, backbone frozen, 3,000 steps, ctc_zero_infinity=True to fix NaN CTC loss)."
)

# Real ASR-native example banner (shows concrete Georgian morphology error -> LM fix!)
card(s, Inches(0.45), Inches(1.00), Inches(12.43), Inches(0.92), border=LIGHT, fill=RGBColor(0xF8, 0xFA, 0xFC))
tf = s.shapes.add_textbox(Inches(0.62), Inches(1.06), Inches(12.1), Inches(0.44)).text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
for txt, col, bld in [
    ("Real CV test example:  ", BLACK, True),
    ("Ref ", GREY, False), ("საქართველოს  ", BLACK, True),
    ("→  MMS greedy ", GREY, False), ("საქართველო ", RED_DARK, True),
    ("(30× on CV test)  →  ", GREY, False),
    ("FT + 3-gram LM ", BLUE, True), ("საქართველოს ✓", TEAL, True),
]:
    r = p.add_run()
    r.text = txt
    r.font.name, r.font.size, r.font.bold, r.font.color.rgb = "Calibri", Pt(15), bld, col

text(s, Inches(0.62), Inches(1.50), Inches(12.1), Inches(0.36),
     "Low-resource ka: Canary v2, Parakeet v3 & Qwen3-ASR lack Georgian (model cards in README); zero-shot Whisper-small & turbo loop >100% WER.",
     size=13.8, colour=GREY)

# 4 paradigm cards packed with clean, concrete ASR technical depth (objectives, decoding math, params)
cards_spec = [
    ("GMM-HMM", "MFCC + LDA + MLLT + SAT",
     "CLASSICAL BASELINE",
     "Kaldi tri3b (trained by us, CPU)\n91k closed graphemic lexicon\n+ Kneser-Ney 3-gram LM",
     "DECODING & ROLE",
     "Per-speaker CMVN + 2-pass\nfMLLR SAT; lattice decode\n(LMWT/WIP frozen on dev)", False),
    ("Enc-Dec", "Transformer Seq2Seq",
     "PRETRAINED BASELINES",
     "openai/whisper-small,\nwhisper-large-v3,\nwhisper-large-v3-turbo",
     "OUR CONTRIBUTION",
     "Full FT whisper-turbo (809M)\nCE loss, orthographic targets\n+ 14 s pause-chunk ablation", True),
    ("CTC", "wav2vec 2.0 encoder",
     "PRETRAINED BASELINES",
     "xsway/wav2vec2-large-\nxlsr-georgian,\nfacebook/mms-1b-all (kat)",
     "OUR CONTRIBUTION",
     "kat adapter FT (2.3M, zero_inf)\n+ beam-100 shallow fusion:\nlog P_CTC + α log P_LM + β|W|", True),
    ("Transducer", "FastConformer RNN-T",
     "PRETRAINED BASELINE",
     "nvidia/stt_ka_fastconformer\n_hybrid_large_pc\n(NeMo RNN-T head)",
     "AUDIT FINDING",
     "CV 17.0 + FLEURS train/dev\n→ excluded on CV; FLEURS\ntest held out (valid baseline)", False),
]

for i, (arch, sub, base_hdr, base, ours_hdr, ours, is_ours) in enumerate(cards_spec):
    x = Inches(0.45 + i * 3.16)
    card(s, x, Inches(2.08), Inches(2.96), Inches(4.36),
         border=BLUE if is_ours else LIGHT,
         fill=RGBColor(0xF6, 0xFA, 0xFF) if is_ours else CARD_BG)
    text(s, x + Inches(0.1), Inches(2.18), Inches(2.76), Inches(0.46),
         arch, size=24, bold=True, align=PP_ALIGN.CENTER)
    text(s, x + Inches(0.1), Inches(2.65), Inches(2.76), Inches(0.32),
         sub, size=13.5, colour=GREY, align=PP_ALIGN.CENTER)

    text(s, x + Inches(0.10), Inches(3.08), Inches(2.76), Inches(0.28),
         base_hdr, size=11.5, bold=True, colour=GREY, align=PP_ALIGN.CENTER)
    text(s, x + Inches(0.08), Inches(3.36), Inches(2.80), Inches(1.14),
         base, size=13.8, colour=BLACK, align=PP_ALIGN.CENTER)

    tag_col = BLUE if is_ours else GREY
    text(s, x + Inches(0.10), Inches(4.62), Inches(2.76), Inches(0.28),
         ours_hdr, size=11.5, bold=True, colour=tag_col, align=PP_ALIGN.CENTER)
    text(s, x + Inches(0.06), Inches(4.92), Inches(2.84), Inches(1.36),
         ours, size=13.8, bold=is_ours, colour=BLACK if is_ours else GREY, align=PP_ALIGN.CENTER)

# ==============================================================================
# 3. THE BENCHMARK: BASELINES VS OURS (~34 s) — CLEAN, RESTRAINED RED CALLOUTS!
# ==============================================================================
s = slide(
    "the benchmark: baselines vs ours (frozen test)",
    "MMS FT + 3-gram LM wins fair CV (11.07%, 340×); Whisper FT wins punctuation (15.9%); NVIDIA leads FLEURS (15.5%).",
    "~34 s (60 words). THE MAIN BENCHMARK SLIDE.\n"
    "SAY: Here is the frozen benchmark with 95-percent intervals. The best pretrained baseline, MMS, scores "
    "24 percent. Fine-tuned Whisper reaches 12.8 and wins when punctuation counts. In a follow-up round, MMS "
    "plus our 3-gram LM reaches 11.0 to 11.1 percent over three seeds, and runs eight-and-a-half times faster. "
    "On clean FLEURS, NVIDIA still leads at 15.5.\n\n"
    "IF ASKED:\n"
    "- Round 1 vs Round 2: Round 1 (Whisper FT, MMS FT) was blind test; Round 2 (+LM, r2 retrain) is disclosed "
    "as follow-up on a reused test set (all settings still selected strictly on dev).\n"
    "- Key paired bootstrap Δ WER (positive = ours better): Turbo FT vs MMS zero-shot +11.34 [10.91, 11.75]; "
    "MMS FT+LM vs Turbo FT +1.73 [1.33, 2.12]; MMS FT+LM vs MMS zero-shot+LM +2.44 [2.16, 2.74].\n"
    "- 3-seed MMS FT (seeds 42/7/13): greedy CV 21.97±0.06%, +LM CV 11.04±0.06%, FLEURS 19.17±0.10%. "
    "Three headline paired comparisons keep their sign with 95% CIs excluding 0 across all 3 seeds "
    "(greedy MMS FT vs zero-shot on FLEURS has CIs crossing 0 for seeds 7 and 13).\n"
    "- On FLEURS CER, MMS FT+LM beats NVIDIA (4.64% vs 5.32%, Δ +0.67 [0.33, 1.05]).\n"
    "- Kaldi tri3b uses CV-train 3-gram LM + test-time speaker SAT; our two best neural systems beat it by 9.9-11.6 pts "
    "(greedy MMS FT beats it by 0.64 pts, with less than half the CER)."
)

at_b = figure(s, "benchmark", Inches(0.35), Inches(1.04), Inches(12.63), Inches(5.48), centre=True)
cb = coords["benchmark"]

# Restrained red layer: ONLY 2 crisp callouts + 1 clean highlight ring on Whisper Ortho (15.9%)!
circle(s, at_b, cb["nvidia_fl"][0] - 8, cb["nvidia_fl"][1], 210, 52)
scribble(s, at_b, 1410, 500, "LEADS CLEAN FLEURS!", size=14.2, width=Inches(2.8), rotation=-1.0)
arrow(s, at_b, (1395, 525), (1260, 542), bend=0.12)

# Clean ring only on Whisper FT orthographic win (no noisy extra text/arrow)
circle(s, at_b, cb["whisper_ortho"][0], cb["whisper_ortho"][1], 162, 62)

# Main headline callout on MMS FT + LM (nudged left so 11.1) stays well clear of the table border)
circle(s, at_b, cb["mms_lm_cv"][0] + 15, cb["mms_lm_cv"][1], 205, 56)
circle(s, at_b, cb["mms_lm_rtfx"][0], cb["mms_lm_rtfx"][1], 150, 56)
scribble(s, at_b, 1360, 868, "BEST FAIR CV (3 SEEDS: 11.0-11.1)|8.5x FASTER THAN WHISPER!", size=13.2, width=Inches(3.35), rotation=-0.8)
arrow(s, at_b, (1350, 912), (1260, 912), bend=0.08)

# ==============================================================================
# 4. CAN WE TRUST IT? SPLITS (A2 COMPLETE), CV17 OVERLAP & 4 METRICS (~24 s)
# ==============================================================================
s = slide(
    "can we trust it? splits, CV17 overlap & 4 metrics",
    "Speaker-disjoint splits (0 raw verbatim overlap), clip-age check for CV17, and 4 metrics exposing every trade-off.",
    "~24 s (47 words). SPLITS, CONTAMINATION EVIDENCE & METRIC JUSTIFICATION.\n"
    "SAY: We train on 147 hours of Common Voice with zero speaker or raw verbatim overlap. Left: NVIDIA jumps "
    "13 times from 1.8 to 23 percent on the newest clips, versus 1.5 to 3 times for other models, consistent "
    "with CV17 overlap. Right: CER exposes Kaldi, and punctuation flips the winner.\n\n"
    "IF ASKED:\n"
    "- Split audit (A2): Train 99,768 utt / 147.5 h / 139 spk; Dev 14,216 utt / 23.2 h / 221 spk; "
    "Test 14,259 utt / 23.3 h / 1,058 spk. 0 shared speakers; 0 raw verbatim test sentences in train "
    "(18 / 0.13% after norm). FLEURS: dev 409 utt (1.2 h), test 979 utt (3.1 h), 0 overlap with CV train.\n"
    "- Why 'consistent with' not 'proven': NVIDIA's card lists CV 17.0 without clip IDs. NVIDIA degrades 13× "
    "(1.77% in 40.0-40.3M bin to 22.98% in 44M+) while MMS, Kaldi, and Whisper FT degrade only 1.5-3×.\n"
    "- Why corpus WER (HF Audio Course ch. 5): pools (S+D+I)/N and can exceed 100%, exposing Whisper loops "
    "(WAcc breaks >100%). 1 corrupted CV test ref ('????') excluded identically and logged separately.\n"
    "- Why CER: Georgian is agglutinative (1 wrong suffix letter breaks a word); Kaldi (22.6% WER, 8.2% CER) vs "
    "greedy MMS FT (22.0% WER, 3.6% CER) shows 2.3x higher CER at identical WER."
)

# A2-COMPLETE split strip: hours + utterances + speakers for EVERY split!
splits_strip = [
    ("147.5 h", "CV train · 99,768 utt · 139 spk", BLUE, CARD_BG),
    ("23.2 h",  "CV dev · 14,216 utt · 221 spk",   BLACK, CARD_BG),
    ("23.3 h",  "CV test · 14,259 utt · 1,058 spk\n0 spk leak · 0 raw verbatim (0.1% norm.)", BLUE, RGBColor(0xF6, 0xFA, 0xFF)),
    ("3.1 h",   "FLEURS test · 979 utt (dev 409 / 1.2 h)\nOOD for our CV train", ORANGE, RGBColor(0xFF, 0xF8, 0xF4)),
]
for i, (num, sub, col, bg) in enumerate(splits_strip):
    x = Inches(0.45 + i * 3.16)
    card(s, x, Inches(1.02), Inches(2.96), Inches(1.00), border=col if i >= 2 else LIGHT, fill=bg)
    text(s, x + Inches(0.08), Inches(1.03), Inches(2.80), Inches(0.44), num, size=26, bold=True, colour=col,
         align=PP_ALIGN.CENTER)
    text(s, x + Inches(0.04), Inches(1.48), Inches(2.88), Inches(0.50), sub, size=10.6, colour=GREY,
         align=PP_ALIGN.CENTER)

at_dm = figure(s, "data_and_metrics", Inches(0.35), Inches(2.14), Inches(12.63), Inches(4.36), centre=True)
cdm = coords["data_and_metrics"]

# Restrained red layer: ONLY 1 clean red callout per panel (accurate 13x vs 1.5-3x framing!)
circle(s, at_dm, cdm["nvidia_cliff"][0] + 15, cdm["nvidia_cliff"][1], 210, 82)
scribble(s, at_dm, 875, 622, "1.8% -> 23% (13x VS 1.5-3x)|CONSISTENT WITH CV17 OVERLAP", size=12.0, width=Inches(3.05), rotation=-0.8)
arrow(s, at_dm, (1185, 608), (1255, 482), bend=0.22)

# Tight circle around 15.9 (width 92 so it never clips 12.8!)
circle(s, at_dm, cdm["whisper_ortho_bar"][0] + 4, cdm["whisper_ortho_bar"][1] - 16, 92, 74)
scribble(s, at_dm, 2010, 295, "PUNCT. FLIPS|THE WINNER!", size=13.2, width=Inches(1.8), rotation=-1.5)
arrow(s, at_dm, (2175, 408), (2215, 480), bend=-0.12)

# ==============================================================================
# 5. WHY MODELS BREAK: TWO MECHANISMS (~22 s)
# ==============================================================================
s = slide(
    "why models break: two mechanisms",
    "BPE inflation truncates Whisper at ~14.5 s (short tails broke chunking); the 3-gram LM gives ~all the −11 pt CTC gain.",
    "~22 s (44 words). ERROR ANALYSIS & MECHANISMS.\n"
    "SAY: Two mechanisms explain the errors. Left: Whisper spends about 20 tokens per Georgian word, cutting "
    "off around 14.5 seconds. Pause chunking cut long-clip error 41 percent, but looped on short tails, a "
    "negative result. Right: dev ablation shows the LM drives almost the entire 11-point gain.\n\n"
    "IF ASKED:\n"
    "- Why 20.6 tokens/word? Georgian letters are 3 UTF-8 bytes each; Whisper's byte-BPE has almost no Georgian "
    "merges (~1 tok/byte, ~31 tok/s → 448 cap ≈ 14.5 s at observed FLEURS rate; 22% of FLEURS exceeds it).\n"
    "- Exact pooled >=16 s chunking result (94 FLEURS clips): WER dropped 45.10% → 26.45% (-41% relative), "
    "but overall FLEURS WER worsened 27.33% → 30.00% because 41 of 53 clips in 14-15 s looped on short silent tails "
    "(all 49 looping clips caused 73% of insertions: 1,049 of 1,441). Balanced splitting is in the harness, deliberately not re-tested on test.\n"
    "- Whisper >30 s batch bug (Round 3 fix): found by review & re-run once on FLEURS; r2 moved 27.33 → 27.27% (n.s.); rankings unchanged.\n"
    "- Digits mismatch: 0 of 99,768 CV train transcripts have digits vs 20% of FLEURS test; explains 77% of the "
    "MMS FT+LM vs zero-shot+LM gap on FLEURS (19.28% vs 18.36%, both with LM)."
)

at_d = figure(s, "diagnostics", Inches(0.35), Inches(1.08), Inches(12.63), Inches(5.40), centre=True)
cd = coords["diagnostics"]

# Restrained red layer: 1 crisp callout per panel (right circle narrowed so it never clips "(beam alone)"!)
circle(s, at_d, cd["tail_spike"][0], cd["tail_spike"][1] - 12, 130, 82)
scribble(s, at_d, 645, 365, "41/53 CLIPS LOOP!|SHORT SILENT TAIL", size=14.0, width=Inches(2.4), rotation=-1.5)
arrow(s, at_d, (640, 385), (595, 302), bend=-0.2)

circle(s, at_d, cd["lm_delta"][0] + 12, cd["lm_delta"][1], 275, 102)
scribble(s, at_d, 2365, 70, "LM = ~ALL OF|THE GAIN!", size=13.5, width=Inches(1.85), rotation=-1.0)
arrow(s, at_d, (2485, 165), (2515, 222), bend=-0.15)

prs.save(OUT)
print("Saved:", OUT)
