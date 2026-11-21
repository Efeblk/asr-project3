# whisper-large-v3-turbo+lf-split_fleurs-ka_test (test)

- Model: `openai/whisper-large-v3-turbo` @ `41f01f3fe87f28c78e2fbf8b568835947dd65ed9` (hf-whisper, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 16
- Dataset: `data/fleurs/ka_ge/manifest.jsonl` sha256 `d95e58e9db45`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 979 | 11054 | 126.05% | 121.58% – 130.92% | 129.28% | 108.51% | 105.51% – 111.75% | 123.25% | 107.23% | 99.97% | 100.00% | 0.015 | 68.3 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 7, 'S': 4836, 'D': 12295, 'I': 4471, 'N': 17138, 'M': 9314}  
Char counts: {'C': 19078, 'S': 103568, 'D': 14530, 'I': 30752, 'N': 137176, 'M': 153398}

Top substitutions (ref → hyp × n): და→შრის×20, და→დის×19, და→ერის×17, რომ→შრის×15, და→ევის×14, და→გის×13, არ→ერის×9, რომ→ერის×8, და→რის×8, რომ→დის×8

Worst items:

- `fleurs-ka_ge-test-3829894572460928182` {'C': 0, 'S': 11, 'D': 0, 'I': 211, 'N': 11, 'M': 222}
  - ref: ამაზონზე წყლის სრული 20 პროცენტი მოდის რომელიც ოკეანეებში პლანეტის მდინარეებიდან ჩაედინება
  - hyp: amazon z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z
- `fleurs-ka_ge-test-8445087190321283400` {'C': 0, 'S': 38, 'D': 0, 'I': 113, 'N': 38, 'M': 151}
  - ref: tmz ის გასართობები ახალი ამბების ვებგვერდის მიხედვით ფოტოგრაფმა თავისი მანქანა გააჩერა სეპულვედას ბულვარის მოპირდაპირე მხარეს გზის გადაჭრამდე და გაგრძელებამდე პოლიციის გაჩერების გადასაღებად რამაც აიძულა კალიფორნიის მაგისტრალის საპატრულო პოლიცია რომ ორჯერ გაეჩერებინა მოძრაობა იმისთვის რომ ებრძანა მისთვის უკან დაბრუნება
  - hyp: t m z s gacar tovev e b aqali a b aqali a b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b aqali b a
- `fleurs-ka_ge-test-17644889022942506393` {'C': 0, 'S': 26, 'D': 0, 'I': 124, 'N': 26, 'M': 150}
  - ref: კრისტინა ფერნანდეს დე კირხნერმა არგენტინის მოქმედმა სენატორმა და პირველმა ლედიმ ბუენოს აირესიდან 50 კილომეტრის 31 მილის დაშორებით ქალაქ ლა პლატაში წუხელ გააკეთა განცხადება საპრეზიდენტო კანდიდატობასთან დაკავშირებით
  - hyp: cristina pérdantes de círcnerma argentiní smoque medo senat o rmada b hirva alma l edim buéno sáires tën 90 km y d ašro b hid kala klaplata shid zúhálg gag etr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n
- `fleurs-ka_ge-test-11278009017393569939` {'C': 0, 'S': 13, 'D': 0, 'I': 92, 'N': 13, 'M': 105}
  - ref: ვირტუალური ექსკურსია არის მომავალი მოსწავლეებისთვის მოგზაურობის ასახვისა და საკუთარი გამოცდილების გაზიარების შესანიშნავი საშუალება
  - hyp: virtual re excursiya ariz mamao ol imasao ol ebis yus moqzao ol ebis asaxista saku tariqa maisu ebis qaziyyara ebis shasani ishin evi sašo ol ebis gaziyyara ebis shasani evi sašo ol ebis gaziyyara ebis shasani evi sašo ol ebis gaziyyara ebis shasani evi sašo ol ebis gaziyyara ebis shasani evi sašo ol ebis gaziyyara ebis shasani evi sašo ol ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara e
- `fleurs-ka_ge-test-8281069223978847593` {'C': 0, 'S': 15, 'D': 0, 'I': 74, 'N': 15, 'M': 89}
  - ref: ფოლკლენდის ფუნტი fkp ფოლკლენდის ოფიციალური ვალუტას წარმოადგენს რომლის ვალუტის კურსი ერთ ბრიტანულ ფუნტს gbp უდრის
  - hyp: poglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis
