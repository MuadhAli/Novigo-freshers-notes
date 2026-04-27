"""
view_embeddings.py
──────────────────
Run this from the same folder as your notebook to inspect
everything stored inside the local ChromaDB vector store.

Usage:
    python view_embeddings.py
"""

import os
import json
import chromadb
import numpy as np

# ── Config ────────────────────────────────────────────────────────────────────
CHROMA_PATH      = "./chroma_db"
COLLECTION_NAME  = "rbac_documents"


def get_collection():
    """Connect to the local ChromaDB and return the collection."""
    if not os.path.exists(CHROMA_PATH):
        raise FileNotFoundError(
            f"❌ No ChromaDB found at '{CHROMA_PATH}'.\n"
            "   Run the notebook first to generate and save the embeddings."
        )
    client     = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)
    return collection


# ── 1. Basic Stats ────────────────────────────────────────────────────────────
def show_stats(collection):
    count = collection.count()
    print("\n" + "=" * 60)
    print("  📊  ChromaDB Collection Stats")
    print("=" * 60)
    print(f"  Collection name : {COLLECTION_NAME}")
    print(f"  Storage path    : {os.path.abspath(CHROMA_PATH)}")
    print(f"  Total documents : {count}")
    print("=" * 60)


# ── 2. Show All Documents + Metadata ─────────────────────────────────────────
def show_documents(collection):
    results = collection.get(include=["documents", "metadatas"])

    print("\n📄  Stored Documents & Metadata")
    print("-" * 60)
    for i, (doc, meta) in enumerate(zip(results["documents"], results["metadatas"])):
        print(f"\n  [{i+1}] ID       : {results['ids'][i]}")
        print(f"       Title    : {meta.get('title', 'N/A')}")
        print(f"       Group    : {meta.get('access_group', 'N/A')}")
        print(f"       Category : {meta.get('category', 'N/A')}")
        print(f"       Content  : {doc[:120].strip()}...")
    print("-" * 60)


# ── 3. Show Raw Embedding Vectors ─────────────────────────────────────────────
def show_embeddings(collection):
    results = collection.get(include=["embeddings", "metadatas"])

    print("\n🔢  Raw Embedding Vectors")
    print("-" * 60)
    for i, (embedding, meta) in enumerate(zip(results["embeddings"], results["metadatas"])):
        vec = np.array(embedding)
        print(f"\n  [{i+1}] {meta.get('title', 'N/A')}")
        print(f"       Dimensions  : {len(embedding)}")
        print(f"       Min value   : {vec.min():.6f}")
        print(f"       Max value   : {vec.max():.6f}")
        print(f"       Mean        : {vec.mean():.6f}")
        print(f"       Norm (L2)   : {np.linalg.norm(vec):.6f}")
        print(f"       First 8 vals: {np.round(vec[:8], 6).tolist()}")
    print("-" * 60)


# ── 4. Show Similarity Between Documents ──────────────────────────────────────
def show_similarity_matrix(collection):
    results = collection.get(include=["embeddings", "metadatas"])

    titles     = [m.get("title", f"doc_{i}") for i, m in enumerate(results["metadatas"])]
    embeddings = np.array(results["embeddings"])

    # Normalize for cosine similarity
    norms      = np.linalg.norm(embeddings, axis=1, keepdims=True)
    normalized = embeddings / norms

    similarity = np.dot(normalized, normalized.T)

    print("\n📐  Cosine Similarity Matrix (1.0 = identical)")
    print("-" * 60)

    # Header row
    short = [t[:18] for t in titles]
    header = f"{'':22}" + "".join(f"{s:>22}" for s in short)
    print(header)

    for i, row_title in enumerate(short):
        row = f"  {row_title:<20}" + "".join(f"{similarity[i][j]:>22.4f}" for j in range(len(short)))
        print(row)
    print("-" * 60)
    print("  💡 Documents in the same access group should score higher\n"
          "     similarity to each other than across groups.")


# ── 5. Filter by Access Group ─────────────────────────────────────────────────
def show_by_group(collection, group: str):
    results = collection.get(
        where={"access_group": group},
        include=["documents", "metadatas"]
    )
    print(f"\n🔐  Documents in group: '{group}'")
    print("-" * 60)
    if not results["ids"]:
        print(f"   No documents found for group '{group}'")
    for i, (doc, meta) in enumerate(zip(results["documents"], results["metadatas"])):
        print(f"  [{i+1}] {meta.get('title')}  (id: {results['ids'][i]})")
        print(f"       {doc[:100].strip()}...")
    print("-" * 60)


# ── 6. Export to JSON ──────────────────────────────────────────────────────────
def export_to_json(collection, output_file="embeddings_export.json"):
    results = collection.get(include=["documents", "metadatas", "embeddings"])

    export = []
    for i in range(len(results["ids"])):
        export.append({
            "id":           results["ids"][i],
            "title":        results["metadatas"][i].get("title"),
            "access_group": results["metadatas"][i].get("access_group"),
            "category":     results["metadatas"][i].get("category"),
            "content":      results["documents"][i],
            "embedding_dims": len(results["embeddings"][i]),
            "embedding_preview": results["embeddings"][i][:10],  # first 10 values
        })

    with open(output_file, "w") as f:
        json.dump(export, f, indent=2)

    print(f"\n💾  Exported to '{output_file}' ({len(export)} records)")


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    collection = get_collection()

    show_stats(collection)
    show_documents(collection)
    show_embeddings(collection)
    show_similarity_matrix(collection)

    # Filter by specific group
    show_by_group(collection, "finance_team")
    show_by_group(collection, "hr_team")

    # Export everything to JSON
    export_to_json(collection)

    print("\n✅ Done! All embedding data inspected.")