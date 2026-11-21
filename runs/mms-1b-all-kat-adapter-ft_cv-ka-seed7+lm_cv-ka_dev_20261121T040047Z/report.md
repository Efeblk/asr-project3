# mms-1b-all-kat-adapter-ft_cv-ka-seed7+lm_cv-ka_dev (dev)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka-seed7_20261121T002912Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka-seed7_20261121T002912Z)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 10.11% | 9.31% – 11.00% | 9.91% | 1.84% | 1.57% – 2.16% | 29.46% | 4.27% | 10.05% | 16.61% | 0.003 | 386.2 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 98410, 'S': 7731, 'D': 2554, 'I': 708, 'N': 108695, 'M': 106849}  
Char counts: {'C': 877617, 'S': 5315, 'D': 8541, 'I': 2572, 'N': 891473, 'M': 885504}

Top substitutions (ref → hyp × n): ახალგაზრდა→ახალგაზდა×14, წმიდა→წმინდა×8, ციხესიმაგრე→სიმაგრე×6, უეფა→უეფას×5, თავის→თავისი×5, ერთ→ერთი×5, მსოფლიოს→მსოფლიო×4, ლამაზ→ლამას×4, მართლმადიდებელი→მართმადიდებელი×4, დავით→დავიდ×4

Worst items:

- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 1, 'D': 12, 'I': 0, 'N': 13, 'M': 1}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: აი
- `cv-ka-dev-common_voice_ka_49293620` {'C': 3, 'S': 5, 'D': 6, 'I': 0, 'N': 14, 'M': 8}
  - ref: დრო არი ჩემო პატარავ იცოდე ერტი ამბავი ედელის როდა ბადალი დღეს საქართელოს მთა ბრი
  - hyp: მდროარი ჩემკენ ამბავი ედელისროდაბადალი დღეს საქართველოს მთა ბრინი
- `cv-ka-dev-common_voice_ka_39760415` {'C': 0, 'S': 1, 'D': 10, 'I': 0, 'N': 11, 'M': 1}
  - ref: მანამდე გენერალური მდივნის პოსტს დიმიტრი ბოკერია ბოლო ერთი თვის განმავლობაში იკავებდა
  - hyp: ამბიგიმირაიდიმიტრიუკერიაბოეისალობაშიმკარი
- `cv-ka-dev-common_voice_ka_40618092` {'C': 0, 'S': 1, 'D': 10, 'I': 0, 'N': 11, 'M': 1}
  - ref: საბოლოო ჯამში იანგმა ჯგუფი დატოვა და მისი ადგილი სტივ ვესტმა დაიკავა
  - hyp: აი
- `cv-ka-dev-common_voice_ka_40356724` {'C': 0, 'S': 4, 'D': 7, 'I': 0, 'N': 11, 'M': 4}
  - ref: გუგენჰაიმის სპირალურად დახვეული თეთრი აივნებიდანაც ავტომობილის ნაწილებით დამზადებული ექსტრავაგანტული ფიგურები იმზირებიან
  - hyp: ეს ჩვენ არის დატოვა
