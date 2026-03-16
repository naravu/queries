# 📝 Questionnaire WebApp

An interactive questionnaire web application built with **Streamlit**.  
This app loads questions from a Markdown file, allows participants to enter their name, select multiple answers, records their responses, and provides easy export options to **CSV** and **Excel**.

---

## ✨ Features
- **Markdown-driven questions**: Maintain your questionnaire in a simple `.md` file.
- **Name capture**: Each participant enters their name before answering.
- **Multiple choice**: All questions use multiselect dropdowns for flexible responses.
- **Session storage**: Responses are stored during the app session.
- **Export options**: Download all collected responses as CSV or Excel with one click.
- **Optimized performance**: In-memory exports (no temporary files) for cloud deployment.

---

## 📂 Project Structure
.
├── app.py           # Streamlit application
├── questions.md     # Questionnaire in Markdown format
├── requirements.txt # Dependencies
└── README.md        # Documentation

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/questionnaire-app.git
cd questionnaire-app
---

2. Install dependencies
pip install -r requirements.txt

3. Run the app
streamlit run app.py

📦 Requirements
streamlit>=1.30.0
pandas>=2.0.0
openpyxl>=3.1.0

🌐 Deployment

You can deploy this app easily on Streamlit Cloud:

    Push your code to GitHub.

    Connect the repo to Streamlit Cloud.

    The app will run online with your questionnaire.

⚠️ Note: Responses are stored only during the session. Use the Export buttons to download results before the app restarts.

