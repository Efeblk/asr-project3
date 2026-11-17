# Course announcement: "Project 3 Baselines and Bonus Points"

Posted on the course page's announcements board ("Ders Duyuruları"). Passed on by the student on 2026-11-17; the exact posting date is not recorded. Verbatim text below (only the list formatting is added).

---

Dear students,

Here are some points about the baselines and bonus points:

- All methods covered in Week 9, in their standard form, are baselines. This includes basic MFCC + GMM-HMM systems, CTC, attention-based encoder-decoder and transducer systems, and pretrained models such as HuBERT/wav2vec 2.0-based ASR, Whisper, Canary, Parakeet, and Qwen3-ASR. An advanced model is still a baseline. Simply running Qwen3-ASR does not count as your model contribution. Use checkpoints suitable for your language; a bare HuBERT or wav2vec 2.0 encoder without an ASR head cannot transcribe audio.
- Your own training or fine-tuning counts as your contribution. "Without training" means without additional training by your group; pretrained models have already been trained by their creators. Keep the standard baseline results and report your trained version separately on the same test set. A simpler method remains a baseline, but implementing and training it yourself earns credit for that work.
- Each group must choose a non-English language that is different from the other groups' languages. Coordinate before starting. Low-resource languages can earn higher points, provided there is enough usable data and reliable reference transcription for evaluation. Do not invent reference transcripts or treat another model's output as verified ground truth.
- Domain-specific ASR is another bonus dimension: legal, medical, financial, or another specialized domain. Support the choice with appropriate audio and trustworthy reference transcripts.

Compare the applicable baselines using the same test data and scoring rules, and justify your choice of WER, CER, and additional metrics that are here: https://huggingface.co/learn/audio-course/en/chapter5/evaluation.

Clearly separate baseline performance from your contribution.

Good luck and see you next with at presentations.
