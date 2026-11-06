
import re
from sentence_transformers import SentenceTransformer

# Sample sentences
samples = [
    "AI, search!",
    "I can't log in.",
    "help@example.com",
    "CS4944 version 2.1",
    "",
    "Python is easy to learn!"
]

print("=== TOKENIZATION COMPARISON ===")

for text in samples:

    # Split text using spaces
    ws = text.split()

    # Split text into words using regex
    words = re.findall(r"\b\w+\b", text)

    print("\nOriginal:", repr(text))
    print("Whitespace:", len(ws), ws)
    print("Word-like:", len(words), words)


# Check empty string
assert re.findall(r"\b\w+\b", "") == []


# Compare model tokenizer
print("\n=== MODEL SUBWORD TOKENIZER COMPARISON ===")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")

for text in samples[:2]:
    subwords = model.tokenizer.tokenize(text)

    print("\nText:", text)
    print("Subwords:", len(subwords), subwords)


# Display observations
print("\n--- Explanations & Observations ---")

print("1. Whitespace keeps can't as one token, but regex splits it into can and t.")

print("2. Whitespace keeps punctuation with words, while regex removes punctuation.")

print("3. Removing special characters can affect emails, IDs and programming syntax.")

print("Note: This regex is a simple tokenizer and does not handle every language perfectly.")
