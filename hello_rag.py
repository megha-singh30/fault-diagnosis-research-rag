"""
hello_rag.py — Session 1: ONE paper PDF -> ONE query -> ONE grounded, cited answer.

Run:
    python hello_rag.py papers/your_paper.pdf "What signal filtering methods are used?"
    python hello_rag.py papers/your_paper.pdf "..." --no-llm      # retrieval only, no API call

Deliberately minimal: in-memory Chroma (nothing saved to disk), one file, no eval yet.
"""

import argparse                      # reads the command-line arguments (pdf path, question, flags)
import os                            # reads the API key / model name from environment variables

from dotenv import load_dotenv       # loads key=value pairs from a local .env file into os.environ
from langchain_community.document_loaders import PyMuPDFLoader     # PDF -> list of Documents (1 per page)
from langchain_text_splitters import RecursiveCharacterTextSplitter  # long text -> overlapping chunks
from langchain_huggingface import HuggingFaceEmbeddings            # wraps sentence-transformers
from langchain_chroma import Chroma                                # vector store

load_dotenv()                        # do this first so ANTHROPIC_API_KEY is visible below

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001")   # cheap default; override in .env
CHUNK_SIZE = 1000                    # characters, not tokens (~200-250 tokens of paper text)
CHUNK_OVERLAP = 150                  # so a sentence cut at a boundary still appears whole in one chunk
TOP_K = 4


def load_pdf(path):
    """Load a PDF and show what the extractor actually produced.

    NEW vs your last corpus: real IEEE/Elsevier PDFs are messy. This function exists
    mostly so you LOOK at the raw text before trusting it.
    """
    pages = PyMuPDFLoader(path).load()          # one Document per page; metadata['page'] is 0-indexed
    total_chars = sum(len(p.page_content) for p in pages)
    print(f"\n[load] {path}: {len(pages)} pages, {total_chars:,} characters")
    print(f"[load] metadata keys on page 1: {sorted(pages[0].metadata.keys())}")
    print(f"[load] PDF title field: {pages[0].metadata.get('title')!r}  <- often empty/junk in IEEE PDFs")
    print("[load] first 400 chars of page 1 (check: running header? columns interleaved?):")
    print("-" * 60)
    print(pages[0].page_content[:400])
    print("-" * 60)
    return pages


def chunk(pages):
    """Split page-level Documents into overlapping chunks.

    split_documents (not split_text) keeps each page's metadata on every chunk,
    which is what lets us cite 'page N' later.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],   # try paragraph breaks first, then lines, sentences, words
    )
    chunks = splitter.split_documents(pages)
    print(f"[chunk] {len(pages)} pages -> {len(chunks)} chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    return chunks


def build_store(chunks):
    """Embed every chunk and put it in an in-memory Chroma collection.

    MiniLM silently truncates input past 256 word-pieces — that's why chunks stay ~1000 chars.
    normalize_embeddings=True -> unit vectors, so similarity is cosine.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        encode_kwargs={"normalize_embeddings": True},
    )
    store = Chroma.from_documents(
        chunks,
        embeddings,
        collection_name="hello",
        collection_metadata={"hnsw:space": "cosine"},   # distance = 1 - cosine similarity
    )
    print(f"[store] embedded {len(chunks)} chunks with {EMBED_MODEL}")
    return store


def retrieve(store, question, k=TOP_K):
    """kNN search: return the k chunks closest to the question vector, with distances."""
    hits = store.similarity_search_with_score(question, k=k)   # list of (Document, distance); lower = closer
    print(f"\n[retrieve] top-{k} for: {question!r}")
    for rank, (doc, dist) in enumerate(hits, start=1):
        page = doc.metadata.get("page", 0) + 1                 # convert 0-indexed -> human page number
        preview = doc.page_content[:90].replace("\n", " ")
        print(f"  {rank}. page {page}  dist={dist:.3f}  {preview}...")
    return hits


def build_prompt(question, hits):
    """Augment step: paste the retrieved chunks into the prompt, each tagged with its page."""
    context = "\n\n".join(
        f"[page {doc.metadata.get('page', 0) + 1}]\n{doc.page_content}"
        for doc, _ in hits
    )
    return (
        "Answer the question using ONLY the excerpts below from one research paper.\n"
        "Cite every claim with its page tag, e.g. [page 3].\n"
        "If the excerpts don't contain the answer, say so plainly — do not guess.\n\n"
        f"EXCERPTS:\n{context}\n\nQUESTION: {question}"
    )


def generate(prompt):
    """Generate step: one call to Claude. Imported here so --no-llm runs without the SDK/key."""
    import anthropic                                   # reads ANTHROPIC_API_KEY from the environment
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=LLM_MODEL,
        max_tokens=600,                               # same question -> (nearly) same answer; matters for eval later
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text                    # content is a list of blocks; first is the text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("question")
    parser.add_argument("--no-llm", action="store_true", help="stop after retrieval")
    args = parser.parse_args()

    pages = load_pdf(args.pdf)
    chunks = chunk(pages)
    store = build_store(chunks)
    hits = retrieve(store, args.question)

    if args.no_llm:
        return
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\n[generate] ANTHROPIC_API_KEY not set — add it to .env or rerun with --no-llm")
        return
    print("\n[answer]\n" + generate(build_prompt(args.question, hits)))


if __name__ == "__main__":
    main()
