"""Source-aware lexical retrieval for Work 103 (v2, BM25-lite ranking).

This is an isolated Sandbox prototype, not yet wired into ROOM-HOP Core/MCP.
Only pass explicitly approved text/Markdown files to index_documents().

v2 changes (2026-10-28):
- RetrievalIndex: cached per-chunk term frequencies, document frequencies,
  and average length; BM25-lite scoring (k1=1.2, b=0.75) with IDF weighting
  and length normalization, replacing the raw set-overlap score.
- Scores are normalized to (0, 1] by dividing by the sum of query-term IDFs,
  so min_score thresholds remain comparable across corpora.
- chunk_document(): unchanged public behaviour; a single line longer than
  max_chars becomes its own (oversized) chunk instead of looping forever.
- search(): now a thin wrapper over RetrievalIndex for backward compatibility.
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
import re
from typing import Iterable, Sequence


TOKEN_RE = re.compile(r"[\w'-]+", re.UNICODE)

# BM25 parameters. k1 controls term-frequency saturation, b controls
# length normalization (0 = none, 1 = full).
K1 = 1.2
B = 0.75


@dataclass(frozen=True)
class Document:
    source_id: str
    title: str
    text: str


@dataclass(frozen=True)
class Chunk:
    source_id: str
    title: str
    chunk_id: str
    start_line: int
    end_line: int
    text: str


@dataclass(frozen=True)
class SearchResult:
    source_id: str
    title: str
    chunk_id: str
    start_line: int
    end_line: int
    text: str
    score: float

    def to_dict(self) -> dict:
        return asdict(self)


def tokenize(text: str) -> list[str]:
    return [token.casefold() for token in TOKEN_RE.findall(text)]


def chunk_document(document: Document, max_chars: int = 1200, overlap_chars: int = 160) -> list[Chunk]:
    """Split a document into line-aligned chunks.

    A single line longer than max_chars becomes one oversized chunk
    (documented behaviour: never loop forever, never split a line).
    """
    if max_chars <= 0:
        raise ValueError("max_chars must be > 0")
    if overlap_chars < 0 or overlap_chars >= max_chars:
        raise ValueError("overlap_chars must be >= 0 and < max_chars")
    if not document.source_id.strip():
        raise ValueError("source_id must not be empty")

    lines = document.text.splitlines() or [""]
    chunks: list[Chunk] = []
    start = 0
    while start < len(lines):
        end = start
        size = 0
        while end < len(lines):
            line_size = len(lines[end]) + (1 if end > start else 0)
            if end > start and size + line_size > max_chars:
                break
            size += line_size
            end += 1
            if size >= max_chars:
                break
        if end == start:
            end += 1
        text = "\n".join(lines[start:end])
        chunks.append(Chunk(
            source_id=document.source_id,
            title=document.title,
            chunk_id=f"{document.source_id}#chunk-{len(chunks) + 1}",
            start_line=start + 1,
            end_line=end,
            text=text,
        ))
        if end >= len(lines):
            break
        # Keep overlap at line boundaries; always advance to avoid infinite loops.
        next_start = end
        carried = 0
        while next_start > start + 1 and carried < overlap_chars:
            next_start -= 1
            carried += len(lines[next_start]) + 1
        start = max(start + 1, next_start)
    return chunks


def index_documents(documents: Iterable[Document], max_chars: int = 1200, overlap_chars: int = 160) -> list[Chunk]:
    chunks: list[Chunk] = []
    seen: set[str] = set()
    for doc in documents:
        if doc.source_id in seen:
            raise ValueError(f"duplicate source_id: {doc.source_id}")
        seen.add(doc.source_id)
        chunks.extend(chunk_document(doc, max_chars=max_chars, overlap_chars=overlap_chars))
    return chunks


def load_approved_text_files(paths: Sequence[Path], allowed_roots: Sequence[Path]) -> list[Document]:
    """Load explicitly supplied .txt/.md files only from approved roots."""
    roots = [root.resolve() for root in allowed_roots]
    docs: list[Document] = []
    for raw_path in paths:
        path = raw_path.resolve()
        if path.suffix.casefold() not in {".txt", ".md"}:
            raise ValueError(f"unsupported file type: {path.suffix}")
        if not any(path == root or root in path.parents for root in roots):
            raise ValueError(f"path outside approved roots: {path}")
        if not path.is_file():
            raise FileNotFoundError(path)
        text = path.read_text(encoding="utf-8")
        docs.append(Document(source_id=path.as_posix(), title=path.name, text=text))
    return docs


class RetrievalIndex:
    """BM25-lite in-memory index with cached statistics.

    Scores are normalized to (0, 1] by dividing the raw BM25 sum by the
    sum of query-term IDFs. The score is a ranking signal, not a
    calibrated probability; calibrate min_score on a labeled set.
    """

    def __init__(self, chunks: Sequence[Chunk]):
        self.chunks = list(chunks)
        self._tf: list[Counter[str]] = []
        self._len: list[int] = []
        self._df: Counter[str] = Counter()
        for chunk in self.chunks:
            counts = Counter(tokenize(chunk.text))
            self._tf.append(counts)
            self._len.append(sum(counts.values()))
            self._df.update(counts.keys())
        total = sum(self._len)
        self._avg_len = (total / len(self._len)) if self._len else 0.0

    def idf(self, term: str) -> float:
        n = len(self.chunks)
        df = self._df.get(term, 0)
        return math.log(1 + (n - df + 0.5) / (df + 0.5))

    def search(self, query: str, top_k: int = 5, min_score: float = 0.15) -> list[SearchResult]:
        if not query.strip():
            raise ValueError("query must not be empty")
        if top_k < 1:
            raise ValueError("top_k must be >= 1")
        query_terms = sorted(set(tokenize(query)))
        if not query_terms:
            return []
        idf_sum = sum(self.idf(term) for term in query_terms) or 1.0
        results: list[SearchResult] = []
        for i, chunk in enumerate(self.chunks):
            raw = 0.0
            for term in query_terms:
                freq = self._tf[i].get(term, 0)
                if not freq:
                    continue
                if self._avg_len:
                    norm = freq * (K1 + 1) / (
                        freq + K1 * (1 - B + B * (self._len[i] / self._avg_len))
                    )
                else:
                    norm = float(freq)
                raw += self.idf(term) * norm
            score = round(raw / idf_sum, 6)
            if score >= min_score:
                results.append(SearchResult(
                    source_id=chunk.source_id,
                    title=chunk.title,
                    chunk_id=chunk.chunk_id,
                    start_line=chunk.start_line,
                    end_line=chunk.end_line,
                    text=chunk.text,
                    score=score,
                ))
        results.sort(key=lambda item: (-item.score, item.source_id, item.start_line, item.chunk_id))
        return results[:top_k]


def search(chunks: Sequence[Chunk], query: str, top_k: int = 5, min_score: float = 0.15) -> list[SearchResult]:
    """Backward-compatible wrapper: builds a RetrievalIndex over chunks."""
    return RetrievalIndex(chunks).search(query, top_k=top_k, min_score=min_score)


def build_context(results: Sequence[SearchResult]) -> dict:
    """Build traceable evidence context; caller must abstain when results are empty."""
    return {
        "sufficient_evidence": bool(results),
        "abstention_reason": None if results else "NO_RELEVANT_SOURCE_FOUND",
        "citations": [
            {
                "source_id": r.source_id,
                "title": r.title,
                "chunk_id": r.chunk_id,
                "start_line": r.start_line,
                "end_line": r.end_line,
                "score": r.score,
            }
            for r in results
        ],
        "context": "\n\n".join(
            f"[{r.title} | {r.chunk_id} | lines {r.start_line}-{r.end_line}]\n{r.text}"
            for r in results
        ),
    }
