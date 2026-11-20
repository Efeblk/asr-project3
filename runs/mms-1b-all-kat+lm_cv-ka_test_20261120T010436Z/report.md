# mms-1b-all-kat+lm_cv-ka_test (test)

- Model: `facebook/mms-1b-all` @ `3d33597edbdaaba14a8e858e2c8caa76e3cec0cd` (hf-ctc, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14258 | 84004 | 13.50% | 12.73% – 14.39% | 13.75% | 3.08% | 2.59% – 3.67% | 32.20% | 5.52% | 13.42% | 21.57% | 0.003 | 366.7 | 0/1 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 93901, 'S': 9729, 'D': 4171, 'I': 655, 'N': 107801, 'M': 104285}  
Char counts: {'C': 856493, 'S': 10802, 'D': 13463, 'I': 2855, 'N': 880758, 'M': 870150}

Top substitutions (ref → hyp × n): საქართველოს→საქართველო×17, ახალგაზრდა→ახალგაზდა×16, გვხვდება→ხვდება×14, ერთ→ერთერთი×9, წმიდა→წმინდა×8, სახელმწიფოს→სახელმწიფო×8, ერთ→ერთად×8, დააარსა→დაარსა×7, მათგანი→მადგანი×6, მსოფლიოს→მსოფლიო×5

Worst items:

- `cv-ka-test-common_voice_ka_39760373` {'C': 0, 'S': 2, 'D': 13, 'I': 0, 'N': 15, 'M': 2}
  - ref: ამის შემდეგ ერთხანს მსახურობდა მღვდლად ხოლო პირველი მსოფლიო ომის დროს იყო ავსტრია უნგრეთის არმიის კაპელანი
  - hyp: abcenlatnsacontaencascomty ncucnonbcacaffoucnnatsalmecafla
- `cv-ka-test-common_voice_ka_40338901` {'C': 0, 'S': 2, 'D': 12, 'I': 0, 'N': 14, 'M': 2}
  - ref: სწორედ ამ შენობასთან მოკლეს ფრანც ფერდინანდი რაც შემდგომ პირველი მსოფლიო ომის დაწყების მიზეზი გახდა
  - hyp: soensenbasangkuvesaansaendananscenewalnsala onussabisnececikafa
- `cv-ka-test-common_voice_ka_40097233` {'C': 0, 'S': 1, 'D': 13, 'I': 0, 'N': 14, 'M': 1}
  - ref: კერძოდ მასთან ერთად იყვენ ჯო ლინ ტერნერი იენს იუჰანსონი და მისი ძმა პატრიკ იუჰანსონი
  - hyp: essmansamanjonntenerycunhansonamcicnamatriunhanony
- `cv-ka-test-common_voice_ka_40855669` {'C': 0, 'S': 5, 'D': 9, 'I': 0, 'N': 14, 'M': 5}
  - ref: ვინაიდან მას მაქსიმილიანის სახით უკვე ჰყავდა უფროსი ძმა ტახტზე ასვლის იმედი არ უნდა ჰქონოდა
  - hyp: მინა დრამას მაქსიმილიანი სასულე ყავდოლქერწმატახწეასუმედიაუნდაქუმდა
- `cv-ka-test-common_voice_ka_40097318` {'C': 0, 'S': 1, 'D': 12, 'I': 0, 'N': 13, 'M': 1}
  - ref: ანტისოციალური პიროვნების აშლილობის მქონე ადამიანი ხასიათდება სხვა ადამიანის უფლებების უგულვებელყოფით და მათი დარღვევით
  - hyp: andnsatnnanashinehaanannkankberabichuwelafitemantangoabire
