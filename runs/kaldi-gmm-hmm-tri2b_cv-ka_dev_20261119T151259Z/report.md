# kaldi-gmm-hmm-tri2b_cv-ka_dev (dev)

- Model: `kaldi-gmm-hmm-tri2b (recipes/kaldi-gmm-ka)` @ `bf455f8c389b6ad42ba86d1aa9bcc8e435ab59e6` (kaldi-gmm-hmm, float32, cpu)
- System: **baseline, trained by us from scratch** (standard MFCC + GMM-HMM, A3): MFCC(13)+splice(±3)+LDA(40)+MLLT triphone GMM-HMM (no speaker adaptation), 4000 leaves / 40k Gaussians; graphemic lexicon (91145 words), trigram KN LM on CV ka train text only; trained on CV 27.0 ka train (147.46 h)
- Hardware: AMD Ryzen 7 7800X3D 8-Core Processor (16 threads, WSL2 Ubuntu 24.04); batch size None
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: wall clock of MFCC+CMVN extraction and decoding (incl. fMLLR 2nd pass) over parallel CPU jobs; graph building and model loading excluded; per-clip compute_sec is pro-rated by duration

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 24.88% | 23.12% – 26.81% | 24.39% | 9.98% | 8.75% – 11.33% | 41.05% | 12.12% | 24.43% | 39.47% | 0.030 | 33.8 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 83656, 'S': 20703, 'D': 4336, 'I': 2005, 'N': 108695, 'M': 106364}  
Char counts: {'C': 817237, 'S': 39597, 'D': 34639, 'I': 14751, 'N': 891473, 'M': 871585}

Top substitutions (ref → hyp × n): და→სადა×12, და→ზედა×12, დიდ→დიდი×11, ის→ეს×9, მისი→მის×9, ერთ→ერთი×9, ან→და×9, წმიდა→წმინდა×8, ერთ→ერთად×8, აქვთ→აქვს×7

Worst items:

- `cv-ka-dev-common_voice_ka_41206209` {'C': 0, 'S': 8, 'D': 6, 'I': 0, 'N': 14, 'M': 8}
  - ref: ფილმი კონსპირაციის თეორიებით არის გაჯერებული და ცდილობს დაამტკიცოს რომ ამერიკის პრეზიდენტს ფარული ზრახვები აქვს
  - hyp: იუგოსლავიას ზნეობრივი კარისკაცები გასცილდა აქცევს გომბორის კრეზის ქორწილს
- `cv-ka-dev-common_voice_ka_39695153` {'C': 0, 'S': 0, 'D': 14, 'I': 0, 'N': 14, 'M': 0}
  - ref: მოსკოვის სახელმწიფო ლინგვისტური უნივერსიტეტი არის რუსეთის ერთ ერთი ყველაზე დიდი უმაღლესი სასწავლებელი ენათმეცნიერების დარგში
  - hyp: 
- `cv-ka-dev-common_voice_ka_26759863` {'C': 0, 'S': 9, 'D': 5, 'I': 0, 'N': 14, 'M': 9}
  - ref: სილვიო ემუდარება ნედას რომ მიატოვოს ქმარი და მასთან ერთად გაიქცეს რასაც ნედა საბოლოოდ თანხმდება
  - hyp: სიბიუ მდებარე ფერმენტებს რომლებიც ნუსხური გამოსვლები ფუნქციასაც მიტაცებულ დაპყრობა
- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 0, 'D': 13, 'I': 0, 'N': 13, 'M': 0}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: 
- `cv-ka-dev-common_voice_ka_40334033` {'C': 7, 'S': 6, 'D': 0, 'I': 7, 'N': 13, 'M': 20}
  - ref: მან ტარანტინოს საუკეთესო სცენარისტის და საუკეთესო ფილმის პრიზები მოუტანა კომედიის და მიუზიკლის ჟანრებში
  - hyp: კენას ან საუკეთესო სცენარის დასს გააუქმა ეთერსა ფილმის გააქვთ პრიზები მოუტანა კომერციისა და ამ კომედიის და მუსიკამ იბნ კლდის ჟანრებში
