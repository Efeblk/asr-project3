# mms-1b-all-kat+lm_cv-ka_dev (dev)

- Model: `facebook/mms-1b-all` @ `3d33597edbdaaba14a8e858e2c8caa76e3cec0cd` (hf-ctc, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 12.68% | 11.58% – 13.87% | 12.77% | 2.61% | 2.13% – 3.17% | 31.26% | 5.04% | 12.61% | 20.50% | 0.003 | 378.8 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 95519, 'S': 9462, 'D': 3714, 'I': 610, 'N': 108695, 'M': 105591}  
Char counts: {'C': 870933, 'S': 9176, 'D': 11364, 'I': 2684, 'N': 891473, 'M': 882793}

Top substitutions (ref → hyp × n): საქართველოს→საქართველო×17, ახალგაზრდა→ახალგაზდა×12, გვხვდება→ხვდება×8, ნიკოლოზ→ნიკოლას×7, ერთ→ერთერთი×6, ერთმანეთისაგან→ერთმანეთისგან×6, წმიდა→წმინდა×6, ესე→ესეიგი×6, უეფა→უეფას×5, მსოფლიოს→მსოფლიო×5

Worst items:

- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 0, 'D': 13, 'I': 0, 'N': 13, 'M': 0}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: 
- `cv-ka-dev-common_voice_ka_49293620` {'C': 2, 'S': 5, 'D': 7, 'I': 0, 'N': 14, 'M': 7}
  - ref: დრო არი ჩემო პატარავ იცოდე ერტი ამბავი ედელის როდა ბადალი დღეს საქართელოს მთა ბრი
  - hyp: დროარი ჩემოტირიამბავი ედელის როდაბადალი დღეს საქართველოს მთავბრი
- `cv-ka-dev-common_voice_ka_39695150` {'C': 0, 'S': 2, 'D': 9, 'I': 0, 'N': 11, 'M': 2}
  - ref: ეკლესიის კედლების ქვეშ დასაფლავებულია გერმანელი ჯარისკაცი შემორჩენილია საფლავის ქვა გერმანული წარწერით
  - hyp: leსinenlnecaoua genmanencanntacoenmanaten
- `cv-ka-dev-common_voice_ka_40185500` {'C': 2, 'S': 3, 'D': 8, 'I': 0, 'N': 13, 'M': 5}
  - ref: ცნობები ნერვული სისტემის დაავადებების შესახებ მოიპოვება ძველ ეგვიპტურ ჩინურ ბერძნულ და რომაულ ხელნაწერებში
  - hyp: ცნოვები ნერვული სისტემის დაავადების შესახემოიპოვედაძველეგუტურშინურბერზუნდარუმაულხენაწერებში
- `cv-ka-dev-common_voice_ka_39760415` {'C': 0, 'S': 1, 'D': 10, 'I': 0, 'N': 11, 'M': 1}
  - ref: მანამდე გენერალური მდივნის პოსტს დიმიტრი ბოკერია ბოლო ერთი თვის განმავლობაში იკავებდა
  - hyp: oyambigniramtukeryabowajk
