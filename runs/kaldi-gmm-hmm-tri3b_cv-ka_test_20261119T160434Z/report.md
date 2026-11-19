# kaldi-gmm-hmm-tri3b_cv-ka_test (test)

- Model: `kaldi-gmm-hmm-tri3b (recipes/kaldi-gmm-ka)` @ `2dd43974bc2edadc01deee6385bfa8f47ddde02f` (kaldi-gmm-hmm, float32, cpu)
- System: **baseline, trained by us from scratch** (standard MFCC + GMM-HMM, A3): MFCC(13)+splice(±3)+LDA(40)+MLLT, speaker-adaptive (fMLLR/SAT) triphone GMM-HMM, 4000 leaves / 40k Gaussians; graphemic lexicon (91145 words), trigram KN LM on CV ka train text only; trained on CV 27.0 ka train (147.46 h)
- Hardware: AMD Ryzen 7 7800X3D 8-Core Processor (16 threads, WSL2 Ubuntu 24.04); batch size None
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: wall clock of MFCC+CMVN extraction and decoding (incl. fMLLR 2nd pass) over parallel CPU jobs; graph building and model loading excluded; per-clip compute_sec is pro-rated by duration

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14258 | 84004 | 22.64% | 21.60% – 23.76% | 22.60% | 8.22% | 7.54% – 9.00% | 39.64% | 10.42% | 22.08% | 36.10% | 0.030 | 33.0 | 0/1 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 86135, 'S': 18831, 'D': 2835, 'I': 2745, 'N': 107801, 'M': 107711}  
Char counts: {'C': 824281, 'S': 31445, 'D': 25032, 'I': 15889, 'N': 880758, 'M': 871615}

Top substitutions (ref → hyp × n): და→სადა×26, და→სადაც×10, იგი→დიდი×9, ეს→ის×9, დიდ→დიდი×9, ძირითადად→ძირითად×8, მის→მისი×8, აქვთ→აქვს×8, ერთ→ერთი×8, მან→მას×7

Worst items:

- `cv-ka-test-common_voice_ka_40443346` {'C': 2, 'S': 12, 'D': 0, 'I': 4, 'N': 14, 'M': 18}
  - ref: წმინდა მელქისედეკი არის საქართველოს სამოციქულო ეკლესიის პირველი საჭეთმპყრობელი რომელიც მოიხსენიება ტიტულით საქართველოს კათოლიკოს პატრიარქი
  - hyp: ვერა გვერდზე არტერიაა არის სარადარო საოცრებაა როე რევერსზე ფერარას ადრე ბაბალე რობერტო იწერება პრეტორი საქართველოს გამყარება პატარა ადრე
- `cv-ka-test-common_voice_ka_36821474` {'C': 0, 'S': 7, 'D': 0, 'I': 9, 'N': 7, 'M': 16}
  - ref: სიმღერა მუსიკოსმა მიუძღვნა მეუღლე ლინდა მაკ კარტნის
  - hyp: სერიალი ორ სიკო ეკლესიაა მაღალი ილო ეძლეოდათ ყველგანაა მაია უკვე ლოიოლა ილირიელი და მაგა კარატე დენის
- `cv-ka-test-common_voice_ka_40899928` {'C': 4, 'S': 7, 'D': 0, 'I': 8, 'N': 11, 'M': 19}
  - ref: გავედი დავინახე ქათამი კადანისკარტებული გვერდზე ედგა გავშავპაიჭნაბადიანი ბატი ბატმა ქათამიც გააშავპაიჭნაბადიანა
  - hyp: გავიტი დავინახე ქათამი კატანიის კარ ტყიბული გვერდზე იდგა გამო შაბთაი მითში ნალბანდიანი ბატი დადგმა ქათამი მისგან შავ გაიჩინა დადიან
- `cv-ka-test-common_voice_ka_39760373` {'C': 0, 'S': 7, 'D': 8, 'I': 0, 'N': 15, 'M': 7}
  - ref: ამის შემდეგ ერთხანს მსახურობდა მღვდლად ხოლო პირველი მსოფლიო ომის დროს იყო ავსტრია უნგრეთის არმიის კაპელანი
  - hyp: გამოსცემდა დასახლდა ტყეები იღუნება ყველა ნოველა ესპანური
- `cv-ka-test-common_voice_ka_40077605` {'C': 1, 'S': 11, 'D': 0, 'I': 3, 'N': 12, 'M': 15}
  - ref: იგი ასოცირდება სპეციფიკური მენტალური მდგომარეობების გამოვლინებასთან რომელიც დამოკიდებულია გამა რხევის სიხშირის დიაპაზონზე
  - hyp: რვა სპეციფიკური მედელინ ბიბი მდგომარეობებს სრული ვრცელი რომლის დამოკიდებულია გამოცვლილი სელინს ხშირი სევერნი აქვს მზე
