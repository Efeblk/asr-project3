"""Generate crisp, classroom-readable matplotlib figures for the 2-minute Project 3 deck.
Consistent color semantics across the entire deck:
  BLUE (#2A78D6)   = Common Voice ka (in-domain)
  ORANGE (#EB6834) = FLEURS ka (out-of-domain for our CV training)
Other charts use distinct non-CV/FLEURS hues (Navy, Purple, Teal, Red, Slate).
Outputs:
  presentation/figures/benchmark.png        (Slide 3)
  presentation/figures/data_and_metrics.png (Slide 4)
  presentation/figures/diagnostics.png      (Slide 5)
  presentation/figures/coords.json          (Exact pixel coordinates for red-pen overlays)
"""

from pathlib import Path
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUT_DIR = Path(__file__).parent / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Calibri", "DejaVu Sans"],
    "axes.edgecolor": "#CCCCCC",
    "axes.linewidth": 0.9,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})

# Consistent corpus colors
BLUE = "#2A78D6"      # Common Voice ka
ORANGE = "#EB6834"    # FLEURS ka

# Non-corpus chart colors
NAVY = "#355070"      # Norm. WER / Plain Whisper r2
PURPLE = "#8E5BD0"    # Ortho. WER (punctuation)
TEAL = "#1BAF7A"      # CER / Positive chunking win
RED = "#C62828"       # Alert / Contamination / Loop spike
SLATE = "#95A5A6"     # Untouched / Secondary baseline
DARK = "#111111"
GREY = "#555555"
LIGHT_GREY = "#E8E8E8"


def data_to_img_px(fig, ax, x, y, dpi):
    """Convert axes data coordinates (x, y) to top-left-origin PNG pixel coordinates."""
    disp_x, disp_y = ax.transData.transform((x, y))
    fig_h_px = fig.get_figheight() * dpi
    return round(float(disp_x), 1), round(float(fig_h_px - disp_y), 1)


def make_benchmark():
    dpi = 220
    fig = plt.figure(figsize=(12.2, 5.25), dpi=dpi)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.85, 0.92], wspace=0.04,
                          left=0.315, right=0.985, top=0.835, bottom=0.165)
    ax = fig.add_subplot(gs[0])
    ax_tbl = fig.add_subplot(gs[1], sharey=ax)

    # (label, group, cv_wer, cv_lo, cv_hi, fl_wer, fl_lo, fl_hi, fl_mark, cv_cer, ortho_cv, rtfx, flags)
    rows = [
        # Baselines
        ("Whisper-large-v3 (zero-shot)",          "base", 72.04, 71.05, 73.04, 69.68, 68.29, 71.02, "‡", "16.6%", "74.7%",  "12×",  ""),
        ("XLS-R-300M xsway (CTC)",                "base", 46.26, 45.05, 47.58, 52.49, 51.12, 53.87, "",   "9.0%", "57.9%", "788×",  ""),
        ("MMS-1b-all + kat (best pretrained)",    "base", 24.14, 23.22, 25.18, 25.32, 24.22, 26.48, "",   "4.5%", "40.1%", "382×",  ""),
        ("Kaldi tri3b (GMM-HMM + LM + SAT)",      "base", 22.64, 21.60, 23.76, 39.64, 37.99, 41.32, "",   "8.2%", "39.6%",  "33×*", ""),
        ("NVIDIA FastConformer (RNN-T)",          "base",  4.85,  4.49,  5.23, 15.49, 14.25, 16.80, "",  "1.3%†", "9.5%†", "253×",  "contam"),
        # Ours — Round 1 (blind test)
        ("MMS kat adapter FT (2.3M, greedy)",     "r1",   22.00, 21.16, 22.97, 26.02, 24.88, 27.22, "",   "3.6%", "39.2%", "357×",  ""),
        ("Whisper-turbo full FT (809M, r1)",      "r1",   12.80, 12.02, 13.65, 27.47, 25.58, 29.45, "§",  "2.6%", "15.9%",  "40×",  "ortho_best"),
        # Round 2 (follow-up on reused test: ablation + ours+decoder)
        ("MMS zero-shot + 3-gram LM (ablation)",  "r2",   13.50, 12.73, 14.39, 18.36, 17.28, 19.50, "",   "3.1%", "32.2%", "341×",  ""),
        ("MMS adapter FT + 3-gram LM (seed 42)",  "r2",   11.07, 10.47, 11.72, 19.28, 18.14, 20.51, "",   "2.1%", "30.5%", "340×",  "cv_best"),
    ]

    y_pos = []
    cur = 0.0
    prev_grp = None
    group_seps = []
    for r in rows:
        grp = r[1]
        if prev_grp is not None and grp != prev_grp:
            cur += 0.55
            group_seps.append(cur - 0.775)
        y_pos.append(cur)
        cur += 1.0
        prev_grp = grp

    for y, r in zip(y_pos, rows):
        if r[1] in ("r1", "r2"):
            bg = "#F4F8FF" if r[1] == "r1" else "#F2FBF7"
            ax.axhspan(y - 0.44, y + 0.44, color=bg, zorder=0)
            ax_tbl.axhspan(y - 0.44, y + 0.44, color=bg, zorder=0)

    for sep in group_seps:
        ax.axhline(sep, color="#BBBBBB", linestyle="--", linewidth=1.1, zorder=1)
        ax_tbl.axhline(sep, color="#BBBBBB", linestyle="--", linewidth=1.1, zorder=1)

    ax.text(77.5, y_pos[2] - 0.10, "BASELINES", fontsize=9.8, fontweight="bold",
            color=GREY, ha="right", va="center")
    ax.text(77.5, y_pos[5] - 0.10, "OURS · ROUND 1 (BLIND)", fontsize=9.8, fontweight="bold",
            color=BLUE, ha="right", va="center")
    ax.text(77.5, y_pos[7] - 0.10, "ROUND 2 · DECODER FOLLOW-UP", fontsize=9.6, fontweight="bold",
            color=TEAL, ha="right", va="center")

    for y, r in zip(y_pos, rows):
        label, grp, cv, cv_lo, cv_hi, fl, fl_lo, fl_hi, fl_mk, cer, ortho, rtfx, flag = r
        is_contam = (flag == "contam")

        if is_contam:
            ax.errorbar(cv, y - 0.15, xerr=[[cv - cv_lo], [cv_hi - cv]],
                        fmt="o", color=RED, markerfacecolor="white", markeredgewidth=2.2,
                        markersize=7.2, elinewidth=2.0, capsize=3, zorder=4)
            ax.text(cv + 1.5, y - 0.15, f"{cv:.2f}%†", fontsize=10.4, fontweight="bold",
                    color=RED, va="center", ha="left")
        else:
            ax.errorbar(cv, y - 0.15, xerr=[[cv - cv_lo], [cv_hi - cv]],
                        fmt="o", color=BLUE, markersize=7.2, elinewidth=2.0, capsize=3, zorder=4)
            txt_x = cv_hi + 1.2 if cv < 64 else cv_lo - 1.3
            ha = "left" if cv < 64 else "right"
            ax.text(txt_x, y - 0.15, f"{cv:.2f}%", fontsize=10.2,
                    fontweight="bold" if flag in ("cv_best", "ortho_best") else "normal",
                    color=BLUE, va="center", ha=ha)

        ax.errorbar(fl, y + 0.18, xerr=[[fl - fl_lo], [fl_hi - fl]],
                    fmt="D", color=ORANGE, markersize=6.2, elinewidth=2.0, capsize=3, zorder=4)
        fl_txt_x = fl_hi + 1.2 if fl < 62 else fl_lo - 1.3
        fl_ha = "left" if fl < 62 else "right"
        ax.text(fl_txt_x, y + 0.18, f"{fl:.2f}%{fl_mk}", fontsize=9.8,
                fontweight="bold" if is_contam else "normal",
                color=ORANGE, va="center", ha=fl_ha)

        c_cer = RED if is_contam else DARK
        c_ortho = PURPLE if flag == "ortho_best" else (RED if is_contam else DARK)
        c_rtfx = TEAL if flag == "cv_best" else DARK
        ax_tbl.text(0.45, y, cer, fontsize=10.8, ha="center", va="center",
                    fontweight="bold" if flag == "cv_best" else "normal", color=c_cer)
        ax_tbl.text(1.42, y, ortho, fontsize=10.8, ha="center", va="center",
                    fontweight="bold" if flag == "ortho_best" else "normal", color=c_ortho)
        ax_tbl.text(2.40, y, rtfx, fontsize=10.8, ha="center", va="center",
                    fontweight="bold" if flag == "cv_best" else "normal", color=c_rtfx)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([r[0] for r in rows], fontsize=11.0, color=DARK)
    for tick, r in zip(ax.get_yticklabels(), rows):
        if r[1] in ("r1", "r2"):
            tick.set_fontweight("bold")
    ax.invert_yaxis()
    ax.set_xlim(0, 79)
    ax.set_ylim(y_pos[-1] + 0.65, y_pos[0] - 0.65)
    ax.tick_params(axis="x", labelsize=10.5)
    ax.set_xlabel("Normalized Corpus WER (%) — lower is better  (bars = 95% cluster-bootstrap CI)",
                  fontsize=11.0, fontweight="bold", color=DARK, labelpad=6)
    ax.grid(axis="x", color=LIGHT_GREY, linewidth=0.8, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax_tbl.set_xlim(0, 2.9)
    ax_tbl.axis("off")
    header_y = y_pos[0] - 0.85
    ax_tbl.text(0.45, header_y, "CV CER", fontsize=10.5, fontweight="bold", color=DARK, ha="center", va="bottom")
    ax_tbl.text(1.42, header_y, "CV Ortho\nWER", fontsize=10.2, fontweight="bold", color=DARK, ha="center", va="bottom")
    ax_tbl.text(2.40, header_y, "RTFx\n(4070S)", fontsize=10.2, fontweight="bold", color=DARK, ha="center", va="bottom")
    ax_tbl.plot([0.05, 2.85], [header_y + 0.14, header_y + 0.14], color="#999999", linewidth=1.0, clip_on=False)

    # Top row 1: Legend (kept well left of right table)
    leg_cv = plt.Line2D([0], [0], marker="o", color=BLUE, linestyle="-", markersize=7.0,
                        label="Common Voice ka (1,058 spk)")
    leg_fl = plt.Line2D([0], [0], marker="D", color=ORANGE, linestyle="-", markersize=6.0,
                        label="FLEURS ka (OOD for ours; NVIDIA test held out)")
    leg_ct = plt.Line2D([0], [0], marker="o", color=RED, markerfacecolor="white", markeredgewidth=2,
                        linestyle="None", markersize=7.0, label="†CV17 overlap (excl. on CV)")
    fig.legend(handles=[leg_cv, leg_fl, leg_ct], loc="upper left", bbox_to_anchor=(0.012, 0.992),
               ncol=3, frameon=False, fontsize=9.8, handletextpad=0.35, columnspacing=1.0)

    # Top row 2: Prominent off-scale zero-shot Whisper callout bar (clearly visible, not buried!)
    fig.text(0.015, 0.902,
             "Off-scale zero-shot Whisper loops:   Whisper-small → 825% CV / 289%‡ FL (14×)    ·    "
             "Whisper-turbo → 142% CV / 126%‡ FL (23×)",
             fontsize=9.6, fontweight="bold", color=RED,
             bbox=dict(boxstyle="round,pad=0.28", facecolor="#FFF5F5", edgecolor="#F0C0C0"))

    # Bottom clean note
    fig.text(0.015, 0.016,
             "MMS FT+LM 3-seed: CV 11.04±0.06%, FLEURS 19.17±0.10%.  "
             "‡ Post-fix FLEURS; § r1 bug-affected (r2 fixed = 12.71/27.27%; 40× timed on r2, 500 CV dev).  "
             "*Kaldi CPU.  NVIDIA: FLEURS train/dev; MMS card lists FLEURS.",
             fontsize=8.3, color=GREY)

    fig.canvas.draw()
    coords = {
        "img_size": [int(fig.get_figwidth() * dpi), int(fig.get_figheight() * dpi)],
        "nvidia_fl": data_to_img_px(fig, ax, 20.5, y_pos[4] + 0.18, dpi),
        "whisper_ortho": data_to_img_px(fig, ax_tbl, 1.42, y_pos[6], dpi),
        "whisper_cv_end": data_to_img_px(fig, ax, 24.0, y_pos[6] - 0.15, dpi),
        "mms_lm_cv": data_to_img_px(fig, ax, 14.5, y_pos[8] - 0.15, dpi),
        "mms_lm_fl_end": data_to_img_px(fig, ax, 30.5, y_pos[8] + 0.18, dpi),
        "mms_lm_rtfx": data_to_img_px(fig, ax_tbl, 2.40, y_pos[8], dpi),
    }

    out_path = OUT_DIR / "benchmark.png"
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)
    return coords, out_path


def make_data_and_metrics():
    dpi = 220
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.2, 4.25), dpi=dpi,
                                   gridspec_kw={"width_ratios": [1.12, 1.10], "wspace": 0.22,
                                                "left": 0.065, "right": 0.985, "top": 0.84, "bottom": 0.21})

    # --- Panel A: CV17 contamination audit by clip-ID age ---
    # Exact 11 buckets from docs/error-analysis-georgian-data.md §7
    buckets = ["0–38", "38–39.5", "39.5–40", "40–40.3", "40.3–.4",
               "40.4–.5", "40.5–.7", "40.7–41", "41–42", "42–44", "44+"]
    x = np.arange(len(buckets))
    nvidia = [4.21, 2.83, 3.62, 1.77, 5.46, 7.58, 11.99, 6.26, 10.93, 10.54, 22.98]
    whisper_ft = [9.64, 11.99, 18.28, 12.11, 13.65, 17.42, 27.80, 15.24, 19.58, 17.98, 29.21]
    mms_zs = [20.77, 22.71, 32.25, 24.26, 25.40, 28.85, 29.97, 27.40, 34.43, 24.45, 40.25]

    ax1.plot(x, mms_zs, marker="s", markersize=5.0, linewidth=1.8, linestyle="--",
             color="#7F8C8D", label="MMS zero-shot (20.8 → 40.3%)", zorder=2)
    ax1.plot(x, whisper_ft, marker="^", markersize=5.5, linewidth=2.0, linestyle="-",
             color=BLUE, label="Whisper FT ours (9.6 → 29.2%)", zorder=3)
    ax1.plot(x, nvidia, marker="o", markersize=6.4, linewidth=2.8, linestyle="-",
             color=RED, label="NVIDIA FastConformer (4.2 → 23.0%)", zorder=4)

    # Clean endpoint value labels
    ax1.text(0.0, 4.21 + 2.0, "4.2%", fontsize=9.8, fontweight="bold", color=RED, ha="center")
    ax1.text(3.0, 1.77 + 2.0, "1.8%", fontsize=9.8, fontweight="bold", color=RED, ha="center")
    ax1.text(10.18, 22.98, "23.0%", fontsize=10.4, fontweight="bold", color=RED, ha="left", va="center")
    ax1.text(10.18, 29.21, "29.2%", fontsize=9.6, fontweight="bold", color=BLUE, ha="left", va="center")

    # Show readable sparse x-ticks (every 2nd + last) so they are 10.5 pt and crisp from the back!
    tick_idx = [0, 2, 4, 6, 8, 10]
    ax1.set_xticks(tick_idx)
    ax1.set_xticklabels([buckets[i] for i in tick_idx], fontsize=10.2, color=DARK)
    ax1.set_xlim(-0.45, 11.45)
    ax1.set_ylim(0, 46)
    ax1.tick_params(axis="y", labelsize=10.2)
    ax1.set_ylabel("CV Dev+Test WER (%)", fontsize=11.0, fontweight="bold", color=DARK)
    ax1.set_xlabel("Common Voice clip ID in millions (older → newer)", fontsize=10.2, color=GREY, labelpad=4)
    ax1.set_title("A. CV17 overlap check by clip age",
                  fontsize=12.4, fontweight="bold", color=DARK, loc="left", pad=10)
    ax1.grid(axis="y", color=LIGHT_GREY, linewidth=0.8, zorder=0)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#DDDDDD", fontsize=9.2)

    # --- Panel B: Why 4 metrics? (4 systems showing BOTH CER gap AND Punctuation flip!) ---
    # Distinct non-CV/FLEURS palette: Navy (Norm WER), Purple (Ortho WER), Teal (CER)
    systems = ["Kaldi tri3b\n(33× CPU)", "MMS FT greedy\n(357× GPU)", "Whisper FT\n(40× GPU)", "MMS FT + LM\n(340× GPU)"]
    norm_wer = [22.64, 22.00, 12.80, 11.07]
    ortho_wer = [39.64, 39.15, 15.91, 30.45]
    cer = [8.22, 3.63, 2.60, 2.13]
    ortho_lbls = ["39.6", "39.2", "15.9", "30.5"]

    xb = np.arange(len(systems))
    wb = 0.26
    b_norm = ax2.bar(xb - wb, norm_wer, width=wb, color=NAVY, label="Norm. WER", zorder=3)
    b_orth = ax2.bar(xb, ortho_wer, width=wb, color=PURPLE, label="Ortho. WER (punct.)", zorder=3)
    b_cer = ax2.bar(xb + wb, cer, width=wb, color=TEAL, label="CER (char-level)", zorder=3)

    for rect, val in zip(b_norm, norm_wer):
        ax2.text(rect.get_x() + rect.get_width()/2, val + 0.9, f"{val:.1f}",
                 ha="center", va="bottom", fontsize=9.2, color=NAVY, fontweight="bold")
    for rect, val, lbl in zip(b_orth, ortho_wer, ortho_lbls):
        ax2.text(rect.get_x() + rect.get_width()/2, val + 0.9, lbl,
                 ha="center", va="bottom", fontsize=9.2, color=PURPLE, fontweight="bold")
    for rect, val in zip(b_cer, cer):
        ax2.text(rect.get_x() + rect.get_width()/2, val + 0.9, f"{val:.1f}",
                 ha="center", va="bottom", fontsize=9.2, color=TEAL, fontweight="bold")

    ax2.set_xticks(xb)
    ax2.set_xticklabels(systems, fontsize=9.6, fontweight="bold", color=DARK)
    ax2.set_ylim(0, 48)
    ax2.tick_params(axis="y", labelsize=10.2)
    ax2.set_ylabel("CV Test Error Rate (%)", fontsize=11.0, fontweight="bold", color=DARK)
    ax2.set_title("B. Why 4 metrics? (WER · Ortho · CER · RTFx)",
                  fontsize=12.4, fontweight="bold", color=DARK, loc="left", pad=10)
    ax2.grid(axis="y", color=LIGHT_GREY, linewidth=0.8, zorder=0)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#DDDDDD", fontsize=9.0)

    # Clean Calibri bracket highlighting 2.3x CER gap at same ~22% WER (keeps red pen minimal!)
    ax2.annotate("2.3× CER at\nsame WER",
                 xy=(0.0 + wb, 11.2), xytext=(0.45, 29.5),
                 fontsize=8.8, fontweight="bold", color=TEAL, ha="center", va="center",
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="#F2FBF7", edgecolor=TEAL, lw=0.9),
                 arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2, connectionstyle="arc3,rad=0.15"))

    fig.canvas.draw()
    coords = {
        "img_size": [int(fig.get_figwidth() * dpi), int(fig.get_figheight() * dpi)],
        "nvidia_cliff": data_to_img_px(fig, ax1, 10.35, 22.98, dpi),
        "kaldi_cer": data_to_img_px(fig, ax2, 0.0 + wb, 8.22, dpi),
        "mms_greedy_cer": data_to_img_px(fig, ax2, 1.0 + wb, 3.63, dpi),
        "whisper_ortho_bar": data_to_img_px(fig, ax2, 2.0, 15.91, dpi),
    }

    out_path = OUT_DIR / "data_and_metrics.png"
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)
    return coords, out_path


def make_diagnostics():
    dpi = 220
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.2, 4.95), dpi=dpi,
                                   gridspec_kw={"width_ratios": [1.34, 1.0], "wspace": 0.22,
                                                "left": 0.068, "right": 0.985, "top": 0.82, "bottom": 0.21})

    # --- Panel A: Whisper BPE budget & 14s pause-chunking on FLEURS test ---
    # Distinct non-CV/FLEURS palette: Navy (Plain r2), Slate (<14s untouched), Red (tail loops), Teal (>16s win)
    buckets = ["<14 s\n(n=782)", "14–15 s\n(n=53)", "15–16 s\n(n=50)",
               "16–20 s\n(n=72)", "20–25 s\n(n=15)", "≥25 s\n(n=7)"]
    plain_r2 = [22.8, 25.9, 32.3, 40.4, 53.5, 60.8]
    chunk_14 = [22.8, 98.3, 42.3, 25.7, 27.9, 28.7]

    x = np.arange(len(buckets))
    w = 0.36
    b1 = ax1.bar(x - w/2, plain_r2, width=w, color=NAVY, zorder=3)
    b2 = ax1.bar(x + w/2, chunk_14, width=w, color=TEAL, zorder=3)
    b2[0].set_color(SLATE)       # identical / untouched <14 s
    b2[1].set_color(RED)         # 41/53 loop
    b2[2].set_color("#E0665A")   # 7/50 loop

    for rect, val in zip(b1, plain_r2):
        ax1.text(rect.get_x() + rect.get_width()/2, val + 1.5, f"{val:.1f}",
                 ha="center", va="bottom", fontsize=9.6, color=NAVY, fontweight="bold")
    for idx, (rect, val) in enumerate(zip(b2, chunk_14)):
        col = GREY if idx == 0 else (RED if idx in (1, 2) else TEAL)
        ax1.text(rect.get_x() + rect.get_width()/2, val + 1.5, f"{val:.1f}",
                 ha="center", va="bottom", fontsize=9.6, color=col, fontweight="bold")

    ax1.axvline(0.5, color="#888888", linestyle=":", linewidth=1.4, zorder=2)
    ax1.annotate("3 UTF-8 bytes/char\n→ 20.6 tok/word\n448 cap ≈ 14.5 s\n(22% FLEURS > cap)",
                 xy=(0.5, 76), xytext=(-0.49, 76),
                 fontsize=8.6, color=DARK, va="center", ha="left",
                 bbox=dict(boxstyle="round,pad=0.35", facecolor="#F8F8F8", edgecolor="#CCCCCC"),
                 arrowprops=dict(arrowstyle="->", color="#777777", lw=1.1))

    ax1.set_xticks(x)
    ax1.set_xticklabels(buckets, fontsize=10.0, color=DARK)
    ax1.set_xlim(-0.55, 5.55)
    ax1.set_ylim(0, 114)
    ax1.tick_params(axis="y", labelsize=10.2)
    ax1.set_ylabel("FLEURS Test WER (%)", fontsize=11.0, fontweight="bold", color=DARK)
    ax1.set_xlabel("FLEURS test clip duration", fontsize=10.2, color=GREY, labelpad=4)
    ax1.set_title("A. Whisper BPE token cap & pause-chunk failure",
                  fontsize=12.4, fontweight="bold", color=DARK, loc="left", pad=14)
    ax1.grid(axis="y", color=LIGHT_GREY, linewidth=0.8, zorder=0)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    h_plain = mpatches.Patch(color=NAVY, label="Plain r2 (truncates >14.5 s)")
    h_unsp = mpatches.Patch(color=SLATE, label="14 s chunks: <14 s (not split)")
    h_loop = mpatches.Patch(color=RED, label="14 s chunks: tail loops (14–16 s)")
    h_win = mpatches.Patch(color=TEAL, label="14 s chunks: −41% WER (≥16 s)")
    ax1.legend(handles=[h_plain, h_unsp, h_loop, h_win], loc="upper right", frameon=True,
               facecolor="white", edgecolor="#DDDDDD", fontsize=8.8)

    # --- Panel B: Dev decoder ablation on MMS FT (same RTX 4070 SUPER) ---
    # Consistent corpus colors: BLUE = CV dev, ORANGE = FLEURS dev!
    stages = ["Greedy\n(same GPU)", "+ Unpadded\nframes", "+ Beam 100\n(no LM)", "+ 3-gram LM\n(α=0.5, β=0)"]
    cv_dev = [21.43, 21.43, 21.26, 10.28]
    fl_dev = [25.90, 25.90, 25.92, 20.41]

    xb = np.arange(len(stages))
    wb = 0.35
    p1 = ax2.bar(xb - wb/2, cv_dev, width=wb, color=BLUE, label="CV dev WER (%)", zorder=3)
    p2 = ax2.bar(xb + wb/2, fl_dev, width=wb, color=ORANGE, label="FLEURS dev WER (%)", zorder=3)
    # Emphasize final CV bar with a crisp dark border while keeping BLUE = CV!
    p1[3].set_edgecolor(DARK)
    p1[3].set_linewidth(1.8)

    for rect, val in zip(p1, cv_dev):
        ax2.text(rect.get_x() + rect.get_width()/2, val + 0.55, f"{val:.2f}%",
                 ha="center", va="bottom", fontsize=9.6, color=BLUE, fontweight="bold")
    for rect, val in zip(p2, fl_dev):
        ax2.text(rect.get_x() + rect.get_width()/2, val + 0.55, f"{val:.2f}%",
                 ha="center", va="bottom", fontsize=9.4, color=ORANGE, fontweight="bold")

    ax2.text(1.0, 32.2, "Δ = 0.00\n(0 clips diff)", ha="center", va="center", fontsize=9.2, color=GREY)
    ax2.text(2.0, 32.2, "Δ = −0.16\n(beam alone)", ha="center", va="center", fontsize=9.2, color=GREY)
    ax2.text(3.0, 32.2, "Δ = −10.98 CV\nΔ = −5.51 FL", ha="center", va="center",
             fontsize=9.6, fontweight="bold", color=BLUE)

    ax2.set_xticks(xb)
    ax2.set_xticklabels(stages, fontsize=9.8, color=DARK)
    ax2.set_ylim(0, 36.5)
    ax2.tick_params(axis="y", labelsize=10.2)
    ax2.set_ylabel("Dev WER (%)", fontsize=11.0, fontweight="bold", color=DARK)
    ax2.set_title("B. Dev decoder ablation (MMS adapter FT)",
                  fontsize=12.4, fontweight="bold", color=DARK, loc="left", pad=22)
    ax2.grid(axis="y", color=LIGHT_GREY, linewidth=0.8, zorder=0)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.legend(loc="upper left", bbox_to_anchor=(0.0, 1.075), ncol=2,
               frameon=False, fontsize=9.4, handletextpad=0.4, columnspacing=1.0)

    # Accurate, verified footnote (matching report §5 items 2, 4, 10)
    fig.text(0.015, 0.018,
             "Digits mismatch (0% CV train vs 20% FLEURS) explains 77% of MMS FT+LM vs zero-shot+LM gap (19.28% vs 18.36%).  "
             "Combined decoder change cuts 1-char substitutions by 67% on CV test (10,088 → 3,336).",
             fontsize=8.9, color=GREY)

    fig.canvas.draw()
    coords = {
        "img_size": [int(fig.get_figwidth() * dpi), int(fig.get_figheight() * dpi)],
        "tail_spike": data_to_img_px(fig, ax1, 1 + w/2, 98.3, dpi),
        "lm_delta": data_to_img_px(fig, ax2, 3.0, 32.2, dpi),
    }

    out_path = OUT_DIR / "diagnostics.png"
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)
    return coords, out_path


if __name__ == "__main__":
    c1, p1 = make_benchmark()
    c0, p0 = make_data_and_metrics()
    c2, p2 = make_diagnostics()
    all_coords = {"benchmark": c1, "data_and_metrics": c0, "diagnostics": c2}
    (OUT_DIR / "coords.json").write_text(json.dumps(all_coords, indent=2), encoding="utf-8")
    print("Wrote:", p1, p0, p2)
    print(json.dumps(all_coords, indent=2))
