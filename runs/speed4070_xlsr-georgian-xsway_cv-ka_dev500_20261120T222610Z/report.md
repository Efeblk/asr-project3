# speed4070_xlsr-georgian-xsway_cv-ka_dev500 (dev)

- Model: `xsway/wav2vec2-large-xlsr-georgian` @ `b29b81945f5fa2e35fbb05da5256815d8cc71e20` (hf-ctc, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 500 | 2926 | 9.35% | 3.09% – 23.97% | 8.58% | 1.32% | 0.33% – 3.76% | 26.70% | 3.64% | 9.33% | 15.87% | 0.001 | 788.3 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 3539, 'S': 275, 'D': 77, 'I': 12, 'N': 3891, 'M': 3826}  
Char counts: {'C': 31367, 'S': 183, 'D': 167, 'I': 68, 'N': 31717, 'M': 31618}

Top substitutions (ref → hyp × n): ერთ→ერთერთი×10, ერთ→ერთერთ×2, ჩრდილო→ჩრდილოაღმოსავლეთ×2, ეკონომიკურ→ეკონომიკურსტატისტიკურ×2, სამხრეთ→სამხრეთდასავლეთ×2, ალ→ალტაბარის×1, ნატო→ნატოში×1, ში→გაწებლიანების×1, მხარდამჭერი→მხადამჭერი×1, კათალიკოს→კათალიკოსპატრიარქის×1

Worst items:

- `cv-ka-dev-common_voice_ka_21382493` {'C': 4, 'S': 6, 'D': 4, 'I': 1, 'N': 14, 'M': 11}
  - ref: მომდევნო წლებში მისი ხუთი ვაჟი ავიდა ტახტზე რომლებიც ერთმანეთს ხოცავდნენ და შემდეგ ასე ანაცვლებდნენ
  - hyp: რუმდუმნოწლებში მისი ხუთივაჟი ავიდა ტახტზე რობლებიც ერთმანე ცხო ცავდნენ და შემდეგასეანაცვლებდნენ
- `cv-ka-dev-common_voice_ka_21365362` {'C': 7, 'S': 8, 'D': 1, 'I': 1, 'N': 16, 'M': 16}
  - ref: მდებარეობს ჩეხეთის ისტორიული მხარის ბოჰემიის სამხრეთ აღმოსავლეთ ნაწილში და ნაწილობრივ ისტორიული მხარის მორავიის სამხრეთ დასავლეთ ნაწილში
  - hyp: მდებარეობს ჩეხეთის ისტორიული მხარ ის ბოჰიმიის ემხლით ეხასმსელად ნაწილში დანაწილობრივ ისტორიული მხარის მორავიი საფხრეთ დასავეთ ნაწილში
- `cv-ka-dev-common_voice_ka_23826173` {'C': 6, 'S': 7, 'D': 1, 'I': 1, 'N': 14, 'M': 14}
  - ref: სამარხი ერქვა აგრეთვე მოკლულის დასაკრძალავი ხარჯების საზღაურს რომელიც მკვლელს ან მისთვის პასუხისმგებელ პირს ეკისრებოდა
  - hyp: სამარხიერქვა აგრეთვე მოკლუის დასაკრძალავი ხარჩების სასხოვრს რომელიც კვლელს ან მისთვის ფასხვიდგებალ პირს იგის რეპუტა
- `cv-ka-dev-common_voice_ka_23826182` {'C': 5, 'S': 6, 'D': 1, 'I': 1, 'N': 12, 'M': 12}
  - ref: მეფე დედოფალმა თავიანთი ხანმოკლე მმართველობის უმეტესი ნაწილი დედაქალაქისგან შორს საზღვაო კურორტზე გაატარეს
  - hyp: მეფედედოფალმა თავიანთი ხანმოკლე მართველობის უმეთეს ნაწილი დედაქალაქის გან შორს საზღვავ კურორთსე გაატარეს
- `cv-ka-dev-common_voice_ka_23826174` {'C': 5, 'S': 6, 'D': 2, 'I': 0, 'N': 13, 'M': 11}
  - ref: ზურგის ზედა მხარე შავია აყრია ოთხკუთხა და მრავალრიცხოვანი მცირე ზომის მომრგვალებული თეთრი ლაქები
  - hyp: ზურგისედამღარე შავია აღრიოოდკუთხა და მრავალ რცხოვანი მცირე ზომის მორგვალებული თეთრი ლაქები
