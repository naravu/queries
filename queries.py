import streamlit as st

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

    # Add last question
    if current_question:
        questions.append({"question": current_question, "options": options})

    return questions

# --- Streamlit UI ---
st.title("📝 Questionnaire WebApp")
st.write("Choose multiple options for each question below:")

questions = load_questions("questions.md")
responses = {}

for i, q in enumerate(questions):
    st.subheader(q["question"])
    if len(q["options"]) <= 6:
        # Use multiselect for shorter option lists
        selected = st.multiselect("Select all that apply:", q["options"], key=f"q{i}")
    else:
        # Use checkboxes for longer option lists
        selected = []
        for opt in q["options"]:
            if st.checkbox(opt, key=f"{i}_{opt}"):
                selected.append(opt)
    responses[q["question"]] = selected

if st.button("Submit"):
    st.success("Thank you for completing the questionnaire!")
    st.write("### Your Responses:")
    for question, answer in responses.items():
        st.write(f"**{question}**")
        st.write(", ".join(answer) if answer else "No selection")
