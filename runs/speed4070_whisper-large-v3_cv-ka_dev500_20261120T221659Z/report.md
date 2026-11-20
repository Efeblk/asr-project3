# speed4070_whisper-large-v3_cv-ka_dev500 (dev)

- Model: `openai/whisper-large-v3` @ `06f233fe06e710322aca913c1bc4249a0d71fce1` (hf-whisper, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 500 | 2926 | 73.97% | 65.80% – 80.83% | 76.33% | 17.19% | 12.96% – 22.08% | 76.39% | 17.50% | 70.04% | 90.04% | 0.084 | 11.8 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 1231, 'S': 2462, 'D': 198, 'I': 218, 'N': 3891, 'M': 3911}  
Char counts: {'C': 27351, 'S': 2925, 'D': 1441, 'I': 1085, 'N': 31717, 'M': 31361}

Top substitutions (ref → hyp × n): მდებარეობს→დებარეობს×8, მთავარი→თავარი×6, და→ადა×6, მდინარე→დინარე×4, ერთ→ერთერთი×4, სხვა→ხვა×3, თუმცა→მცა×3, არა→არამ×3, მცირე→ცირე×3, ეკლესია→ეგლესია×3

Worst items:

- `cv-ka-dev-common_voice_ka_21382342` {'C': 0, 'S': 3, 'D': 0, 'I': 19, 'N': 3, 'M': 22}
  - ref: მკლავები თანაბარი ზომისაა
  - hyp: მედისის მედისის მედისის მედისის მედისის მედისის მედისის მედისის მედისის მედისის მედისის მედისის მედისის მედისის მედისის მედისის მედისის მედისის მედისის მედისის მედისის მ
- `cv-ka-dev-common_voice_ka_21382336` {'C': 0, 'S': 12, 'D': 2, 'I': 0, 'N': 14, 'M': 12}
  - ref: ჯერ კიდევ გამეფებამდე უთანხმოება ჰქონდა მამასთან და უმცროს ძმასთან დიმიტრისთან რომელსაც თავის მეტოქედ თვლიდა
  - hyp: ჩერკიდო გამეფებაბდე უთახმებახ ქონდა მამასტანდა მსვრს მასაი დიმეტრისთან რომ უსეს თავისმეტო ქეთვლიდა
- `cv-ka-dev-common_voice_ka_21358400` {'C': 1, 'S': 13, 'D': 1, 'I': 0, 'N': 15, 'M': 14}
  - ref: კუნძულის კლიმატი სუბტროპიკულია რბილი ზამთრით და ავსტრალიაში ერთ ერთი პოპულარული ადგილია წყალქვეშა ცურვის მოყვარულებს შორის
  - hyp: კუნდულის ქლიმატი სუბტროპიქულიარ ბილის ამთით ავსტრელეს დერსესი პოპულა რულია დგილეთ ყავქვშეთ სხულის მოყავრულების შორის
- `cv-ka-dev-common_voice_ka_21382328` {'C': 2, 'S': 12, 'D': 0, 'I': 0, 'N': 14, 'M': 14}
  - ref: ავტორია ხალხთა გამოცდილებების წიგნისა რომელიც ალ ტაბარის თხზულებების შემდეგ პირველი მნიშვნელოვანი შრომაა მსოფლიო ისტორიაში
  - hyp: ავტორია ხალხდა გამოცილებების ზიგნისა მემოლთა ალტა ბარის ფხრსულებების შემდეგ პიროლი მისნავოვანიშ რომამ სოფრიო ესტორიაში
- `cv-ka-dev-common_voice_ka_21356983` {'C': 2, 'S': 10, 'D': 1, 'I': 1, 'N': 13, 'M': 13}
  - ref: ალბომზე უკრავენ ცნობილი მუსიკოსები ჯეფ პორკარო პინო პალადინო ჯონ ლორდი და სტივ უინვუდი
  - hyp: ალბომ ზე უკრავენც ნობილი მუსიკოსები ჩეფ ორგარო პინო ბალადინო ჩონ ლორდიტა სთივ ბვინუდი
