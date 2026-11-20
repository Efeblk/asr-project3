# speed4070_whisper-large-v3-turbo-ft-r2_cv-ka_cv-ka_dev500 (dev)

- Model: `checkpoints/whisper-large-v3-turbo-ft-r2_cv-ka_20261120T000532Z/final` @ `main` (hf-whisper, float16, cuda)
- System: **ours**: fine-tuned by us from `openai/whisper-large-v3-turbo` on 147.463 h (runs/train_whisper-large-v3-turbo-ft-r2_cv-ka_20261120T000532Z)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 500 | 2926 | 10.64% | 6.33% – 15.97% | 10.01% | 1.85% | 0.96% – 3.02% | 13.56% | 2.20% | 10.61% | 19.18% | 0.025 | 39.8 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 3489, 'S': 370, 'D': 32, 'I': 12, 'N': 3891, 'M': 3871}  
Char counts: {'C': 31227, 'S': 315, 'D': 175, 'I': 97, 'N': 31717, 'M': 31639}

Top substitutions (ref → hyp × n): მხარის→მხარეს×2, მიეღო→მიიღო×2, წმიდა→წმინდა×2, ზღვაში→სხვაში×2, რომელიც→რომელთა×1, ალ→ალტაბარის×1, შრომაა→შრომა×1, წესრიგის→წესრიგი×1, სახელმწიფოთაშორისი→შორისი×1, ნატო→ნატოში×1

Worst items:

- `cv-ka-dev-common_voice_ka_21381415` {'C': 5, 'S': 7, 'D': 0, 'I': 0, 'N': 12, 'M': 12}
  - ref: ითვლება რომ სწორედ დედის რომანტიკულმა ბუნებამ იქონია უდიდესი ზეგავლენა ახალგაზრდა მოდილიანის მსოფლმხედველობაზე
  - hyp: ითვლება რომ სწორა დედის რომანტიკულმა ბუნება მიქონე აუდიდესი ძეგოვენა ახალდაცდა მოდილიანის მსოფლხედველობაზე
- `cv-ka-dev-common_voice_ka_21358400` {'C': 9, 'S': 6, 'D': 0, 'I': 0, 'N': 15, 'M': 15}
  - ref: კუნძულის კლიმატი სუბტროპიკულია რბილი ზამთრით და ავსტრალიაში ერთ ერთი პოპულარული ადგილია წყალქვეშა ცურვის მოყვარულებს შორის
  - hyp: კუნძულის კლიმატი სუბტროპიკულია რბილის ზამთრით და ავსტრილების ერთ ერთი პოპულარული ადგიდა წყალქუშო ცხულვის მოყოვრულების შორის
- `cv-ka-dev-common_voice_ka_23826173` {'C': 9, 'S': 5, 'D': 0, 'I': 1, 'N': 14, 'M': 15}
  - ref: სამარხი ერქვა აგრეთვე მოკლულის დასაკრძალავი ხარჯების საზღაურს რომელიც მკვლელს ან მისთვის პასუხისმგებელ პირს ეკისრებოდა
  - hyp: სამარხი ერქვა აგრეთვე მოკლულის და საკრძალავი ხარჩების საზღვაურს რომელიც კვლელს ან მისთვის მასუხვიდგებელ პირს ეკისრებოდა
- `cv-ka-dev-common_voice_ka_21381375` {'C': 9, 'S': 5, 'D': 0, 'I': 0, 'N': 14, 'M': 14}
  - ref: ქალაქ ლელუს ნანგრევები მსგავსია ნან მადოლის ნანგრევებთან კუნძულ პონპეიზე მაგრამ თარიღდება უფრო გვიანდელი პერიოდით
  - hyp: ქალაქ ლელუს ნანგრებები მსგავსია ნან მადველის ნანგრებებთა კუნძულ პომპეიზე მაგრამ ცაირიხდება უფრო გვიანდელი პერიოდით
- `cv-ka-dev-common_voice_ka_21455841` {'C': 9, 'S': 4, 'D': 0, 'I': 1, 'N': 13, 'M': 14}
  - ref: სასტიკი ცენზურის პირობებში ვისოცკი ეხებოდა აკრძალულ თემებს მღეროდა ყოველდღიურ საბჭოთა ცხოვრებაზე სამამულო ომზე
  - hyp: სასტიკი ცენზურის პირობებში ვისოც კი ეხებოდა აკრძალურ თემებს მყეროდა ყოველდგიურ საბჭოთა ცხოვრებაზე სამამულო ომზე
