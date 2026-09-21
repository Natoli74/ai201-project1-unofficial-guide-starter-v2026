"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` groups Markdown guides by section and adds the guide and
section context to every generated chunk.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to use a strategy that fits the documents you
actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass
import re

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split Markdown guides into section-local, header-aware chunks.

    Each chunk repeats its guide and section context so it remains useful when
    retrieved without the surrounding document.
    """
    chunks: list[Chunk] = []
    for doc in documents:
        title, sections = _markdown_sections(doc)
        for heading, body in sections:
            context = f"{title} - {heading}"
            body_limit = config.CHUNK_SIZE - len(context) - 2
            if body_limit <= config.CHUNK_OVERLAP:
                raise ValueError("chunk size must leave room for metadata and overlap")

            for piece in _overlapping_windows(body, body_limit, config.CHUNK_OVERLAP):
                chunks.append(
                    Chunk(
                        text=f"{context}\n\n{piece}",
                        source=doc.source,
                        index=sum(chunk.source == doc.source for chunk in chunks),
                        produced_by="chunker.py::split_documents",
                    )
                )

    return chunks


def _markdown_sections(doc: Document) -> tuple[str, list[tuple[str, str]]]:
    """Return the guide title and the text grouped beneath each ``##`` header."""
    lines = doc.text.splitlines()
    title = next(
        (match.group(1).strip() for line in lines if (match := re.match(r"^#\s+(.+?)\s*$", line))),
        doc.source.rsplit(".", 1)[0].replace("_", " ").title(),
    )

    sections: list[tuple[str, str]] = []
    heading = "Introduction"
    content: list[str] = []
    for line in lines:
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            if "\n".join(content).strip():
                sections.append((heading, "\n".join(content).strip()))
            heading = match.group(1).strip()
            content = []
            continue
        if line == f"# {title}" and not sections and not content:
            continue
        content.append(line)

    if "\n".join(content).strip():
        sections.append((heading, "\n".join(content).strip()))
    return title, sections


def _overlapping_windows(text: str, window_size: int, overlap: int) -> list[str]:
    """Split one section into bounded windows without crossing section edges."""
    if not text:
        return []
    step = window_size - overlap
    pieces: list[str] = []
    start = 0
    while start < len(text):
        piece = text[start : start + window_size].strip()
        if piece:
            pieces.append(piece)
        start += step
    return pieces


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
