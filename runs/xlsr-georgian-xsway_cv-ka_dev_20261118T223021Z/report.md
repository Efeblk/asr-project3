# xlsr-georgian-xsway_cv-ka_dev (dev)

- Model: `xsway/wav2vec2-large-xlsr-georgian` @ `b29b81945f5fa2e35fbb05da5256815d8cc71e20` (hf-ctc, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA L4; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 44.58% | 42.29% – 46.90% | 44.03% | 8.33% | 7.61% – 9.17% | 56.46% | 10.50% | 43.52% | 65.56% | 0.002 | 656.8 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 62900, 'S': 40111, 'D': 5684, 'I': 2666, 'N': 108695, 'M': 105677}  
Char counts: {'C': 832145, 'S': 35040, 'D': 24288, 'I': 14947, 'N': 891473, 'M': 882132}

Top substitutions (ref → hyp × n): ერთ→ერთერთი×169, ერთ→ერთერთ×37, იყო→იღო×16, სხვადასხვა→სხვა×16, მისი→მის×15, რამდენიმე→რამდენი×15, მსოფლიო→სოფლიო×14, მმართველობის→მართველობის×14, შემდეგ→შემდე×14, საქართველოს→საქართველო×13

Worst items:

- `cv-ka-dev-common_voice_ka_40319640` {'C': 1, 'S': 14, 'D': 0, 'I': 3, 'N': 15, 'M': 18}
  - ref: ასევე ლუიზამ დაიწყო მეგობრული ურთიერთობების ჩამოყალიბება ოსმალეთის იმპერიასთან რაც შემდგომში მრავალსაუკუნოვან საფრანგეთ ოსმალეთის ალიანსში გადაიზარდა
  - hyp: ასველუიზამ დაიწყო მენკიუვრუვლი იუთ თირთუბსა მოყალიბე ფავს უმალეთის ინპერიასენ დ რაცჩიემთ გონდში მრავალდ საუკურუნოვა მსაფრანგეთ ოსმალეთის ალიანში გადაიძებდა
- `cv-ka-dev-common_voice_ka_40145345` {'C': 2, 'S': 13, 'D': 0, 'I': 1, 'N': 15, 'M': 16}
  - ref: აღნიშნული ნაშრომი ერთ ერთი უძველესი წერილობითი დოკუმენტია რომელიც მნიშვნელოვან ცნობებს გვაწვდის ბალტიისპირეთის ქვეყნების გაქრისტიანების შესახებ
  - hyp: აღდიშთული და შსრობი ერთაერ თუუ უზველეზი წერიდობრდი დოკუმეტია რობელიც მლისდელოა წზოვეზ გაწტის დალტიისპირეთის ქვეყნების გაქსისტიალები შესახებ
- `cv-ka-dev-common_voice_ka_40392984` {'C': 2, 'S': 12, 'D': 0, 'I': 2, 'N': 14, 'M': 16}
  - ref: თავისი საქმიანობის შესახებ ყოველწლიურად წარუდგენდა მოხსენებას გაეროს გენერალური ასამბლეას და საჭიროების შემთხვევაში უშიშროების საბჭოს
  - hyp: თავიში სახვეობეს შესახა ყავლწილიურად წარუკინდა მოხსენე ბას გაეროს გინერალური აასამბლეას და საჭი როის შემთხვეში უშიშროლების სებჭოს
- `cv-ka-dev-common_voice_ka_40145591` {'C': 1, 'S': 14, 'D': 0, 'I': 0, 'N': 15, 'M': 15}
  - ref: ეს არის უკანასკნელი იმ ნახატებს შორის რომლებიც ვინსენტმა სენ რემი დე პროვანსში საფრანგეთში ყოფნისას დახატა
  - hyp: ეალის უპარასკლელი იბ და ხატებს შორის რობლები ვიზეტუა სეედ რები დეეპოროოვა ასი საფრაგეტში ყოფრდისდას დახადა
- `cv-ka-dev-common_voice_ka_40030973` {'C': 3, 'S': 9, 'D': 0, 'I': 5, 'N': 12, 'M': 17}
  - ref: კათოლიკეები პაპს ხედავენ როგორც წმინდა პეტრეს გამგრძელებელს და კათოლიკური ეკლესიის მიწიერ ხელმძღვანელს
  - hyp: ყებარში ჭალის ათოლრი კეები ჰკაფს ხიდავენ როგორც მინდა პეტერი დამაგრძელებლობ და კატმუუ პირე ილესნაყანი ამი ანელიწიერე ხელმძღვანელს
