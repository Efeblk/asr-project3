# mms-1b-all-kat-adapter-ft_cv-ka+lm-a0.8-b0.0_cv-ka_dev (dev)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z)
- Hardware: NVIDIA GeForce RTX 4070 SUPER; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 11.88% | 10.97% – 12.87% | 11.55% | 2.07% | 1.78% – 2.40% | 30.72% | 4.48% | 11.84% | 18.78% | 0.003 | 378.3 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 96137, 'S': 8206, 'D': 4352, 'I': 350, 'N': 108695, 'M': 104693}  
Char counts: {'C': 875262, 'S': 5693, 'D': 10518, 'I': 2236, 'N': 891473, 'M': 883191}

Top substitutions (ref → hyp × n): ახალგაზრდა→ახალგაზდა×12, წმიდა→წმინდა×8, უეფა→უეფას×5, თავმჯდომარე→თავჯდომარე×5, ერთ→ერთი×5, თავის→თავისი×5, დიდ→დიდი×4, აბსიდით→აფსიდით×4, მატჩში→მათში×4, აბსიდის→აფსიდის×4

Worst items:

- `cv-ka-dev-common_voice_ka_34227472` {'C': 4, 'S': 3, 'D': 10, 'I': 0, 'N': 17, 'M': 7}
  - ref: მუსტაფა იყო ქოფრიულიუ მეჰმედ ფაშას შვილი ქოფრიულიუ ფაზილ აჰმედ ფაშას ძმა და ქოფრიულიუ ამჯაზადე ჰუსეინ ფაშას ბიძაშვილი
  - hyp: მუსტაფა იყო ქოფრიულიუმეჰმედფაშასშვილი ქოფრიულიუფაზილაჰმედფაშასძმა და ქოფრიულიუ ამჯაზადეჰუზეინფაშასბიძაშვილი
- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 1, 'D': 12, 'I': 0, 'N': 13, 'M': 1}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: არის
- `cv-ka-dev-common_voice_ka_39695153` {'C': 2, 'S': 5, 'D': 7, 'I': 0, 'N': 14, 'M': 7}
  - ref: მოსკოვის სახელმწიფო ლინგვისტური უნივერსიტეტი არის რუსეთის ერთ ერთი ყველაზე დიდი უმაღლესი სასწავლებელი ენათმეცნიერების დარგში
  - hyp: მოსკოვის სახელმსიფოლინგვისსტუდიუნივერსიტეტი არისრუსეთის ერთიდხველაზებებიუმანასის სასწავებელი ენათმეცნიების დარგში
- `cv-ka-dev-common_voice_ka_40255793` {'C': 1, 'S': 4, 'D': 7, 'I': 0, 'N': 12, 'M': 5}
  - ref: მიუხედავად დამთვალიერებლების სიჭარბისა მომავალი წლის ივნისში ედგარ ალან პოს სახლ მუზეუმი დაიხურება
  - hyp: მიუხედავად დამთვალიელების სჭასიჭარბისამომავალიწლისი მშიედგარააპოსსახლმუზეობი დაიხურა
- `cv-ka-dev-common_voice_ka_49293620` {'C': 3, 'S': 5, 'D': 6, 'I': 0, 'N': 14, 'M': 8}
  - ref: დრო არი ჩემო პატარავ იცოდე ერტი ამბავი ედელის როდა ბადალი დღეს საქართელოს მთა ბრი
  - hyp: დროარი ჩემოტიიამბავი ედელის როდაბადალი დღეს საქართველოს მთა ფრი
