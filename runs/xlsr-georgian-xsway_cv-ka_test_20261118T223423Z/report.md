# xlsr-georgian-xsway_cv-ka_test (test)

- Model: `xsway/wav2vec2-large-xlsr-georgian` @ `b29b81945f5fa2e35fbb05da5256815d8cc71e20` (hf-ctc, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA L4; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14258 | 84004 | 46.26% | 45.05% – 47.58% | 45.88% | 9.02% | 8.49% – 9.64% | 57.85% | 11.17% | 45.14% | 67.39% | 0.002 | 637.7 | 0/1 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 60612, 'S': 41226, 'D': 5963, 'I': 2678, 'N': 107801, 'M': 104516}  
Char counts: {'C': 817579, 'S': 37474, 'D': 25705, 'I': 16222, 'N': 880758, 'M': 871275}

Top substitutions (ref → hyp × n): ერთ→ერთერთი×144, ერთ→ერთერთ×46, საქართველოს→საქართველო×16, არის→არი×15, ეკლესიის→ეკლესის×14, მისი→მის×13, წარმოადგენს→წარმოადგეს×12, ასევე→ასევი×12, მმართველობის→მართველობის×11, ჩრდილო→ჩრდილოაღმოსავლეთ×11

Worst items:

- `cv-ka-test-common_voice_ka_40443346` {'C': 1, 'S': 13, 'D': 0, 'I': 5, 'N': 14, 'M': 19}
  - ref: წმინდა მელქისედეკი არის საქართველოს სამოციქულო ეკლესიის პირველი საჭეთმპყრობელი რომელიც მოიხსენიება ტიტულით საქართველოს კათოლიკოს პატრიარქი
  - hyp: წვეილააველი ი ცედეი არის საგარდორო ს ავა წვიქოლო ეგლესეის პიროარი არჯატ ორაბელე რობელი სვაიჰსერიება ტიტორეთ სახარპევროს კატალიყოს ბაატრეა აგეი
- `cv-ka-test-common_voice_ka_40864247` {'C': 3, 'S': 11, 'D': 0, 'I': 5, 'N': 14, 'M': 19}
  - ref: სოფელი შედის რაზინსკოეს სასოფლო დასახლების შემადგენლობაში ასევე ადმინისტრაციულ ტერიტორიული დაყოფის მიხედვით მიეკუთვნება რაზინსკის სოფსაბჭოს
  - hyp: სოფელიში ესოფელი შედის რაზინს კოეს სასოფრო დასახლების შემადგელობაში ასევე ადმის სათული ტერიტორული და ყოფის მხედვის მიეკუთნება რაზისკის სობს საბჭოსს
- `cv-ka-test-common_voice_ka_39239809` {'C': 0, 'S': 13, 'D': 2, 'I': 0, 'N': 15, 'M': 13}
  - ref: ბანფი მსოფლიოში ერთ ერთ ყველაზე ხშირად მონახულებადი ეროვნული პარკია მისი ეკოსისტემის მდგომარეობა საკმაოდ ცუდ მდგომარეობაშია
  - hyp: ბაამ ფრიმ სოფლიოში ერთეტყო აზერხიად მონახურებად ევნულ პარკიამისი ეკვესის წევით გომარეობა საკმაორთრუ მდგოვმარეობაშია
- `cv-ka-test-common_voice_ka_41819006` {'C': 1, 'S': 13, 'D': 0, 'I': 2, 'N': 14, 'M': 16}
  - ref: მისი თქმით მიმდინარე წლის დასაწყისში ახალ დელიში ხელოვნების საერთაშორისო ღონისძიებაზე მხატვრის ნამუშევრების გამოფენა მოეწყო
  - hyp: მისი თ ქმეთ მიმდნაე წლე წა საწყში ახალტელიში ხელნობის სართო შესოღონე ზებაზე მხატვი სამშოვრების გაამფენა მაწმა
- `cv-ka-test-common_voice_ka_39760373` {'C': 0, 'S': 13, 'D': 2, 'I': 0, 'N': 15, 'M': 13}
  - ref: ამის შემდეგ ერთხანს მსახურობდა მღვდლად ხოლო პირველი მსოფლიო ომის დროს იყო ავსტრია უნგრეთის არმიის კაპელანი
  - hyp: ამისიენდმი ერთე საფლელდა ჰი დენდა ცააეობებინიე ომესა ნყალაო ლეა ული ყერე ზარვის მპყაყველალყ
