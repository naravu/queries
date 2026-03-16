import streamlit as st
import pandas as pd

def load_questions(md_file):
    questions = []
    with open(md_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_question = None
    options = []

    for line in lines:
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
st.title("📝 Questionnaire")
st.write("Choose multiple options for each question below:")

questions = load_questions("questions.md")
responses = {}

for i, q in enumerate(questions):
    st.subheader(q["question"])
    selected = st.multiselect("Select all that apply:", q["options"], key=f"q{i}")
    responses[q["question"]] = selected

# Store submissions in memory
if "all_responses" not in st.session_state:
    st.session_state["all_responses"] = []

if st.button("Submit"):
    st.session_state["all_responses"].append(responses)
    st.success("Responses recorded!")

# Export buttons
if st.session_state["all_responses"]:
    df = pd.DataFrame(st.session_state["all_responses"])

    st.write("### Collected Responses")
    st.dataframe(df)

    # CSV export
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="responses.csv",
        mime="text/csv"
    )

    # Excel export
    excel_file = "responses.xlsx"
    df.to_excel(excel_file, index=False)
    with open(excel_file, "rb") as f:
        st.download_button(
            label="Download Excel",
            data=f,
            file_name="responses.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
