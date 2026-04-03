import streamlit as st
import pandas as pd
from io import BytesIO
import re
import requests
from datetime import datetime
import base64
import json

def load_questions(md_file):
    questions = []
    with open(md_file, "r", encoding="utf-8") as f:
        current_question, options = None, []
        for line in f:
            line = line.strip()
            if line.startswith("##"):
                if current_question:
                    questions.append({"question": current_question, "options": options})
                current_question = line.replace("##", "").strip()
                options = []
            elif line.startswith("-"):
                match = re.match(r"(.+?)\s*

\[([\d\.]+)\]

$", line.replace("-", "").strip())
                if match:
                    option_text, score = match.groups()
                    options.append({"text": option_text.strip(), "score": float(score)})
                else:
                    options.append({"text": line.replace("-", "").strip(), "score": 0.0})
        if current_question:
            questions.append({"question": current_question, "options": options})
    return questions

# --- Streamlit UI ---
st.title("📝 Questionnaire WebApp")
st.write("Please enter your name and answer the questions below:")

name = st.text_input("Your Name")
questions = load_questions("questions.md")

if "all_responses" not in st.session_state:
    st.session_state["all_responses"] = []

responses = {"Name": name}
total_score = 0

for i, q in enumerate(questions):
    st.subheader(q["question"])
    option_labels = [opt["text"] for opt in q["options"]]
    selected = st.multiselect("Select all that apply:", option_labels, key=f"q{i}")
    responses[q["question"]] = selected
    for opt in q["options"]:
        if opt["text"] in selected:
            total_score += opt["score"]

responses["Total Score"] = total_score

if st.button("Submit"):
    if not name.strip():
        st.warning("Please enter your name before submitting.")
    else:
        st.session_state["all_responses"].append(responses.copy())
        st.success(f"Responses recorded! Your total score is {total_score}")

        # --- Save to GitHub via API ---
        df = pd.DataFrame(st.session_state["all_responses"])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"responses_{timestamp}.csv"
        csv_content = df.to_csv(index=False)

        # Encode file content for GitHub API
        encoded_content = base64.b64encode(csv_content.encode()).decode()

        # Secrets: set these in Streamlit Cloud (Settings → Secrets)
        github_token = st.secrets["GITHUB_TOKEN"]
        repo = st.secrets["GITHUB_REPO"]  # e.g. "username/repo"
        path = f"data/{filename}"  # folder in repo

        url = f"https://api.github.com/repos/{repo}/contents/{path}"
        headers = {"Authorization": f"token {github_token}"}
        data = {
            "message": f"Add responses at {timestamp}",
            "content": encoded_content,
            "branch": "main"
        }

        try:
            r = requests.put(url, headers=headers, data=json.dumps(data))
            if r.status_code in [200, 201]:
                st.success("Responses saved to GitHub successfully!")
            else:
                st.error(f"GitHub save failed: {r.json()}")
        except Exception as e:
            st.error(f"Error saving to GitHub: {e}")

if st.session_state["all_responses"]:
    df = pd.DataFrame(st.session_state["all_responses"])
    st.write("### Collected Responses")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "responses.csv", "text/csv")

    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, engine="openpyxl")
    st.download_button(
        "Download Excel",
        excel_buffer.getvalue(),
        "responses.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
