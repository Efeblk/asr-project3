# whisper-large-v3-turbo-ft-r2_cv-ka_cv-ka_test (test)

- Model: `checkpoints/whisper-large-v3-turbo-ft-r2_cv-ka_20261120T000532Z/final` @ `main` (hf-whisper, float16, cuda)
- System: **ours**: fine-tuned by us from `openai/whisper-large-v3-turbo` on 147.463 h (runs/train_whisper-large-v3-turbo-ft-r2_cv-ka_20261120T000532Z)
- Hardware: NVIDIA A100-SXM4-40GB; batch size 32
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14258 | 84004 | 12.71% | 11.95% – 13.56% | 12.87% | 2.59% | 2.30% – 2.91% | 15.83% | 2.97% | 12.62% | 22.39% | 0.012 | 86.7 | 1/1 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 94857, 'S': 11933, 'D': 1011, 'I': 759, 'N': 107801, 'M': 107549}  
Char counts: {'C': 863604, 'S': 10293, 'D': 6861, 'I': 5652, 'N': 880758, 'M': 879549}

Top substitutions (ref → hyp × n): წმიდა→წმინდა×8, მე→მევარ×7, სხეულის→სხევლის×6, ცენტრალური→ცენტრალურ×6, აფსიდის→აბსიდის×6, რომლებიც→რომელიც×5, თავისი→თავის×5, ჯეიმს→ჯეიმზ×4, მათ→მათი×4, მისი→მის×4

Worst items:

- `cv-ka-test-common_voice_ka_39666300` {'C': 0, 'S': 6, 'D': 0, 'I': 24, 'N': 6, 'M': 30}
  - ref: გვაქვს სამი ერთეული და ხუთი ერთეული
  - hyp: მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მის მისის მისის
- `cv-ka-test-common_voice_ka_38676823` {'C': 0, 'S': 7, 'D': 0, 'I': 23, 'N': 7, 'M': 30}
  - ref: მოიცავს რამდენიმე სხვადასხვა ასაკის ვულკანს და კალდერას
  - hyp: მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მის მისის მისის
- `cv-ka-test-common_voice_ka_39666364` {'C': 0, 'S': 10, 'D': 0, 'I': 20, 'N': 10, 'M': 30}
  - ref: ამავე პერიოდში ნილ ტენანტი უფრო ღიად საუბრობდა თავის სექსუალურ ორიენტაციაზე
  - hyp: მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მის მისის მისის
- `cv-ka-test-common_voice_ka_39666251` {'C': 0, 'S': 5, 'D': 0, 'I': 18, 'N': 5, 'M': 23}
  - ref: არის კურდღლის სერიის პირველი წიგნი
  - hyp: მისის მისის მისის მისის მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების ის
- `cv-ka-test-common_voice_ka_40339021` {'C': 0, 'S': 5, 'D': 0, 'I': 18, 'N': 5, 'M': 23}
  - ref: კარგ მთქმელს კარგი გამგონი უნდა
  - hyp: მორის მისის მისის მისის მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების ისების მისების ისე
