# speed4070_mms-1b-all-kat-adapter-ft_cv-ka_cv-ka_dev500 (dev)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 500 | 2926 | 19.92% | 14.21% – 26.65% | 19.44% | 2.88% | 1.78% – 4.20% | 37.58% | 5.32% | 19.70% | 33.61% | 0.003 | 356.9 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 3159, 'S': 661, 'D': 71, 'I': 43, 'N': 3891, 'M': 3863}  
Char counts: {'C': 30988, 'S': 471, 'D': 258, 'I': 186, 'N': 31717, 'M': 31645}

Top substitutions (ref → hyp × n): მხარის→მხარეს×2, სწორედ→სწორად×2, მიეღო→მიიღო×2, წმიდა→წმინდა×2, სამხრეთ→სავხრეთ×2, ქართულ→ქართულკავკასიური×1, ხალხთა→ხალხდა×1, რომელიც→რომელთა×1, ალ→ალტაბარის×1, ტაბარის→თხძულებების×1

Worst items:

- `cv-ka-dev-common_voice_ka_21358400` {'C': 5, 'S': 8, 'D': 2, 'I': 0, 'N': 15, 'M': 13}
  - ref: კუნძულის კლიმატი სუბტროპიკულია რბილი ზამთრით და ავსტრალიაში ერთ ერთი პოპულარული ადგილია წყალქვეშა ცურვის მოყვარულებს შორის
  - hyp: კუნძულის კლიმატის სუბტროპიკულია რბილის ზამთრითდ ავსტრალიაშჯერთ ერთი პოპულარული ადგინდა წყალქოშა ცხუგვის მოყოვრულებს შორის
- `cv-ka-dev-common_voice_ka_21455841` {'C': 6, 'S': 6, 'D': 1, 'I': 1, 'N': 13, 'M': 13}
  - ref: სასტიკი ცენზურის პირობებში ვისოცკი ეხებოდა აკრძალულ თემებს მღეროდა ყოველდღიურ საბჭოთა ცხოვრებაზე სამამულო ომზე
  - hyp: წასტიკი ცენზურის პირობებში ვისაც კი ეხებოდა აგრძავლობ თემებს მყეროდა ყოველდგიურ საბჭოთა ცხოვრებაზე წამომოლოომზე
- `cv-ka-dev-common_voice_ka_21362490` {'C': 6, 'S': 7, 'D': 0, 'I': 1, 'N': 13, 'M': 14}
  - ref: მეფემ ბრძანა მოეკლათ ყველა მამაკაცი ვისაც იარაღის ტარება შეუძლია ხოლო დანარჩენი მოსახლეობა განდევნა
  - hyp: მეფემბრძანა მოეკლოთ ყველა მამა კაცი ვისაც იარ აღის სტარება შეუძლია ხოლო დანარჩენი მოსახლეობა განდევნა
- `cv-ka-dev-common_voice_ka_21365362` {'C': 9, 'S': 6, 'D': 1, 'I': 0, 'N': 16, 'M': 15}
  - ref: მდებარეობს ჩეხეთის ისტორიული მხარის ბოჰემიის სამხრეთ აღმოსავლეთ ნაწილში და ნაწილობრივ ისტორიული მხარის მორავიის სამხრეთ დასავლეთ ნაწილში
  - hyp: მდებარეობს ჩახეთის ისტორიული მხარეს ბოჰემიის სამხლით აგავძალეთ ნაწილში და ნაწილობრივ ისტორიული მხარეს მორავიის სამხრეთდასავლეთ ნაწილში
- `cv-ka-dev-common_voice_ka_21381415` {'C': 5, 'S': 7, 'D': 0, 'I': 0, 'N': 12, 'M': 12}
  - ref: ითვლება რომ სწორედ დედის რომანტიკულმა ბუნებამ იქონია უდიდესი ზეგავლენა ახალგაზრდა მოდილიანის მსოფლმხედველობაზე
  - hyp: ითვლება რომ სწორა დედის რომანტიკულმა ბუნება მიქონია უდიდესის რეგოვენა ახალდარცდა მოდილიანის მსოფხედველობაზე
