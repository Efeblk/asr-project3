# whisper-large-v3-turbo_fleurs-ka_test (test)

- Model: `openai/whisper-large-v3-turbo` @ `41f01f3fe87f28c78e2fbf8b568835947dd65ed9` (hf-whisper, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA A100-SXM4-40GB; batch size 32
- Dataset: `data/fleurs/ka_ge/manifest.jsonl` sha256 `d95e58e9db45`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 979 | 11054 | 126.84% | 122.00% – 132.11% | 129.79% | 108.54% | 105.43% – 111.93% | 124.53% | 107.30% | 99.98% | 100.00% | 0.010 | 103.0 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 5, 'S': 4895, 'D': 12238, 'I': 4604, 'N': 17138, 'M': 9504}  
Char counts: {'C': 19131, 'S': 103525, 'D': 14520, 'I': 30839, 'N': 137176, 'M': 153495}

Top substitutions (ref → hyp × n): და→დის×21, და→რის×16, და→ერის×15, და→შრის×14, და→გის×12, რომ→დის×11, რომ→შრის×10, არ→ერის×9, და→ევის×9, რომ→რის×8

Worst items:

- `fleurs-ka_ge-test-3829894572460928182` {'C': 0, 'S': 11, 'D': 0, 'I': 211, 'N': 11, 'M': 222}
  - ref: ამაზონზე წყლის სრული 20 პროცენტი მოდის რომელიც ოკეანეებში პლანეტის მდინარეებიდან ჩაედინება
  - hyp: amazon z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z
- `fleurs-ka_ge-test-17644889022942506393` {'C': 0, 'S': 26, 'D': 0, 'I': 124, 'N': 26, 'M': 150}
  - ref: კრისტინა ფერნანდეს დე კირხნერმა არგენტინის მოქმედმა სენატორმა და პირველმა ლედიმ ბუენოს აირესიდან 50 კილომეტრის 31 მილის დაშორებით ქალაქ ლა პლატაში წუხელ გააკეთა განცხადება საპრეზიდენტო კანდიდატობასთან დაკავშირებით
  - hyp: cristina pérdantes de círcnerma argentiní smoque medo senat o rmada b hirva alma l edim buéno sáires tën 90 km y d ašro b hid kala klaplata shid zúhálg gag etr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n hidr n
- `fleurs-ka_ge-test-1695286420858857376` {'C': 0, 'S': 26, 'D': 0, 'I': 119, 'N': 26, 'M': 145}
  - ref: კრისტინა ფერნანდეს დე კირხნერმა არგენტინის მოქმედმა სენატორმა და პირველმა ლედიმ ბუენოს აირესიდან 50 კილომეტრის 31 მილის დაშორებით ქალაქ ლა პლატაში წუხელ გააკეთა განცხადება საპრეზიდენტო კანდიდატობასთან დაკავშირებით
  - hyp: cristina fernandez d a kierxner ma argentismocondos senat urmada pirmadadad urmada ledi nusarist nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd nd
- `fleurs-ka_ge-test-11278009017393569939` {'C': 0, 'S': 13, 'D': 0, 'I': 92, 'N': 13, 'M': 105}
  - ref: ვირტუალური ექსკურსია არის მომავალი მოსწავლეებისთვის მოგზაურობის ასახვისა და საკუთარი გამოცდილების გაზიარების შესანიშნავი საშუალება
  - hyp: virtual re excursiya ariz mamao ol imasao ol ebis yus moqzao ol ebis asaxista saku tariqa maisu ebis qaziyyara ebis shasani ishin evi sašo ol ebis gaziyyara ebis shasani evi sašo ol ebis gaziyyara ebis shasani evi sašo ol ebis gaziyyara ebis shasani evi sašo ol ebis gaziyyara ebis shasani evi sašo ol ebis gaziyyara ebis shasani evi sašo ol ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara ebis gaziyyara e
- `fleurs-ka_ge-test-8281069223978847593` {'C': 0, 'S': 15, 'D': 0, 'I': 74, 'N': 15, 'M': 89}
  - ref: ფოლკლენდის ფუნტი fkp ფოლკლენდის ოფიციალური ვალუტას წარმოადგენს რომლის ვალუტის კურსი ერთ ბრიტანულ ფუნტს gbp უდრის
  - hyp: poglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis pooglandis
