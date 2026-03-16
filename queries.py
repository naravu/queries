import streamlit as st
import pandas as pd
from io import BytesIO

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
                options.append(line.replace("-", "").strip())
        if current_question:
            questions.append({"question": current_question, "options": options})
    return questions

# --- Streamlit UI ---
st.title("📝 Questionnaire WebApp")
st.write("Choose multiple options for each question below:")

questions = load_questions("questions.md")

# Initialize session state
if "all_responses" not in st.session_state:
    st.session_state["all_responses"] = []

responses = {}

# Render questions
for i, q in enumerate(questions):
    st.subheader(q["question"])
    responses[q["question"]] = st.multiselect(
        "Select all that apply:", q["options"], key=f"q{i}"
    )

# Submit button
if st.button("Submit"):
    st.session_state["all_responses"].append(responses.copy())
    st.success("Responses recorded!")

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
