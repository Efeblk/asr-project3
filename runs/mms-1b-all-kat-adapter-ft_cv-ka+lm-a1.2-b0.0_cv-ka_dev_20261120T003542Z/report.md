# mms-1b-all-kat-adapter-ft_cv-ka+lm-a1.2-b0.0_cv-ka_dev (dev)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 20.01% | 18.88% – 21.22% | 19.33% | 2.87% | 2.56% – 3.24% | 37.37% | 5.25% | 19.98% | 29.22% | 0.003 | 369.6 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 87106, 'S': 11358, 'D': 10231, 'I': 158, 'N': 108695, 'M': 98622}  
Char counts: {'C': 867926, 'S': 6785, 'D': 16762, 'I': 2080, 'N': 891473, 'M': 876791}

Top substitutions (ref → hyp × n): წმიდა→წმინდა×8, ერთ→ერთი×7, თავმჯდომარე→თავჯდომარე×5, არა→არამხოლოდ×5, ახალგაზრდა→ახალგაზდა×5, თავის→თავისი×5, დიდ→დიდი×4, აბსიდით→აფსიდით×4, უეფა→უეფას×4, აბსიდის→აფსიდის×4

Worst items:

- `cv-ka-dev-common_voice_ka_34227472` {'C': 3, 'S': 3, 'D': 11, 'I': 0, 'N': 17, 'M': 6}
  - ref: მუსტაფა იყო ქოფრიულიუ მეჰმედ ფაშას შვილი ქოფრიულიუ ფაზილ აჰმედ ფაშას ძმა და ქოფრიულიუ ამჯაზადე ჰუსეინ ფაშას ბიძაშვილი
  - hyp: მუსტაფა იყო ქოფრიულიუმეჰმედფაშასშვილი ქოფრიულიუფაზილაჰმედფაშასძმა და ქოფრიულიუამჯაზადეჰუზეინფაშასბიძაშვილი
- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 1, 'D': 12, 'I': 0, 'N': 13, 'M': 1}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: არის
- `cv-ka-dev-common_voice_ka_49293754` {'C': 2, 'S': 6, 'D': 6, 'I': 0, 'N': 14, 'M': 8}
  - ref: თანამშრომლობდა ისეთ გამოჩენილ მუსიკოსებთან როგორებიც არიან პოლ მაკარტნი ტონი ბენეტი დაიანა კროლი მარიან მაკპორტლანდი
  - hyp: თანამშრომლობდაისეთიგამაჩენი მუსიკოსებთან როგორებიცაარიან პოლმაკარტნი ტომი ბენეტი დაიანაკროლი მარიანმაკროპტრანდი
- `cv-ka-dev-common_voice_ka_39695153` {'C': 2, 'S': 5, 'D': 7, 'I': 0, 'N': 14, 'M': 7}
  - ref: მოსკოვის სახელმწიფო ლინგვისტური უნივერსიტეტი არის რუსეთის ერთ ერთი ყველაზე დიდი უმაღლესი სასწავლებელი ენათმეცნიერების დარგში
  - hyp: მოსკოვის სახელმსიფოლინგვისსტუდიუნივერსიტეტი არისრუსეთის ერთიდხველაზებებიუმანასის სასწავებელი ენათმეცნიების დარგში
- `cv-ka-dev-common_voice_ka_40057383` {'C': 0, 'S': 3, 'D': 9, 'I': 0, 'N': 12, 'M': 3}
  - ref: კუნძულოვან სკანდინავიურ ენებს განეკუთვნება რომელიც დიდი ხნის მანძილზე სხვა ენებისგან იზოლირებულად ვითარდებოდა
  - hyp: კუნძულოვანიკანდინავიურიენებისგანებოთობა რომელითამოძედასხვალიათან ისურებლადვითარდებოდ
