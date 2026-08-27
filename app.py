import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI StudyMate",
    page_icon="🎓",
    layout="wide"
)

# Title
st.title("🎓 AI StudyMate")
st.subheader("Your Personal AI-Powered Study Assistant")

st.write(
    "Upload your study material and use AI to create notes, "
    "quizzes, important questions, and personalized study plans."
)

st.divider()

# Sidebar
with st.sidebar:
    st.header("📚 StudyMate Menu")

    option = st.radio(
        "Choose a feature:",
        [
            "🏠 Home",
            "📝 AI Notes",
            "❓ AI Quiz",
            "💬 Ask My Material",
            "📅 Study Planner"
        ]
    )

# Home
if option == "🏠 Home":
    st.header("Welcome to AI StudyMate! 👋")

    st.write(
        "AI StudyMate helps students understand and revise "
        "their study material more effectively."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📄\n\n**Upload Material**\n\nUpload your study PDF.")

    with col2:
        st.success("🧠\n\n**Learn Smarter**\n\nGenerate AI-powered study content.")

    with col3:
        st.warning("📊\n\n**Track Learning**\n\nTest your knowledge with quizzes.")

# AI Notes
elif option == "📝 AI Notes":
    st.header("📝 AI Notes Generator")

    uploaded_file = st.file_uploader(
        "Upload your study material",
        type=["pdf"]
    )

    note_type = st.selectbox(
        "Choose note type:",
        [
            "Short Notes",
            "Detailed Notes",
            "Exam-Focused Notes"
        ]
    )

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

        if st.button("✨ Generate Notes"):
            st.info(
                "AI Notes generation will be connected in the next stage."
            )

# AI Quiz
elif option == "❓ AI Quiz":
    st.header("❓ AI Quiz Generator")

    uploaded_file = st.file_uploader(
        "Upload study material for the quiz",
        type=["pdf"]
    )

    number_of_questions = st.slider(
        "Number of questions:",
        min_value=5,
        max_value=20,
        value=10
    )

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

        if st.button("🚀 Generate Quiz"):
            st.info(
                "AI Quiz generation will be connected in the next stage."
            )

# Ask My Material
elif option == "💬 Ask My Material":
    st.header("💬 Ask My Material")

    uploaded_file = st.file_uploader(
        "Upload your study material",
        type=["pdf"]
    )

    question = st.text_input(
        "Ask a question about your study material:"
    )

    if st.button("🔍 Ask AI"):
        if uploaded_file and question:
            st.info(
                "AI question answering will be connected in the next stage."
            )
        elif not uploaded_file:
            st.warning("Please upload a PDF first.")
        else:
            st.warning("Please enter a question.")

# Study Planner
elif option == "📅 Study Planner":
    st.header("📅 Personalized Study Planner")

    exam_date = st.date_input("Select your exam date")

    study_hours = st.slider(
        "How many hours can you study per day?",
        min_value=1,
        max_value=12,
        value=3
    )

    topics = st.text_area(
        "Enter your topics/chapters:",
        placeholder="Example:\nPython\nMachine Learning\nDBMS\nData Structures"
    )

    if st.button("📅 Create Study Plan"):
        if topics:
            st.success("Study plan generation will be connected in the next stage.")
        else:
            st.warning("Please enter your topics first.")

st.divider()

st.caption("AI StudyMate | Built for students 🚀")
