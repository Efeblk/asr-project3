# mms-1b-all-kat-adapter-ft_cv-ka-seed7+lm_cv-ka_test (test)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka-seed7_20261121T002912Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka-seed7_20261121T002912Z)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14258 | 84004 | 10.97% | 10.37% – 11.61% | 10.88% | 2.12% | 1.90% – 2.39% | 30.40% | 4.56% | 10.90% | 17.99% | 0.003 | 377.2 | 1/1 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 96732, 'S': 8343, 'D': 2726, 'I': 759, 'N': 107801, 'M': 105834}  
Char counts: {'C': 864900, 'S': 6373, 'D': 9485, 'I': 2805, 'N': 880758, 'M': 874078}

Top substitutions (ref → hyp × n): ახალგაზრდა→ახალგაზდა×18, წმიდა→წმინდა×8, თავისი→თავის×7, საქართველოს→საქართველო×6, მეფემ→მეფე×5, ტერიტორიაზე→ტერიტორიას×5, სახელმწიფოს→სახელმწიფო×5, მსოფლიოს→მსოფლიო×4, ბოლოს→ბოლო×4, ციხესიმაგრის→სიმაგრის×4

Worst items:

- `cv-ka-test-common_voice_ka_39760373` {'C': 1, 'S': 12, 'D': 2, 'I': 0, 'N': 15, 'M': 13}
  - ref: ამის შემდეგ ერთხანს მსახურობდა მღვდლად ხოლო პირველი მსოფლიო ომის დროს იყო ავსტრია უნგრეთის არმიის კაპელანი
  - hyp: ამის შენი აისახებოდა იძენდა ხალებიანი ციკლი იყო მასას ახაშალა ომისათვის არ მის კაპელას
- `cv-ka-test-common_voice_ka_41819001` {'C': 0, 'S': 4, 'D': 10, 'I': 0, 'N': 14, 'M': 4}
  - ref: გარდამოიხილე ზეცით ღმერთო იხილე მოხედე ვენახსა მას და განამტკიცე ესე რომელ დაასხა მარჯვენამან შენმან
  - hyp: გარდა მოიხილესზაცითხმერთოიხილემოხედევენახსამასდაგანარგცეეზე რომელთა ასამარჯვემანშენმან
- `cv-ka-test-common_voice_ka_40097318` {'C': 0, 'S': 6, 'D': 7, 'I': 0, 'N': 13, 'M': 6}
  - ref: ანტისოციალური პიროვნების აშლილობის მქონე ადამიანი ხასიათდება სხვა ადამიანის უფლებების უგულვებელყოფით და მათი დარღვევით
  - hyp: ამის სოციალური ბრაუნების კავშირების ადამია ეხელძელემააურბებებიუგველყოფიდამათიდამგოები
- `cv-ka-test-common_voice_ka_39760147` {'C': 2, 'S': 3, 'D': 9, 'I': 0, 'N': 14, 'M': 5}
  - ref: საშუალო სკოლის დამთავრების შემდეგ სწავლა განაგრძო ივანე ჯავახიშვილის სახელობის სახელმწიფო უნივერსიტეტში გეოგრაფია გეოლოგიის ფაკულტეტზე
  - hyp: საშოს აისორებშებდესხავლაგანაგდაიპანეჯაუჩვისაღებობისახეისაუნივერსიტეტში გეოგრაფია გეოლოგიის აგდებენ
- `cv-ka-test-common_voice_ka_49319910` {'C': 1, 'S': 3, 'D': 9, 'I': 0, 'N': 13, 'M': 4}
  - ref: აბა იქით გაიხედე მაიმუნი მაიმუნობს აბა კლასში ეს ბიჭები რასღა ჩხუბობთ თქვა პიშკებო
  - hyp: აბა იქეთგაიხედემაიმონიმაიმუნობსაბაკლასშიეზბიჭები რაღაც ჩხუდთქვაპიშკებო
