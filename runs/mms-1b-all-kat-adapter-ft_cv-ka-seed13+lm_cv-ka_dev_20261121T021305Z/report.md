# mms-1b-all-kat-adapter-ft_cv-ka-seed13+lm_cv-ka_dev (dev)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka-seed13_20261121T004458Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka-seed13_20261121T004458Z)
- Hardware: NVIDIA A100-SXM4-40GB; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 10.35% | 9.54% – 11.26% | 10.16% | 1.90% | 1.63% – 2.22% | 29.67% | 4.32% | 10.29% | 16.94% | 0.002 | 515.6 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 98163, 'S': 7847, 'D': 2685, 'I': 723, 'N': 108695, 'M': 106733}  
Char counts: {'C': 877105, 'S': 5520, 'D': 8848, 'I': 2550, 'N': 891473, 'M': 885175}

Top substitutions (ref → hyp × n): ახალგაზრდა→ახალგაზდა×12, წმიდა→წმინდა×7, თავმჯდომარე→თავჯდომარე×6, ნიკოლოზ→ნიკოლას×6, უეფა→უეფას×5, ან→ამ×5, აბსიდით→აფსიდით×4, ჰქონდათ→ჰქონდა×4, ქვეშ→ქვეში×4, ლამაზ→ლამას×4

Worst items:

- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 1, 'D': 12, 'I': 0, 'N': 13, 'M': 1}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: არესის
- `cv-ka-dev-common_voice_ka_49293620` {'C': 3, 'S': 5, 'D': 6, 'I': 0, 'N': 14, 'M': 8}
  - ref: დრო არი ჩემო პატარავ იცოდე ერტი ამბავი ედელის როდა ბადალი დღეს საქართელოს მთა ბრი
  - hyp: დრო ვარი ჩემოტიიამბავი ედელისროდაბადალი დღეს საქართველოს მთა ბრინი
- `cv-ka-dev-common_voice_ka_40363534` {'C': 0, 'S': 5, 'D': 6, 'I': 0, 'N': 11, 'M': 5}
  - ref: სამ წლიანი პაუზის შემდეგ ქანთრის ვარსკვლავმა კით ურბანმა ახალი კრებული გამოსცა
  - hyp: სამს ნეიმპაუზიშემდეგ ქანწრის ვასლავმა ქითურბანმაახალიკრებულიგამოსცა
- `cv-ka-dev-common_voice_ka_40618092` {'C': 0, 'S': 1, 'D': 10, 'I': 0, 'N': 11, 'M': 1}
  - ref: საბოლოო ჯამში იანგმა ჯგუფი დატოვა და მისი ადგილი სტივ ვესტმა დაიკავა
  - hyp: არაადამიანური
- `cv-ka-dev-common_voice_ka_40356724` {'C': 0, 'S': 4, 'D': 7, 'I': 0, 'N': 11, 'M': 4}
  - ref: გუგენჰაიმის სპირალურად დახვეული თეთრი აივნებიდანაც ავტომობილის ნაწილებით დამზადებული ექსტრავაგანტული ფიგურები იმზირებიან
  - hyp: ეს შენობა არის დატოვა
