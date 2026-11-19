# whisper-large-v3_cv-ka_dev (dev)

- Model: `openai/whisper-large-v3` @ `06f233fe06e710322aca913c1bc4249a0d71fce1` (hf-whisper, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA A100-SXM4-40GB; batch size 32
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 72.40% | 70.80% – 74.02% | 74.98% | 16.38% | 15.53% – 17.34% | 75.01% | 16.70% | 67.69% | 88.39% | 0.047 | 21.1 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 37553, 'S': 66602, 'D': 4540, 'I': 7550, 'N': 108695, 'M': 111705}  
Char counts: {'C': 779661, 'S': 73443, 'D': 38369, 'I': 34224, 'N': 891473, 'M': 887328}

Top substitutions (ref → hyp × n): და→ადა×138, მდებარეობს→დებარეობს×107, მდინარე→დინარე×52, მთავარი→თავარი×48, ერთ→ერთერთი×46, შემდეგ→შემდე×45, სხვა→ხვა×32, მცირე→ცირე×31, ჰქონდა→ქონდა×28, როგორც→როგორ×28

Worst items:

- `cv-ka-dev-common_voice_ka_39695118` {'C': 0, 'S': 4, 'D': 0, 'I': 85, 'N': 4, 'M': 89}
  - ref: ჰააგა დიდი სატრანსპორტო კვანძია
  - hyp: ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ამ ა�
- `cv-ka-dev-common_voice_ka_40324002` {'C': 2, 'S': 6, 'D': 0, 'I': 35, 'N': 8, 'M': 43}
  - ref: სარკმლის სამხრეთით და ჩრდილოეთით თითო ოთხკუთხა ნიშაა მოწყობილი
  - hyp: სარგმის სამხრეთით და ჩვენ მისით და მისით და მისით და მისით და მისით და მისით და მისით და მისით და მისით და მისით და მისით და მისით და მისით და მისით და მისით და მისით და მისით და მისით და მისით და �
- `cv-ka-dev-common_voice_ka_39932321` {'C': 0, 'S': 6, 'D': 0, 'I': 32, 'N': 6, 'M': 38}
  - ref: ქრისტიანები თავიანთი სისხლით ამოწმებდნენ საკუთარ აღმსარებლობას
  - hyp: ეს ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ისერ ის
- `cv-ka-dev-common_voice_ka_40352987` {'C': 0, 'S': 9, 'D': 0, 'I': 28, 'N': 9, 'M': 37}
  - ref: ფილმში მონაწილეობენ მაიკლ დუგლასი გლენ კლოუზი და ენ არჩერი
  - hyp: მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი
- `cv-ka-dev-common_voice_ka_37347116` {'C': 0, 'S': 5, 'D': 0, 'I': 27, 'N': 5, 'M': 32}
  - ref: ყველა კომპოზიციის ავტორია პიტერ გებრიელი
  - hyp: კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კველა კვე�
