# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
import string
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS

# Words that flip the sentiment of the next sentiment word ("not happy").
NEGATION_WORDS = {
    "not", "no", "never", "dont", "don't", "isnt", "isn't", "wasnt", "wasn't",
    "cant", "can't", "wont", "won't", "aint", "ain't",
}

# How many tokens after a negation word can still be flipped.
NEGATION_WINDOW = 3

# Part 3 fix: slang phrases that start with a negation word but don't negate.
# "no cap" means "for real", so "no cap best day ever" must stay positive.
NOT_A_NEGATION = {("no", "cap")}

# Emoticons like ":)" or ":-(" first, then words (with apostrophes),
# then any other single non-space character (this catches emojis).
TOKEN_PATTERN = re.compile(r"[:;]-?[()dp]|[a-z0-9']+|[^\sa-z0-9']")


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂")
          - Normalize repeated characters ("soooo" -> "soo")
        """
        cleaned = text.strip().lower()
        # "soooo" -> "soo", so stretched words still look alike.
        cleaned = re.sub(r"(.)\1{2,}", r"\1\1", cleaned)
        tokens = TOKEN_PATTERN.findall(cleaned)
        # Drop plain punctuation (",", "!") but keep emoticons and emojis.
        return [tok for tok in tokens if tok not in string.punctuation]

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        TODO: You must choose AT LEAST ONE modeling improvement to implement.
        For example:
          - Handle simple negation such as "not happy" or "not bad"
          - Count how many times each word appears instead of just presence
          - Give some words higher weights than others (for example "hate" < "annoyed")
          - Treat emojis or slang (":)", "lol", "💀") as strong signals
        """
        score, _, _ = self._analyze(text)
        return score

    def _analyze(self, text: str) -> Tuple[int, List[str], List[str]]:
        """
        Shared scoring loop for score_text, predict_label, and explain.

        Returns (score, positive_hits, negative_hits). Modeling improvement:
        negation. A negation word flips the next sentiment word within
        NEGATION_WINDOW tokens, so "not happy" counts as negative and
        "not bad" counts as positive. A flipped word is reported in the
        opposite bucket, e.g. "not happy" puts "not happy" in negative_hits.
        """
        score = 0
        positive_hits: List[str] = []
        negative_hits: List[str] = []
        negation_left = 0  # tokens remaining in which a negation still applies

        tokens = self.preprocess(text)
        for i, token in enumerate(tokens):
            next_token = tokens[i + 1] if i + 1 < len(tokens) else None
            if token in NEGATION_WORDS and (token, next_token) not in NOT_A_NEGATION:
                negation_left = NEGATION_WINDOW
                continue

            value = 0
            if token in self.positive_words:
                value = 1
            elif token in self.negative_words:
                value = -1

            label = token
            if value != 0 and negation_left > 0:
                value = -value
                label = f"not {token}"
                negation_left = 0  # a negation only flips one word
            elif negation_left > 0:
                negation_left -= 1

            if value > 0:
                positive_hits.append(label)
            elif value < 0:
                negative_hits.append(label)
            score += value

        return score, positive_hits, negative_hits

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        The default mapping is:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        TODO: You can adjust this mapping if it makes sense for your model.
        For example:
          - Use different thresholds (for example score >= 2 to be "positive")
          - Add a "mixed" label for scores close to zero
        Just remember that whatever labels you return should match the labels
        you use in TRUE_LABELS in dataset.py if you care about accuracy.
        """
        score, positive_hits, negative_hits = self._analyze(text)

        # Both kinds of signal ("tired but hopeful") -> mixed, even if one
        # side outweighs the other.
        if positive_hits and negative_hits:
            return "mixed"
        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        score, positive_hits, negative_hits = self._analyze(text)

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
