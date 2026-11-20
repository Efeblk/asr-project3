# mms-1b-all-kat-adapter-ft_cv-ka+lm_cv-ka_test (test)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14258 | 84004 | 11.07% | 10.47% – 11.72% | 10.97% | 2.13% | 1.91% – 2.41% | 30.45% | 4.57% | 10.99% | 18.11% | 0.003 | 373.8 | 1/1 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 96644, 'S': 8389, 'D': 2768, 'I': 772, 'N': 107801, 'M': 105805}  
Char counts: {'C': 864826, 'S': 6478, 'D': 9454, 'I': 2865, 'N': 880758, 'M': 874169}

Top substitutions (ref → hyp × n): ახალგაზრდა→ახალგაზდა×17, წმიდა→წმინდა×8, საქართველოს→საქართველო×7, სახელმწიფოს→სახელმწიფო×6, ეს→ის×5, ჰქონდათ→ჰქონდა×5, ქვეშ→ქვეში×5, თავისი→თავის×5, თვითმმართველობის→თვითმართველობის×4, ჩრდილოეთ→ჩდილოეთ×4

Worst items:

- `cv-ka-test-common_voice_ka_39760373` {'C': 1, 'S': 11, 'D': 3, 'I': 0, 'N': 15, 'M': 12}
  - ref: ამის შემდეგ ერთხანს მსახურობდა მღვდლად ხოლო პირველი მსოფლიო ომის დროს იყო ავსტრია უნგრეთის არმიის კაპელანი
  - hyp: ამის შენი აისახებოდა იძენდა ხანაშივე ციკლი ყოფნისას უკავია ომისათვის არ მის კაპელას
- `cv-ka-test-common_voice_ka_40097318` {'C': 1, 'S': 5, 'D': 7, 'I': 1, 'N': 13, 'M': 7}
  - ref: ანტისოციალური პიროვნების აშლილობის მქონე ადამიანი ხასიათდება სხვა ადამიანის უფლებების უგულვებელყოფით და მათი დარღვევით
  - hyp: ანი სოციალური ბრაუნების კავშირების ორი ადამიანი ხერძელეომასწავაურბებებიუიველყოფიდამათიდარღვევი
- `cv-ka-test-common_voice_ka_41819001` {'C': 1, 'S': 4, 'D': 9, 'I': 0, 'N': 14, 'M': 5}
  - ref: გარდამოიხილე ზეცით ღმერთო იხილე მოხედე ვენახსა მას და განამტკიცე ესე რომელ დაასხა მარჯვენამან შენმან
  - hyp: გარდა მოიხილასზაცითხმერთოიხილემოხედევენახსამასდაგანარგცეეზე რომელ და ასამარჯვემანშენმან
- `cv-ka-test-common_voice_ka_39695177` {'C': 0, 'S': 11, 'D': 0, 'I': 1, 'N': 11, 'M': 12}
  - ref: ესპანეთთან დაზავების შემდგომ ანრიმ განიზრახა ფრანკო ესპანური ალიანსი დინასტიური ქორწინებით გაემყარებინა
  - hyp: კაცი შედის სახელის ვარაუდები ნიკა დენიკინის იულიანას ხმელი ამარა მას შეიყვარა საყურებლად
- `cv-ka-test-common_voice_ka_40097326` {'C': 1, 'S': 5, 'D': 6, 'I': 1, 'N': 12, 'M': 7}
  - ref: ქრისტიანობის შემოსვლის შემდეგ წარმართულ ლამარიას ცვლის მარიამ ღვთისმშობელი კულტი კი იგივე რჩება
  - hyp: ტიან ობის სამსარის შემდეგ წარმოადგინა მარია შრისმარიანხრიშომელიკილიდაივერჩიბა
