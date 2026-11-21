# mms-1b-all-kat-adapter-ft_cv-ka+beam100-nolm_cv-ka_dev (dev)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 21.26% | 19.99% – 22.70% | 21.39% | 3.37% | 3.02% – 3.78% | 38.38% | 5.74% | 20.94% | 35.33% | 0.003 | 334.2 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 87258, 'S': 19384, 'D': 2053, 'I': 1676, 'N': 108695, 'M': 108318}  
Char counts: {'C': 867970, 'S': 13313, 'D': 10190, 'I': 6564, 'N': 891473, 'M': 887847}

Top substitutions (ref → hyp × n): საქართველოს→საქართველო×21, მდიდარია→მდიდარეა×11, გარეშე→გარეში×9, მიწისქვეშა→ქვეშა×9, უკანასკნელი→უკანასკნილი×8, ამიერკავკასიის→კავკასიის×8, მსოფლიოს→მსოფლიო×8, წმიდა→წმინდა×8, სწორკუთხა→წორკუთხა×7, ციხესიმაგრე→სიმაგრე×7

Worst items:

- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 5, 'D': 8, 'I': 0, 'N': 13, 'M': 5}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: არ ო ი ის იი
- `cv-ka-dev-common_voice_ka_40332704` {'C': 3, 'S': 11, 'D': 0, 'I': 1, 'N': 14, 'M': 15}
  - ref: მოკავშირეთა კონტროლქვეშ აღმოჩნდა სპლიტ ლივნო კუპრეს ბუგოინოს გზატკეცილი რაც მებრძოლი მხარეების მომარაგების პრობლემებს ხსნიდა
  - hyp: მოკავშირათა კონტროლ ქვეშ აღმნიჩნა სპლიტ ლივნო კუპრეს ბეგოინოს გზადკეცინი რამაც ვებრდოლი მხარეები მომარაგეების პრობლემად იხსნა
- `cv-ka-dev-common_voice_ka_40185500` {'C': 2, 'S': 9, 'D': 2, 'I': 1, 'N': 13, 'M': 12}
  - ref: ცნობები ნერვული სისტემის დაავადებების შესახებ მოიპოვება ძველ ეგვიპტურ ჩინურ ბერძნულ და რომაულ ხელნაწერებში
  - hyp: ცნოვები ნერვული სისტემით დაავადების შესახი მოიპოვე და ძველ ეგვიტურში ნურ ბერძნულდა რომაულხინაწირებში
- `cv-ka-dev-common_voice_ka_39695153` {'C': 3, 'S': 9, 'D': 2, 'I': 1, 'N': 14, 'M': 13}
  - ref: მოსკოვის სახელმწიფო ლინგვისტური უნივერსიტეტი არის რუსეთის ერთ ერთი ყველაზე დიდი უმაღლესი სასწავლებელი ენათმეცნიერების დარგში
  - hyp: მოსკავის სახელმსიფო ლინგვის სტუდი უნივერსიტეტი არის რუსეთის ერთედ ხველაზებები უმანასის სასავებელი ენარქმეცელების დარკშა
- `cv-ka-dev-common_voice_ka_40319640` {'C': 6, 'S': 7, 'D': 2, 'I': 2, 'N': 15, 'M': 15}
  - ref: ასევე ლუიზამ დაიწყო მეგობრული ურთიერთობების ჩამოყალიბება ოსმალეთის იმპერიასთან რაც შემდგომში მრავალსაუკუნოვან საფრანგეთ ოსმალეთის ალიანსში გადაიზარდა
  - hyp: ასველუიზამ დაიწყო მენკრუვრვლიურთიერთობის ამოყალებება ოსმალეთის იმპერიასთანდა რაც შემ დგონში მრავალ საუკუნოვან საფრანგეთ ოსმალეთის ალიანში გადაიზარდა
