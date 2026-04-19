import pandas as pd
import re
#for removing punctuation and special characters
import nltk
#prebuilt list of English stopwords (common words like “the” and “and”).
from nltk.corpus import stopwords

nltk.download("stopwords")
#downloads the stopwords dataset from NLTK (only on the first run; its cahched)

stop_words = set(stopwords.words("english"))
#words that dont add much meaning to the text and are often removed during preprocessing

#preprocess_text function: lowercases, removes punctuation, and removes stopwords from the input text
def preprocess_text(text):

    text = text.lower()

    text = re.sub(r"[^\w\s]", "", text) #any character that is not a word character and not whitespace

    words = text.split() #splits into words (tokens)

    words = [w for w in words if w not in stop_words]

    return " ".join(words) #joins the remaining words back into a single string and returns itle string and returns it



def clean_data_simple(data):

    print("Initial dataset size:", len(data))

    clean_rows = []
    removed_missing = []

    for _, row in data.iterrows(): #iterates over each row in the dataset using iterrows()
        if isinstance(row["sentence"], str):
            clean_rows.append(row)
        else:
            removed_missing.append(row) #if missing remove

    print("\nMissing values removed:", len(removed_missing))
    for r in removed_missing[:3]: #prints the first 3 removed rows with missing values for inspection
        print("Removed (missing):", r["sentence"])

    seen = set()
    final_rows = []
    removed_duplicates = []

    for row in clean_rows:
        sentence = row["sentence"]

    #    if sentence not in seen: #checks if the sentence has already been seen (to remove duplicates)
            #seen.add(sentence)
        final_rows.append(row)
    #    else:
       #     removed_duplicates.append(row)

    print("\nDuplicate rows removed:", len(removed_duplicates))
    for r in removed_duplicates[:3]:
        print("Removed (duplicate):", r["sentence"])

    
    print("\nFinal dataset size:", len(final_rows))

    return pd.DataFrame(final_rows) #returns a new DataFrame containing only the cleaned rows (with missing values and duplicates removed)