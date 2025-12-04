"""
Runner script for The Mood Machine lab.
"""

from dataset import SAMPLE_POSTS
from mood_analyzer import MoodAnalyzer


def run_batch_demo() -> None:
    """
    Run the MoodAnalyzer on all posts in SAMPLE_POSTS
    and print the predicted labels.
    """
    analyzer = MoodAnalyzer()

    print("=== Mood Machine: Batch Demo ===")
    for post in SAMPLE_POSTS:
        try:
            label = analyzer.predict_label(post)
        except NotImplementedError as e:
            print("\nMoodAnalyzer is not fully implemented yet.")
            print(e)
            print("\nOpen mood_analyzer.py and complete the TODO sections.")
            return

        print(f'"{post}"  ->  {label}')
    print()  # blank line


def run_interactive_loop() -> None:
    """
    Type 'quit' to exit.
    """
    analyzer = MoodAnalyzer()
    print("=== Mood Machine: Interactive Mode ===")
    print("Type a sentence and I will guess the mood.")
    print("Type 'quit' to exit.\n")

    while True:
        user_text = input("Your text: ").strip()
        if user_text.lower() in {"quit", "exit"}:
            print("Goodbye from the Mood Machine.")
            break

        try:
            label = analyzer.predict_label(user_text)
        except NotImplementedError as e:
            print("\nMoodAnalyzer is not fully implemented yet.")
            print(e)
            print("\nOpen mood_analyzer.py and complete the TODO sections.")
            break

        print(f"Predicted mood: {label}\n")


if __name__ == "__main__":
    run_batch_demo()
    run_interactive_loop()
