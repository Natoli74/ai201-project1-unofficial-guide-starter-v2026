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

| Criterion                              | Target        | Run 1  | Run 2  | Run 3  | Verdict |
| -------------------------------------- | ------------- | ------ | ------ | ------ | ------- |
| 1. Retrieved chunk contains the answer | 4 of 5        | 5 of 5 | 5 of 5 | 5 of 5 | MET     |
| 2. Every answer names a source         | 5 of 5        | 5 of 5 | 5 of 5 | 5 of 5 | MET     |
| 3. Gate stops out-of-corpus questions  | 4 of 5        | 5 of 5 | 5 of 5 | 5 of 5 | MET     |
| 4. Chunk integrity                     | 100%          | 100%   | 100%   | 100%   | MET     |
| 5. Relevance gate distance gap         | <0.60 / >0.80 | MISSED | MISSED | MISSED | MISSED  |

Raw evidence from `run_eval.py::main`, using `store.py::search` and
`chunker.py::split_documents`:

**Criterion 1, retrieval accuracy:**

```text
The railway line north of Brightwater closed in 1963.
Source: guide_regional_transport.md
```

This same expected fact was present in all three runs for all five questions.

**Criterion 2, source citation:**

```text
Marchwood trams run every 8 minutes on weekdays and every 15 minutes at weekends (guide_marchwood.md).
```

All 15 generated responses named at least one source file.

**Criterion 3, relevance gate:**

```text
refused (best distance 0.887) What is the capital of Mongolia?
-> gate refused 5 of 5
```

**Criterion 4, chunk integrity:**

```text
chunk_integrity=100%; chunks=94; max_length=758
```

Generated by `chunker.py::split_documents`; every chunk had a guide and section
prefix.

**Criterion 5, distance gap:**

```text
in-scope: 0.317031 to 0.632330
out-of-scope: 0.829332 to 0.902628
```

The measured in-scope maximum did not satisfy the strict `<0.60` requirement.

Three-round deterministic evidence is recorded in
`results/qualification_checks_2026-09-26.md`, produced by
`tools/qualification_checks.py::main`. It records gate refusal, chunk
integrity, and distance measurements for rounds 1 through 3; the model-backed
criteria use the three uncached runs in each before and after evaluation log.

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

| #   | Criterion                   | Verdict | How I decided                                                                                                                          |
| --- | --------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Retrieval accuracy          | MET     | All five questions retrieved chunks containing the expected answer in all three runs, giving 5 of 5 each time against a 4 of 5 target. |
| 2   | Source citation             | MET     | Every one of the 15 generated answers named at least one source file, meeting 5 of 5 in every run.                                     |
| 3   | Relevance gate refusal      | MET     | The deterministic gate refused all 5 out-of-scope questions, exceeding the 4 of 5 target.                                              |
| 4   | Chunk integrity             | MET     | All 94 generated chunks had the required guide and section prefix and stayed under the 1200-character ceiling.                         |
| 5   | Relevance Gate Distance Gap | MISSED  | Four in-scope distances were below 0.60, but the bus-ticket question was 0.632330, so the strict target did not hold.                  |

## Diagnoses

Criterion 5 was missed at the retrieval stage, specifically in the embedding
similarity measurement rather than loading, chunking, or generation. The
retrieved regional transport chunk contained the exact answer and generation
was correct, but its best cosine distance was 0.632330, above the criterion's
strict 0.60 boundary. The overall pattern is that answer quality and refusal
behavior are strong, while the distance target is stricter than the observed
semantic score for one valid regional question.

## The Improvement

**What I changed:**
Reduced `TOP_K` in `config.py` from 5 to 3 so generation receives only the
three closest chunks.

**Why I picked it:**
The baseline retrieved several unrelated guide files alongside the answer
source. This targeted retrieval change addresses context precision without
changing the embedding model, chunking strategy, or gate threshold.

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion                              | Target        | Run 1  | Run 2  | Run 3  | Verdict |
| -------------------------------------- | ------------- | ------ | ------ | ------ | ------- |
| 1. Retrieved chunk contains the answer | 4 of 5        | 5 of 5 | 5 of 5 | 5 of 5 | MET     |
| 2. Every answer names a source         | 5 of 5        | 5 of 5 | 5 of 5 | 5 of 5 | MET     |
| 3. Gate stops out-of-corpus questions  | 4 of 5        | 5 of 5 | 5 of 5 | 5 of 5 | MET     |
| 4. Chunk integrity                     | 100%          | 100%   | 100%   | 100%   | MET     |
| 5. Relevance gate distance gap         | <0.60 / >0.80 | MISSED | MISSED | MISSED | MISSED  |

**Did it help?**
Yes, partially. The after run preserved 5 of 5 retrieval answers, 15 of 15
source citations, and 5 of 5 gate refusals while reducing context from five to
three chunks per query. It did not change the deterministic best distances, so
criterion 5 remains missed and would require an embedding or criterion change.

## What's Still Broken

Criterion 5 is still broken: the bus-ticket query scores 0.632330 even though
the retrieved chunk and generated answer are correct. The next step would be
to calibrate the target against more in-scope samples or test a second
embedding model, but I stopped after one targeted retrieval fix as required.

## What I'd Do Differently

I would rewrite Criterion 5 to measure gate separation directly, for example
all in-scope queries below 0.70 and all out-of-scope queries above 0.70, rather
than requiring an arbitrary 0.60 upper bound for valid queries. I would also
keep the chunk integrity criterion because its 100% metadata check is directly
observable and reproducible.
