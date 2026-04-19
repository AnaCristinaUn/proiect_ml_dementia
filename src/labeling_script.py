import pandas as pd
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_PATH = BASE_DIR / "train" / "dialogues_train.txt"
TEST_PATH = BASE_DIR / "test" / "dialogues_test.txt"

OUTPUT_PATH = BASE_DIR / "data" / "dailydialog_dataset.csv"



health_keywords = [
    "doctor", "hospital", "clinic", "nurse", "appointment", "checkup",
    "medicine", "medication", "treatment", "therapy", "prescription",
    "pharmacy", "diagnosis", "surgery", "emergency", "ambulance",
    "pain", "fever", "headache", "cough", "infection", "injury",
    "ill", "sick", "disease", "condition", "symptom"
]

symptom_keywords = [
    "dizzy", "dizziness", "fatigue", "tired", "weak",
    "nausea", "vomiting", "shortness of breath",
    "chest pain", "back pain", "joint pain",
    "swelling", "rash", "bleeding",
    "confusion", "memory loss", "forget", "forgot",
    "anxiety", "depressed", "stress"
]

treatment_keywords = [
    "took medicine", "take medicine", "missed medication",
    "forgot medication", "pill", "pills", "tablet", "dose",
    "injection", "insulin", "antibiotic",
    "bandage", "ointment", "treatment",
    "rehab", "exercise therapy"
]

daily_important_keywords = [
    "appointment", "meeting", "schedule", "scheduled",
    "reminder", "alarm", "calendar",
    "visited", "visit", "went to",
    "called doctor", "called hospital",
    "checkup", "test", "blood test",
    "result", "report"
]

care_keywords = [
    "caregiver", "helped me", "assisted me",
    "my daughter", "my son", "my spouse",
    "my nurse", "my doctor",
    "someone helped", "needed help",
    "support", "assistance"
]

risk_keywords = [
    "fell", "fall", "injured", "hurt",
    "emergency", "urgent", "accident",
    "could not breathe", "passed out",
    "lost consciousness", "severe pain"
]

monitoring_keywords = [
    "blood pressure", "heart rate", "pulse",
    "temperature", "glucose", "blood sugar",
    "oxygen level", "monitor", "measured",
    "checked my health", "health data"
]



def compute_score(sentence: str) -> int:
    s = sentence.lower()
    score = 0

    # High importance (health + symptoms)
    if any(word in s for word in health_keywords):
        score += 2

    if any(word in s for word in symptom_keywords):
        score += 2

    # Medium importance (treatment + risk)
    if any(word in s for word in treatment_keywords):
        score += 2

    if any(word in s for word in risk_keywords):
        score += 2

    # Medium-low (daily + care + monitoring)
    if any(word in s for word in daily_important_keywords):
        score += 1

    if any(word in s for word in care_keywords):
        score += 1

    if any(word in s for word in monitoring_keywords):
        score += 1

    if "feel" in s or "felt" in s:
        score += 1

    if "help" in s:
        score += 1

    return score


def label_sentence(sentence: str) -> int:
    score = compute_score(sentence)

    return 1 if score >= 1 else 0




data = []

def process_file(file_path):
    print("Processing:", file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        sentences = line.split("__eou__")

        for sentence in sentences:
            sentence = sentence.strip()

            if not sentence:
                continue

            label = label_sentence(sentence)
            data.append((sentence, label))


# Run

process_file(TRAIN_PATH)
process_file(TEST_PATH)

df = pd.DataFrame(data, columns=["sentence", "label"])

print("\nBefore balancing:")
print(df["label"].value_counts())

df_majority = df[df.label == 0]
df_minority = df[df.label == 1]

from sklearn.utils import resample

df_minority_upsampled = resample(
    df_minority,
    replace=True,
    n_samples=len(df_majority),
    random_state=42
)


df_balanced = pd.concat([df_majority, df_minority_upsampled])


df_balanced = df_balanced.sample(frac=1, random_state=42)

print("\nAfter balancing:")
print(df_balanced["label"].value_counts())


df_balanced.to_csv(OUTPUT_PATH, index=False)

#df.to_csv(OUTPUT_PATH, index=False)

print(f"\nSaved dataset with {len(df)} rows to {OUTPUT_PATH}")