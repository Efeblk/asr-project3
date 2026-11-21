# mms-1b-all-kat+beam100-nolm_cv-ka_dev (dev)

- Model: `facebook/mms-1b-all` @ `3d33597edbdaaba14a8e858e2c8caa76e3cec0cd` (hf-ctc, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 23.55% | 22.13% – 25.13% | 23.97% | 4.04% | 3.52% – 4.65% | 39.55% | 6.35% | 23.22% | 38.66% | 0.003 | 339.2 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 84643, 'S': 21270, 'D': 2782, 'I': 1549, 'N': 108695, 'M': 107462}  
Char counts: {'C': 862223, 'S': 17446, 'D': 11804, 'I': 6752, 'N': 891473, 'M': 886421}

Top substitutions (ref → hyp × n): საქართველოს→საქართველო×29, გვხვდება→გხვდება×23, ოლქში→ოლგში×16, წევრი→სწევრი×13, ესე→ესეიგი×10, მიიღო→მიიყო×10, უკანასკნელი→უკანასკნილი×9, მის→მისმიერ×9, საბავშვო→საბავშო×8, ამიერკავკასიის→კავკასიის×8

Worst items:

- `cv-ka-dev-common_voice_ka_37420739` {'C': 1, 'S': 11, 'D': 2, 'I': 0, 'N': 14, 'M': 12}
  - ref: სექტემბრისთვის ქალაქის ზედა ნაწილიც დაინგრა და აღებულ იქნა მაგრამ ცენტრალური ციხესიმაგრე კვლავ განაგრძობდა წინააღმდეგობას
  - hyp: სეფტემბრისთვის ქალაქის ზედანაწილის დაინდრა დავაღებული მაგრამ ცენტრალული ციხესი მაგრე ბლავ განარცოდა ძინააბდებას
- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 2, 'D': 11, 'I': 0, 'N': 13, 'M': 2}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: nnnnn nnnnnnn
- `cv-ka-dev-common_voice_ka_40332704` {'C': 3, 'S': 11, 'D': 0, 'I': 1, 'N': 14, 'M': 15}
  - ref: მოკავშირეთა კონტროლქვეშ აღმოჩნდა სპლიტ ლივნო კუპრეს ბუგოინოს გზატკეცილი რაც მებრძოლი მხარეების მომარაგების პრობლემებს ხსნიდა
  - hyp: მოკავშირათა კონტროლ ქვეშ აღმნიჩნდა სპლიტ ლივნო კუპრეს ბეგოინოს გზადკეცინი რამაც ვებრძოლი მხარეები მომარაგეების პრობლემად იხსნა
- `cv-ka-dev-common_voice_ka_40319640` {'C': 5, 'S': 9, 'D': 1, 'I': 2, 'N': 15, 'M': 16}
  - ref: ასევე ლუიზამ დაიწყო მეგობრული ურთიერთობების ჩამოყალიბება ოსმალეთის იმპერიასთან რაც შემდგომში მრავალსაუკუნოვან საფრანგეთ ოსმალეთის ალიანსში გადაიზარდა
  - hyp: ასველუიზამ დაიწყო მენკრუბრული ურთიერთობის ამოყალიბება ოსუმალეთის იმპერიასთან და რაც შემდგონში მრავალ საუკუნოვან საფრანგეთ ოსუმალეთის ალიანში გადაიზარდა
- `cv-ka-dev-common_voice_ka_40185500` {'C': 2, 'S': 9, 'D': 2, 'I': 1, 'N': 13, 'M': 12}
  - ref: ცნობები ნერვული სისტემის დაავადებების შესახებ მოიპოვება ძველ ეგვიპტურ ჩინურ ბერძნულ და რომაულ ხელნაწერებში
  - hyp: ცნოვები ნერვული სისტემით დაავადების შესახე მოიპოვე და ძველ ეგუტურში ნურ ბერზუნდა რუმაულხენაწერებში
