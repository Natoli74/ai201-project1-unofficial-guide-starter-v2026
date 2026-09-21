# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This command-line Q&A tool searches the `city_guides` corpus of travel guides
covering towns, food, accommodation, attractions, and regional transport. It
retrieves relevant document chunks, checks whether the question is within the
corpus, and generates a brief answer grounded in the retrieved source files.
Run it with `python app.py ask "your question"`.

## Chunking Strategy

**Chunk size:** 1200 characters maximum, including the contextual metadata line.
**Overlap:** 200 characters within a Markdown section.

`split_documents` parses each guide by `##` headers and keeps the text under
each section together. Every generated chunk starts with `<guide title> - <section heading>` on its first line, including an `Introduction` section for
content before the first `##` header. Long sections are split into windows
with 200 characters of overlap, but chunks never cross a Markdown section
boundary.

The original fixed-window baseline produced 51 chunks with an average length
of 650 characters, a shortest length of 24, and a longest length of 800. The
header-aware strategy produced 94 chunks with an average length of 320
characters, a shortest length of 187, and a longest length of 758. The chunk
count increased because each guide section is now independently retrievable;
the average length decreased because short sections stay intact instead of
being combined with neighboring sections.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1**: source: `guide_accessibility.md#0` - produced by: `chunker.py::split_documents`

```
Getting around the region with limited mobility - Introduction

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Chunk 2**: source: `guide_corry_vale.md#5` - produced by: `chunker.py::split_documents`

```
Corry Vale - Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful
of farmhouse rooms. In summer these are booked months ahead. Camping is
permitted on two marked fields and nowhere else.
```

**Chunk 3**: source: `guide_givens_mill.md#2` - produced by: `chunker.py::split_documents`

```
Givens Mill - Getting around

Everything is on one street along the river. The mill is at one end and the
church at the other, eight minutes apart. The riverside path continues in both
directions for as far as you want to walk.
```

**Chunk 4**: source: `guide_kestrelford.md#4` - produced by: `chunker.py::split_documents`

```
Kestrelford - What to see

The market square on a Saturday morning is the main event and has run
continuously since the 1400s. The parish church has a 13th-century tower you
can climb for £2. The old trackbed walk runs six miles to the next village
along an easy gradient and is the best half-day here.
```

**Chunk 5**: source: `guide_pellew_sands.md#6` - produced by: `chunker.py::split_documents`

```
Pellew Sands - When to go

June and September for the beach without the crowds. July and August are busy
and the town is at its most itself, for better and worse. Winter is bleak,
largely closed, and has a following among people who like that sort of thing.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**
What hours do the pubs in Kestrelford serve food?

**Answer:**
In Kestrelford, the pubs serve food from 12 to 2 and again between 6 and 8:30
(guide_eating.md and guide_kestrelford.md).

```
Best distance: 0.343
Sources retrieved: guide_eating.md, guide_elder_ness.md, guide_givens_mill.md,
guide_kestrelford.md
```

**My relevance cutoff:**
0.70. The in-scope questions had best distances from 0.317 to 0.632. The
out-of-scope questions ranged from 0.829 to 0.903, leaving a gap above 0.632
and below 0.829. A 0.70 cutoff keeps all five measured in-scope questions
below the threshold and all five out-of-scope questions above it.

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question                                                                                         | In corpus? | Best distance |
| ------------------------------------------------------------------------------------------------ | ---------- | ------------: |
| What hours do the pubs in Kestrelford serve food?                                                | Yes        |      0.343182 |
| When did the railway line north of Brightwater close?                                            | Yes        |      0.317031 |
| How often do Marchwood trams run on weekdays and at weekends?                                    | Yes        |      0.382069 |
| Where can visitors find Brightwater food that costs about a third less than the riverside strip? | Yes        |      0.420492 |
| What is the main ticket problem when using buses in the region?                                  | Yes        |      0.632330 |
| What is the capital of Mongolia?                                                                 | No         |      0.887442 |
| How do I change the oil in a diesel engine?                                                      | No         |      0.896901 |
| Who won the 1994 World Cup?                                                                      | No         |      0.902628 |
| What is the recommended dosage of ibuprofen for a headache?                                      | No         |      0.829332 |
| How do I write a for loop in Rust?                                                               | No         |      0.852919 |

## How I Used AI

**1.** I asked Copilot to implement a section-aware Markdown splitter with
header metadata and overlap. The first approach could drop introduction
paragraphs before the first `##` header, so I tested headerless leading content
and added explicit `Introduction` handling in `split_documents`.

**2.** I asked Copilot to stress-test the acceptance criteria for measurable
thresholds. It identified subjective wording as a risk, so I expressed the
chunk integrity target as 100% header context and the relevance target as
explicit distance ranges with zero false positives.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion                              | Target | Run 1 | Run 2 | Run 3 | Verdict |
| -------------------------------------- | ------ | ----- | ----- | ----- | ------- |
| 1. Retrieved chunk contains the answer | 4 of 5 |       |       |       |         |
| 2. Every answer names a source         | 5 of 5 |       |       |       |         |
| 3. Gate stops out-of-corpus questions  | 4 of 5 |       |       |       |         |
| 4.                                     |        |       |       |       |         |
| 5.                                     |        |       |       |       |         |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| #   | Criterion | Verdict | How I decided |
| --- | --------- | ------- | ------------- |
| 1   |           |         |               |
| 2   |           |         |               |
| 3   |           |         |               |
| 4   |           |         |               |
| 5   |           |         |               |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion                              | Target | Run 1 | Run 2 | Run 3 | Verdict |
| -------------------------------------- | ------ | ----- | ----- | ----- | ------- |
| 1. Retrieved chunk contains the answer | 4 of 5 |       |       |       |         |
| 2. Every answer names a source         | 5 of 5 |       |       |       |         |
| 3. Gate stops out-of-corpus questions  | 4 of 5 |       |       |       |         |
| 4.                                     |        |       |       |       |         |
| 5.                                     |        |       |       |       |         |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
