# S.I.R.A (Self-Initiated Research Agent)

## What to Build ?

- CLI/GUI AI-agent that opens with targeted questions to scope a topic
- Drafts a research plan with papers, abstracts, etc.
- Uses a large knowledgebase like --> arXiv, PubMed, Google Scholar (optional)
- Downloadable PDFs, Parse texts, chunks and embed them. (Build local vector index - FAISS)
- Systematic summaries, annotated bibliographies, running notes with citations

---
## Possible Tech-Stack ?

- Python
- Pydantic
- AsyncIO
- tiktoken
- Sentence-Transformer/ Local-Embedding model
- Random LLM/transformer
- (Optional): SQL

---
## Secret Sauce: Agent Roles & Training Loop

1. **Interviewer**: Asks the clarifying questions to define scope using the user's answers (Topic, outcomes, depth, time, preferences, datasets, data ranges, etc.)
2. **Planner**: Converts answers into a research strategy (sources, keywords, abstract, methodology, boolean queries, inclusion/exclusion criteria)
3. **Searcher**: Executes queries against arXiv, PubMed, Google Scholar (Optional via external API)
4. **Reader**: Fetches PDFs. abstracts, parses, embeds, chunks, indexes
5. **Critic**: Challenges the research strategy, suggests improvements and next questions/experiments for interviewer to ask to user.

---
## Basic Workflow

![Work-Flow Diagram](<images/Pasted image 20250814210243.png>)

---
## Every Individual Agent In Detail

### 1. Interviewer

**Goal:** Turn a fuzzy request into a well-scoped research brief.

**Inputs:** User prompt + any prior notes.  
**Primary output:** `ScopeBrief` (JSON-like record) + a short list of unresolved questions for the user.

**What it captures (fields):**

- Objective & success criteria (what “good” looks like)
    
- Audience & use case (paper, product decision, quick brief)
    
- Constraints (time, budget, compute, data availability)
    
- Topical scope (entities/phenomena), geography, population
    
- Time window/recency, languages
    
- Desired evidence types (RCTs, surveys, benchmarks, meta-analyses, tutorials, repos, datasets)
    
- Must-include / must-exclude items (e.g., “exclude paywalled reviews”, “focus on MeSH:Diabetes Mellitus, Type 2”)
    

**How it works (prompting pattern):**

1. **Triage →** ask 3–5 high-leverage clarifiers (topic, outcome, time window, audience, exclusions).
    
2. **Frame →** apply a schema: PICO (biomed), TREC/IR style “aspect list” (CS), or custom facets.
    
3. **Confirm →** mirror back the `ScopeBrief` in bullet form; ask for any corrections.
    

**Failure-mode guards:**

- Never ask >7 questions at once; batch by priority.
    
- Default sensible values (e.g., last 5 years) with “change if wrong”.
    
- Keep a `changes[]` log so the strategy remains reproducible.

---
## 2. Planner

**Goal:** Convert the `ScopeBrief` into an executable research strategy.

**Inputs:** `ScopeBrief`.  
**Primary outputs:** `ResearchStrategy` + per-source `QueryPlan[]`.

**What it produces:**

- **Source list:** arXiv, PubMed/PMC, Google Scholar (via an API provider), Semantic Scholar/Crossref, plus optional web/news/code/data portals.
    
- **Keyword graph:** seed terms → synonyms/stems → controlled vocab (e.g., MeSH) → negatives.
    
- **Boolean strings** per source (respecting each API’s syntax limits).
    
- **Inclusion/Exclusion criteria:** study types, date ranges, languages, venues.
    
- **Ranking rubric:** how to pick top-K (recency, venue tier, citation velocity, relevance score).
    
- **Evidence plan:** which questions each source should answer.
    

**How it works (algorithm sketch):**

1. Expand terms → de-duplicate → map to controlled vocab (e.g., MeSH, ACM CCS).
    
2. Build **per-source** queries (arXiv categories, PubMed MeSH+Title/Abstract, GS generic).
    
3. Create a **reproducible plan**:
    
    `{   "source": "PubMed",   "query": "(\"type 2 diabetes\"[MeSH Terms]) AND (GLP-1 OR semaglutide) AND 2019:3000[dp]",   "page_size": 100,   "max_pages": 5,   "fields": ["pmid","title","year","mesh","pmcid","doi"] }`
    
4. Define **quality gates** (e.g., exclude predatory venues; require DOI or PMCID).
    
5. Hand off to Searcher.

---
## 3. Searcher

**Goal:** Execute the plan, harvest clean, deduped metadata you can trust.

**Inputs:** `QueryPlan[]`.  
**Primary outputs:** `CorpusIndex` (normalized metadata, de-duplicated) + `ProvenanceLog`.

**What it does:**

- Calls source APIs (e.g., arXiv API; NCBI E-utilities for PubMed/PMC; Crossref/Semantic Scholar; GS via a compliant API provider). Stores raw responses in a log for reproducibility.
    
- Normalizes records to a common schema:
    
    `{ id, title, authors[], year, venue, abstract, doi, arxiv_id, pmid, pmcid,   url_pdf?, url_landing, source, terms_hit[], score_source }`
    
- **De-dupes** by DOI → strong title match (normalized Levenshtein/Jaro) → author+year fallback.
    
- **Ranks** using a blended score: query match, recency decay, venue whitelist, citation velocity (if available).
    
- Returns top-K plus a “long tail” queue for later.
    

**How it works (process):**

1. For each plan → paginate with rate-limit awareness → collect results.
    
2. Normalize & dedupe → compute scores → persist `ProvenanceLog` (query string, timestamp, page).
    
3. Emit `CorpusIndex(top_k=200)` to Reader.
    

**Guards:**

- Respect API terms/rate limits.
    
- Record the **exact** query string used and time of retrieval.
    
- If a source fails, degrade gracefully and flag for the Critic.

---
## 4. Reader

**Goal:** Pull the papers, parse them, and turn them into verifiable evidence.

**Inputs:** `CorpusIndex`.  
**Primary outputs:** `EvidenceTable` + `PaperCards` (summaries with citations) + `Gaps`.

**What it does:**

- **Fetches PDFs** (arXiv direct; PMC PDFs; Unpaywall for OA links; DOI resolver for landing pages).
    
- **Parses** PDFs (e.g., GROBID for structure + BibTeX; PyMuPDF/PDFMiner for text; simple table/figure extraction).
    
- **Sections** & **chunks** each paper (e.g., 600–1000 tokens, overlap=100) with section labels.
    
- Builds light embeddings to support **targeted Q/A**: answer user questions per chunk, citing span offsets.
    
- Extracts **claims** + **evidence snippets** + **limitations** + **study design**.
    
- Produces per-paper cards:
    
    `{   id, key_findings[], methods, dataset/task, metrics, limitations[],   direct_quotes[{span, page}], citations[{standard format}], confidence }`
    
- Aggregates into an `EvidenceTable` across papers (columns: Paper • Year • Setting • Measure • Result • Caveats • Link).
    

**How it works (flow):**

1. Prioritize top-ranked papers until a token/page/time budget is hit.
    
2. For each user question/aspect, run retrieval → answer → attach citation (paper id + page/section).
    
3. Summarize **consensus vs disagreement** and surface **unknowns** as `Gaps`.
    

**Guards:**

- All claims carry **attribution** (paper id + section/page).
    
- Mark anything inferred without a direct cite as **interpretation**.
    
- Prefer OA/PMC/arXiv where possible to avoid access issues.

---
## 5. Critic

**Goal:** Stress-test the strategy and the evidence; drive the next iteration.

**Inputs:** `ResearchStrategy`, `CorpusIndex`, `EvidenceTable`, `Gaps`, user’s goal.  
**Primary outputs:** `ImprovementPlan` + `ReviewerQuestions` (for the user) + `PatchSet` (edits for Planner/Searcher).

**What it checks:**

- **Coverage:** Are key aspects/entities missing? (e.g., “no RCTs included”, “Asia-Pacific studies absent”)
    
- **Balance:** Too many reviews vs. primary studies? Overweight old citations?
    
- **Methodology:** Are comparisons apples-to-apples? Metric leakage? Small-N pitfalls?
    
- **Bias & risk:** Publication bias, data leakage, confounders, ethics/safety.
    
- **Reproducibility:** Queries logged? Versioned? Clear inclusion/exclusion?
    

**What it produces:**

- **Actionable patches** (e.g., “Add MeSH term X”, “Include venue list Y”, “Expand year range to 2018–present”).
    
- **Targeted follow-ups** for the Interviewer to ask (e.g., “Do we care about pediatric populations?”).
    
- **Stop/continue** recommendation with an explicit **confidence** score.
    

**Rubric (use as a checklist):**

- Source diversity • Recency • Evidence quality • Traceable citations • Alignment to user’s success criteria.

---
## The Training Loop (glue logic)

1. **Interviewer → Planner:** Clarify scope → produce `ResearchStrategy`.
    
2. **Planner → Searcher:** Create `QueryPlan[]`.
    
3. **Searcher → Reader:** Build `CorpusIndex`.
    
4. **Reader → Critic:** Produce `EvidenceTable` + `Gaps`.
    
5. **Critic → (Interviewer & Planner):** Ask targeted questions and emit `PatchSet`.
    
6. **Repeat** until: user says stop _or_ Critic’s confidence passes a threshold _and_ open questions are minor.
    
7. **Final output:** A clean **Research Brief**: (a) executive summary, (b) key findings with citations, (c) evidence table, (d) limitations & open questions, (e) appendix with query strings & provenance.