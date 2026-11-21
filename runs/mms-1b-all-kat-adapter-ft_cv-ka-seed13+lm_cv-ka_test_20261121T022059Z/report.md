# mms-1b-all-kat-adapter-ft_cv-ka-seed13+lm_cv-ka_test (test)

- Model: `checkpoints/mms-1b-all-kat-adapter-ft_cv-ka-seed13_20261121T004458Z/final` @ `main` (hf-ctc, float16, cuda)
- System: **ours**: fine-tuned by us from `facebook/mms-1b-all` on 147.466 h (runs/train_mms-1b-all-kat-adapter-ft_cv-ka-seed13_20261121T004458Z)
- Hardware: NVIDIA A100-SXM4-40GB; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14258 | 84004 | 11.07% | 10.45% – 11.72% | 10.96% | 2.13% | 1.91% – 2.41% | 30.45% | 4.57% | 11.00% | 18.10% | 0.002 | 478.5 | 1/1 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 96607, 'S': 8367, 'D': 2827, 'I': 741, 'N': 107801, 'M': 105715}  
Char counts: {'C': 864719, 'S': 6369, 'D': 9670, 'I': 2738, 'N': 880758, 'M': 873826}

Top substitutions (ref → hyp × n): ახალგაზრდა→ახალგაზდა×18, წმიდა→წმინდა×8, ტერიტორიაზე→ტერიტორიას×6, სახელმწიფოს→სახელმწიფო×6, მეფემ→მეფე×5, როგორ→როგორც×5, ჰქონდათ→ჰქონდა×5, დააარსა→დაარსა×5, ქვეშ→ქვეში×5, არა→არ×5

Worst items:

- `cv-ka-test-common_voice_ka_39760373` {'C': 1, 'S': 2, 'D': 12, 'I': 0, 'N': 15, 'M': 3}
  - ref: ამის შემდეგ ერთხანს მსახურობდა მღვდლად ხოლო პირველი მსოფლიო ომის დროს იყო ავსტრია უნგრეთის არმიის კაპელანი
  - hyp: ამის შენი აჭისახეოდაიდელდახოლშიპერეცუკლიყომესასუყავსეალიაომიათისარმესკაპელა
- `cv-ka-test-common_voice_ka_41819001` {'C': 0, 'S': 4, 'D': 10, 'I': 0, 'N': 14, 'M': 4}
  - ref: გარდამოიხილე ზეცით ღმერთო იხილე მოხედე ვენახსა მას და განამტკიცე ესე რომელ დაასხა მარჯვენამან შენმან
  - hyp: გარდა მოიხილასზაცითხმერთოიხილემოხედევენახსამასდაგანარგცეეზე რომელთა ასამარჯვემანშენმან
- `cv-ka-test-common_voice_ka_39695177` {'C': 0, 'S': 11, 'D': 0, 'I': 2, 'N': 11, 'M': 13}
  - ref: ესპანეთთან დაზავების შემდგომ ანრიმ განიზრახა ფრანკო ესპანური ალიანსი დინასტიური ქორწინებით გაემყარებინა
  - hyp: კაცი შედის ახლის იმერეთის ხომეინი კადიმია ის ელიასა ცხრამეტი ამარა მას შეიპარა საყურებლად
- `cv-ka-test-common_voice_ka_40097318` {'C': 1, 'S': 7, 'D': 5, 'I': 0, 'N': 13, 'M': 8}
  - ref: ანტისოციალური პიროვნების აშლილობის მქონე ადამიანი ხასიათდება სხვა ადამიანის უფლებების უგულვებელყოფით და მათი დარღვევით
  - hyp: ანი სოციალური ბრაუნების კავშირების ადამიანი ხდება სწავლებები უიველყოფიდამათიდარგვევი
- `cv-ka-test-common_voice_ka_40097326` {'C': 1, 'S': 6, 'D': 5, 'I': 1, 'N': 12, 'M': 8}
  - ref: ქრისტიანობის შემოსვლის შემდეგ წარმართულ ლამარიას ცვლის მარიამ ღვთისმშობელი კულტი კი იგივე რჩება
  - hyp: ტიან ობის სემიტების შემდეგ წარმოადგინა მარიასის მარია ხრიშომელიკილიდაირივერშიბა
