# speed4070_mms-1b-all-kat+lm_cv-ka_dev500 (dev)

- Model: `facebook/mms-1b-all` @ `3d33597edbdaaba14a8e858e2c8caa76e3cec0cd` (hf-ctc, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 500 | 2926 | 10.00% | 7.06% – 13.45% | 9.26% | 1.61% | 0.95% – 2.38% | 29.57% | 4.09% | 9.94% | 16.85% | 0.003 | 341.3 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 3523, 'S': 292, 'D': 76, 'I': 21, 'N': 3891, 'M': 3836}  
Char counts: {'C': 31280, 'S': 238, 'D': 199, 'I': 74, 'N': 31717, 'M': 31592}

Top substitutions (ref → hyp × n): მიეღო→მიიღო×2, წმიდა→წმინდა×2, ხალხთა→ხალხდა×1, რომელიც→რომელთა×1, შრომაა→შრომა×1, პინო→პინოპალადინო×1, სახელმწიფოთაშორისი→შორის×1, ნატო→ნატოში×1, მხარდამჭერი→მხარდამჭერიყო×1, კათალიკოს→კათალიქოს×1

Worst items:

- `cv-ka-dev-common_voice_ka_21381375` {'C': 7, 'S': 6, 'D': 1, 'I': 0, 'N': 14, 'M': 13}
  - ref: ქალაქ ლელუს ნანგრევები მსგავსია ნან მადოლის ნანგრევებთან კუნძულ პონპეიზე მაგრამ თარიღდება უფრო გვიანდელი პერიოდით
  - hyp: ქალაქ ლევუს ნანგრევები მსგავსია ნან მადოლისნანგრევებთამკუნძულ პომპეიზე მაგრამ ცარი ხდება უფრო გვიანდელი პერიოდით
- `cv-ka-dev-common_voice_ka_21381415` {'C': 5, 'S': 7, 'D': 0, 'I': 0, 'N': 12, 'M': 12}
  - ref: ითვლება რომ სწორედ დედის რომანტიკულმა ბუნებამ იქონია უდიდესი ზეგავლენა ახალგაზრდა მოდილიანის მსოფლმხედველობაზე
  - hyp: ითვლება რომ სწორად დედის რომანტიკულმა ბუნება მიქონიაუდიდესის რეგვენა ახალ გაცდა მოდილიანის მსოფხედველობაზე
- `cv-ka-dev-common_voice_ka_21455841` {'C': 8, 'S': 3, 'D': 2, 'I': 1, 'N': 13, 'M': 12}
  - ref: სასტიკი ცენზურის პირობებში ვისოცკი ეხებოდა აკრძალულ თემებს მღეროდა ყოველდღიურ საბჭოთა ცხოვრებაზე სამამულო ომზე
  - hyp: სასტიკი ცენზურის პირობებში ვისაც კი ეხებოდა აკრძალა თემებს მყეროდეყოველდგიურსაბჭოთა ცხოვრებაზე სამამულო ომზე
- `cv-ka-dev-common_voice_ka_21382336` {'C': 8, 'S': 4, 'D': 2, 'I': 0, 'N': 14, 'M': 12}
  - ref: ჯერ კიდევ გამეფებამდე უთანხმოება ჰქონდა მამასთან და უმცროს ძმასთან დიმიტრისთან რომელსაც თავის მეტოქედ თვლიდა
  - hyp: ჯერ კიდველ გამეფებაბდე უთანხმოება ჰქონდა მამასთან და მშროსმასთან დიმიტრისთან რომელსაც თავის მეტოქეთთვლიზა
- `cv-ka-dev-common_voice_ka_21455875` {'C': 6, 'S': 3, 'D': 2, 'I': 0, 'N': 11, 'M': 9}
  - ref: ყირიმში პოლკოვნიკმა აბაშიძემ ჩამოაყალიბა საქართველოს სათვისტომო იყო მისი გამგებლობის პირველი პრეზიდენტი
  - hyp: პირიმში პოლკოვნიკმააბაშიდზემჩამოაყალიბა საქართველო სათვისტომო იყო მისი გამგებლობის პირველი პრეზიდენტი
