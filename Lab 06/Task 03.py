
import csv
import json
import time
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from task2_chunks import make_chunks


def evaluate(scores, chunks, items):

    hits = []
    reciprocal = []

    for row, q in zip(scores, items):

        if q["doc"] is None:
            continue

        top = np.argsort(-row, kind="stable")[:3]

        good = []

        for rank, i in enumerate(top, 1):
            if chunks[i]["doc"] == q["doc"] and q["evidence"] in chunks[i]["text"]:
                good.append(rank)

        if good:
            hits.append(True)
            reciprocal.append(1 / good[0])
        else:
            hits.append(False)
            reciprocal.append(0)

    if hits:
        return float(np.mean(hits)), float(np.mean(reciprocal))

    return None, None


def main():

    # Read documents and queries
    with open("corpus.json", encoding="utf-8") as f:
        docs = json.load(f)

    with open("queries.json", encoding="utf-8") as f:
        items = json.load(f)

    assert docs and items

    # Check query data
    for q in items:

        assert q["split"] in {"dev", "test"}

        if q["doc"] is not None:
            assert q["evidence"]
            assert q["evidence"] in docs[q["doc"]]


    # Load the sentence transformer model
    start = time.perf_counter()

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2",
        device="cpu"
    )

    print("Model load seconds:", time.perf_counter() - start)

    query_texts = [q["query"] for q in items]
    logs = []


    # Try different chunking methods
    for strategy in ["0", "10", "sentence"]:

        chunks = make_chunks(docs, strategy)
        texts = [c["text"] for c in chunks]

        # Check token length
        lengths = []

        for text in texts + query_texts:
            tokens = model.tokenizer(text, truncation=False)["input_ids"]
            lengths.append(len(tokens))

        if max(lengths) > model.max_seq_length:
            raise ValueError("Model limit exceeded; rechunk or shorten query")


        # Try TF-IDF and Embedding methods
        for method in ["tfidf", "embedding"]:

            start = time.perf_counter()

            if method == "tfidf":

                vectorizer = TfidfVectorizer()

                C = vectorizer.fit_transform(texts)
                Q = vectorizer.transform(query_texts)

            else:

                C = model.encode(texts, normalize_embeddings=True)
                Q = model.encode(query_texts, normalize_embeddings=True)

            encode_seconds = time.perf_counter() - start


            # Calculate similarity scores
            start = time.perf_counter()

            if method == "tfidf":
                scores = (Q @ C.T).toarray()
            else:
                scores = Q @ C.T

            search_seconds = time.perf_counter() - start


            # Evaluate development and test data
            for split in ["dev", "test"]:

                indices = []

                for i, q in enumerate(items):
                    if q["split"] == split:
                        indices.append(i)

                selected_scores = scores[indices]
                selected_items = [items[i] for i in indices]

                result = evaluate(selected_scores, chunks, selected_items)

                print(
                    f"Strategy: {strategy} | Method: {method} | "
                    f"Split: {split} | Hit/MRR: {result} | "
                    f"Chunks: {len(chunks)} | "
                    f"Encode/Search Time: {encode_seconds:.4f}s / "
                    f"{search_seconds:.4f}s"
                )


            # Save top 3 search results
            for row, q in zip(scores, items):

                top = np.argsort(-row, kind="stable")[:3]

                for rank, i in enumerate(top, 1):

                    c = chunks[i]

                    record = {
                        "strategy": strategy,
                        "method": method,
                        "query": q["query"],
                        "split": q["split"],
                        "rank": rank,
                        "score": float(row[i]),
                        "chunk_id": c["id"],
                        "doc": c["doc"],
                        "start": c["start"],
                        "end": c["end"],
                        "text": c["text"],
                        "answerable": q["doc"] is not None
                    }

                    logs.append(record)


    # Save results in CSV file
    with open("retrieval_log.csv", "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(f, fieldnames=list(logs[0].keys()))

        writer.writeheader()
        writer.writerows(logs)

    print("Evaluation completed. Results logged to retrieval_log.csv")


if __name__ == "__main__":
    main()
