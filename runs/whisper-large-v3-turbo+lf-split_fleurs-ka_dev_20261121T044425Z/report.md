# whisper-large-v3-turbo+lf-split_fleurs-ka_dev (dev)

- Model: `openai/whisper-large-v3-turbo` @ `41f01f3fe87f28c78e2fbf8b568835947dd65ed9` (hf-whisper, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 16
- Dataset: `data/fleurs/ka_ge/manifest.jsonl` sha256 `d95e58e9db45`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 409 | 4392 | 139.27% | 129.83% – 149.93% | 149.99% | 114.74% | 109.44% – 121.10% | 136.71% | 113.12% | 99.98% | 100.00% | 0.015 | 65.0 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 2, 'S': 1976, 'D': 4632, 'I': 2598, 'N': 6610, 'M': 4576}  
Char counts: {'C': 7492, 'S': 41443, 'D': 4451, 'I': 15361, 'N': 53386, 'M': 64296}

Top substitutions (ref → hyp × n): და→დის×7, და→გის×6, და→ერის×6, ის→რის×5, და→შრის×5, ადგილი→რის×4, მამაკაცთა→რის×4, super→რის×4, g→რის×4, კატეგორიაში→რის×4

Worst items:

- `fleurs-ka_ge-dev-1948622539609985266` {'C': 0, 'S': 8, 'D': 0, 'I': 214, 'N': 8, 'M': 222}
  - ref: პირველად ბიზანტიურმა კულტურამ აღმოსავლეთში სამოსზე დიდი გავლენა მოახდინა
  - hyp: 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
- `fleurs-ka_ge-dev-1264417313833106437` {'C': 0, 'S': 22, 'D': 0, 'I': 52, 'N': 22, 'M': 74}
  - ref: ტყეები არ შედგება მხოლოდ მანგროს ჭაობებისგან ისინი ასევე მოიცავს ერთ დროს ძლიერი ჯუნგლების გადარჩენილ ნაწილს რომლებიც თავის დროზე განგის ვაკეზე იყო გადაჭიმული
  - hyp: ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს
- `fleurs-ka_ge-dev-10930914540372163294` {'C': 0, 'S': 9, 'D': 0, 'I': 65, 'N': 9, 'M': 74}
  - ref: ცხოვრების უმეტესი წლები ებრაელმა ოჯახმა ღია ცის ქვეშ გაატარა
  - hyp: ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს
- `fleurs-ka_ge-dev-14522533026016468981` {'C': 0, 'S': 9, 'D': 0, 'I': 65, 'N': 9, 'M': 74}
  - ref: ცხოვრების უმეტესი წლები ებრაელმა ოჯახმა ღია ცის ქვეშ გაატარა
  - hyp: ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს
- `fleurs-ka_ge-dev-4198887759742858398` {'C': 0, 'S': 12, 'D': 0, 'I': 56, 'N': 12, 'M': 68}
  - ref: არაბებმა ისლამი ამ მიწებზეც ჩამოიტანეს კომორის კუნძულებსა და მაიოტაზე ის ძალიან გავრცელდა
  - hyp: ესსსს ესს ესს ესს ესს ესს ესს ესს ესს ეს ესს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს ეს
