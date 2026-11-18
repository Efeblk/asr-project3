# whisper-large-v3-turbo_cv-ka_dev (dev)

- Model: `openai/whisper-large-v3-turbo` @ `41f01f3fe87f28c78e2fbf8b568835947dd65ed9` (hf-whisper, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA A100-SXM4-40GB; batch size 32
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 140.27% | 136.94% – 143.47% | 143.02% | 185.70% | 182.09% – 189.30% | 138.14% | 181.85% | 99.99% | 100.00% | 0.017 | 58.9 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 10, 'S': 45048, 'D': 63637, 'I': 43783, 'N': 108695, 'M': 88841}  
Char counts: {'C': 96281, 'S': 789023, 'D': 6169, 'I': 860236, 'N': 891473, 'M': 1745540}

Top substitutions (ref → hyp × n): მისი→ეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეე×105, და→ერის×93, ამ→ეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეე×88, მდებარეობს→ეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეე×80, ეს→ეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეე×78, იგი→ეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეე×66, მას→ეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეე×45, და→ეს×42, და→da×38, ის→ეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეეე×37

Worst items:

- `cv-ka-dev-common_voice_ka_37347123` {'C': 0, 'S': 5, 'D': 0, 'I': 439, 'N': 5, 'M': 444}
  - ref: ქვეყნის ერთ ერთი საპორტო ქალაქი
  - hyp: q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q
- `cv-ka-dev-common_voice_ka_39743816` {'C': 0, 'S': 10, 'D': 0, 'I': 255, 'N': 10, 'M': 265}
  - ref: ვინაიდან მას უფროსი ძმა ჰყავდა დაბადებისას მიანიჭეს ნორმანდიის ჰერცოგის წოდება
  - hyp: þín hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að hún er að
- `cv-ka-dev-common_voice_ka_37297651` {'C': 0, 'S': 12, 'D': 0, 'I': 211, 'N': 12, 'M': 223}
  - ref: ინგლისის ისტორიის ამ მნიშვნელოვან ნაწილთან ერთად სკოტი მოგვითხრობს რომანის გმირების საოცარ თავგადასავლებზე
  - hyp: english e s s s tory sam national e s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s
- `cv-ka-dev-common_voice_ka_40084861` {'C': 0, 'S': 13, 'D': 0, 'I': 209, 'N': 13, 'M': 222}
  - ref: პირველი რამდენიმე ეპიზოდი გვიჩვენებს საზაფხულო არდადეგების დასკვნით პერიოდს სკოლის დაწყებამდე ერთი კვირით ადრე
  - hyp: 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
- `cv-ka-dev-common_voice_ka_38321955` {'C': 0, 'S': 13, 'D': 0, 'I': 209, 'N': 13, 'M': 222}
  - ref: ძიუდო ეს არის სხეულისა და სულის შეთანხმებული ოპტიმალური გამოყენება იგი სპორტთან ერთად ფილოსოფიაა
  - hyp: 3 8 0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
