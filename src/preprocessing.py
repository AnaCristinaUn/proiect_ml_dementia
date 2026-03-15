
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

    return " ".join(words) #joins the remaining words back into a single string and returns it