#importing necessary libraries
#for reading the dataset
import pandas as pd
#for handling paths 
from pathlib import Path
#for text vectorization
from sklearn.feature_extraction.text import TfidfVectorizer
#for splitting the dataset into training and testing sets
from sklearn.model_selection import train_test_split
#for machine learning models
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
#for evaluating the models
from sklearn.metrics import classification_report
#for handling warnings
from preprocessing import clean_data_simple, preprocess_text

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent  # repository root
#to get dataset path no matter where the script is run from
DATA_PATH = BASE_DIR /"data"/"dailydialog_llm_labeled.csv"

data = pd.read_csv(DATA_PATH)
#data = pd.read_csv("data/dataset.csv")
data = clean_data_simple(data)
# Preprocess the text data (from preprocessing.py)
#adds a new column "clean" to the dataset, which contains the preprocessed text from the "sentence" column
data["clean"] = data["sentence"].apply(preprocess_text)

LogisticRegression(class_weight="balanced")
LinearSVC(class_weight="balanced")

#using the TfidfVectorizer to convert text data into numerical features
vectorizer = TfidfVectorizer()
#for counting words and weighing them based on their importance in the dataset

X = vectorizer.fit_transform(data["clean"])
#X is obtained by vectorizing the "clean" column of the dataset, then the dataset is split into features (X) and labels (y)

y = data["label"]
#splitting the dataset into training and testing sets, with 80% for training and 20% for testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
#random state is set to 42 to ensure reproducibility of the results

# Define models to train
models = {
    # Logistic Regression
    "LogReg_C1": LogisticRegression(C=1, max_iter=1000, class_weight="balanced"),
    "LogReg_C0.1": LogisticRegression(C=0.1, max_iter=1000, class_weight="balanced"),

    # Naive Bayes
    "NB_alpha1": MultinomialNB(alpha=1.0),
    "NB_alpha0.5": MultinomialNB(alpha=0.5),

    # SVM
    "SVM_C1": LinearSVC(C=1, class_weight="balanced"),
    "SVM_C0.5": LinearSVC(C=0.5, class_weight="balanced")
}

# Train and evaluate each model
for name, model in models.items():

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\nModel:", name)

    print(classification_report(y_test, predictions))