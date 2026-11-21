# mms-1b-all-kat-adapter-ft_cv-ka-seed7_cv-ka_dev (dev)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka-seed7_20261121T002912Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka-seed7_20261121T002912Z)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 21.33% | 20.06% – 22.74% | 21.38% | 3.39% | 3.03% – 3.80% | 38.41% | 5.76% | 21.07% | 35.37% | 0.002 | 423.5 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 86845, 'S': 19184, 'D': 2666, 'I': 1332, 'N': 108695, 'M': 107361}  
Char counts: {'C': 867267, 'S': 13224, 'D': 10982, 'I': 5979, 'N': 891473, 'M': 886470}

Top substitutions (ref → hyp × n): საქართველოს→საქართველო×22, მიიღო→მიიყო×10, მდიდარია→მდიდარეა×10, აღმოჩნდა→აღმოჩდა×9, ამიერკავკასიის→კავკასიის×9, ციხესიმაგრე→სიმაგრე×9, მის→მისმიერ×9, საბავშვო→საბავშო×8, ქვეშ→ქვეში×7, წინაშე→წინაში×7

Worst items:

- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 0, 'D': 13, 'I': 0, 'N': 13, 'M': 0}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: 
- `cv-ka-dev-common_voice_ka_40332704` {'C': 3, 'S': 11, 'D': 0, 'I': 1, 'N': 14, 'M': 15}
  - ref: მოკავშირეთა კონტროლქვეშ აღმოჩნდა სპლიტ ლივნო კუპრეს ბუგოინოს გზატკეცილი რაც მებრძოლი მხარეების მომარაგების პრობლემებს ხსნიდა
  - hyp: მოკავშირათა კონტროლ ქვეშ აღმიჩნდა სპლიტ ლივნო კუპრეს ბეგოინოს გზადკეცენი რამაც ვებრდოლი მხარეები მომარაგეების პრობლემად იხსნა
- `cv-ka-dev-common_voice_ka_37420739` {'C': 2, 'S': 12, 'D': 0, 'I': 0, 'N': 14, 'M': 14}
  - ref: სექტემბრისთვის ქალაქის ზედა ნაწილიც დაინგრა და აღებულ იქნა მაგრამ ცენტრალური ციხესიმაგრე კვლავ განაგრძობდა წინააღმდეგობას
  - hyp: სეფტემბრისთვის ქალაქის ზედა ნაწილის დაინდრა დააღებულ იქა მაგრამ ცენტრალული ციხესი მაგრე ბლავ განარძოდა ძინააბდებას
- `cv-ka-dev-common_voice_ka_40185500` {'C': 2, 'S': 10, 'D': 1, 'I': 1, 'N': 13, 'M': 13}
  - ref: ცნობები ნერვული სისტემის დაავადებების შესახებ მოიპოვება ძველ ეგვიპტურ ჩინურ ბერძნულ და რომაულ ხელნაწერებში
  - hyp: ცნოვები ნერვული სისტემით დაავადების შესახე მოიპოვე და ძველ ეგუტურში ნურ ბერძნუდა რომაულხი ნაწირებში
- `cv-ka-dev-common_voice_ka_39695153` {'C': 3, 'S': 9, 'D': 2, 'I': 1, 'N': 14, 'M': 13}
  - ref: მოსკოვის სახელმწიფო ლინგვისტური უნივერსიტეტი არის რუსეთის ერთ ერთი ყველაზე დიდი უმაღლესი სასწავლებელი ენათმეცნიერების დარგში
  - hyp: მოსკავის სახელმსიფო ლინგვის ტუდი უნივერსიტეტი არის რუსეთის ერთედ ყველაზებელი ურმანესის სასწავებელი ენართმეცილების დარშაა
