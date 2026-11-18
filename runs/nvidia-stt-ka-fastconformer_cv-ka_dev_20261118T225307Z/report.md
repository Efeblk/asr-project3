# nvidia-stt-ka-fastconformer_cv-ka_dev (dev)

- Model: `nvidia/stt_ka_fastconformer_hybrid_large_pc` @ `bdfd7871e0574001e650e741d6201d40205db6bb` (nemo, float32, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA L4; batch size 16
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 4.46% | 3.94% – 5.05% | 4.39% | 1.09% | 0.88% – 1.34% | 8.88% | 1.54% | 4.45% | 7.99% | 0.004 | 272.0 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 104093, 'S': 4006, 'D': 596, 'I': 242, 'N': 108695, 'M': 108341}  
Char counts: {'C': 883352, 'S': 3272, 'D': 4849, 'I': 1622, 'N': 891473, 'M': 888246}

Top substitutions (ref → hyp × n): წმიდა→წმინდა×7, მსოფლიო→მსოფლიოს×4, აბსიდის→აფსიდის×4, ეროვნულ→ეროვნული×4, სამეურვეო→სამეურნეო×3, აღმოსავლეთი→აღმოსავლეთ×3, ერთმანეთისაგან→ერთმანეთისგან×3, თუ→და×3, ერთ→ერთი×3, აფსიდში→აბსიდში×2

Worst items:

- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 2, 'D': 11, 'I': 0, 'N': 13, 'M': 2}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: ხუთი ზურგზე
- `cv-ka-dev-common_voice_ka_40618092` {'C': 0, 'S': 0, 'D': 11, 'I': 0, 'N': 11, 'M': 0}
  - ref: საბოლოო ჯამში იანგმა ჯგუფი დატოვა და მისი ადგილი სტივ ვესტმა დაიკავა
  - hyp: 
- `cv-ka-dev-common_voice_ka_40356724` {'C': 0, 'S': 2, 'D': 9, 'I': 0, 'N': 11, 'M': 2}
  - ref: გუგენჰაიმის სპირალურად დახვეული თეთრი აივნებიდანაც ავტომობილის ნაწილებით დამზადებული ექსტრავაგანტული ფიგურები იმზირებიან
  - hyp: შვიდი ექვსი
- `cv-ka-dev-common_voice_ka_49293620` {'C': 4, 'S': 5, 'D': 5, 'I': 0, 'N': 14, 'M': 9}
  - ref: დრო არი ჩემო პატარავ იცოდე ერტი ამბავი ედელის როდა ბადალი დღეს საქართელოს მთა ბრი
  - hyp: დრორი შემოჭრი ამბავი ედერის როდა ბადალი დღეს საქართველოს მთავრი
- `cv-ka-dev-common_voice_ka_40352416` {'C': 0, 'S': 2, 'D': 8, 'I': 0, 'N': 10, 'M': 2}
  - ref: იმ დროისათვის როდესაც ისინი ინგლისში დაბრუნდნენ მერი უკვე ორსულად იყო
  - hyp: ხუთი ზურგზე
