# main.py
"""
Entry point for the Mood Machine rule based mood analyzer.

You will:
  - Run the rule based model on a small labeled dataset.
  - See its accuracy and some example predictions.
  - Try out your own sentences in an interactive loop.

Later, you will compare this behavior with the ML based version
in ml_experiments.py, which trains a model using scikit learn.
"""

from typing import List

from mood_analyzer import MoodAnalyzer
from dataset import SAMPLE_POSTS, TRUE_LABELS


def evaluate_rule_based(posts: List[str], labels: List[str]) -> float:
    """
    Evaluate the rule based MoodAnalyzer on a labeled dataset.

    Prints each text with its predicted label and the true label,
    then returns the overall accuracy as a float between 0 and 1.
    """
    analyzer = MoodAnalyzer()
    correct = 0
    total = len(posts)

    print("=== Rule Based Evaluation on SAMPLE_POSTS ===")
    for text, true_label in zip(posts, labels):
        predicted_label = analyzer.predict_label(text)
        is_correct = predicted_label == true_label
        if is_correct:
            correct += 1

        # If you implement explain(), you can uncomment these lines:
        # reason = analyzer.explain(text)
        # print(f'"{text}" -> predicted={predicted_label}, true={true_label} ({reason})')

        print(f'"{text}" -> predicted={predicted_label}, true={true_label}')

    if total == 0:
        print("\nNo labeled examples to evaluate.")
        return 0.0

    accuracy = correct / total
    print(f"\nRule based accuracy on SAMPLE_POSTS: {accuracy:.2f}")
    return accuracy


def run_batch_demo() -> None:
    """
    Run the MoodAnalyzer on the sample posts and print predictions only.

    This is a quick way to see how your rules behave without comparing
    to the true labels.
    """
    analyzer = MoodAnalyzer()
    print("\n=== Batch Demo on SAMPLE_POSTS (rule based) ===")
    for text in SAMPLE_POSTS:
        label = analyzer.predict_label(text)
        # If explain() is implemented, show a short explanation.
        # reason = analyzer.explain(text)
        # print(f'"{text}" -> {label} ({reason})')
        print(f'"{text}" -> {label}')


def run_interactive_loop() -> None:
    """
    Let the user type their own sentences and see the predicted mood.

    Type 'quit' or press Enter on an empty line to exit.
    """
    analyzer = MoodAnalyzer()
    print("\n=== Interactive Mood Machine (rule based) ===")
    print("Type a sentence to analyze its mood.")
    print("Type 'quit' or press Enter on an empty line to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input == "" or user_input.lower() == "quit":
            print("Goodbye from the Mood Machine.")
            break

        label = analyzer.predict_label(user_input)
        # If explain() is implemented, you can include an explanation:
        # reason = analyzer.explain(user_input)
        # print(f"Model: {label} ({reason})")
        print(f"Model: {label}")


if __name__ == "__main__":
    # First, evaluate the rule based model on the labeled examples.
    evaluate_rule_based(SAMPLE_POSTS, TRUE_LABELS)

    # Then show a quick batch demo of predictions.
    run_batch_demo()

    # Finally, let the student play with their own inputs.
    run_interactive_loop()

    print("\nTip: After you explore the rule based model here,")
    print("run `python ml_experiments.py` to try a simple ML based model")
    print("trained on the same SAMPLE_POSTS and TRUE_LABELS.")
