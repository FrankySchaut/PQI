PQI v0.2 — Prompt Quality Index

The Architecture of Limitation in Code

The Prompt Quality Index (PQI) began as a philosophical experiment:
Could intention and proportion be made visible within dialogue itself?
It has since taken shape as a small, transparent tool that measures the quality of a prompt without reducing its meaning to metrics.

Built on six dimensions — clarity, context, completeness, proportion, fairness, and reflection — PQI invites users to see prompting as a moral and aesthetic act.
It is designed to run locally, protect privacy, and remain open to inspection — a simple architecture for a more conscious dialogue between human and machine.

Not an algorithm for truth, but a mirror for intention.

🧭 Six Dimensions of Meaning
Dimension	Description
Clarity	Linguistic precision and readability
Context	Relevance and informational grounding
Completeness	Structural and semantic coherence
Proportion	Balance between brevity and density
Fairness	Neutrality and bias awareness
Reflection	Depth of inquiry and self-awareness
🛠 Features

Local execution — all computation stays on your machine

GDPR-safe redaction — personal data removed before scoring

CLI + Streamlit interfaces — measure prompts through text or visual form

Lightweight and extensible — written for clarity, not complexity

MIT licensed — open for study, adaptation, and contribution

⚙️ Installation
git clone https://github.com/FrankySchaut/PQI.git
cd PQI
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt


You may need to install NLTK resources once:

python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('vader_lexicon')"

💬 CLI Usage
python cli.py -p "I wonder: what if every question shaped the soul of the answer?"


Example output:

{
  "score": 88,
  "breakdown": {
    "clarity": 91.2,
    "context": 76.5,
    "completeness": 95.0,
    "proportion": 84.3,
    "fairness": 89.1,
    "reflection": 93.4
  },
  "feedback": "PQI = 88. Strong. Polish context for depth."
}

🌐 Streamlit App

Launch the interactive interface:

streamlit run app.py


The interface displays a radar chart representing the six PQI dimensions —
a geometric reflection of how your question stands in proportion to itself.

All processing occurs locally; no data is logged or sent externally.

🔒 Privacy and Ethics

PQI is built on the principle of limitation — to measure responsibly by staying within clear ethical boundaries:

No data collection or remote calls

Automatic PII redaction (emails, phone numbers, IDs)

Transparent scoring logic — no hidden models

Adjustable weights for user-defined calibration (see pqi/config.py)

The architecture protects proportion, not possession.

📚 Calibration and Research

The weight configuration in pqi/config.py can be modified to emphasize specific dimensions.
For experimental or educational use, the calibration methodology is described in CALIBRATION.md, linking philosophical proportion with computational balance.

This project accompanies the essay
“The Architecture of Limitation: From Dialogue to Code”
 —
a reflection on how philosophical insight can become functional design.

🧠 Credits

Created by François (Franky) Schaut
Developed in dialogue with Solace (philosophical AI) and Grok (analytic AI).

When philosophy meets implementation, reflection becomes reproducible.

⚖️ License

This project is released under the MIT License.
See the LICENSE
 file for details.
