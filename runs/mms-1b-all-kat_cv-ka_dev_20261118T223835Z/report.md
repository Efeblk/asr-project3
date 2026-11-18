# mms-1b-all-kat_cv-ka_dev (dev)

- Model: `facebook/mms-1b-all` @ `3d33597edbdaaba14a8e858e2c8caa76e3cec0cd` (hf-ctc, float16, cuda)
- System: **baseline**: pretrained checkpoint, no training by us (A1)
- Hardware: NVIDIA L4; batch size 8
- Dataset: `data/cv/ka/manifest.jsonl` sha256 `8119119998bb`
- Timing boundary: model forward/decode only; audio loading and model loading excluded; CUDA synchronized before and after each batch; first batch preceded by a warm-up pass

| Language | Items | Audio (s) | WER | WER 95% CI | Mean clip WER | CER | CER 95% CI | Ortho WER | Ortho CER | MER | WIL | RTF | RTFx | Silent clips w/ output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ka | 14216 | 83400 | 23.69% | 22.28% – 25.28% | 24.04% | 4.05% | 3.53% – 4.67% | 39.66% | 6.37% | 23.41% | 38.81% | 0.004 | 283.4 | 0/0 |

WER/CER are corpus rates (pooled edit counts / pooled reference units) after the declared scoring policy. Ortho WER/CER keep case and punctuation (Unicode form only). CIs: cluster bootstrap over sessions/speakers. RTFx = audio seconds / compute seconds. No cross-language average is shown on purpose (S19).

## ka

Word counts: {'C': 84284, 'S': 21176, 'D': 3235, 'I': 1344, 'N': 108695, 'M': 106804}  
Char counts: {'C': 861618, 'S': 17317, 'D': 12538, 'I': 6248, 'N': 891473, 'M': 885183}

Top substitutions (ref → hyp × n): საქართველოს→საქართველო×29, გვხვდება→გხვდება×23, ოლქში→ოლგში×16, წევრი→სწევრი×12, ესე→ესეიგი×10, აღმოჩნდა→აღმოჩდა×9, მის→მისმიერ×9, დააარსა→დაარსა×9, მიიღო→მიიყო×9, უკანასკნელი→უკანასკნილი×8

Worst items:

- `cv-ka-dev-common_voice_ka_37420739` {'C': 1, 'S': 11, 'D': 2, 'I': 0, 'N': 14, 'M': 12}
  - ref: სექტემბრისთვის ქალაქის ზედა ნაწილიც დაინგრა და აღებულ იქნა მაგრამ ცენტრალური ციხესიმაგრე კვლავ განაგრძობდა წინააღმდეგობას
  - hyp: სეფტემბრისთვის ქალაქის ზედანაწილის დაინდრა დავაღებულიეა მაგრამ ცენტრალული ციხესი მაგრე ბლავ განარცოდა ძინააბდებას
- `cv-ka-dev-common_voice_ka_40617840` {'C': 0, 'S': 0, 'D': 13, 'I': 0, 'N': 13, 'M': 0}
  - ref: საბჭოთა ისტორიოგრაფიის შეფასებით ფხოველთა და დიდოელთა აჯანყების დამარცხებას სხვადასხვა არსებითი ხასიათის მიზეზი ჰქონდა
  - hyp: 
- `cv-ka-dev-common_voice_ka_40332704` {'C': 3, 'S': 11, 'D': 0, 'I': 1, 'N': 14, 'M': 15}
  - ref: მოკავშირეთა კონტროლქვეშ აღმოჩნდა სპლიტ ლივნო კუპრეს ბუგოინოს გზატკეცილი რაც მებრძოლი მხარეების მომარაგების პრობლემებს ხსნიდა
  - hyp: მოკავშირათა კონტროლ ქვეშ აღმნიჩნდა სპლიტ ლივნო კუპრეს ბეგოინოს გზადკეცინი რამაც ვებრძოლი მხარეები მომარაგეების პრობლემად იხსნა
- `cv-ka-dev-common_voice_ka_40319640` {'C': 4, 'S': 10, 'D': 1, 'I': 1, 'N': 15, 'M': 15}
  - ref: ასევე ლუიზამ დაიწყო მეგობრული ურთიერთობების ჩამოყალიბება ოსმალეთის იმპერიასთან რაც შემდგომში მრავალსაუკუნოვან საფრანგეთ ოსმალეთის ალიანსში გადაიზარდა
  - hyp: ასველუიზამ დაიწყო მენკრუბრული ურთიერთობისამოყალიბება ოსუმალეთის იმპერიასთან და რაც შემდგონში მრავალ საუკუნოვან საფრანგეთ ოსუმალეთის ალიანში გადაიზარდა
- `cv-ka-dev-common_voice_ka_21358400` {'C': 3, 'S': 9, 'D': 3, 'I': 0, 'N': 15, 'M': 12}
  - ref: კუნძულის კლიმატი სუბტროპიკულია რბილი ზამთრით და ავსტრალიაში ერთ ერთი პოპულარული ადგილია წყალქვეშა ცურვის მოყვარულებს შორის
  - hyp: კუნძულის კლიმატის სუბტროპიკულია რბილის ზამთრითდა ავსტრალიას ჯერთერთი პოპულარულიადიდა წყალქუშა ცხუდვის მოყოვრულებს შორის
