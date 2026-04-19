import pandas as pd
from pathlib import Path
import time
from openai import OpenAI

# ===================== CONFIG =====================

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "data" / "dailydialog_dataset.csv"
OUTPUT_PATH = BASE_DIR / "data" / "dailydialog_llm_labeled.csv"

MAX_SAMPLES = 1000   # IMPORTANT: limit cost

client = OpenAI()  # requires OPENAI_API_KEY in env


# ===================== LLM LABEL FUNCTION =====================

def label_with_llm(sentence: str) -> int:
    prompt = f"""
You are labeling sentences for a machine learning dataset used in a dementia support system.

Goal:
Detect whether a sentence contains IMPORTANT information that should be tracked to help monitor a person's daily health, safety, memory, or essential activities.

A sentence is IMPORTANT (YES) if it includes ANY of the following:
- Health-related actions (medicine, doctor visits, treatment)
- Symptoms or physical/mental condition (pain, dizziness, confusion, feeling unwell)
- Memory issues (forgetting, missing things, confusion)
- Safety risks (falling, injury, emergency, needing help)
- Essential daily responsibilities (appointments, schedules, reminders)
- Monitoring health (blood pressure, glucose, vital signs)
- Assistance from others (caregiver help, needing support)

A sentence is NOT IMPORTANT (NO) if it is:
- Casual conversation (greetings, small talk)
- Entertainment or hobbies (TV, music, games)
- General opinions or vague statements without health/safety relevance
- Neutral daily actions without risk or importance (e.g., "I went for a walk")

Be strict: only label YES if the sentence clearly contributes to tracking health, safety, or critical daily functioning.

Examples:
"I took my medicine this morning" → YES
"I feel dizzy and weak today" → YES
"I forgot my appointment again" → YES
"I fell in the kitchen" → YES
"My daughter helped me take my pills" → YES

"I watched TV last night" → NO
"I like this song" → NO
"I went outside for a walk" → NO
"Hello, how are you?" → NO

Now classify:

Sentence: "{sentence}"

Answer ONLY with YES or NO.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        answer = response.choices[0].message.content.strip().upper()

        return 1 if "YES" in answer else 0

    except Exception as e:
        print("Error:", e)
        return 0  # fallback


# ===================== MAIN =====================

def main():
    print("Loading dataset...")
    df = pd.read_csv(INPUT_PATH)

    print(f"Original size: {len(df)}")

    # take subset to avoid cost
    df_subset = df.sample(n=MAX_SAMPLES, random_state=42).copy()

    print(f"Labeling {len(df_subset)} samples with LLM...")

    llm_labels = []

    for i, sentence in enumerate(df_subset["sentence"]):
        print(f"[{i+1}/{len(df_subset)}]")

        label = label_with_llm(sentence)
        llm_labels.append(label)

        time.sleep(0.5)  # avoid rate limits

    df_subset["llm_label"] = llm_labels

    df_subset.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved LLM-labeled dataset to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()