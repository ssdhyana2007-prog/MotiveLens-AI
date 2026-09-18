# 🔍 MotiveLens

### See Beyond the Click

**MotiveLens** is an explainable user-side recommendation auditing prototype designed to explore an important gap in modern recommendation systems:

> **Attention ≠ Interest ≠ Intent ≠ Need**

Recommendation systems can observe what users view, like, skip, or repeatedly engage with. However, engagement alone may not explain *why* the user interacted with that content.

MotiveLens makes this distinction visible.

---

## 💡 Problem

Modern recommendation systems are highly effective at learning what captures a user's attention.

But the same interaction can represent very different motives.

For example, a user may repeatedly watch BMW videos because they:

- enjoy car content,
- are learning about automobiles,
- are researching,
- are comparing options,
- or actually intend to purchase a car.

Strong engagement therefore provides evidence of **attention and possible interest**, but does not automatically establish **intent or need**.

---

## 🎯 Proposed Solution

MotiveLens acts as a **user-side recommendation auditing layer**.

Instead of simply asking:

> "What should be recommended next?"

MotiveLens asks:

> "What does the available evidence actually tell us about why this recommendation is relevant to the user?"

The prototype analyzes:

- 👁 Attention & Interest
- 🎯 Goal Alignment
- 🧠 Intent Clarification
- 🏢 Commercial Signals
- ⚖️ Evidence Balance
- 🧭 Recommendation Drift & Diversity
- 🎛️ Explicit User Control

MotiveLens does not classify recommendations as good or bad. It surfaces evidence and allows the user to interpret and control their recommendation direction.

---

## ⚙️ How the Prototype Works

```text
User Goal + Interests
        ↓
Simulated Recommendation Feed
        ↓
View / Like / Skip
        ↓
Demo Recommender
        ↓
Feed Adapts to Engagement
        ↓
MotiveLens Auditing Layer
        ↓
Goal + Intent + Influence + Drift Analysis
        ↓
Explainable Insights
        ↓
User Confirms or Refocuses
        ↓
Demo Feed Responds
```

---

## 🧪 Demo Recommendation Logic

The simulated recommender uses transparent interaction weights:

| Interaction | Demo Weight |
|---|---:|
| View | +1 |
| Like | +3 |
| Skip | -2 |

These values are **prototype demonstration weights** and do not represent the private recommendation algorithm of any real platform.

---

## ✨ Key Features

- **Adaptive Demo Feed** – Feed ranking responds to observed engagement.
- **Attention Map** – Shows where positive engagement is concentrated.
- **Goal Alignment** – Checks whether recommendation content relates to the user's stated goal.
- **Ask, Don't Assume** – Allows users to clarify the reason behind their engagement.
- **Commercial Signal Detection** – Detects discounts, urgency and calls to action.
- **Evidence Balance** – Separates user-side relevance evidence from commercial-signal evidence.
- **Drift & Diversity** – Shows whether engagement is broad or becoming concentrated.
- **User Refocus** – Allows explicit user preference to influence the demo feed.

---

## 🛠️ Technology

- Python
- Streamlit
- Regular expressions and keyword-based text analysis
- Streamlit Session State
- Explainable rule/evidence-based scoring

---

## 🤖 Current AI Status

The current version is an **explainable rule- and evidence-based prototype**.

It does **not currently use a trained machine-learning model**.

Future versions can use semantic NLP or trained/fine-tuned models for deeper understanding of user goals, recommendation meaning and intent.

---

## 🚀 Running Locally

Install the requirements:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

---

## 🔮 Future Scope

- Semantic NLP for deeper goal alignment
- Trained or fine-tuned intent classification
- Larger recommendation datasets
- Long-term recommendation drift analysis
- Persistent user profiles
- Privacy and consent-aware data handling
- Integration with supported platform APIs
- Browser-extension-style auditing where platform policies permit

---

## ⚠️ Prototype Limitations

- The recommendation feed is simulated.
- Goal alignment is primarily rule/keyword based.
- Interaction weights are demonstration values.
- Drift thresholds are prototype thresholds.
- Evidence-share percentages are not statistical probabilities.
- User information is temporarily stored using Streamlit Session State.
- The prototype does not access the private recommendation algorithm of any real platform.

---

## 🌱 Vision

Recommendation systems can observe **what we click**.

MotiveLens explores the question:

> **Does what captured our attention actually represent what we intended or needed?**

The goal is to make recommendation environments more **understandable, explainable and user-controlled**.
