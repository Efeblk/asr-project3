# mms-1b-all-kat-adapter-ft_cv-ka-seed13_cv-ka_test (test)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka-seed13_20261121T004458Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka-seed13_20261121T004458Z)
- Hardware: NVIDIA A100-SXM4-40GB; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14258 | 84004 | 21.91% | 21.08% – 22.86% | 22.14% | 3.61% | 3.35% – 3.94% | 38.97% | 5.99% | 21.63% | 36.21% | 0.001 | 796.9 | 0/1 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 85583, 'S': 19528, 'D': 2690, 'I': 1398, 'N': 107801, 'M': 106509}  
Char counts: {'C': 855255, 'S': 14156, 'D': 11347, 'I': 6313, 'N': 880758, 'M': 875724}

Top substitutions (ref → hyp × n): საქართველოს→საქართველო×16, სამეურნეო→სამეორნეო×10, შავი→შავიზღვის×10, არამედ→არამეთ×10, ქვეშ→ქვეში×10, მათგანი→მადგანი×9, თბილისში→თბილიში×9, მიიღო→მიიყო×9, სწორკუთხა→წორკუთხა×9, წმიდა→წმინდა×8

Worst items:

- `cv-ka-test-common_voice_ka_39760373` {'C': 1, 'S': 11, 'D': 3, 'I': 0, 'N': 15, 'M': 12}
  - ref: ამის შემდეგ ერთხანს მსახურობდა მღვდლად ხოლო პირველი მსოფლიო ომის დროს იყო ავსტრია უნგრეთის არმიის კაპელანი
  - hyp: ამის შენნი აჭილ სახეოდა იდელდას ხოლოში იპერეცუკლი იყომესრას უყავსე ალია ომინათისარმეს კამპელა
- `cv-ka-test-common_voice_ka_40855669` {'C': 0, 'S': 7, 'D': 7, 'I': 0, 'N': 14, 'M': 7}
  - ref: ვინაიდან მას მაქსიმილიანის სახით უკვე ჰყავდა უფროსი ძმა ტახტზე ასვლის იმედი არ უნდა ჰქონოდა
  - hyp: მინაიდრამასმაქსიმილიანი სახეთუგე ყავდა უფირწმა ტახწეასუმედი აუნდა ქენდი
- `cv-ka-test-common_voice_ka_39760147` {'C': 1, 'S': 10, 'D': 3, 'I': 0, 'N': 14, 'M': 11}
  - ref: საშუალო სკოლის დამთავრების შემდეგ სწავლა განაგრძო ივანე ჯავახიშვილის სახელობის სახელმწიფო უნივერსიტეტში გეოგრაფია გეოლოგიის ფაკულტეტზე
  - hyp: საშოოის პოისდორცობშებდე სხავლაგანნაგდვა იბანე ჯაუნიჩვის საღებობის ახერთისა უნივერსიტეტში გეოგრაფფია გეოლოპიის ბაგლზენზე
- `cv-ka-test-common_voice_ka_40338901` {'C': 1, 'S': 11, 'D': 2, 'I': 0, 'N': 14, 'M': 12}
  - ref: სწორედ ამ შენობასთან მოკლეს ფრანც ფერდინანდი რაც შემდგომ პირველი მსოფლიო ომის დაწყების მიზეზი გახდა
  - hyp: სწვერი ბამშინობასა მოქვე სობანციები დინანდი რაცია შემგინ პიველი მსობლიო ომისაფაწყების მისიძი გახდა
- `cv-ka-test-common_voice_ka_39930460` {'C': 1, 'S': 10, 'D': 2, 'I': 0, 'N': 13, 'M': 11}
  - ref: მთელი ეს ამბავი მალე გავრცელდა იტალიაში და კატერინას ბიძის ლუდოვიკო სფორცას ყურამდეც მივიდა
  - hyp: თელიესამბავრულ მანე გაღძროდა ითალიშ და კატერინად დიდის რმუდოვნიკოს პორწევს კურამდე სენდას
