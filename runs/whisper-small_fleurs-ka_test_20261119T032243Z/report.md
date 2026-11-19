# whisper-small_fleurs-ka_test (test)

- Model: `openai/whisper-small` @ `973afd24965f72e36ca33b3055d56a652f456b4d` (hf-whisper, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA A100-SXM4-40GB; batch size 32
- Dataset: `data/fleurs/ka_ge/manifest.jsonl` sha256 `d95e58e9db45`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 979 | 11054 | 284.13% | 260.04% – 311.02% | 313.85% | 139.27% | 134.30% – 144.72% | 296.91% | 137.88% | 99.99% | 100.00% | 0.017 | 58.2 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 4, 'S': 8193, 'D': 8941, 'I': 31561, 'N': 17138, 'M': 39758}  
Char counts: {'C': 6630, 'S': 119165, 'D': 11381, 'I': 60493, 'N': 137176, 'M': 186288}

Top substitutions (ref → hyp × n): და→ὁ×94, და→ḍᴀ×53, არ→ὁ×23, რომ→ὁ×22, როგორც→ὁ×20, რომ→ḍᴀ×17, არის→ὁ×17, რომელიც→ὁ×15, იყო→ὁ×14, ის→ὁ×14

Worst items:

- `fleurs-ka_ge-test-9582162545039538338` {'C': 0, 'S': 15, 'D': 0, 'I': 236, 'N': 15, 'M': 251}
  - ref: ბავშვებზე შეიძლება გადავიდეს მხოლოდ სასქესო უჯრედების მუტაციები სხვაგვარმა მუტაციამ შესაძლოა უჯრედის სიკვდილი ან სიმსივნე გამოიწვიოს
  - hyp: павш palshub is a shahitz is a shahitz is a bagada odis chod saske is a udjeda is mutatia is a udjeda is mutatia is mutatia is mutatia is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is a udjeda is
- `fleurs-ka_ge-test-4897513078525575761` {'C': 0, 'S': 34, 'D': 0, 'I': 114, 'N': 34, 'M': 148}
  - ref: იქედან გამომდინარე რომ დინოზავრის ბუმბულებს არ აქვთ კარგად განვითარებული ღერო ეგრეთ წოდებული ხერხემალი თუმცა მათ აქვთ ბუმბულის სხვა მახასიათებლები ჯაგარი და ბალანი მკვლევარები ვარაუდობენ რომ შესაძლოა ხერხემალი უფრო გვიან ჩამოყალიბდა ვიდრე ეს სხვა მახასიათებლები
  - hyp: ὀ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ
- `fleurs-ka_ge-test-618833957383434021` {'C': 0, 'S': 27, 'D': 0, 'I': 121, 'N': 27, 'M': 148}
  - ref: ყოველდღიური განცხადებები მეტროში მხოლოდ კატალონიურ ენაზე ცხადდება თუმცა ავტომატური სისტემა გაუთვალისწინებელი შემთხვევების შესახებ რამდენიმე ენაზე ავრცელებს განცხადებებს მაგალითად ისეთ ენებზე როგორიცაა ესპანური ინგლისური ფრანგული არაბული და იაპონური
  - hyp: ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ
- `fleurs-ka_ge-test-5049282784602300685` {'C': 0, 'S': 26, 'D': 0, 'I': 122, 'N': 26, 'M': 148}
  - ref: ქალბატონი კირჩნერის განცხადებით იგი აპირებს არგენტინის თეატრში პრეზიდენტის პოსტზე კენჭი იყაროს იმავე ადგილას სადაც მან 2005 წელს სენატის კამპანია დაიწყო როგორც ბუენოს აირესის პროვინციის დელეგაციის წევრმა
  - hyp: ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ ὁ
- `fleurs-ka_ge-test-14376816698210131109` {'C': 0, 'S': 28, 'D': 0, 'I': 120, 'N': 28, 'M': 148}
  - ref: ლომების პრაიდი ქცევებით ძალიან ჰგავს მგლების ან ძაღლების ხროვას ცხოველებს რომლებიც ასევე საოცრად ჰგვანან ლომებს ქცევის მანერით მაგრამ არა სხვა დიდ კატებს და ასევე ძალზე მომაკვდინებელია მათი მსხვერპლისთივს
  - hyp: ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន ន
