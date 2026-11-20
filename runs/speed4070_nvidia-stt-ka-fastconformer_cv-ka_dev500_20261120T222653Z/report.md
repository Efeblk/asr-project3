# speed4070_nvidia-stt-ka-fastconformer_cv-ka_dev500 (dev)

- Model: `nvidia/stt_ka_fastconformer_hybrid_large_pc` @ `bdfd7871e0574001e650e741d6201d40205db6bb` (nemo, float32, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 500 | 2926 | 4.65% | 3.30% – 6.27% | 4.47% | 0.92% | 0.55% – 1.39% | 9.97% | 1.45% | 4.64% | 8.43% | 0.004 | 252.5 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 3719, 'S': 154, 'D': 18, 'I': 9, 'N': 3891, 'M': 3882}  
Char counts: {'C': 31477, 'S': 137, 'D': 103, 'I': 53, 'N': 31717, 'M': 31667}

Top substitutions (ref → hyp × n): წმიდა→წმინდა×2, ქართულ→ქართულკასიური×1, პლაკატი→ბლაკატი×1, რომელიც→რომელთა×1, ალ→ალტაბარის×1, შრომაა→შრომა×1, უინვუდი→ბინუდი×1, ნატო→ნატოში×1, მღელვარება→ელვარება×1, იქმნა→იქნა×1

Worst items:

- `cv-ka-dev-common_voice_ka_21382328` {'C': 10, 'S': 3, 'D': 1, 'I': 0, 'N': 14, 'M': 13}
  - ref: ავტორია ხალხთა გამოცდილებების წიგნისა რომელიც ალ ტაბარის თხზულებების შემდეგ პირველი მნიშვნელოვანი შრომაა მსოფლიო ისტორიაში
  - hyp: ავტორია ხალხთა გამოცდილებების წიგნისა რომელთა ალტაბარის თხზულებების შემდეგ პირველი მნიშვნელოვანი შრომა მსოფლიო ისტორიაში
- `cv-ka-dev-common_voice_ka_21381375` {'C': 10, 'S': 3, 'D': 1, 'I': 0, 'N': 14, 'M': 13}
  - ref: ქალაქ ლელუს ნანგრევები მსგავსია ნან მადოლის ნანგრევებთან კუნძულ პონპეიზე მაგრამ თარიღდება უფრო გვიანდელი პერიოდით
  - hyp: ქალაქ ლევუს ნანგრევები მსგავსია ნანადგოლის ნანგრევებთან კუნძულ პომპეიზე მაგრამ თარიღდება უფრო გვიანდელი პერიოდით
- `cv-ka-dev-common_voice_ka_21381399` {'C': 7, 'S': 2, 'D': 2, 'I': 0, 'N': 11, 'M': 9}
  - ref: მისი მიზანი სარაევოს მულტიკულტურული და ტოლერანტული გარემოს აღდგენა და შენარჩუნება იყო
  - hyp: მისი მიზანი სარეევოს მულტიკულტურული და ტოლერანტული გარემოსახდინას შენარჩუნება იყო
- `cv-ka-dev-common_voice_ka_22327453` {'C': 12, 'S': 2, 'D': 1, 'I': 0, 'N': 15, 'M': 14}
  - ref: მისი ხელმძღვანელობით და მონაწილეობით გამოიცა საქართველოს ისტორიულ ეთნოგრაფიული კალენდარი და ქართულ კავკასიური ისტორიულ ეთნოგრაფიული პლაკატი
  - hyp: მისი ხელმძღვანელობით და მონაწილეობით გამოიცა საქართველოს ისტორიულ ეთნოგრაფიული კალენდარი და ქართულკასიური ისტორიულ ეთნოგრაფიული ბლაკატი
- `cv-ka-dev-common_voice_ka_21455841` {'C': 11, 'S': 2, 'D': 0, 'I': 1, 'N': 13, 'M': 14}
  - ref: სასტიკი ცენზურის პირობებში ვისოცკი ეხებოდა აკრძალულ თემებს მღეროდა ყოველდღიურ საბჭოთა ცხოვრებაზე სამამულო ომზე
  - hyp: სასტიკი ცენზორის პირობებში ვისაც კი ეხებოდა აკრძალულ თემებს მღეროდა ყოველდღიურ საბჭოთა ცხოვრებაზე სამამულო ომზე
