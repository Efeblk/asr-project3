# mms-1b-all-kat-adapter-ft_cv-ka+lm-a0.5-b1.0_cv-ka_dev (dev)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 10.30% | 9.45% – 11.24% | 10.16% | 1.86% | 1.58% – 2.18% | 29.71% | 4.28% | 10.22% | 16.92% | 0.003 | 379.5 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 98447, 'S': 7926, 'D': 2322, 'I': 953, 'N': 108695, 'M': 107326}  
Char counts: {'C': 877749, 'S': 5462, 'D': 8262, 'I': 2832, 'N': 891473, 'M': 886043}

Top substitutions (ref → hyp × n): ახალგაზრდა→ახალგაზდა×14, წმიდა→წმინდა×8, ციხესიმაგრე→სიმაგრე×7, დღესდღეობით→დღეობით×6, დავით→დავიდ×6, აბსიდით→აფსიდით×5, უეფა→უეფას×5, თავმჯდომარე→თავჯდომარე×5, ნიკოლოზ→ნიკოლას×5, აბსიდის→აფსიდის×5

Worst items:

- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 1, 'D': 12, 'I': 0, 'N': 13, 'M': 1}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: არის
- `cv-ka-dev-common_voice_ka_40255793` {'C': 1, 'S': 9, 'D': 2, 'I': 0, 'N': 12, 'M': 10}
  - ref: მიუხედავად დამთვალიერებლების სიჭარბისა მომავალი წლის ივნისში ედგარ ალან პოს სახლ მუზეუმი დაიხურება
  - hyp: მიუხედავად დამთვალიელების ჭა სი ჭარბი სა მომავალი წლის მჟიედგარააპოსსახლმუზეობი დაიხურა
- `cv-ka-dev-common_voice_ka_40618092` {'C': 0, 'S': 1, 'D': 10, 'I': 0, 'N': 11, 'M': 1}
  - ref: საბოლოო ჯამში იანგმა ჯგუფი დატოვა და მისი ადგილი სტივ ვესტმა დაიკავა
  - hyp: იასი
- `cv-ka-dev-common_voice_ka_40356724` {'C': 0, 'S': 4, 'D': 7, 'I': 0, 'N': 11, 'M': 4}
  - ref: გუგენჰაიმის სპირალურად დახვეული თეთრი აივნებიდანაც ავტომობილის ნაწილებით დამზადებული ექსტრავაგანტული ფიგურები იმზირებიან
  - hyp: ეს შენობა არის დატოვა
- `cv-ka-dev-common_voice_ka_40332704` {'C': 5, 'S': 7, 'D': 2, 'I': 1, 'N': 14, 'M': 13}
  - ref: მოკავშირეთა კონტროლქვეშ აღმოჩნდა სპლიტ ლივნო კუპრეს ბუგოინოს გზატკეცილი რაც მებრძოლი მხარეების მომარაგების პრობლემებს ხსნიდა
  - hyp: მოკავშირეთა კონტროლ ქვეშ აღნიშნა სპლიტ ლივნოკუპრესბეგოინოს გზატკეცილი რამაც მებრძოლი მხარეები მომარაგების პრობლემად იხსნა
