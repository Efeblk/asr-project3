# speed4070_mms-1b-all-kat_cv-ka_dev500 (dev)

- Model: `facebook/mms-1b-all` @ `3d33597edbdaaba14a8e858e2c8caa76e3cec0cd` (hf-ctc, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 500 | 2926 | 21.36% | 15.21% – 28.29% | 20.70% | 3.09% | 1.91% – 4.46% | 37.79% | 5.44% | 21.09% | 35.48% | 0.003 | 382.0 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 3109, 'S': 692, 'D': 90, 'I': 49, 'N': 3891, 'M': 3850}  
Char counts: {'C': 30936, 'S': 504, 'D': 277, 'I': 198, 'N': 31717, 'M': 31638}

Top substitutions (ref → hyp × n): მიეღო→მიიღო×2, არა→არამხოლოდ×2, მევენახეობა→ნახეობა×2, სამხრეთ→სავხეს×2, პარიზში→პარისში×2, ხალხთა→ხალხდა×1, რომელიც→რომელთა×1, ალ→ალტაბარის×1, ტაბარის→თხვძულებების×1, შრომაა→შრომა×1

Worst items:

- `cv-ka-dev-common_voice_ka_21358400` {'C': 3, 'S': 9, 'D': 3, 'I': 0, 'N': 15, 'M': 12}
  - ref: კუნძულის კლიმატი სუბტროპიკულია რბილი ზამთრით და ავსტრალიაში ერთ ერთი პოპულარული ადგილია წყალქვეშა ცურვის მოყვარულებს შორის
  - hyp: კუნძულის კლიმატის სუბტროპიკულია რბილის ზამთრითდა ავსტრალიას ჯერთერთი პოპულარულიადიდა წყალქუშა ცხუდვის მოყოვრულებს შორის
- `cv-ka-dev-common_voice_ka_21455841` {'C': 5, 'S': 7, 'D': 1, 'I': 1, 'N': 13, 'M': 13}
  - ref: სასტიკი ცენზურის პირობებში ვისოცკი ეხებოდა აკრძალულ თემებს მღეროდა ყოველდღიურ საბჭოთა ცხოვრებაზე სამამულო ომზე
  - hyp: წასტიკი ცენზურის პირობებში ვისაც კი იხებოდა აგრძავლო თემებს მყეროდე ყოველდგიურ საბჭოთა ცხოვრებაზე სამომოლოომზე
- `cv-ka-dev-common_voice_ka_21381375` {'C': 7, 'S': 6, 'D': 1, 'I': 0, 'N': 14, 'M': 13}
  - ref: ქალაქ ლელუს ნანგრევები მსგავსია ნან მადოლის ნანგრევებთან კუნძულ პონპეიზე მაგრამ თარიღდება უფრო გვიანდელი პერიოდით
  - hyp: ქალაქ ლელუს ნანგრებები მსგავსია ნან მადოლის ნანგრევებთა მკუნძულ პომპეიზე მაგრამცაირეხდება უფრო გვიანდრელი პერიოდით
- `cv-ka-dev-common_voice_ka_21382336` {'C': 7, 'S': 7, 'D': 0, 'I': 0, 'N': 14, 'M': 14}
  - ref: ჯერ კიდევ გამეფებამდე უთანხმოება ჰქონდა მამასთან და უმცროს ძმასთან დიმიტრისთან რომელსაც თავის მეტოქედ თვლიდა
  - hyp: ჯერ კიდველ გამეფებაბდე უთახმოება ჰქონდა მამასთან და მშროს მასთან დიმიტრისთან რომელსაც თავის მეტო ქეთთვლიზა
- `cv-ka-dev-common_voice_ka_21381415` {'C': 5, 'S': 7, 'D': 0, 'I': 0, 'N': 12, 'M': 12}
  - ref: ითვლება რომ სწორედ დედის რომანტიკულმა ბუნებამ იქონია უდიდესი ზეგავლენა ახალგაზრდა მოდილიანის მსოფლმხედველობაზე
  - hyp: ითვლება რომ სწორა დედის რომანტიკულმა ბუნება მიქონია უდიდესის ზეგოვენა ახალდარცდა მოდილიანის მსოფხედველობაზე
