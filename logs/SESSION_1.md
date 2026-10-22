## Session 1 — Summary (Part A: notebook exploration)

**Paper used:** Singh & Shaik, IEEE TIM 2020 (Stockwell transform + SVM, stator faults). 9 pages, 40,595 characters, 51 chunks.

### What I did
- Loaded the PDF with PyMuPDFLoader. Got one Document per page (text + metadata like page number, title).
- Lightly cleaned the text, then split it into chunks of 1000 characters with 150 overlap. Each chunk keeps its page number.
- Turned each chunk into a 384-number vector with all-MiniLM-L6-v2 (local, free) and stored them in Chroma.
- Asked questions and looked at the top results with their distances.
- Built the prompt: retrieved chunks tagged with [page N] + the question + rules (answer only from these, cite pages, say if not found).

### What I learned (simple words)
- **Cosine similarity** compares the direction of two vectors. Same direction = similar meaning, even if the words are different.
- **Distance in Chroma** (cosine space) = 1 − similarity. Lower distance = closer match. Example: distance 0.48 → similarity 0.52.
- **Every chunk gets a score.** Retrieval is kNN: it ranks all 51 chunks and keeps the top k.
- **One page = about 5–6 chunks.** The splitter counts characters; it does not know where the abstract or a section ends.
- **Always read the full chunk.** The 100-character preview hid the real answer at rank 1.
- **How I ask matters.** A vague question gave distances 0.711–0.736 (almost no separation). A specific question gave 0.482–0.677 (clear separation).
- **Faithful is not the same as correct.** Claude's answer quoted the retrieved text correctly but listed methods my paper only *cites* (STFT, WT, WVD) as methods it *uses*.

### Problems found (to fix in Session 2–3)
- Journal header repeated on pages ("IEEE TRANSACTIONS…", "SINGH AND SHAIK: …").
- First-page footnote ("Manuscript received…") and IEEE copyright footer became their own chunks.
- Figure and table captions get pasted into the middle of sentences.
- The abstract is split across two chunks and mixed with the header → it ranked only #10 for my question.
- Overlap makes neighbouring chunks show up together in the top results (near-duplicates).

### Measurements (baseline — before any cleaning)
- Query q001: "Which time-frequency method is proposed for stator fault detection?"
  - Correct pages: 1 (abstract), 2 (contributions), 4 (method)
  - Rank 1 = page 4, correct → reciprocal rank = 1.0
  - Abstract chunk: rank 10, distance 0.794

### Errors and fixes
| Error | Cause | Fix |
|---|---|---|
| `source` / `&&` not working | Windows PowerShell, not Linux | Run venv commands separately, use `.venv\Scripts\Activate.ps1` |
| `(.venv) (base)` | Anaconda base also active | Check `sys.executable`; turned off conda auto-activate |
| Temperature error from Claude API | Newer models reject `temperature` | Removed it; will save answers to files for repeatable evals |
| `No module named sentence_transformers` | Jupyter used a different venv | Registered the venv as a Jupyter kernel |
| torch install failed (OSError) | Windows 260-character path limit | Moved project to `C:\dev\faultlit` |
| `not a valid file` | Relative path from `experiment/` folder | Use `pathlib`: `Path.cwd().parent / "papers" / ...` |
| Chroma count doubled | Re-ran the cell; same collection got added to | `delete_collection()` before rebuilding |

### Still to do
- Part A: run generation in the notebook, check `response.usage`; test the "proposed vs cited" prompt fix.
- Part B: update hello_rag.py, commit and push.
- Quiz: questions 1–6 + `C:\temp\report.txt`.




# To be noted for future:
Query q001 · abstract chunk (page 1): rank 10, distance 0.794 · before cleaning