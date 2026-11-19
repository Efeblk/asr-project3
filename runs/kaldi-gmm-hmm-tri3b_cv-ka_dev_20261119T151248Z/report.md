# kaldi-gmm-hmm-tri3b_cv-ka_dev (dev)

- Model: `kaldi-gmm-hmm-tri3b (recipes/kaldi-gmm-ka)` @ `bf455f8c389b6ad42ba86d1aa9bcc8e435ab59e6` (kaldi-gmm-hmm, float32, cpu)
- System: **baseline, trained by us from scratch** (standard MFCC + GMM-HMM, A3): MFCC(13)+splice(±3)+LDA(40)+MLLT, speaker-adaptive (fMLLR/SAT) triphone GMM-HMM, 4000 leaves / 40k Gaussians; graphemic lexicon (91145 words), trigram KN LM on CV ka train text only; trained on CV 27.0 ka train (147.46 h)
- Hardware: AMD Ryzen 7 7800X3D 8-Core Processor (16 threads, WSL2 Ubuntu 24.04); batch size None
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: wall clock of MFCC+CMVN extraction and decoding (incl. fMLLR 2nd pass) over parallel CPU jobs; graph building and model loading excluded; per-clip compute_sec is pro-rated by duration

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 20.29% | 18.86% – 21.84% | 20.05% | 7.00% | 6.15% – 7.99% | 37.51% | 9.22% | 19.85% | 32.90% | 0.034 | 29.5 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 89016, 'S': 17260, 'D': 2419, 'I': 2373, 'N': 108695, 'M': 108649}  
Char counts: {'C': 842829, 'S': 27600, 'D': 21044, 'I': 13728, 'N': 891473, 'M': 884157}

Top substitutions (ref → hyp × n): და→სადა×15, შემდეგ→შემდეგი×12, და→ზედა×11, დიდ→დიდი×9, წმიდა→წმინდა×9, ის→ეს×7, ტბა→ტბაა×7, თავის→თავისი×7, ეს→ის×7, ერთ→ერთი×7

Worst items:

- `cv-ka-dev-common_voice_ka_40334033` {'C': 5, 'S': 8, 'D': 0, 'I': 8, 'N': 13, 'M': 21}
  - ref: მან ტარანტინოს საუკეთესო სცენარისტის და საუკეთესო ფილმის პრიზები მოუტანა კომედიის და მიუზიკლის ჟანრებში
  - hyp: თინას არაა საუკეთესო სცენარის დასს გააუქმა ეთერსა ფილმის გააქვთ ფრიზები მოტანა კომედიის და და ამ კომედიის დაამყარა მიიღო ონლაინ კლდის ჟანრებში
- `cv-ka-dev-common_voice_ka_39695153` {'C': 0, 'S': 6, 'D': 8, 'I': 0, 'N': 14, 'M': 6}
  - ref: მოსკოვის სახელმწიფო ლინგვისტური უნივერსიტეტი არის რუსეთის ერთ ერთი ყველაზე დიდი უმაღლესი სასწავლებელი ენათმეცნიერების დარგში
  - hyp: საყვარლის მეუღლე იყო ადგილას ასტატი მოადგილე
- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 0, 'D': 13, 'I': 0, 'N': 13, 'M': 0}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: 
- `cv-ka-dev-common_voice_ka_49293620` {'C': 1, 'S': 9, 'D': 4, 'I': 0, 'N': 14, 'M': 10}
  - ref: დრო არი ჩემო პატარავ იცოდე ერტი ამბავი ედელის როდა ბადალი დღეს საქართელოს მთა ბრი
  - hyp: მრავალი დრამატული ამბავი ედემის როა და აპარატი დღეს საქართველოს მთავრობა
- `cv-ka-dev-common_voice_ka_49293795` {'C': 1, 'S': 9, 'D': 4, 'I': 0, 'N': 14, 'M': 10}
  - ref: როცა ჩემ მეგობარს ვხედავ რომ არის მოწყენილი მაშინ ისეთ რამეს ვაკეთებ რომ ისინი გავაბედნიერო
  - hyp: როტაციას ევორა გაუმართლა წერილი მას რის გამოც ვაკეთებ რომის მინდობილი
