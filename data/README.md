# data/

Audio and dataset manifests live here and are **not committed** (see `.gitignore`); every
manifest can be regenerated from a pinned source:

    uv run asrbench import-fleurs <config> --splits dev test     # e.g. tr_tr, el_gr, sw_ke
    uv run asrbench import-tsv my_recordings.tsv --language xx --out data/mine/manifest.jsonl

Run manifests record each dataset's sha256, so a regenerated manifest can be checked against a run.
