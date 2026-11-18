# nvidia-stt-ka-fastconformer_cv-ka_test (test)

- Model: `nvidia/stt_ka_fastconformer_hybrid_large_pc` @ `bdfd7871e0574001e650e741d6201d40205db6bb` (nemo, float32, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA L4; batch size 16
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14258 | 84004 | 4.85% | 4.49% – 5.23% | 5.03% | 1.27% | 1.12% – 1.43% | 9.53% | 1.74% | 4.84% | 8.67% | 0.004 | 273.4 | 1/1 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 102820, 'S': 4311, 'D': 670, 'I': 251, 'N': 107801, 'M': 107382}  
Char counts: {'C': 871441, 'S': 3603, 'D': 5714, 'I': 1835, 'N': 880758, 'M': 876879}

Top substitutions (ref → hyp × n): წმიდა→წმინდა×7, არა→არ×4, ჩრდილო→ჩრდილოეთ×4, აქვთ→აქვს×4, აბსიდის→აფსიდის×4, მსოფლიოს→მსოფლიო×3, რომლებიც→რომელიც×3, არა→არამარტო×3, ბარბარე→ბარბარა×3, თუ→და×3

Worst items:

- `cv-ka-test-common_voice_ka_39930460` {'C': 1, 'S': 6, 'D': 6, 'I': 0, 'N': 13, 'M': 7}
  - ref: მთელი ეს ამბავი მალე გავრცელდა იტალიაში და კატერინას ბიძის ლუდოვიკო სფორცას ყურამდეც მივიდა
  - hyp: გილერმა გავრცელდა ეკატერინა დიდი სუდოლიკოს პოსტას ყურამდე
- `cv-ka-test-common_voice_ka_41819001` {'C': 5, 'S': 9, 'D': 0, 'I': 3, 'N': 14, 'M': 17}
  - ref: გარდამოიხილე ზეცით ღმერთო იხილე მოხედე ვენახსა მას და განამტკიცე ესე რომელ დაასხა მარჯვენამან შენმან
  - hyp: გარდა მოიხილე ზეცით ღმერთო იხილე მოხეტვენ ახლა მას და განამტკიცა ეს ეროვნულმა და ასა მარჯვე მაშენ მან
- `cv-ka-test-common_voice_ka_49325466` {'C': 1, 'S': 10, 'D': 1, 'I': 0, 'N': 12, 'M': 11}
  - ref: რა ჭირი კაცსა სოფელმან მოუთმოს მოუთმინამან ქაცვი ლერწამმან ზაფრანა იმსგავსოს ფერად მინამან
  - hyp: რაჭა სოფელმა მოუწმოს მოუთმინათ ცაცმი მან საფრენ და მსგავს ფერად მინარეთი
- `cv-ka-test-common_voice_ka_39760360` {'C': 2, 'S': 5, 'D': 6, 'I': 0, 'N': 13, 'M': 7}
  - ref: იგი მიემგზავრება სან ფრანცისკოში სადაც იგებს რომ ის კაცი თვითონ არის ოღონდ მომავალში
  - hyp: იგი მდებარეობს სამას ხუშტაჟი როკის გასიფორმა მომავალში
- `cv-ka-test-common_voice_ka_40340115` {'C': 0, 'S': 2, 'D': 8, 'I': 0, 'N': 10, 'M': 2}
  - ref: კლასიცისტური ელემენტების მქონე შენობები ხის და რკინის აივნებით არის შემკული
  - hyp: კლასიცი კლასიცისტი
