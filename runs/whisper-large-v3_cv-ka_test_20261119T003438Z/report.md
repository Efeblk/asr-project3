# whisper-large-v3_cv-ka_test (test)

- Model: `openai/whisper-large-v3` @ `06f233fe06e710322aca913c1bc4249a0d71fce1` (hf-whisper, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA A100-SXM4-40GB; batch size 32
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14258 | 84004 | 72.04% | 71.05% – 73.04% | 74.77% | 16.64% | 15.98% – 17.38% | 74.73% | 16.98% | 67.26% | 88.03% | 0.047 | 21.3 | 1/1 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 37811, 'S': 65271, 'D': 4719, 'I': 7671, 'N': 107801, 'M': 110753}  
Char counts: {'C': 769036, 'S': 72722, 'D': 39000, 'I': 34843, 'N': 880758, 'M': 876601}

Top substitutions (ref → hyp × n): და→ადა×169, მდებარეობს→დებარეობს×110, მდინარე→დინარე×60, მთავარი→თავარი×44, ერთ→ერთერთი×43, მცირე→ცირე×41, შემდეგ→შემდე×39, ჰქონდა→ქონდა×38, სხვა→ხვა×30, თუმცა→თუ×28

Worst items:

- `cv-ka-test-common_voice_ka_37332410` {'C': 0, 'S': 7, 'D': 0, 'I': 67, 'N': 7, 'M': 74}
  - ref: ქორწინების შემდეგ იგი ბიზანტიის თანა დედოფალი გახდა
  - hyp: ეს ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის ის სის ის ის ის ის ის ის ის ის ი
- `cv-ka-test-common_voice_ka_40307530` {'C': 0, 'S': 10, 'D': 0, 'I': 31, 'N': 10, 'M': 41}
  - ref: ჩხერიმელა ასპარეზობდა მაშინდელ საბჭოთა კავშირის ჩემპიონატში დასავლეთ საქართველოს ზონალურ პირველობაზე
  - hyp: მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მელა მ�
- `cv-ka-test-common_voice_ka_41505407` {'C': 0, 'S': 4, 'D': 0, 'I': 33, 'N': 4, 'M': 37}
  - ref: არაუმეტეს თხუთმეტი სიტყვის შემცველი
  - hyp: ხოდისი მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მიში მი
- `cv-ka-test-common_voice_ka_40348694` {'C': 0, 'S': 2, 'D': 0, 'I': 34, 'N': 2, 'M': 36}
  - ref: არცოდნა არცოდვააო
  - hyp: არცოდ ნარცოდ ვავლის მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი მესი
- `cv-ka-test-common_voice_ka_40357714` {'C': 0, 'S': 8, 'D': 0, 'I': 27, 'N': 8, 'M': 35}
  - ref: მათი მშენებლობა მანჰეტენზე ძირითადად მეოცე საუკუნის დასაწყისში დაიწყო
  - hyp: მართ მშენებლობამან ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის ერის
