# Model Card: Mood Machine

This model card is for the Mood Machine project. I used and compared two versions of the mood classifier:

1. A rule-based model implemented in `mood_analyzer.py`
2. A machine learning model implemented in `ml_experiments.py` using scikit-learn

## 1. Model Overview

**Model type:**
I used both the rule-based model and the machine learning model.

**Intended purpose:**
The Mood Machine is designed to classify short text messages as one of four mood labels:

* positive
* negative
* neutral
* mixed

The purpose of this project is to understand how simple AI systems behave, how data affects predictions, and why language classification can be difficult.

**How it works:**
The rule-based model uses handcrafted logic. It cleans the text, breaks it into tokens, checks for positive and negative words or phrases, calculates a score, and then converts that score into a label.

The machine learning model uses the examples in `SAMPLE_POSTS` and the labels in `TRUE_LABELS` to learn patterns from the dataset. Instead of using rules I directly wrote, it learns from the labeled examples.

## 2. Data

**Dataset description:**
The dataset is stored in `dataset.py`. It contains two connected lists:

* `SAMPLE_POSTS`
* `TRUE_LABELS`

Each post in `SAMPLE_POSTS` has one matching label in `TRUE_LABELS`.

The starter dataset had 6 posts. I added 8 new posts, so the final dataset has 14 posts and 14 labels.

Examples I added include:

* “I passed the test and I feel amazing”
* “That update broke everything again”
* “It's okay I guess”
* “I love the design but the app keeps crashing”
* “Bruh this took forever but it finally works”
* “Yeah great another error message”
* “Not bad at all actually pretty good”
* “I'm exhausted but proud of myself”

**Labeling process:**
I labeled each post manually as positive, negative, neutral, or mixed. I chose labels based on the overall meaning of each sentence, not just one word.

Some examples were easy to label. For example, “I passed the test and I feel amazing” is clearly positive, and “That update broke everything again” is clearly negative.

Some examples were harder to label because they included mixed feelings or sarcasm. For example, “Bruh this took forever but it finally works” includes frustration and relief, so I labeled it mixed.

**Important characteristics of the dataset:**

The dataset includes:

* short social-media-style posts
* positive messages
* negative messages
* neutral messages
* mixed emotions
* slang such as “bruh”
* sarcastic or subtle wording
* phrases that can confuse a simple keyword model

**Possible issues with the dataset:**
The dataset is very small. Because it only has 14 examples, it does not represent all the ways people express mood. The labels also depend on my interpretation. Another person might label some examples differently, especially mixed or sarcastic sentences.

The dataset is also mostly short English text. It may not work well for longer posts, bilingual language, regional slang, cultural references, or different writing styles.

## 3. How the Rule-Based Model Works

**Scoring rules:**
The rule-based model works by giving the text a numeric score.

The basic rules are:

* Positive words add points.
* Negative words subtract points.
* If both positive and negative signals appear, the model may predict mixed.
* Negation can flip the meaning of a word.
* Some phrase-based rules were added to catch context that single words missed.

For example:

* “love” adds a positive point.
* “terrible” subtracts a point.
* “not happy” becomes negative.
* “not bad” becomes positive.
* “another error” counts as a negative phrase.
* “keeps crashing” counts as a negative phrase.
* “proud of myself” counts as a positive phrase.

I added extra vocabulary and phrase rules after testing the model. This helped the model handle examples like “Yeah great another error message,” which was originally misclassified as positive because of the word “great.”

**Strengths of this approach:**
The rule-based model is easy to understand and debug. I can explain exactly why it made a prediction by looking at the words or phrases that changed the score.

It works well on simple sentences with clear emotional words, such as:

* “I love this class so much”
* “Today was a terrible day”
* “So excited for the weekend”

**Weaknesses of this approach:**
The rule-based model is brittle. It only understands the words and phrases I manually added. It does not truly understand sarcasm, context, slang, or subtle tone.

For example, the sentence “Yeah great another error message” can look positive because of the word “great,” but the full sentence is negative or sarcastic. I fixed this specific case by adding phrase rules, but the model could still fail on a new sarcastic sentence.

## 4. How the ML Model Works

**Features used:**
The ML model uses a bag-of-words style representation through scikit-learn. It looks at words in the text and learns patterns from the labeled examples.

**Training data:**
The ML model trained on the same `SAMPLE_POSTS` and `TRUE_LABELS` from `dataset.py`.

**Training behavior:**
After I expanded the dataset, the ML model performed very well on the same examples it trained on. It reached an accuracy of 1.00 on the dataset.

However, this does not mean the model is perfect. Since the dataset is small and the model was evaluated on the same examples it trained on, the result may be overly optimistic. It may not perform as well on new sentences.

**Strengths and weaknesses:**
The ML model can learn patterns automatically instead of needing every rule to be written by hand. It correctly classified all 14 examples in the current dataset.

Its weakness is that it depends heavily on the training data. With only 14 examples, the model may overfit. It may memorize patterns from the dataset instead of learning general rules about mood.

## 5. Evaluation

**How I evaluated the models:**
I evaluated both models using the labeled examples in `dataset.py`.

The rule-based model was run with:

`python main.py`

The ML model was run with:

`python ml_experiments.py`

**Observed accuracy:**

* Rule-based model accuracy: 0.93
* ML model accuracy: 1.00

**Examples of correct rule-based predictions:**

1. “I love this class so much”

   * Predicted: positive
   * True label: positive
   * This was correct because the model detected “love” as a positive word.

2. “Today was a terrible day”

   * Predicted: negative
   * True label: negative
   * This was correct because the model detected “terrible” as a negative word.

3. “Feeling tired but kind of hopeful”

   * Predicted: mixed
   * True label: mixed
   * This was correct because the model detected both negative and positive signals.

4. “Yeah great another error message”

   * Predicted: negative
   * True label: negative
   * This was correct after I added the phrase rule for “another error.”

**Example of an incorrect rule-based prediction:**

“I love the design but the app keeps crashing”

* Predicted: negative
* True label: mixed

The model found the positive word “love,” but it also found strong negative signals like “keeps crashing” and “crashing.” The negative signals were stronger, so the model predicted negative instead of mixed. A human reader would likely understand the sentence as mixed because the person likes the design but is frustrated that the app crashes.

**ML model results:**
The ML model correctly classified all 14 examples in the dataset. However, this result should be interpreted carefully because the dataset is small and the model was tested on the same examples it trained on.

## 6. Limitations

The Mood Machine has several important limitations.

First, the dataset is small. Fourteen examples are not enough to represent real human language.

Second, the rule-based model depends on manually written words and phrases. If a sentence uses a word that is not in the vocabulary, the model may ignore it.

Third, sarcasm is difficult. For example, a sentence like “I love getting stuck in traffic” may be sarcastic, but the model may focus on the word “love” and classify it incorrectly unless I add a specific phrase rule.

Fourth, slang can be confusing. Words like “sick,” “fire,” or “wicked” can be positive or negative depending on context.

Fifth, mixed emotions are difficult. A sentence can include both positive and negative feelings, and the model may let one side dominate the final prediction.

Finally, the ML model may overfit because the dataset is small. Its 1.00 accuracy does not prove that it will work well on new examples.

## 7. Ethical Considerations

Mood detection can be risky if used in real applications. A system like this could misclassify someone’s message and create a false impression about their emotions.

This model should not be used for serious decisions about students, employees, customers, mental health, discipline, hiring, or safety.

The model may also misunderstand certain language communities. People use different slang, dialects, emojis, bilingual phrases, and cultural references. If those styles are not represented in the dataset, the model may classify them incorrectly.

Privacy is also important. Analyzing personal messages can be sensitive, especially if people do not know their messages are being analyzed.

## 8. Ideas for Improvement

Several improvements could make the Mood Machine better:

* Add more labeled examples.
* Create a separate test set instead of evaluating on the training data.
* Add more slang examples.
* Add better emoji handling.
* Improve sarcasm detection.
* Add more phrase-based rules for the rule-based model.
* Use TF-IDF instead of simple word counts.
* Compare performance across different types of sentences.
* Test the model on completely new posts.
* Collect labels from multiple people to reduce personal labeling bias.

## Conclusion

The Mood Machine shows that even a simple mood classifier can become complicated quickly. The rule-based model is easier to explain, but it is brittle and depends on manual rules. The ML model can learn from data, but it depends heavily on the quality and size of the dataset.

The project shows that AI systems are shaped by their data, rules, labels, and assumptions. Even when the accuracy looks good, the results still need to be inspected carefully.
