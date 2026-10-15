"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    # Added in Part 1:
    "proud",
    "hopeful",
    "best",
    "glad",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    # Added in Part 1:
    "exhausted",
    "worst",
    "ugh",
    "mad",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
]

# ---------------------------------------------------------------------
# Added posts (Part 1): slang, emojis, sarcasm, mixed feelings, negation
# ---------------------------------------------------------------------
# Each post is added together with its label so the two lists stay aligned.
NEW_EXAMPLES = [
    ("Lowkey stressed but highkey proud of myself", "mixed"),
    ("I absolutely love getting stuck in traffic", "negative"),  # sarcasm
    ("this new album is fire 🔥", "positive"),                    # slang + emoji
    ("that game last night was sick", "positive"),               # slang: "sick" = great
    ("I'm fine 🙂", "neutral"),                                   # ambiguous: could be passive-aggressive
    ("exhausted but proud of myself", "mixed"),
    ("not bad at all, actually pretty good", "positive"),        # negation
    ("ugh my phone died again 💀", "negative"),
    ("no cap this is the best day ever", "positive"),            # slang
    ("i aint even mad, it was kinda funny tho", "positive"),     # informal spelling + negation
]

for post, label in NEW_EXAMPLES:
    SAMPLE_POSTS.append(post)
    TRUE_LABELS.append(label)

# Guard: crash early with a clear message if the lists ever drift apart.
assert len(SAMPLE_POSTS) == len(TRUE_LABELS), (
    f"SAMPLE_POSTS has {len(SAMPLE_POSTS)} posts but TRUE_LABELS has "
    f"{len(TRUE_LABELS)} labels"
)

# Hard-to-label notes:
#   - "I'm fine 🙂" could be read as calm (neutral) or passive-aggressive
#     (negative). I labeled it neutral; a friend might not.
#   - "I absolutely love getting stuck in traffic" is sarcastic, so its true
#     label is negative even though "love" is a positive word.
