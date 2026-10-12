# Fault-Diagnosis Paper RAG

A research assistant over a private library of 50+ papers on electrical-machine fault diagnosis
(bearing, broken rotor bar, stator inter-turn, induction motor faults). Ask technical questions,
get answers grounded in the papers with citations.

**Status:** Session 1 — single-paper hello world. Nothing evaluated yet.

## Stack
Python · LangChain · ChromaDB · sentence-transformers (all-MiniLM-L6-v2) · PyMuPDF · Claude API

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then put your Anthropic API key in .env
```

## Run
```bash
python hello_rag.py papers/<paper>.pdf "What signal filtering methods are used?"
python hello_rag.py papers/<paper>.pdf "..." --no-llm   # retrieval only
```

## About the papers
The PDFs are copyrighted (IEEE / Elsevier) and are **not** in this repo. `references.csv` lists
them by DOI so results can be reproduced by anyone with access.
