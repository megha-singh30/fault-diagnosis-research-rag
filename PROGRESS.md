# PROGRESS — Fault-Diagnosis Paper RAG

## Session tracker
| # | Session | Status | One-line result |
|---|---------|--------|-----------------|
| 1 | Setup + one paper → one query → one answer | IN PROGRESS | |
| 2 | PDF extraction noise: headers, columns, references, equations | NOT STARTED | |
| 3 | Paper metadata (title/authors/year via references.csv) + chunking for long papers | NOT STARTED | |
| 4 | Scale to 50+ papers, persistent Chroma, cited multi-paper answers | NOT STARTED | |
| 5 | Eval I: gold set + recall@k, MRR | NOT STARTED | |
| 6 | Eval II: answer faithfulness + refusal path | NOT STARTED | |
| 7 | Aggregation questions ("which papers use CNNs?") via per-paper extraction | NOT STARTED | |
| 8 | Agentic extension: literature-review agent (multi-hop, compare methods) | NOT STARTED | |
| 9 | README thesis + ship | NOT STARTED | |

## Built vs designed (honesty ledger — resume claims come ONLY from "Built + measured")
| Item | Built | Measured | Number |
|------|-------|----------|--------|
| Single-paper RAG loop | — | — | — |

## Re-quiz watchlist (concepts I fumbled — keep re-asking until solid)
-

## Open questions / decisions
- Which paper goes first? (pick one you know well, two-column IEEE, ideally open access)
