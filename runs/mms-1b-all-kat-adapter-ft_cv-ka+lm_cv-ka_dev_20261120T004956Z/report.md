# mms-1b-all-kat-adapter-ft_cv-ka+lm_cv-ka_dev (dev)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 10.28% | 9.45% – 11.20% | 10.11% | 1.86% | 1.59% – 2.19% | 29.61% | 4.29% | 10.21% | 16.86% | 0.003 | 381.4 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 98237, 'S': 7833, 'D': 2625, 'I': 715, 'N': 108695, 'M': 106785}  
Char counts: {'C': 877464, 'S': 5426, 'D': 8583, 'I': 2597, 'N': 891473, 'M': 885487}

Top substitutions (ref → hyp × n): ახალგაზრდა→ახალგაზდა×14, წმიდა→წმინდა×8, დავით→დავიდ×6, აბსიდით→აფსიდით×5, უეფა→უეფას×5, თავმჯდომარე→თავჯდომარე×5, ნიკოლოზ→ნიკოლას×5, აბსიდის→აფსიდის×5, თავის→თავისი×5, მატჩში→მათში×4

Worst items:

- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 1, 'D': 12, 'I': 0, 'N': 13, 'M': 1}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: არესის
- `cv-ka-dev-common_voice_ka_40255793` {'C': 1, 'S': 4, 'D': 7, 'I': 0, 'N': 12, 'M': 5}
  - ref: მიუხედავად დამთვალიერებლების სიჭარბისა მომავალი წლის ივნისში ედგარ ალან პოს სახლ მუზეუმი დაიხურება
  - hyp: მიუხედავად დამთვალიელების სჭასიჭარბისამომავალიწლისი მჟიედგარააპლოსსახლმუზეობი დაიხურა
- `cv-ka-dev-common_voice_ka_49293620` {'C': 3, 'S': 7, 'D': 4, 'I': 0, 'N': 14, 'M': 10}
  - ref: დრო არი ჩემო პატარავ იცოდე ერტი ამბავი ედელის როდა ბადალი დღეს საქართელოს მთა ბრი
  - hyp: დროარი ჩემოტიიამბავი ედელის რო და ბადალი დღეს საქართველოს მთა ფრი
- `cv-ka-dev-common_voice_ka_39760415` {'C': 0, 'S': 1, 'D': 10, 'I': 0, 'N': 11, 'M': 1}
  - ref: მანამდე გენერალური მდივნის პოსტს დიმიტრი ბოკერია ბოლო ერთი თვის განმავლობაში იკავებდა
  - hyp: ააბიგიმირაგიისდიმიტრიუკერიაბოუეისალობაშიკაი
- `cv-ka-dev-common_voice_ka_40618092` {'C': 0, 'S': 1, 'D': 10, 'I': 0, 'N': 11, 'M': 1}
  - ref: საბოლოო ჯამში იანგმა ჯგუფი დატოვა და მისი ადგილი სტივ ვესტმა დაიკავა
  - hyp: იასი
