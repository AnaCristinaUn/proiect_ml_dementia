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

duration_phrases = [
    "for a few minutes",
    "for an hour",
    "for two hours",
    "for a while",
    "for a short time",
]

health_templates = [
    "I had severe {symptom} and needed medical attention {time}",
    "I forgot my {item} and my condition got worse {time}",
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
    "I used my {device} to get to the kitchen {time}",
    "{caregiver} helped me with my {task} {time}",
    "I felt some {symptom} so I rested {time}",
    "I applied the {item} to my skin {time}",
    "I practiced my {task} with the {professional} {time}",
    "I brushed my teeth and did my hygiene routine {time}",
    "I took a shower with help from {caregiver} {time}",
    "I updated {caregiver} about my {symptom} {time}",
    "I organized my {item} into the weekly pill box {time}",
    "I checked my calendar for the next {professional} visit {time}",
    "I set up my {device} to remind me about the {task} {time}",
    "I made sure to get some exercise as part of my {task} {time}",
    "I followed the doctor's advice and took my {item} {time}",
    "I felt {symptom} so I called the {professional} for advice {time}",
    "I asked {caregiver} to help me with my {task} {time}",
    "I used my {device} to call for help when I felt {symptom} {time}",
    "I made a healthy meal as part of my diet plan {time}",
    "I took a walk outside to get some fresh air {time}",
    "I practiced my rehab exercises in the living room {time}",
    "I checked my {device} to see how many steps I took today {time}",
    "I made sure to get enough sleep last night {time}",
    "I took my {item} with a glass of water {time}",
    "I followed my therapy routine with the help of {caregiver} {time}",
    "I felt {symptom} so I took a break and rested {time}",
    "I used my {device} to listen to music while I rested {time}",
    "I updated my health journal with my symptoms and how I felt {time}",
    "I made a list of questions to ask the {professional} at my next appointment {time}",
    "I took my {item} and then went for a walk {time}",
    "I practiced my {task} with the {professional} and felt better afterward {time}",
    "I set up my {device} to track my sleep and health data {time}",
    "I asked {caregiver} to remind me about my {task} and they were very helpful {time}",
    "I forgot to take my {item} and felt worse {time}",
    "I experienced {symptom} and needed help {time}",
    "I felt {symptom} so I took my {item} immediately {time}",
    "I missed my {task} and started to feel {symptom} {time}",
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
    "I sat on the porch and watched the birds {time}",
    "I folded the laundry while listening to the radio {time}",
    "I looked through old photo albums {duration}",
    "I swept the living room floor {time}",
    "I watched the news on the television {duration}",
    "I sat by the window and watched the rain {duration}",
    "I chatted with the neighbor over the fence {time}",
    "I dusted the bookshelves {time}",
    "I spent some time doing a crossword puzzle {time}",
    "I spent {duration} {activity} with {friend} {time}",
    "I invited {friend} over for some {hobby} {time}",
    "I talked to {friend} about {hobby} {duration}",
    "I really enjoyed {hobby} {time}",
    "I went to the park for some {hobby} {duration}",
    "I focused on {chore} {time}",
    "I spent {duration} {chore} today",
    "I noticed the {item} was dusty while I was {activity} {time}",
    "I misplaced the {item} while I was {chore} {time}",
    "I put the {item} back where it belongs {time}",
    "I used the {electronic} for {activity} {duration}",
    "I spent {duration} on my {electronic} {time}",
    "I was using the {electronic} to look up more about {hobby} {time}",
    "I checked the {electronic} for messages {time}",
    "I felt like {hobby} would be a nice way to spend the {time}",
    "I helped {friend} with {chore} {duration}",
    "I practiced {hobby} {duration} {time}",
]

# Word lists used to fill placeholders in the templates.
health_items = [
    "medicine", "medicine", "medicine", "medicine", "medication", "medication", "medication", "medication",
    "therapy", "therapy", "drug", "drug",
    "pills", "pills", "supplement", "supplement", "vitamin", "vitamin", "inhaler", "ointment", "cream", "bandage", "cast", "brace", "splint", "heating pad", "ice pack", "compression wrap", "antibiotic", "pain reliever", "allergy medication", "sleep aid", "cough syrup", "nasal spray", "eye drops", "ear drops", "topical gel"
]

health_professionals = [
    "doctor", "dentist", "pharmacist", "therapist", "nurse", "specialist", "physiotherapist", "caregiver", "social worker", "optometrist", "podiatrist", "audiologist", "dietitian", "occupational therapist", "home health aide", "personal trainer", "chiropractor", "massage therapist", "counselor", "psychiatrist", "neurologist", "geriatrician", "cardiologist", "endocrinologist", "rheumatologist", "urologist", "gastroenterologist", "pulmonologist", "oncologist", "dermatologist", "ophthalmologist", "aesthetician", "acupuncturist", "naturopath", "herbalist", "midwife", "doula", "hospice worker", "palliative care specialist", "respite care provider", "home care nurse"
]

health_places = [
    "clinic", "pharmacy", "hospital", "health center", "care facility", "doctor's office", "dentist's office", "therapist's office", "nurse's station", "specialist's office", "physiotherapy center", "rehab center", "home health agency", "assisted living facility", "nursing home", "urgent care center", "community health clinic", "outpatient center", "diagnostic lab", "imaging center", "surgery center", "long-term care facility", "memory care unit", "adult day care center", "hospice center", "palliative care unit", "respite care facility"
]

health_devices = ["watch", "medical bracelet", "hearing aid", "fitness tracker", "walker", "cane", "wheelchair", "oxygen tank", "CPAP machine", "blood sugar monitor", "heart rate monitor", "pill organizer", "medication reminder device", "fall detection device", "emergency alert system", "smart home health device", "telehealth equipment", "assistive communication device", "mobility scooter", "prosthetic limb", "orthotic brace", "home blood pressure monitor", "glucometer", "pulse oximeter", "thermometer", "smart scale"]

health_tasks = ["medication", "appointment", "therapy", "exercise", "diet plan", "rehab exercises", "blood test", "insulin shot", "physio session", "weight check", "health monitoring", "symptom tracking", "hygiene routine", "mobility practice", "cognitive exercises", "social engagement", "mental health check-in", "hydration reminder", "sleep routine", "fall prevention measures", "emergency preparedness plan"]

symptoms = ["dizziness", "fatigue", "headache", "nausea", "shortness of breath", "chest pain", "joint pain", "swelling", "rash", "fever", "cough", "sore throat", "confusion", "memory loss", "mood changes"]

caregivers = ["my daughter", "my son", "my spouse", "my friend", "my neighbor", "my caregiver", "my assistant", "my family member", "my aide", "my helper", "my support person", "my companion"]

hobbies = ["painting", "gardening", "cooking", "knitting", "playing music", "writing", "photography", "bird watching", "hiking", "fishing", "collecting stamps", "playing board games", "doing puzzles", "volunteering", "traveling", "dancing", "yoga", "meditation"]

household_items = ["TV", "phone", "laptop", "radio", "newspaper", "magazine", "book", "remote control", "kitchen appliances", "furniture", "decorations", "tools", "cleaning supplies"]

friends = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"]

activities = ["watching a movie", "going for a walk", "cooking dinner", "playing a game", "reading a book", "listening to music", "doing a puzzle", "gardening", "knitting", "painting"]

electronics = ["TV", "phone", "laptop", "radio", "tablet", "smartwatch", "gaming console", "e-reader", "headphones", "speaker"]

chores = ["cleaning the kitchen", "folding laundry", "sweeping the floor", "dusting the shelves", "washing dishes", "taking out the trash", "organizing the closet", "watering the plants", "vacuuming the living room", "mopping the floor"]

# Generate a dataset with at least `target_count` unique rows.
# We add the seed examples first, then generate more until we hit the target.
# `seen` tracks which (sentence, label) pairs have already been added.
target_count = 50000

seen = set()
unique_examples = []

for sentence, label in seed_examples:
    key = (sentence.strip().lower(), label)
    if key not in seen:
        seen.add(key)
        unique_examples.append((sentence, label))

# Try to generate enough unique examples; If we make too many attempts without
# increasing the dataset size, we stop to avoid an infinite loop
max_attempts = target_count * 50
attempts = 0

# Keep the dataset balanced by generating (roughly) the same number of examples per class.
target_per_class = target_count // 2
count_0 = 0
count_1 = 0

while len(unique_examples) < target_count and attempts < max_attempts:
    attempts += 1

    # Choose the next label so we end up with roughly balanced classes.
    if count_1 < target_per_class:
        label = 1
    elif count_0 < target_per_class:
        label = 0
    else:
        # We've filled both classes to the desired size.
        break

    if label == 1:
        # For health/self-care examples, fill a template with random words.
        template = random.choice(health_templates)
        time = random.choice(time_phrases)
        sentence = template.format(
            item=random.choice(health_items),
            professional=random.choice(health_professionals),
            place=random.choice(health_places),
            device=random.choice(health_devices),
            task=random.choice(health_tasks),
            time=time,
            caregiver=random.choice(caregivers),
            symptom=random.choice(symptoms),
        )
    else:
        template = random.choice(other_templates)
        if random.random() < 0.5:
            time = random.choice(time_phrases)
        else:
            time = ""
        sentence = template.format(
            time=time,
            duration=random.choice(duration_phrases),
            hobby=random.choice(hobbies),
            item=random.choice(household_items),
            friend=random.choice(friends),
            activity=random.choice(activities),
            electronic=random.choice(electronics),
            chore=random.choice(chores),
        )

    key = (sentence.strip().lower(), label)
    if key not in seen:
        seen.add(key)
        unique_examples.append((sentence, label))
        if label == 1:
            count_1 += 1
        else:
            count_0 += 1

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
