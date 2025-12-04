"""
Defines the MoodAnalyzer class for The Mood Machine lab.

This is a simple rule based "model" that:
- Looks for positive and negative words in text
- Computes a score
- Returns a label: "positive", "negative", or "neutral"
"""

from typing import List
from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    def __init__(
        self,
        positive_words: List[str] | None = None,
        negative_words: List[str] | None = None,
    ) -> None:
        """
        Initialize a MoodAnalyzer with lists of positive and negative words.
        """
        self.positive_words = positive_words or POSITIVE_WORDS
        self.negative_words = negative_words or NEGATIVE_WORDS

    def preprocess(self, text: str) -> str:
        """
        TODO: Implement basic preprocessing for the input text.

        Suggestions:
        - Convert the text to lowercase
        - Optionally strip leading and trailing spaces

        For now this method just returns the text unchanged.
        Replace this with your own implementation.
        """
        # TODO: replace this line with a real implementation
        return text

    def score_text(self, text: str) -> int:
        """
        TODO: Compute a numeric "mood score" for the given text.

        Ideas:
        - Start from score = 0
        - For each positive word found, increase the score
        - For each negative word found, decrease the score

        You can use "word in text" checks or more advanced logic later.
        """
        # TODO: remove the placeholder implementation below
        # and replace it with your own logic.
        raise NotImplementedError(
            "score_text is not implemented yet. "
            "Open mood_analyzer.py and complete this method."
        )

    def predict_label(self, text: str) -> str:
        """
        TODO: Use the score from score_text to return a label.

        Simple rules you can start with:
        - If score > 0  -> "positive"
        - If score < 0  -> "negative"
        - If score == 0 -> "neutral"
        """
        # TODO: remove the placeholder implementation below
        # and replace it with your own logic.
        raise NotImplementedError(
            "predict_label is not implemented yet. "
            "Open mood_analyzer.py and complete this method."
        )

    def explain(self, text: str) -> str:
        """
        Optional extension

        TODO (optional):
        - Return a short string that explains why the model chose a label
        - For example, list which words were counted as positive or negative

        This method is not required for the lab, but it can support reflection
        and the model card.
        """
        # You can leave this unimplemented for the main lab.
        return "Explanation not implemented yet."
