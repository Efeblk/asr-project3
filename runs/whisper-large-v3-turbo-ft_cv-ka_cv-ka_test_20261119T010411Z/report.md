# whisper-large-v3-turbo-ft_cv-ka_cv-ka_test (test)

- Model: `checkpoints/whisper-large-v3-turbo-ft_cv-ka_20261118T222928Z/final` @ `main` (hf-whisper, float16, cuda)
- System: **ours**: fine-tuned by us from `openai/whisper-large-v3-turbo` on 147.463 h (runs/train_whisper-large-v3-turbo-ft_cv-ka_20261118T222928Z)
- Hardware: NVIDIA A100-SXM4-40GB; batch size 32
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14258 | 84004 | 12.80% | 12.02% – 13.65% | 12.99% | 2.60% | 2.31% – 2.92% | 15.91% | 2.98% | 12.70% | 22.54% | 0.012 | 86.6 | 1/1 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 94789, 'S': 12024, 'D': 988, 'I': 782, 'N': 107801, 'M': 107595}  
Char counts: {'C': 863548, 'S': 10420, 'D': 6790, 'I': 5698, 'N': 880758, 'M': 879666}

Top substitutions (ref → hyp × n): წმიდა→წმინდა×8, სხეულის→სხევლის×7, რომლებიც→რომელიც×6, აბსიდის→აფსიდის×6, მე→მევარ×6, თავისი→თავის×5, ცენტრალური→ცენტრალურ×5, აფსიდის→აბსიდის×5, ჯეიმს→ჯეიმზ×4, შავიზღვისპირა→ზღვისპირა×4

Worst items:

- `cv-ka-test-common_voice_ka_49303090` {'C': 3, 'S': 2, 'D': 1, 'I': 27, 'N': 6, 'M': 32}
  - ref: რასაც გასცემ შენია რაც არა დაკარგულია
  - hyp: რასაც აგასცემშენია რაც არა დაკარობს და განის განის განის განის განის განის განის განის განის განის განის განის განის განის განის განის განის განის განის განის განის განის განის გენის გენის გ
- `cv-ka-test-common_voice_ka_39743812` {'C': 0, 'S': 5, 'D': 0, 'I': 24, 'N': 5, 'M': 29}
  - ref: დანიშვნას ნეგატიურად გამოეხმაურნენ დასავლეთის ქვეყნები
  - hyp: კაყოყობელიურის მისის მერის მისის მერის მისის მერის მისის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის ერის �
- `cv-ka-test-common_voice_ka_40339021` {'C': 0, 'S': 5, 'D': 0, 'I': 23, 'N': 5, 'M': 28}
  - ref: კარგ მთქმელს კარგი გამგონი უნდა
  - hyp: მოდების მისისის მისების მერის მისების მერის მისების მერის მორის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის ერი
- `cv-ka-test-common_voice_ka_39666275` {'C': 0, 'S': 4, 'D': 0, 'I': 23, 'N': 4, 'M': 27}
  - ref: ქვემოთ გვიწერია სამას ოცდაოთხი
  - hyp: მოდების მერის მისების მერის მისების მერის მისების მერის მისების მერის მისების მერის მისების მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერი
- `cv-ka-test-common_voice_ka_40818116` {'C': 3, 'S': 1, 'D': 0, 'I': 22, 'N': 4, 'M': 26}
  - ref: ფასადის დიზაინი განსაკუთრებით მნიშვნელოვანია
  - hyp: ჰასადის დიზაინი განსაკუთრებით მნიშვნელოვანია და მერიაჯერთ იმ ოთხილი მოდების მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის ერის მერის მერის
