# FaultLit — a research assistant for fault-diagnosis papers

FaultLit lets you ask questions about a library of research papers on electrical machine fault diagnosis — bearing faults, broken rotor bars, stator inter-turn faults, induction motors — and get answers that cite the paper and page they came from.

It is built with retrieval-augmented generation (RAG): the papers are split into small pieces, the pieces most relevant to your question are found, and an LLM (Claude) writes an answer using only those pieces.

Example questions:
- Which time-frequency method is proposed for stator fault detection?
- Which papers use CNNs for fault classification?
- Which datasets appear across these papers?

## Status

Early stage. What works today:
- Load one paper (PDF), split it into chunks, embed them, and retrieve the most relevant ones for a question
- Generate an answer with page citations using Claude

Planned, not built yet:
- Cleaning PDF noise (headers, footers, captions, references)
- Paper metadata (title, authors, year) for filtering and citations
- Scaling to 50+ papers
- An evaluation set with retrieval metrics (recall@k, MRR) and answer faithfulness checks
- Hybrid search, contextual retrieval and reranking, each measured against the baseline
- An agent that can compare methods across papers

Results will be added here only once they are measured.

## Tech stack

Python · LangChain · ChromaDB · sentence-transformers (all-MiniLM-L6-v2) · PyMuPDF · Claude API

## Getting started

```bash
git clone <this-repo-url>
cd fault-diagnosis-research-rag

python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
# macOS / Linux:         source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Anthropic API key. Put a PDF in `papers/`, then run:

```bash
python hello_rag.py papers/your_paper.pdf "What signal processing methods are used?"

# retrieval only, no API call:
python hello_rag.py papers/your_paper.pdf "What signal processing methods are used?" --no-llm
```

Windows tip: if `pip install` fails while installing torch with a path error, move the project to a short path such as `C:\dev\faultlit`.

## Project layout

```
hello_rag.py       single-paper prototype (load → chunk → embed → retrieve → answer)
src/               pipeline code (in progress)
eval/              evaluation questions and scripts (planned)
logs/              session notes
papers/            your PDFs — not included in this repo
references.csv     list of papers used (title, authors, year, DOI)
PROGRESS.md        build plan and progress
```

## About the papers

The papers used in this project are published by IEEE and Elsevier and are copyrighted, so they are not included here. `references.csv` lists them by DOI so anyone with access can rebuild the same library.

## Author

Megha Singh