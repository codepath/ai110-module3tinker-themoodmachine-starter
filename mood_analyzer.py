# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.
"""

from typing import List, Optional
import re

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A simple rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

        # Extra vocabulary added after testing the dataset.
        self.extra_positive_words = {
            "hopeful",
            "passed",
            "finally",
            "works",
            "proud",
            "pretty",
        }

        self.extra_negative_words = {
            "broke",
            "error",
            "crashing",
            "exhausted",
            "forever",
        }

        # Phrase rules help with context that single-word rules miss.
        self.positive_phrases = {
            "finally works",
            "proud of myself",
            "pretty good",
        }

        self.negative_phrases = {
            "another error",
            "keeps crashing",
            "broke everything",
            "stuck in traffic",
        }

        self.last_positive_hits: List[str] = []
        self.last_negative_hits: List[str] = []
        self.last_score = 0

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into lowercase word tokens.
        """
        cleaned = text.strip().lower()
        tokens = re.findall(r"[a-z']+", cleaned)
        return tokens

    def score_text(self, text: str) -> int:
        """
        Compute a numeric mood score for the given text.

        Positive signals increase the score.
        Negative signals decrease the score.

        Improvements:
        - Negation handling
        - Extra vocabulary
        - Phrase handling for context
        """
        tokens = self.preprocess(text)
        lower_text = text.lower()

        score = 0
        positive_hits: List[str] = []
        negative_hits: List[str] = []

        negation_words = {"not", "no", "never", "dont", "don't", "isnt", "isn't"}

        # Phrase-based scoring first.
        for phrase in self.positive_phrases:
            if phrase in lower_text:
                score += 1
                positive_hits.append(phrase)

        for phrase in self.negative_phrases:
            if phrase in lower_text:
                score -= 2
                negative_hits.append(phrase)

        # Word-based scoring.
        all_positive_words = self.positive_words | self.extra_positive_words
        all_negative_words = self.negative_words | self.extra_negative_words

        for i, token in enumerate(tokens):
            previous_token = tokens[i - 1] if i > 0 else ""
            is_negated = previous_token in negation_words

            if token in all_positive_words:
                if is_negated:
                    score -= 1
                    negative_hits.append(f"{previous_token} {token}")
                else:
                    score += 1
                    positive_hits.append(token)

            elif token in all_negative_words:
                if is_negated:
                    score += 1
                    positive_hits.append(f"{previous_token} {token}")
                else:
                    score -= 1
                    negative_hits.append(token)

        self.last_positive_hits = positive_hits
        self.last_negative_hits = negative_hits
        self.last_score = score

        return score

    def predict_label(self, text: str) -> str:
        """
        Convert the numeric score into a mood label.
        """
        score = self.score_text(text)

        # If both positive and negative signals appear, usually label it mixed.
        # But if the negative score is much stronger, call it negative.
        if self.last_positive_hits and self.last_negative_hits:
            if score <= -2:
                return "negative"
            return "mixed"

        if score > 0:
            return "positive"

        if score < 0:
            return "negative"

        return "neutral"

    def explain(self, text: str) -> str:
        """
        Return a short explanation of the prediction.
        """
        score = self.score_text(text)

        return (
            f"Score = {score} "
            f"(positive: {self.last_positive_hits or '[]'}, "
            f"negative: {self.last_negative_hits or '[]'})"
        )