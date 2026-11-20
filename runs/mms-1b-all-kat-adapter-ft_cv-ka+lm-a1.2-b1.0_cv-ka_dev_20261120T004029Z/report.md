# mms-1b-all-kat-adapter-ft_cv-ka+lm-a1.2-b1.0_cv-ka_dev (dev)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 17.62% | 16.57% – 18.82% | 17.04% | 2.64% | 2.34% – 3.00% | 35.40% | 5.03% | 17.59% | 26.17% | 0.003 | 372.4 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 89734, 'S': 10416, 'D': 8545, 'I': 192, 'N': 108695, 'M': 100342}  
Char counts: {'C': 870010, 'S': 6483, 'D': 14980, 'I': 2096, 'N': 891473, 'M': 878589}

Top substitutions (ref → hyp × n): წმიდა→წმინდა×8, ახალგაზრდა→ახალგაზდა×6, ერთ→ერთი×6, თავმჯდომარე→თავჯდომარე×5, თავის→თავისი×5, დიდ→დიდი×4, აბსიდით→აფსიდით×4, უეფა→უეფას×4, მსოფლიოს→მსოფლიო×4, აბსიდის→აფსიდის×4

Worst items:

- `cv-ka-dev-common_voice_ka_34227472` {'C': 3, 'S': 3, 'D': 11, 'I': 0, 'N': 17, 'M': 6}
  - ref: მუსტაფა იყო ქოფრიულიუ მეჰმედ ფაშას შვილი ქოფრიულიუ ფაზილ აჰმედ ფაშას ძმა და ქოფრიულიუ ამჯაზადე ჰუსეინ ფაშას ბიძაშვილი
  - hyp: მუსტაფა იყო ქოფრიულიუმეჰმედფაშასშვილი ქოფრიულიუფაზილაჰმედფაშასძმა და ქოფრიულიუამჯაზადეჰუზეინფაშასბიძაშვილი
- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 1, 'D': 12, 'I': 0, 'N': 13, 'M': 1}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: არის
- `cv-ka-dev-common_voice_ka_39695153` {'C': 2, 'S': 5, 'D': 7, 'I': 0, 'N': 14, 'M': 7}
  - ref: მოსკოვის სახელმწიფო ლინგვისტური უნივერსიტეტი არის რუსეთის ერთ ერთი ყველაზე დიდი უმაღლესი სასწავლებელი ენათმეცნიერების დარგში
  - hyp: მოსკოვის სახელმსიფოლინგვისსტუდიუნივერსიტეტი არისრუსეთის ერთიდხველაზებებიუმანასის სასწავებელი ენათმეცნიების დარგში
- `cv-ka-dev-common_voice_ka_40057383` {'C': 0, 'S': 3, 'D': 9, 'I': 0, 'N': 12, 'M': 3}
  - ref: კუნძულოვან სკანდინავიურ ენებს განეკუთვნება რომელიც დიდი ხნის მანძილზე სხვა ენებისგან იზოლირებულად ვითარდებოდა
  - hyp: კუნძულოვანიკანდინავიურიენებისგანებოთობა რომელითამოძედასხვალიათან ისურებლადვითარდებოდ
- `cv-ka-dev-common_voice_ka_49295110` {'C': 1, 'S': 5, 'D': 7, 'I': 0, 'N': 13, 'M': 6}
  - ref: მეფეს ხელში თოფი მისცა ბრმა თვალი დაუხუჭა და საღი თვალით ირემი მიზანში ამოაღებინა
  - hyp: მეფესხელში თოფიმისცა ბრმათვალიდაუხუჭა და საღირთვალითირემი მიზანშიამოაღებინა
