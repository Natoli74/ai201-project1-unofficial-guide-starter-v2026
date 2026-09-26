"""Repeat deterministic acceptance checks three times for qualification evidence."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import config
import questions
from chunker import split_documents
from gate import check
from ingest import load_documents
from store import search

ROUNDS = 3


def main() -> None:
    chunks = split_documents(load_documents(config.CORPUS))
    lines = [
        "# Qualification checks",
        "",
        "- Produced by: `tools/qualification_checks.py::main`",
        f"- Rounds: {ROUNDS}",
        "- Corpus: `city_guides`",
        "",
        "| Criterion | Round 1 | Round 2 | Round 3 |",
        "|---|---:|---:|---:|",
    ]

    gate_results = []
    integrity_results = []
    distance_results = []
    for round_number in range(1, ROUNDS + 1):
        gate_results.append(_gate_refusals())
        integrity_results.append(_chunk_integrity(chunks))
        distance_results.append(_distance_gap())

    lines.append(
        f"| 3. Gate refusal | {gate_results[0]} of 5 | "
        f"{gate_results[1]} of 5 | {gate_results[2]} of 5 |"
    )
    lines.append(
        f"| 4. Chunk integrity | {integrity_results[0]}% | "
        f"{integrity_results[1]}% | {integrity_results[2]}% |"
    )
    lines.append(
        f"| 5. Distance gap | {distance_results[0]} | "
        f"{distance_results[1]} | {distance_results[2]} |"
    )
    lines.extend(
        [
            "",
            "Criterion 3 is repeated as a deterministic gate check. Criterion 4",
            "is repeated against all generated chunks. Criterion 5 is repeated",
            "against all ten recorded distance measurements.",
        ]
    )
    output = config.RESULTS_DIR / "qualification_checks_2026-09-26.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(output)
    print("\n".join(lines))


def _gate_refusals() -> int:
    return sum(
        not check(
            search(question, top_k=config.TOP_K, corpus=config.CORPUS),
            threshold=config.THRESHOLD,
        ).passed
        for question in questions.OUT_OF_SCOPE
    )


def _chunk_integrity(chunks) -> int:
    valid = sum(
        chunk.text.splitlines()[0].count(" - ") == 1
        and len(chunk.text) <= config.CHUNK_SIZE
        for chunk in chunks
    )
    return round(valid * 100 / len(chunks))


def _distance_gap() -> str:
    in_scope = [
        search(item["question"], top_k=1, corpus=config.CORPUS)[0].distance
        for item in questions.QUESTIONS
    ]
    out_of_scope = [
        search(question, top_k=1, corpus=config.CORPUS)[0].distance
        for question in questions.OUT_OF_SCOPE
    ]
    return f"{min(in_scope):.3f}-{max(in_scope):.3f} / {min(out_of_scope):.3f}-{max(out_of_scope):.3f}"


if __name__ == "__main__":
    main()
