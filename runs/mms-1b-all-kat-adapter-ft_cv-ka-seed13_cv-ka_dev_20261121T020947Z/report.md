# mms-1b-all-kat-adapter-ft_cv-ka-seed13_cv-ka_dev (dev)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka-seed13_20261121T004458Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka-seed13_20261121T004458Z)
- Hardware: NVIDIA A100-SXM4-40GB; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 21.48% | 20.19% – 22.90% | 21.57% | 3.40% | 3.04% – 3.81% | 38.51% | 5.77% | 21.21% | 35.60% | 0.001 | 796.6 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 86710, 'S': 19339, 'D': 2646, 'I': 1363, 'N': 108695, 'M': 107412}  
Char counts: {'C': 867091, 'S': 13305, 'D': 11077, 'I': 5908, 'N': 891473, 'M': 886304}

Top substitutions (ref → hyp × n): საქართველოს→საქართველო×12, უკანასკნელი→უკანასკნილი×10, მდიდარია→მდიდარეა×10, სამეურნეო→სამეორნეო×10, გარეშე→გარეში×10, ამიერკავკასიის→კავკასიის×8, ქვეშ→ქვეში×8, სხვადასხვა→ხვადასხვა×8, აღმოჩნდა→აღმოჩდა×7, ექვემდებარება→მდებარება×7

Worst items:

- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 1, 'D': 12, 'I': 0, 'N': 13, 'M': 1}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: აესიის
- `cv-ka-dev-common_voice_ka_40332704` {'C': 3, 'S': 11, 'D': 0, 'I': 1, 'N': 14, 'M': 15}
  - ref: მოკავშირეთა კონტროლქვეშ აღმოჩნდა სპლიტ ლივნო კუპრეს ბუგოინოს გზატკეცილი რაც მებრძოლი მხარეების მომარაგების პრობლემებს ხსნიდა
  - hyp: მოკავშირათა კონტროლ ქვეშ აღმიჩნდა სპლიტ ლივნო კუპრეს ბეგოინოს გზადკეცენი რამაც ვებრძოლი მხარეები მომარაგეების პრობლემად იხსნა
- `cv-ka-dev-common_voice_ka_40185500` {'C': 2, 'S': 9, 'D': 2, 'I': 1, 'N': 13, 'M': 12}
  - ref: ცნობები ნერვული სისტემის დაავადებების შესახებ მოიპოვება ძველ ეგვიპტურ ჩინურ ბერძნულ და რომაულ ხელნაწერებში
  - hyp: ცნოვები ნერვული სისტემით დაავადების შესახე მოიპოვე და ძველ ეგუტურში ნურ ბერძნუდა რომაულხინაწირებში
- `cv-ka-dev-common_voice_ka_39695153` {'C': 3, 'S': 9, 'D': 2, 'I': 1, 'N': 14, 'M': 13}
  - ref: მოსკოვის სახელმწიფო ლინგვისტური უნივერსიტეტი არის რუსეთის ერთ ერთი ყველაზე დიდი უმაღლესი სასწავლებელი ენათმეცნიერების დარგში
  - hyp: მოსკავის სახელმსიფო ლინგვის სტუნი უნივერსიტეტი არის რუსეთის ერთედ ყველაზებელი უმაესის სასწოვებელი ენარქმეცელების დარკშია
- `cv-ka-dev-common_voice_ka_40818635` {'C': 2, 'S': 8, 'D': 4, 'I': 0, 'N': 14, 'M': 10}
  - ref: ავღანეთის ეს რეგიონი მდიდარია უძველესი არქეოლოგიური ძეგლებით რომლებიც ჯერ კიდევ სრულყოფილად შესწავლილი არ არის
  - hyp: ავღანითისის რეგიონი მდედა რელძვილისი არქეოლორგიური ძეკრებით რომლებიც ჯერყიდასულკეფილად ჩესწავლილი არავის
