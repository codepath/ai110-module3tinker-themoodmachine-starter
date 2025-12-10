# ml_experiments.py
"""
Simple ML experiments for the Mood Machine lab.

This file uses a "real" machine learning library (scikit-learn)
to train a tiny text classifier on the same SAMPLE_POSTS and
TRUE_LABELS that you use with the rule based model.

You will:
  - Add more labeled examples in dataset.py
  - Run this script to train a model on your labels
  - See how well the model fits your data
  - Compare its behavior to the rule based MoodAnalyzer

Right now, this script only evaluates on the training data.
That is fine for this lab, but in the real world you would
want to test on separate data that the model has not seen.
"""

from typing import List, Tuple

from sklearn.feature_extraction.text import CountVectorizer  # or TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from dataset import SAMPLE_POSTS, TRUE_LABELS


def train_ml_model(
    texts: List[str],
    labels: List[str],
) -> Tuple[CountVectorizer, LogisticRegression]:
    """
    Train a simple text classifier using bag of words features
    and logistic regression.

    Steps:
      1. Convert the texts into numeric vectors using CountVectorizer.
      2. Fit a LogisticRegression model on those vectors and labels.

    Returns:
      (vectorizer, model)
    """
    if len(texts) != len(labels):
        raise ValueError(
            "texts and labels must be the same length. "
            "Check SAMPLE_POSTS and TRUE_LABELS in dataset.py."
        )

    if not texts:
        raise ValueError("No training data provided. Add examples in dataset.py.")

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression(max_iter=1000)
    model.fit(X, labels)

    return vectorizer, model


def evaluate_on_dataset(
    texts: List[str],
    labels: List[str],
    vectorizer: CountVectorizer,
    model: LogisticRegression,
) -> float:
    """
    Evaluate the trained model on a labeled dataset.

    Prints each text with its predicted label and the true label,
    then returns the overall accuracy as a float between 0 and 1.

    In this starter, we evaluate on the same data used for training.
    That helps you see how well the model fits your dataset, but in
    practice you would want to use separate test data.
    """
    if len(texts) != len(labels):
        raise ValueError(
            "texts and labels must be the same length. "
            "Check your dataset."
        )

    X = vectorizer.transform(texts)
    preds = model.predict(X)

    print("=== ML Model Evaluation on Dataset ===")
    correct = 0
    for text, true_label, pred_label in zip(texts, labels, preds):
        is_correct = pred_label == true_label
        if is_correct:
            correct += 1
        print(f'"{text}" -> predicted={pred_label}, true={true_label}')

    accuracy = accuracy_score(labels, preds)
    print(f"\nAccuracy on this dataset: {accuracy:.2f}")
    return accuracy


def predict_single_text(
    text: str,
    vectorizer: CountVectorizer,
    model: LogisticRegression,
) -> str:
    """
    Predict the mood label for a single text string using
    the trained ML model.
    """
    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    return pred


def run_interactive_loop(
    vectorizer: CountVectorizer,
    model: LogisticRegression,
) -> None:
    """
    Let the user type their own sentences and see the ML model's
    predicted mood label.

    Type 'quit' or press Enter on an empty line to exit.
    """
    print("\n=== Interactive Mood Machine (ML model) ===")
    print("Type a sentence to analyze its mood.")
    print("Type 'quit' or press Enter on an empty line to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input == "" or user_input.lower() == "quit":
            print("Goodbye from the ML Mood Machine.")
            break

        label = predict_single_text(user_input, vectorizer, model)
        print(f"ML model: {label}")


if __name__ == "__main__":
    print("Training an ML model on SAMPLE_POSTS and TRUE_LABELS from dataset.py...")
    print("Make sure you have added enough labeled examples before running this.\n")

    # Train the model on the current dataset.
    vectorizer, model = train_ml_model(SAMPLE_POSTS, TRUE_LABELS)

    # Evaluate on the same dataset (training accuracy).
    evaluate_on_dataset(SAMPLE_POSTS, TRUE_LABELS, vectorizer, model)

    # Let the user try their own examples.
    run_interactive_loop(vectorizer, model)

    print("\nTip: Compare these predictions with the rule based model")
    print("by running `python main.py`. Notice where they fail in")
    print("similar ways and where they fail in different ways.")
