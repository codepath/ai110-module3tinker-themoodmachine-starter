# Model Card: Mood Machine

This model card covers **both** versions of the Mood Machine mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

## 1. Model Overview

**Model type:**
I compared both models on the same 16 labeled posts, plus 16 extra posts that neither model was built or trained on.

**Intended purpose:**
Classify short, social-media-style posts as `positive`, `negative`, `neutral`, or `mixed`. It is a classroom prototype, not something to use on real people's messages.

**How it works (brief):**
- *Rule based:* `preprocess` lowercases the text, shortens stretched letters ("soooo" → "soo"), and splits it into tokens. Emoticons (`:)`) and emojis (`🔥`) become their own tokens, and plain punctuation is dropped. `score_text` adds +1 for each word in `POSITIVE_WORDS` and −1 for each word in `NEGATIVE_WORDS`. `predict_label` returns `mixed` if the post has both positive and negative hits, otherwise `positive` / `negative` / `neutral` by the sign of the score.
- *ML:* `CountVectorizer` turns each post into word counts (bag of words), and `LogisticRegression` learns from the labels which words go with which mood. It knows nothing about the word lists. It only knows the 16 posts it was trained on.

## 2. Data

**Dataset description:**
16 posts in `SAMPLE_POSTS`: the 6 starter posts plus 10 I added in `dataset.py` (as `NEW_EXAMPLES`, each post stored with its label so the two lists can't drift apart; an `assert` crashes early if they ever do). I also added 8 words to the word lists: `proud`, `hopeful`, `best`, `glad` and `exhausted`, `worst`, `ugh`, `mad`.

**Labeling process:**
I labeled each post by its *intended* mood, not its surface words. That is why the sarcastic "I absolutely love getting stuck in traffic" is labeled `negative`. Posts that were hard to label:
- **"I'm fine 🙂"**: I labeled it `neutral`, but many people read 🙂 as passive-aggressive (`negative`). Reasonable people could disagree.
- **"i aint even mad, it was kinda funny tho"**: `positive`, but it's really "relieved / amused", which the four labels don't capture well.

**Important characteristics of your dataset:**
- Slang: "lowkey/highkey", "fire", "sick", "no cap", "aint"
- Emojis: 🔥, 🙂, 💀
- Sarcasm: "I absolutely love getting stuck in traffic"
- Mixed feelings: "exhausted but proud of myself", "Lowkey stressed but highkey proud of myself"
- Negation: "not bad at all, actually pretty good", "I am not happy about this"

**Possible issues with the dataset:**
- **Tiny:** 16 posts, labeled by one person.
- **Unbalanced:** 7 positive, 4 negative, 3 mixed, only 2 neutral.
- **Narrow language:** all English, and the slang is mostly one generation's internet slang.
- **Missing words:** common negative words like "hate" and "boring" appear in the word lists but in *no* training post, so the ML model never learns them (see Section 5).

## 3. How the Rule Based Model Works

**Your scoring rules:**
- +1 per positive word, −1 per negative word (all words weighted equally).
- **Enhancement: negation handling.** A negation word (`not`, `no`, `never`, `dont`, `aint`, …) flips the *next* sentiment word within 3 tokens. "I am not happy" → `not happy` counts −1. "not bad at all" → `not bad` counts +1.
- **Part 3 fix:** "no cap" (slang for "for real") is *not* treated as a negation. Before the fix, "no cap best day ever" was predicted `negative` (`not best`, score −1). After the fix it is `positive` (`best`, score +1).
- **Labels:** both positive and negative hits → `mixed`. Otherwise the sign of the score decides, and a score of 0 → `neutral`.
- `explain()` shows the score and which words counted, e.g. `Score = 2 (positive: ['not bad', 'good'], negative: [])`.

**Strengths of this approach:**
- Fully predictable and explainable: every decision traces to specific words.
- Handles simple negation the ML model can't reason about: "I'm not upset, it was kind of funny" → `positive`.
- Mixed feelings joined by "but" work well when both words are in the lists: "Feeling tired but kind of hopeful" → `mixed`.

**Weaknesses of this approach:**
- Any word not in the lists is invisible. "that beat is fire" scores 0 → `neutral`.
- Sarcasm is read literally. "I love getting stuck in traffic" → `positive` from `love`.
- No word sense. "sick" can't be both "great" (slang) and "ill / fed up", so I left it out of both lists.
- Negation is crude. Because punctuation is dropped, "no, this is bad" → `positive` (`not bad`): the interjection "no" gets read as negating "bad".

## 4. How the ML Model Works

**Features used:**
Bag of words with scikit-learn's `CountVectorizer` defaults. Those defaults **drop every emoji and every one-letter word** (like "I"). So 🔥, 💀 and 🙂 carry no information for the ML model at all.

**Training data:**
Trained on the 16 posts in `SAMPLE_POSTS` with their `TRUE_LABELS`.

**Training behavior:**
- **Adding data:** I retrained with 4 extra posts ("I love waiting in line for an hour" → negative, "this taco is sick" → positive, "so sick of the rain" → negative, "the vibes were great" → positive). Accuracy on unseen posts went *down* from 0.69 to 0.62. "I'm not upset, it was kind of funny" flipped from `positive` to `negative`. More data didn't help, because a few posts can shift word weights in unexpected ways.
- **Changing one label:** flipping "I'm fine 🙂" from `neutral` to `negative` made the ML model call "I'm fine" and "fine by me 🙂" `negative` too. The rule-based model didn't change at all. **The ML model is far more sensitive to my labels.**

**Strengths and weaknesses:**
- *Strength:* it learned slang from just one example each. "this pizza is sick" and "that beat is fire" → `positive`, because "sick" and "fire" appeared in positive training posts. It also caught the sarcastic "I love getting stuck in traffic" → `negative`.
- *Weakness: overfitting and spurious cues.* "I love my dog" → `negative`, probably because "my" appears in the negative training post "ugh my phone died again 💀". "the building is on fire" → `positive`, because "fire" only ever appeared in a positive post.

## 5. Evaluation

**How you evaluated the model:**
- **On the 16 dataset posts:** rule based **0.81** (13/16). ML **1.00**, but that's training accuracy: the model is graded on the same posts it learned from, so it says little.
- **On 16 unseen posts** (breakers, slang, plain sentences), a fairer test: rule based **0.56** (9/16), ML **0.69** (11/16).

**Examples of correct predictions:**
- "not bad at all, actually pretty good" → rule based `positive`, score +2: negation flips `bad` into +1, plus +1 for `good`.
- "exhausted but proud of myself" → rule based `mixed`: one negative hit (`exhausted`) and one positive hit (`proud`).
- "I love getting stuck in traffic" → ML `negative` (correct). The training set has a near-identical sarcastic post labeled negative.

**Examples of incorrect predictions:**
- "I absolutely love getting stuck in traffic" → rule based `positive`. It only sees `love`; it has no way to detect sarcasm.
- "I hate Mondays" → ML `positive`. "hate" never appears in any training post, so the ML model has no idea it's negative. The rule-based model gets it right from its word list.
- "the building is on fire" → `positive` (ML) and `neutral` (rule based). Both are wrong in different ways. The ML model learned "fire" = positive from slang, and the rule-based model doesn't know "fire" at all.

**How the failures differ:** the rule-based model fails on words it doesn't *know*, and ends up `neutral`. The ML model fails on words it learned the *wrong lesson* about, and is confidently wrong.

## 6. Limitations

- **Tiny dataset, one labeler.** 16 posts and my own judgment of each one's "true" mood.
- **Sarcasm:** the rule-based model can't detect it ("I absolutely love getting stuck in traffic" → `positive`). The ML model only catches sarcasm that closely matches a training post.
- **Vocabulary:** the rule-based model can't score words outside its lists ("that beat is fire" → `neutral`). The ML model can't score words outside its 16 posts ("I hate Mondays" → `positive`).
- **Emojis:** the rule-based model keeps emoji tokens, but none are in the word lists, so "I'm dead 💀 this is hilarious" → `neutral`. The ML model drops emojis completely.
- **Crude negation:** "no, this is bad" → `positive`.
- **No real test set:** the 1.00 ML score is training accuracy only.

## 7. Ethical Considerations

**Overt bias (from Part 3):** I wrote 6 pairs of posts with the same meaning, one in standard English and one in informal / AAVE-style phrasing. The rule-based model got **5 of 6** standard posts right and **0 of 6** informal ones. Every informal post was scored `neutral`, for example:
- "That song is really good" → `positive`, but "that song go hard fr" → `neutral`
- "This outfit looks great" → `positive`, but "this fit is bussin" → `neutral`
- "I'm annoyed with my roommate" → `neutral` (wrong: "annoyed" isn't in the list either), and "my roommate be getting on my nerves" → `neutral`

The errors cluster around *who wrote the post*, not what it means. That's a systematic bias: people who write in AAVE or heavy slang would have their feelings missed far more often. The word lists reflect the vocabulary of whoever wrote them, which here is me. The "no cap" bug shows the same thing from another angle: my negation rule *added* an error that only hit slang speakers until I fixed it.

**Covert compliance:** <!-- TODO: check and rewrite this in your own words -->
I used Claude Code (an AI agent) to build this. When it expanded the word lists in Part 1, it didn't flag that they only cover standard English. It added words like `proud` and `ugh` and moved on. The coverage gap only showed up because the Part 3 instructions told us to look for bias, and the agent then ran the paired-phrasing check. It should have pointed out the gap when it first chose the words, without being told. It did point out the "no cap" negation bug and the "no, this is bad" limitation on its own. Lesson: an AI assistant can look helpful while quietly building in a blind spot, so I have to ask about bias explicitly.

**Other risks:**
- **Distress missed:** "I'm fine 🙂" is scored `neutral`, which could hide that someone is not fine.
- **Privacy:** running this on people's personal messages without consent would be a problem, especially given how often it's wrong.

## 8. Ideas for Improvement

- Add many more labeled posts, from more than one person and more than one dialect, and keep a separate test set the model never trains on.
- Add slang and AAVE expressions to the word lists, *and* to the ML training data. Have speakers of those dialects check the labels.
- Keep emojis in the ML model: give `CountVectorizer` a `token_pattern` (or a custom tokenizer) that keeps them.
- Handle negation scope better: stop a negation at punctuation, so "no, this is bad" stays negative.
- Weight words (`hate` stronger than `annoyed`) and handle intensifiers ("so", "really").
- Try TF-IDF or a small pretrained model, which would already know words like "hate" without needing them in 16 posts.
