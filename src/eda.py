#importing necessary libraries
import pandas as pd
from collections import Counter
from preprocessing import preprocess_text

#holds the dataset 
data = pd.read_csv("data/dataset.csv")

print("Number of samples:", len(data))

print("\nClass distribution:")
#value_counts() method is used to count the occurrences of each unique value in the "label" column.
#it represents the class distribution in the dataset. 
print(data["label"].value_counts())

#calculating the length of each sentence and storing it in a new column called "length".
data["length"] = data["sentence"].apply(lambda x: len(x.split()))

print("\nAverage sentence length:", data["length"].mean())


# build a list of tokens using the same preprocessing as the model pipeline
cleaned = data["sentence"].dropna().apply(preprocess_text)

# split each preprocessed sentence into words and flatten into a single list
tokens = [w for sent in cleaned for w in sent.split()]
counts = Counter(tokens)

print("\nTop 20 words after normalization:")
for word, count in counts.most_common(20):
    print(f"  {word:>12}  {count}")

important = ["medicine", "doctor"]
unimportant = ["tv", "sleep"]

def keyword_counts(words, counter):
    return {w: counter.get(w, 0) for w in words}

print("\nImportant keywords (should be relevant):", keyword_counts(important, counts))
print("Unimportant keywords (might be noise):", keyword_counts(unimportant, counts))
