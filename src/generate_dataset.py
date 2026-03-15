"""
The dataset is a CSV with two columns: sentence,label
- label 1: activity related to health/self-care (e.g., medication, appointments)
- label 0: other everyday activities (e.g., hobbies, leisure)

This script is deterministic (seeded) so it produces the same output every run (based on given seed).
"""

from __future__ import annotations  # enable modern type annotations for better readability

import random  # for deterministic randomness (seeded generation)
from pathlib import Path 

# Find the repository root and point to the dataset file.
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "dataset.csv"

#Change this to generate a different dataset
SEED = 42
random.seed(SEED)

# Seed examples
# These original sentences are always included in the output.
seed_examples = [
    ("I took my medicine in the morning", 1),
    ("I went to the pharmacy", 1),
    ("I had lunch with my daughter", 1),
    ("I visited the doctor", 1),
    ("I paid my bills online", 1),
    ("I watched television for two hours", 0),
    ("I slept in the afternoon", 0),
    ("I scrolled on my phone", 0),
    ("I played a video game", 0),
    ("I read a magazine", 0),
]

# Templates for generating more examples.
# We include optional time/duration phrases to create more unique sentences.
time_phrases = [
    "in the morning",
    "in the afternoon",
    "in the evening",
    "before bed",
    "after breakfast",
    "after dinner",
    "during the day",
    "at night",
]

# Optional duration phrases to vary the wording further.
duration_phrases = [
    "for a few minutes",
    "for an hour",
    "for two hours",
    "for a while",
    "for a short time",
]

health_templates = [
    "I set a reminder to take my {item} {time}",
    "I scheduled an appointment with the {professional} {time}",
    "I checked the expiry date on my {item} {time}",
    "I called the {professional} to confirm my visit {time}",
    "I went to the {place} for a checkup {time}",
    "I made sure to drink enough water today {time}",
    "I measured my blood pressure in the {place} {time}",
    "I asked my family to remind me about the {task} {time}",
    "I wore my {device} as the doctor advised {time}",
    "I recorded my symptoms in a notebook {time}",
    "I followed my {task} plan {time}",
    "I reviewed my medication list {time}",
    "I checked my calendar for the next {professional} visit {time}",
]

other_templates = [
    "I cooked dinner for myself {time}",
    "I walked in the park for a bit {time}",
    "I listened to music while resting {time}",
    "I called a friend to chat {time}",
    "I painted a picture for fun {time}",
    "I practiced a few chords on the guitar {time}",
    "I organized my closet {time}",
    "I watered the plants {time}",
    "I watched a movie on my laptop {time}",
    "I went for a drive around the neighborhood {time}",
    "I read a book {time}",
    "I cleaned the kitchen {time}",
    "I did a puzzle {time}",
    "I took a nap {time}",
    "I baked a cake {time}",
    "I played a board game {time}",
]

# Word lists used to fill placeholders in the templates.
# These help create a variety of health-related sentences.
health_items = [
    "pills", "medicine", "supplements", "vitamins", "inhaler", "eye drops"
]

health_professionals = [
    "doctor", "dentist", "pharmacist", "therapist", "nurse", "specialist"
]

health_places = [
    "clinic", "pharmacy", "hospital", "health center", "care facility"
]

health_devices = ["watch", "medical bracelet", "hearing aid", "fitness tracker"]

health_tasks = ["medication", "appointment", "therapy", "exercise", "diet plan"]

# Generate a dataset with at least `target_count` unique rows.
# We add the seed examples first, then generate more until we hit the target.
# `seen` tracks which (sentence, label) pairs have already been added.
target_count = 500

seen = set()
unique_examples = []

for sentence, label in seed_examples:
    key = (sentence.strip().lower(), label)
    if key not in seen:
        seen.add(key)
        unique_examples.append((sentence, label))

# Try to generate enough unique examples. If we make too many attempts without
# increasing the dataset size, we stop to avoid an infinite loop.
max_attempts = target_count * 50
attempts = 0

while len(unique_examples) < target_count and attempts < max_attempts:
    attempts += 1
    # Randomly choose a class label (0 or 1).
    label = random.choice([0, 1])

    if label == 1:
        # For health/self-care examples, fill a template with random words.
        template = random.choice(health_templates)
        sentence = template.format(
            item=random.choice(health_items),
            professional=random.choice(health_professionals),
            place=random.choice(health_places),
            device=random.choice(health_devices),
            task=random.choice(health_tasks),
            time=random.choice(time_phrases),
        )
    else:
        # For non-health examples, use a different set of templates.
        template = random.choice(other_templates)
        sentence = template.format(time=random.choice(time_phrases))

    key = (sentence.strip().lower(), label)
    if key not in seen:
        seen.add(key)
        unique_examples.append((sentence, label))

if len(unique_examples) < target_count:
    # Print a warning if we could not build enough unique rows.
    print(
        "Warning: could not generate enough unique examples; "
        f"generated {len(unique_examples)} unique rows after {attempts} attempts."
    )

# Write the final dataset out to `data/dataset.csv`.
with open(DATA_PATH, "w", encoding="utf-8") as f:
    f.write("sentence,label\n")
    for sentence, label in unique_examples:
        f.write(f"{sentence},{label}\n")

print(f"Wrote {len(unique_examples)} rows to {DATA_PATH}")
