# Course announcement (A2): "Project 3: split your data by speaker, not by clip"

Passed on by the student on 2026-11-18; the exact posting date is not recorded. Verbatim text below (only the
list formatting is added).

---

Dear all,

A question from one group showed that the train/validation/test split in Project 3 needs a clear rule. Please read this before you build your splits.

**The rule**

Split by speaker, not by clip. All clips of one speaker go to the same split. This is the Week 9 slide "Assign related recordings together before splitting": speaker A's clip 1 and clip 2 both go to train, speaker B's both go to development, and speaker C's both go to test.

**Why**

If the same speaker appears in train and in test, the model has already heard that voice, microphone, and room. The test result then looks better than it will be for a new speaker. This is a data leak, and I grade it as one in Correctness.

**How**

1. If your dataset has a documented train/development/test split, you can use it. Write in the README which split you used and whether its speakers are separate.
2. If you make your own split, first group the clips by speaker (and by recording session, if the dataset has sessions). Then assign whole groups to train, validation, and test. Do this in a committed script with a fixed seed.
3. If your dataset has no speaker IDs, group by the closest unit that it has, such as the recording or the source file. Explain this in the README.
4. Long recordings cut into short clips count as one recording. Do not spread the clips of one recording across splits.

**What to report**

For each split: the number of speakers, the number of utterances, and the total hours. Also check how many test sentences appear word for word in your training set, and report that number.

Development and test have different jobs. Use the development split to choose settings and checkpoints, such as the beam size or the best epoch. Use the test split once, at the end, after you freeze everything.

Good luck.
