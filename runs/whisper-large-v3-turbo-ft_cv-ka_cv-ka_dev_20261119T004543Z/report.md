# whisper-large-v3-turbo-ft_cv-ka_cv-ka_dev (dev)

- Model: `checkpoints/whisper-large-v3-turbo-ft_cv-ka_20261118T222928Z/final` @ `main` (hf-whisper, float16, cuda)
- System: **ours**: fine-tuned by us from `openai/whisper-large-v3-turbo` on 147.463 h (runs/train_whisper-large-v3-turbo-ft_cv-ka_20261118T222928Z)
- Hardware: NVIDIA A100-SXM4-40GB; batch size 32
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 11.88% | 10.74% – 13.14% | 11.79% | 2.27% | 1.88% – 2.75% | 14.81% | 2.63% | 11.80% | 21.04% | 0.011 | 87.3 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 96509, 'S': 11288, 'D': 898, 'I': 730, 'N': 108695, 'M': 108527}  
Char counts: {'C': 876326, 'S': 9135, 'D': 6012, 'I': 5126, 'N': 891473, 'M': 890587}

Top substitutions (ref → hyp × n): წმიდა→წმინდა×9, მსოფლიო→მსოფლიოს×6, ერთი→ერთ×4, რომლებიც→რომელიც×4, ძირითადად→ძირითად×4, დასავლეთი→დასავლეთ×4, პირველი→პირველ×4, ააშენეს→აშენეს×4, შორის→სორის×4, მღრღნელებით→მღრნელებით×4

Worst items:

- `cv-ka-dev-common_voice_ka_40356724` {'C': 0, 'S': 11, 'D': 0, 'I': 19, 'N': 11, 'M': 30}
  - ref: გუგენჰაიმის სპირალურად დახვეული თეთრი აივნებიდანაც ავტომობილის ნაწილებით დამზადებული ექსტრავაგანტული ფიგურები იმზირებიან
  - hyp: ეს ჩვენვა არცს რადუმაც იომების მერის მორის მერის მერის მერის მორის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის ერი
- `cv-ka-dev-common_voice_ka_40352416` {'C': 0, 'S': 10, 'D': 0, 'I': 17, 'N': 10, 'M': 27}
  - ref: იმ დროისათვის როდესაც ისინი ინგლისში დაბრუნდნენ მერი უკვე ორსულად იყო
  - hyp: მოდების მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისების მისების მისების მისების მისების მისები
- `cv-ka-dev-common_voice_ka_40435671` {'C': 0, 'S': 10, 'D': 0, 'I': 14, 'N': 10, 'M': 24}
  - ref: ჩრდილოეთისა და სამხრეთის ფასადებზე შემორჩენილია კვადრატული აგურით ნაწყობი თაროსებრი ლავგარდანი
  - hyp: მისის მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მერის მერის მერის მერის მერის მერის მერის მერ
- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 13, 'D': 0, 'I': 11, 'N': 13, 'M': 24}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: მოდების მისის მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მერის მერის მერის მერის მერის მერის მერის მერ
- `cv-ka-dev-common_voice_ka_40618050` {'C': 0, 'S': 10, 'D': 0, 'I': 14, 'N': 10, 'M': 24}
  - ref: ეს პაქტი რიბენტროპის და მთელი გერმანული დიპლომატიის დიდი გამარჯვება იყო
  - hyp: მისის მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მერის მერის მერის მერის მერის მერის მერის მერ
