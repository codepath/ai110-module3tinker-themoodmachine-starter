# The Mood Machine  

The Mood Machine is a simple rule based text classifier. It tries to guess whether a short piece of text sounds **positive**, **negative**, or **neutral** based on lists of keywords. This lab gives you a hands on look at how basic systems work, where they break, and why even simple choices can create bias.

You will edit the code, run experiments, add data, and create a short model card reflection.

---

## Repo Structure

```plaintext
├── dataset.py        # Starter word lists and example posts
├── mood_analyzer.py  # Core class with TODOs for you to implement
├── main.py           # Runner script for demos and interactive testing
└── model_card.md     # Template you will fill out after experimenting
```

---

## Getting Started

1. Open this folder in VS Code.
2. Make sure your Python environment is set up.
3. Run the starter script:

    ```bash
    python main.py
    ```

If parts of the analyzer are not implemented yet, you will see helpful error messages that point you to the TODOs.

---

## What You Will Do

During this lab you will:

- Implement the missing methods inside `MoodAnalyzer`.
- Add new positive and negative words.
- Expand the dataset with more example posts, including slang or emojis.
- Observe unusual or incorrect predictions.
- Compare your system to an AI tool such as ChatGPT.
- Fill out the model card template with your findings.

This activity helps you reason about how models behave, why they fail, and how design decisions influence fairness and accuracy.

---

## Tips

- Start small. Get `preprocess` working before moving on to scoring.
- When debugging, print intermediate results to see what your code is doing.
- Ask an AI assistant to generate example posts, alternative keyword lists, or explanations of unfamiliar Python ideas.
- Try examples that break your system. Surprising cases teach you the most.
