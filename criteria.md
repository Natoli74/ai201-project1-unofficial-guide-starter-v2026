# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. _"Retrieval works"_ is an opinion. _"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"_ is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; _"80% seemed reasonable"_ does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
The city guides contain specific facts under distinct sections, and the top
retrieved chunks should contain enough of those facts to answer nearly every
test question. Allowing one miss accounts for the region-wide transport
question, which may match several related sections.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
The answer prompt explicitly asks for the filename used, and every retrieved
chunk retains its source field. Requiring all five answers makes attribution a
consistent contract rather than an occasional enhancement.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
The measured in-scope distances run from 0.317 to 0.632, while out-of-scope
distances run from 0.829 to 0.903. The 0.70 cutoff sits between those groups
and leaves a measurable margin for refusing unsupported questions.

---

## 4. Chunk integrity

100% of generated chunks preserve header context by prepending `<guide title> - <section heading>` to ensure full standalone context.

**Why this target:**
City guides organize important facts under section headings, so every chunk needs its guide and section context to remain interpretable after retrieval. A 100% target is appropriate because any chunk without that context can produce an incomplete or misattributed answer.

---

## 5. Relevance Gate Distance Gap

The distance threshold strictly separates in-corpus queries (best distance < 0.60) from out-of-scope queries (best distance > 0.80) with 0 false positives.

**Why this target:**
The 0.60 cutoff is the configured gate threshold, while requiring out-of-scope results above 0.80 creates a measurable safety margin instead of relying on a borderline refusal. Zero false positives matters because allowing an out-of-scope question through can lead to an unsupported answer.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
