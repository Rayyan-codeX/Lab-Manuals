
import re


def word_spans(text):
    spans = []

    for m in re.finditer(r"\S+", text):
        spans.append((m.start(), m.end()))

    return spans


def windows(text, size=40, overlap=10, offset=0):

    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("Invalid size or overlap")

    spans = word_spans(text)
    result = []

    step = size - overlap

    for i in range(0, len(spans), step):
        j = min(i + size, len(spans))

        start = offset + spans[i][0]
        end = offset + spans[j - 1][1]

        result.append((start, end))

        if j == len(spans):
            break

    return result


def sentence_chunks(text, size=40):

    if size <= 0:
        raise ValueError("Size must be positive")

    cuts = [0]

    for m in re.finditer(r"[.!?]\s+", text):
        cuts.append(m.end())

    cuts.append(len(text))

    result = []
    pending = None
    count = 0

    for a, b in zip(cuts, cuts[1:]):

        segment = text[a:b]
        n = len(segment.split())

        if n == 0:
            continue

        if n > size:

            if pending is not None:
                result.append(pending)

            result.extend(windows(segment, size, 0, a))
            pending = None
            count = 0

        elif pending is not None and count + n <= size:

            pending = (pending[0], b)
            count = count + n

        else:

            if pending is not None:
                result.append(pending)

            pending = (a, b)
            count = n

    if pending is not None:
        result.append(pending)

    return result


def make_chunks(docs, strategy):

    result = []

    for doc_id, text in docs.items():

        if strategy == "sentence":
            spans = sentence_chunks(text)
        else:
            spans = windows(text, 40, int(strategy))

        for i, (a, b) in enumerate(spans):

            chunk = {
                "id": doc_id + ":" + str(i),
                "doc": doc_id,
                "start": a,
                "end": b,
                "text": text[a:b]
            }

            result.append(chunk)

    return result


# Main program
if __name__ == "__main__":

    # Testing empty text
    assert windows("") == []

    # Testing short text
    assert windows("short text") == [(0, 10)]

    # Testing invalid overlap
    try:
        windows("a b", 2, 2)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid overlap was accepted")

    # Testing long text
    long_text = "".join(["word "] * 95) + "."

    chunks = sentence_chunks(long_text)

    for a, b in chunks:
        assert len(long_text[a:b].split()) <= 40

    # Testing different chunking methods
    docs = {
        "example": "Reset your password. Keep recovery codes private."
    }

    for strategy in ["0", "10", "sentence"]:

        chunks = make_chunks(docs, strategy)

        for c in chunks:
            assert c["text"] == docs[c["doc"]][c["start"]:c["end"]]

    print("Task 2 chunking tests passed successfully.")
