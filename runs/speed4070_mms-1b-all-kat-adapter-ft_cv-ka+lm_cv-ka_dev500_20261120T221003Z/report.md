# speed4070_mms-1b-all-kat-adapter-ft_cv-ka+lm_cv-ka_dev500 (dev)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 500 | 2926 | 8.79% | 6.13% – 11.99% | 8.24% | 1.31% | 0.72% – 2.01% | 29.07% | 3.79% | 8.73% | 14.60% | 0.003 | 340.4 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 3575, 'S': 245, 'D': 71, 'I': 26, 'N': 3891, 'M': 3846}  
Char counts: {'C': 31374, 'S': 176, 'D': 167, 'I': 73, 'N': 31717, 'M': 31623}

Top substitutions (ref → hyp × n): მიეღო→მიიღო×2, წმიდა→წმინდა×2, ხალხთა→ხალხდა×1, რომელიც→რომელთა×1, თხზულებების→თხძულებების×1, შრომაა→შრომა×1, პინო→პინოპალადინო×1, სახელმწიფოთაშორისი→შორისი×1, ნატო→ნატოში×1, კათალიკოს→კათალიქოს×1

Worst items:

- `cv-ka-dev-common_voice_ka_21455841` {'C': 6, 'S': 4, 'D': 3, 'I': 1, 'N': 13, 'M': 11}
  - ref: სასტიკი ცენზურის პირობებში ვისოცკი ეხებოდა აკრძალულ თემებს მღეროდა ყოველდღიურ საბჭოთა ცხოვრებაზე სამამულო ომზე
  - hyp: სასტიკი ცენზურის პირობებში ვისაც კი ეხებოდა აკრძალა თემებს მყეროდაყოველდგიურსაბჭოთა ცხოვრებაზე წამომოლოომზე
- `cv-ka-dev-common_voice_ka_21381375` {'C': 7, 'S': 4, 'D': 3, 'I': 0, 'N': 14, 'M': 11}
  - ref: ქალაქ ლელუს ნანგრევები მსგავსია ნან მადოლის ნანგრევებთან კუნძულ პონპეიზე მაგრამ თარიღდება უფრო გვიანდელი პერიოდით
  - hyp: ქალაქ ლევუს ნანგრევები მსგავსია ნანმადოლის ნაკრებებთან კუნძულ პომპეიზემაგრამცაირიხდება უფრო გვიანდელი პერიოდით
- `cv-ka-dev-common_voice_ka_21381415` {'C': 5, 'S': 7, 'D': 0, 'I': 0, 'N': 12, 'M': 12}
  - ref: ითვლება რომ სწორედ დედის რომანტიკულმა ბუნებამ იქონია უდიდესი ზეგავლენა ახალგაზრდა მოდილიანის მსოფლმხედველობაზე
  - hyp: ითვლება რომ სწორად დედის რომანტიკულმა ბუნება მიქონიაუდიდესის რეგვენა ახალ გაცდა მოდილიანის მსოფხედველობაზე
- `cv-ka-dev-common_voice_ka_23826174` {'C': 7, 'S': 4, 'D': 2, 'I': 0, 'N': 13, 'M': 11}
  - ref: ზურგის ზედა მხარე შავია აყრია ოთხკუთხა და მრავალრიცხოვანი მცირე ზომის მომრგვალებული თეთრი ლაქები
  - hyp: ზურგის ედამღარე შავია აღრია ოთკუთხა და მრავალრიცხოვანი მცირე ზომის მორგვალებულითეთრი ლაქები
- `cv-ka-dev-common_voice_ka_21382340` {'C': 2, 'S': 3, 'D': 3, 'I': 0, 'N': 8, 'M': 5}
  - ref: ყვავილები შეკრებილია ფარისებრ ან საგველა ყვავილედებად იშვიათად ერთეულია
  - hyp: ყვავილები შეკრებილია ფარისებანსაგველა ყვავილებად იშვიადადერთეულია
