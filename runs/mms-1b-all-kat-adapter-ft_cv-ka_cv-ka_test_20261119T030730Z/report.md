# mms-1b-all-kat-adapter-ft_cv-ka_cv-ka_test (test)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z)
- Hardware: NVIDIA A100-SXM4-40GB; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14258 | 84004 | 22.00% | 21.16% – 22.97% | 22.22% | 3.63% | 3.36% – 3.95% | 39.15% | 6.01% | 21.70% | 36.33% | 0.001 | 777.8 | 0/1 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 85570, 'S': 19625, 'D': 2606, 'I': 1490, 'N': 107801, 'M': 106685}  
Char counts: {'C': 855408, 'S': 14227, 'D': 11123, 'I': 6619, 'N': 880758, 'M': 876254}

Top substitutions (ref → hyp × n): საქართველოს→საქართველო×24, ქვეშ→ქვეში×10, სწორკუთხა→წორკუთხა×10, მათგანი→მადგანი×9, შავი→შავიზღვის×9, წმიდა→წმინდა×8, ჰყავდა→ყავდა×8, ახალგაზრდა→ახალგაზდა×8, მხოლოდ→ხოლოდ×8, შტაბ→შტაბბინა×8

Worst items:

- `cv-ka-test-common_voice_ka_39760373` {'C': 0, 'S': 14, 'D': 1, 'I': 0, 'N': 15, 'M': 14}
  - ref: ამის შემდეგ ერთხანს მსახურობდა მღვდლად ხოლო პირველი მსოფლიო ომის დროს იყო ავსტრია უნგრეთის არმიის კაპელანი
  - hyp: აბის შენნი აწილ სახელოდა ათი გელდას ქოლოში იბერეცუკლი იყომისრას უყავასო ალია ომაყნათის არმეს კამპელა
- `cv-ka-test-common_voice_ka_40855669` {'C': 0, 'S': 8, 'D': 6, 'I': 0, 'N': 14, 'M': 8}
  - ref: ვინაიდან მას მაქსიმილიანის სახით უკვე ჰყავდა უფროსი ძმა ტახტზე ასვლის იმედი არ უნდა ჰქონოდა
  - hyp: მინაიდრამას მაქსიმილიონი სახეტუგა ყავდა უფირწმა ტახწეასუმედი აუნდა ჰქონდა
- `cv-ka-test-common_voice_ka_40338901` {'C': 1, 'S': 9, 'D': 4, 'I': 0, 'N': 14, 'M': 10}
  - ref: სწორედ ამ შენობასთან მოკლეს ფრანც ფერდინანდი რაც შემდგომ პირველი მსოფლიო ომის დაწყების მიზეზი გახდა
  - hyp: სწველიბამშინობასარ მოკდე სობსანციებ დინანდი რაცია შემღირა კიველიმსოდლიო ომისაფაწების მისიცი გახდა
- `cv-ka-test-common_voice_ka_40097233` {'C': 1, 'S': 7, 'D': 6, 'I': 0, 'N': 14, 'M': 8}
  - ref: კერძოდ მასთან ერთად იყვენ ჯო ლინ ტერნერი იენს იუჰანსონი და მისი ძმა პატრიკ იუჰანსონი
  - hyp: ეძოდმასსაკიყნენ ჯოულინტერნერი იეს იუჰანსტონი და მისითმაა პატრი ილჰანსტონი
- `cv-ka-test-common_voice_ka_40883367` {'C': 0, 'S': 11, 'D': 2, 'I': 0, 'N': 13, 'M': 11}
  - ref: უოლ ი ცდილობს ივა ყოველგვარი საფრთხისგან დაიცვას თუმცა მალე მის წასაყვანად ხომალდი დაბრუნდება
  - hyp: უილი თთილებდა ივო ყოველ გვარი სამეთხისგან დაეჩაქმისა მანი მისწასაყანად ხომადი დაბრურდა
