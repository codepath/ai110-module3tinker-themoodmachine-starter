# Mood Machine Model Card

> Template for reflection and documentation  
> Fill this in after you have implemented and experimented with your MoodAnalyzer.

---

## 1. Model Overview

**Model name:**  
Mood Machine (rule based mood classifier)

**Short description:**  
Describe in 2 to 3 sentences what your system does.  
For example: It predicts whether a short text is positive, negative, or neutral based on simple keyword rules.

**Version or date:**  
Example: Fall 2025 AI110, Module 3 Lab

---

## 2. Intended Use

### Primary intended uses and users

- What is this model supposed to be used for in this lab?
- Who is the user in this context (student, instructor, end user)?

### Out of scope uses

- What should this model not be used for?
- For example: real mental health assessment, high stakes decisions, or serious content moderation.

---

## 3. Data and Rules

### Keyword lists

- Briefly describe your positive and negative word lists.
- How did you choose or change these lists during the lab?

### Example inputs

- What kinds of text did you test on (social posts, class comments, made up examples)?

---

## 4. Evaluation

### How you evaluated the model

- Did you label a small set of posts by hand?
- Did you compare the model output to your own judgment or to an AI tool?

### Results and patterns

- Where did the model work well?
- Where did it fail or behave in a surprising way?

---

## 5. Limitations and Risks

### Technical limitations

- What are the main weaknesses of using simple keyword rules?
- How does it handle:
  - Sarcasm
  - Mixed emotions
  - Slang or emojis
  - Negation (for example, "not happy")

### Social or fairness concerns

- Could some groups or ways of speaking be misclassified more often?
- Does your word list reflect any stereotypes or hidden assumptions?

---

## 6. Example Failures

List 2 to 4 specific examples where the model prediction did not match your own label.

For each example, include:

- The text
- The model prediction
- Your preferred label
- A short explanation of why the model might be wrong

---

## 7. Possible Improvements

If you had more time or more tools, how could you improve the Mood Machine?

You might consider:

- Better word lists
- Handling negation more carefully
- Different weights for particular words
- Using an ML based model instead of simple rules
- Adding an explanation feature that shows which words influenced the decision

---

## 8. Reflection

In 3 to 5 sentences, reflect on:

- What this lab taught you about how simple models work
- How limitations in design and data can affect fairness and accuracy
- How you would communicate these limits to a non technical stakeholder
