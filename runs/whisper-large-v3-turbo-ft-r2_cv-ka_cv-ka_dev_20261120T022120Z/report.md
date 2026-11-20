# whisper-large-v3-turbo-ft-r2_cv-ka_cv-ka_dev (dev)

- Model: `checkpoints/whisper-large-v3-turbo-ft-r2_cv-ka_20261120T000532Z/final` @ `main` (hf-whisper, float16, cuda)
- System: **ours**: fine-tuned by us from `openai/whisper-large-v3-turbo` on 147.463 h (runs/train_whisper-large-v3-turbo-ft-r2_cv-ka_20261120T000532Z)
- Hardware: NVIDIA A100-SXM4-40GB; batch size 32
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 11.92% | 10.82% – 13.17% | 11.86% | 2.28% | 1.89% – 2.76% | 14.78% | 2.63% | 11.84% | 21.08% | 0.011 | 87.1 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 96498, 'S': 11293, 'D': 904, 'I': 759, 'N': 108695, 'M': 108550}  
Char counts: {'C': 876325, 'S': 9169, 'D': 5979, 'I': 5179, 'N': 891473, 'M': 890673}

Top substitutions (ref → hyp × n): წმიდა→წმინდა×9, მსოფლიო→მსოფლიოს×5, ერთი→ერთ×4, აბსიდით→აფსიდით×4, აბსიდის→აფსიდის×4, მღრღნელებით→მღრნელებით×4, მხარი→მხარე×4, წვრილი→წვლილი×4, წელს→წერს×4, აფსიდის→აბსიდის×4

Worst items:

- `cv-ka-dev-common_voice_ka_40356724` {'C': 0, 'S': 11, 'D': 0, 'I': 20, 'N': 11, 'M': 31}
  - ref: გუგენჰაიმის სპირალურად დახვეული თეთრი აივნებიდანაც ავტომობილის ნაწილებით დამზადებული ექსტრავაგანტული ფიგურები იმზირებიან
  - hyp: ეს ჩვედვა ასის რადომაც იომის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მის მის ისის
- `cv-ka-dev-common_voice_ka_40435618` {'C': 0, 'S': 7, 'D': 0, 'I': 22, 'N': 7, 'M': 29}
  - ref: აქვე ნაპოვნი იქნა თიხის საბეჭდავები სვასტიკის გამოსახულებით
  - hyp: ყიანთრებული მერთონის კიავული კილის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მისის მის ისის �
- `cv-ka-dev-common_voice_ka_39743816` {'C': 1, 'S': 9, 'D': 0, 'I': 19, 'N': 10, 'M': 29}
  - ref: ვინაიდან მას უფროსი ძმა ჰყავდა დაბადებისას მიანიჭეს ნორმანდიის ჰერცოგის წოდება
  - hyp: ვინაიდან გიტოსიან იყო და დადებების დადინის დანიჭენის კომაგიის ერს როგულის შემის შემის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის მერის ის მერის მერის ის მე�
- `cv-ka-dev-common_voice_ka_40435610` {'C': 0, 'S': 8, 'D': 0, 'I': 15, 'N': 8, 'M': 23}
  - ref: დღესდღეობით ის ისევ აზერბაიჯანის მწერალთა კავშირის ორგანოდ რჩება
  - hyp: მისის მისის მისის მისის მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების ის
- `cv-ka-dev-common_voice_ka_40617925` {'C': 0, 'S': 6, 'D': 0, 'I': 17, 'N': 6, 'M': 23}
  - ref: შედის ეკონომიკურ სტატისტიკურ მიკრორეგიონ გოიანიის შემადგენლობაში
  - hyp: მისის მისის მისის მისის მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების მისების ის
