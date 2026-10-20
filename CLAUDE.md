# CLAUDE.md — FaultLit (fault-diagnosis-research-rag)

## What this project is
A RAG research assistant over 50+ papers on electrical-machine fault diagnosis (bearing, broken rotor bar,
stator inter-turn, induction motor). Portfolio + interview project. The plan is in PROGRESS.md (13 sessions).

## Who I am
PhD, 12+ yrs industrial ML (vibration, condition monitoring, time-series). Strong Python, new to GenAI/RAG.
Bridge new ideas to ML concepts I know (vectors, kNN, features, metrics). Don't re-teach basic RAG.

## How to work with me (strict)
- I am LEARNING. Do not write or change code unless I ask. Default: explain, review, debug, quiz.
- When I ask for code: explain each function BEFORE showing it, then give annotated code, one step at a time.
- Never dump many files at once. One function or one change per turn.
- When debugging: explain the cause first, then the smallest fix. Make me run it.
- Be direct. No praise. Lead with what is wrong or missing.

## Honesty rules
- Never put a metric in README, PROGRESS.md or resume text unless I measured it. Mark "built" vs "designed".
- If unsure about a library API, check the installed version instead of guessing.

## Environment
- Windows, PowerShell, venv at .venv (Anaconda also installed — check `python -c "import sys; print(sys.executable)"` points to .venv).
- Run: `python hello_rag.py papers/<file>.pdf "<question>" [--no-llm]`

## Never
- Commit or push anything in papers/, chroma_db/, or .env (papers are copyrighted IEEE/Elsevier).
- Copy paper text into eval files — store paper id + page numbers only.

## Logging
After each session, help me fill logs/SESSION_N.md and update PROGRESS.md (one-line result).