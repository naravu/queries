import streamlit as st
import pandas as pd
from io import BytesIO
import re

def load_questions(md_file):
    questions = []
    with open(md_file, "r", encoding="utf-8") as f:
        current_question, options = None, []
        for line in f:
            line = line.strip()
            if line.startswith("##"):  # Question line
                if current_question:
                    questions.append({"question": current_question, "options": options})
                current_question = line.replace("##", "").strip()
                options = []
            elif line.startswith("-"):  # Option line
                # Regex to capture option text and score (supports integers and decimals)
                match = re.match(r"(.+?)\s*\[([\d\.]+)\] $", line.replace("-", "").strip())
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

# Name input
name = st.text_input("Your Name")

questions = load_questions("questionsscore.md")

# Initialize session state
if "all_responses" not in st.session_state:
    st.session_state["all_responses"] = []

responses = {"Name": name}
total_score = 0

# Render questions
for i, q in enumerate(questions):
    st.subheader(q["question"])
    option_labels = [opt["text"] for opt in q["options"]]
    selected = st.multiselect("Select all that apply:", option_labels, key=f"q{i}")

    # Calculate score for this question based on selected options
    question_score = 0
    for opt in q["options"]:
        if opt["text"] in selected:
            question_score += opt["score"]

    responses[q["question"]] = question_score
    total_score += question_score

responses["Total Score"] = total_score

# Submit button
if st.button("Submit"):
    if not name.strip():
        st.warning("Please enter your name before submitting.")
    else:
        st.session_state["all_responses"].append(responses.copy())
        st.success(f"Responses recorded! Your total score is {total_score}")

# Export section
if st.session_state["all_responses"]:
    df = pd.DataFrame(st.session_state["all_responses"])
    st.write("### Collected Responses")
    st.dataframe(df)

    # CSV export
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "responses.csv", "text/csv")

    # Excel export (in-memory)
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, engine="openpyxl")
    st.download_button(
        "Download Excel",
        excel_buffer.getvalue(),
        "responses.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
