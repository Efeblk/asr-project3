# whisper-small+lf-split_fleurs-ka_test (test)

- Model: `openai/whisper-small` @ `973afd24965f72e36ca33b3055d56a652f456b4d` (hf-whisper, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 16
- Dataset: `data/fleurs/ka_ge/manifest.jsonl` sha256 `d95e58e9db45`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 979 | 11054 | 288.95% | 265.93% – 314.91% | 316.41% | 139.05% | 134.20% – 144.50% | 296.72% | 137.68% | 99.99% | 100.00% | 0.018 | 54.1 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 4, 'S': 8755, 'D': 8379, 'I': 32387, 'N': 17138, 'M': 41146}  
Char counts: {'C': 7208, 'S': 120439, 'D': 9529, 'I': 60781, 'N': 137176, 'M': 188428}

Top substitutions (ref → hyp × n): და→ὁ×108, და→ḍᴀ×60, რომ→ὁ×26, არ→ὁ×25, რომ→ḍᴀ×23, როგორც→ὁ×20, არის→ὁ×17, რომელიც→ὁ×15, უფრო→ὁ×14, იყო→ὁ×14

Worst items:

- `fleurs-ka_ge-test-9582162545039538338` {'C': 0, 'S': 15, 'D': 0, 'I': 236, 'N': 15, 'M': 251}
  - ref: ბავშვებზე შეიძლება გადავიდეს მხოლოდ სასქესო უჯრედების მუტაციები სხვაგვარმა მუტაციამ შესაძლოა უჯრედის სიკვდილი ან სიმსივნე გამოიწვიოს
  - hyp: павш palshub is a shahitz is a shahitz is a bagada odis chod saske is a udjeda is mutatia is a udjeda is mutatia is mutatia is mutatia is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is
- `fleurs-ka_ge-test-8344484193456880997` {'C': 0, 'S': 47, 'D': 0, 'I': 101, 'N': 47, 'M': 148}
  - ref: თუმცა ამ გეგმებმა ერთ ღამეში ძალა დაკარგა როდესაც პოლონეთის აღმოსავლეთ რეგიონების დაკავების შემდეგ საბჭოთა კავშირის წითელი არმიის 800 000 ზე მეტი ჯარისკაცი შემოვიდა და ბელორუსიის და უკრაინის ფრონტები გახსნა რაც რიგის სამშვიდობო ხელშეკრულების საბჭოთა პოლონეთის არა აგრესიის პაქტის და სხვა ორმხრივი და მრავალმხრივი საერთაშორისო ხელშეკრულებების დარღვევას წარმოადგენდა
  - hyp: ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ
- `fleurs-ka_ge-test-9429206554614431092` {'C': 0, 'S': 47, 'D': 0, 'I': 101, 'N': 47, 'M': 148}
  - ref: თუმცა ამ გეგმებმა ერთ ღამეში ძალა დაკარგა როდესაც პოლონეთის აღმოსავლეთ რეგიონების დაკავების შემდეგ საბჭოთა კავშირის წითელი არმიის 800 000 ზე მეტი ჯარისკაცი შემოვიდა და ბელორუსიის და უკრაინის ფრონტები გახსნა რაც რიგის სამშვიდობო ხელშეკრულების საბჭოთა პოლონეთის არა აგრესიის პაქტის და სხვა ორმხრივი და მრავალმხრივი საერთაშორისო ხელშეკრულებების დარღვევას წარმოადგენდა
  - hyp: ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ
- `fleurs-ka_ge-test-5692698162144733243` {'C': 0, 'S': 43, 'D': 0, 'I': 105, 'N': 43, 'M': 148}
  - ref: 1988 წლიდან გადაწყდა რომ საარჩევნო ყუთი გამჭვირვალე უნდა იყოს რათა ამომრჩევლებს და დამკვირვებლებს ჰქონდეთ შესაძლებლობა თავად დარწმუნდნენ იმაში რომ კენჭისყრის დასაწყისში ყუთში კონვერტი არ ყოფილა და რომ მას არ დაემატა ზედმეტი კონვერტები გარდა იმ სწორად დათვლილის და ხმის მიცემის უფლების მქონე პირების კონვერტებისა
  - hyp: ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ
- `fleurs-ka_ge-test-8281898248373405277` {'C': 0, 'S': 39, 'D': 0, 'I': 109, 'N': 39, 'M': 148}
  - ref: ჩვენებიდან ხუთ წუთში ქარი იწყებს ბზრიალს დაახლოებით ერთი წუთის შემდეგ ქარი აღწევს 70 კმ სთ ში შემდეგ მოდის წვიმა მაგრამ ისეთი ძლიერი და ისეთი დიდი რომ კანზე ნემსივით გერჭობათ შემდეგ ციდან სეტყვა მოდის ხალხი პანიკაშია ყვირიან და ერთმანეთს თელავენ
  - hyp: ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ
