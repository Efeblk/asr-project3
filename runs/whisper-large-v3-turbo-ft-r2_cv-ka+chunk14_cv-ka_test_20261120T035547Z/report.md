# whisper-large-v3-turbo-ft-r2_cv-ka+chunk14_cv-ka_test (test)

- Model: `checkpoints/whisper-large-v3-turbo-ft-r2_cv-ka_20261120T000532Z/final` @ `main` (hf-whisper, float16, cuda)
- System: **ours**: fine-tuned by us from `openai/whisper-large-v3-turbo` on 147.463 h (runs/train_whisper-large-v3-turbo-ft-r2_cv-ka_20261120T000532Z)
- Hardware: NVIDIA A100-SXM4-40GB; batch size 32
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14258 | 84004 | 12.84% | 12.04% – 13.69% | 12.94% | 2.70% | 2.41% – 3.04% | 15.96% | 3.08% | 12.73% | 22.49% | 0.011 | 87.4 | 1/1 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 94857, 'S': 11934, 'D': 1010, 'I': 898, 'N': 107801, 'M': 107689}  
Char counts: {'C': 863604, 'S': 10293, 'D': 6861, 'I': 6612, 'N': 880758, 'M': 880509}

Top substitutions (ref → hyp × n): წმიდა→წმინდა×8, მე→მევარ×7, სხეულის→სხევლის×6, ცენტრალური→ცენტრალურ×6, აფსიდის→აბსიდის×6, რომლებიც→რომელიც×5, თავისი→თავის×5, ჯეიმს→ჯეიმზ×4, მათ→მათი×4, მისი→მის×4

Worst items:

- `cv-ka-test-common_voice_ka_40358737` {'C': 10, 'S': 4, 'D': 0, 'I': 31, 'N': 14, 'M': 45}
  - ref: ტემპერატურის ასეთი დიდი სხვაობა ინკებს შესაძლებლობას აძლევდა შეესწავლათ განსხვავებული კლიმატური პირობების ეფექტი სხვადასხვა მცენარეზე
  - hyp: ტემპერატურის ასეთი დიდი სხვაობა იმკებს შესაძლებლობას აძლევ და შეესწავლად განსხვავებული კლიმატური პირობების ეფექტის სხვადასხვა მცენარეზე მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მის მისის მისის
- `cv-ka-test-common_voice_ka_39666300` {'C': 0, 'S': 6, 'D': 0, 'I': 24, 'N': 6, 'M': 30}
  - ref: გვაქვს სამი ერთეული და ხუთი ერთეული
  - hyp: მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მის მისის მისის
- `cv-ka-test-common_voice_ka_38676823` {'C': 0, 'S': 7, 'D': 0, 'I': 23, 'N': 7, 'M': 30}
  - ref: მოიცავს რამდენიმე სხვადასხვა ასაკის ვულკანს და კალდერას
  - hyp: მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მის მისის მისის
- `cv-ka-test-common_voice_ka_39666364` {'C': 0, 'S': 10, 'D': 0, 'I': 20, 'N': 10, 'M': 30}
  - ref: ამავე პერიოდში ნილ ტენანტი უფრო ღიად საუბრობდა თავის სექსუალურ ორიენტაციაზე
  - hyp: მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მის მისის მისის
- `cv-ka-test-common_voice_ka_40258779` {'C': 12, 'S': 4, 'D': 0, 'I': 22, 'N': 16, 'M': 38}
  - ref: დივიზიონში ხუთი გუნდია სან ანტონიო სპურსი მემფის გრიზლი ჰიუსტონ როკეტსი ნიუ ორლეან ჰორნეტსი და დალას მევერიქსი
  - hyp: დივიზიოში ხუთი გუნდია სან ანტონიოს სპურსი მემფის გრიზლი ჰიუსტონ როკეტსი ნიუს ორლეან ჰორნეტსი და დალას მევერიგსი მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების ი
