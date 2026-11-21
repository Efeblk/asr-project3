# mms-1b-all-kat-adapter-ft_cv-ka-seed7_cv-ka_test (test)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka-seed7_20261121T002912Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka-seed7_20261121T002912Z)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14258 | 84004 | 22.01% | 21.17% – 22.95% | 22.22% | 3.62% | 3.36% – 3.94% | 39.08% | 6.00% | 21.72% | 36.30% | 0.002 | 423.6 | 0/1 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 85496, 'S': 19537, 'D': 2768, 'I': 1419, 'N': 107801, 'M': 106452}  
Char counts: {'C': 855286, 'S': 14133, 'D': 11339, 'I': 6415, 'N': 880758, 'M': 875834}

Top substitutions (ref → hyp × n): საქართველოს→საქართველო×24, მიიღო→მიიყო×11, მათგანი→მადგანი×10, შავი→შავიზღვის×9, არამედ→არამეთ×9, მამამისი→მისი×9, სწორკუთხა→წორკუთხა×9, შტაბ→შტაბბინა×9, წმიდა→წმინდა×8, ქვეშ→ქვეში×8

Worst items:

- `cv-ka-test-common_voice_ka_39760373` {'C': 0, 'S': 9, 'D': 6, 'I': 0, 'N': 15, 'M': 9}
  - ref: ამის შემდეგ ერთხანს მსახურობდა მღვდლად ხოლო პირველი მსოფლიო ომის დროს იყო ავსტრია უნგრეთის არმიის კაპელანი
  - hyp: აბიშენნი აწილ სახეოდა თიგელდას ქოლეშიმერეცუკლიიყომისრას უყავსე ალია ომიყნათისარმეს კამპელა
- `cv-ka-test-common_voice_ka_40855669` {'C': 0, 'S': 8, 'D': 6, 'I': 0, 'N': 14, 'M': 8}
  - ref: ვინაიდან მას მაქსიმილიანის სახით უკვე ჰყავდა უფროსი ძმა ტახტზე ასვლის იმედი არ უნდა ჰქონოდა
  - hyp: მინაიდრამას მაქსიმილიანი სახთუგა ყავდა უქირწმა ტახწეასუმედი აონდა ქუნდა
- `cv-ka-test-common_voice_ka_40338901` {'C': 1, 'S': 9, 'D': 4, 'I': 0, 'N': 14, 'M': 10}
  - ref: სწორედ ამ შენობასთან მოკლეს ფრანც ფერდინანდი რაც შემდგომ პირველი მსოფლიო ომის დაწყების მიზეზი გახდა
  - hyp: სწვერი ბამშინობასარ მოკვე სოანცებდინანდი რაციაშიმგირ კეველი მსობლიო ომისადმწების მისეცი გახდა
- `cv-ka-test-common_voice_ka_40097233` {'C': 1, 'S': 8, 'D': 5, 'I': 0, 'N': 14, 'M': 9}
  - ref: კერძოდ მასთან ერთად იყვენ ჯო ლინ ტერნერი იენს იუჰანსონი და მისი ძმა პატრიკ იუჰანსონი
  - hyp: ეძოდმასაიწყნენ ჯონ ლინტერნერი იეს იჰანსტონი და მისითმაა პატრი ილჰანსტონი
- `cv-ka-test-common_voice_ka_39760147` {'C': 2, 'S': 9, 'D': 3, 'I': 0, 'N': 14, 'M': 11}
  - ref: საშუალო სკოლის დამთავრების შემდეგ სწავლა განაგრძო ივანე ჯავახიშვილის სახელობის სახელმწიფო უნივერსიტეტში გეოგრაფია გეოლოგიის ფაკულტეტზე
  - hyp: საშავისპოის ნორცხებშებდე სხავლაგანდაგდავა იპანე ჯაურიჩვის საღებობის ახერთისა უნივერსიტეტში გეოგრაფია გეოლოპიის ბაგლდენდე
