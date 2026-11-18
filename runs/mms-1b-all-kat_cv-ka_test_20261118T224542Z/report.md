# mms-1b-all-kat_cv-ka_test (test)

- Model: `facebook/mms-1b-all` @ `3d33597edbdaaba14a8e858e2c8caa76e3cec0cd` (hf-ctc, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA L4; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14258 | 84004 | 24.14% | 23.22% – 25.18% | 24.76% | 4.45% | 3.97% – 5.04% | 40.14% | 6.77% | 23.83% | 39.42% | 0.004 | 283.3 | 0/1 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 83181, 'S': 21367, 'D': 3253, 'I': 1401, 'N': 107801, 'M': 105949}  
Char counts: {'C': 848039, 'S': 19413, 'D': 13306, 'I': 6477, 'N': 880758, 'M': 873929}

Top substitutions (ref → hyp × n): საქართველოს→საქართველო×30, გვხვდება→გხვდება×17, ოლქში→ოლგში×14, მათგანი→მადგანი×11, არამედ→არამეთ×11, შავი→შავიზღვის×10, მიიღო→მიიყო×10, ქვეშ→ქვეში×10, წევრი→სწევრი×9, სწორკუთხა→წორკუთხა×9

Worst items:

- `cv-ka-test-common_voice_ka_39743792` {'C': 0, 'S': 12, 'D': 0, 'I': 5, 'N': 12, 'M': 17}
  - ref: მნიშვნელოვანი საქმიანობა იყო ცხენებისა და ძაღლების რეგულარული გასეირნება ასევე საფეხბურთო მატჩები ყინულზე
  - hyp: naconal d afიაnabl cs cn fcn cაn ლeბc reguლarn s neboყ fn safeჭ მუto nაn cen 1nnn
- `cv-ka-test-common_voice_ka_39760373` {'C': 0, 'S': 11, 'D': 4, 'I': 0, 'N': 15, 'M': 11}
  - ref: ამის შემდეგ ერთხანს მსახურობდა მღვდლად ხოლო პირველი მსოფლიო ომის დროს იყო ავსტრია უნგრეთის არმიის კაპელანი
  - hyp: anbicently atensacontafbencas comity bn encucne onbencancaf foucn na a natusalmec anfela
- `cv-ka-test-common_voice_ka_40338901` {'C': 0, 'S': 7, 'D': 7, 'I': 0, 'N': 14, 'M': 7}
  - ref: სწორედ ამ შენობასთან მოკლეს ფრანც ფერდინანდი რაც შემდგომ პირველი მსოფლიო ომის დაწყების მიზეზი გახდა
  - hyp: soe kensen basangkuvesesabfansaendi anansicenten ewalinsalwa onusonsabisi nencencikafa
- `cv-ka-test-common_voice_ka_40097233` {'C': 0, 'S': 9, 'D': 5, 'I': 0, 'N': 14, 'M': 9}
  - ref: კერძოდ მასთან ერთად იყვენ ჯო ლინ ტერნერი იენს იუჰანსონი და მისი ძმა პატრიკ იუჰანსონი
  - hyp: esas mansack manjon ninternery yec unhansonina mucicna matricc unhanstony
- `cv-ka-test-common_voice_ka_40855669` {'C': 0, 'S': 7, 'D': 7, 'I': 0, 'N': 14, 'M': 7}
  - ref: ვინაიდან მას მაქსიმილიანის სახით უკვე ჰყავდა უფროსი ძმა ტახტზე ასვლის იმედი არ უნდა ჰქონოდა
  - hyp: ინაიდრამაას მაქსიმილიამი სახდუგა ყავდოლქვერწმა ტახწეასუმედი აუნდა ქუმდა
