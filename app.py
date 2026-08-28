import streamlit as st
from pypdf import PdfReader
import urllib.request
import urllib.error
import json


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI StudyMate",
    page_icon="📚",
    layout="centered"
)


# ---------------------------------------------------------
# GEMINI API FUNCTION
# ---------------------------------------------------------

def ask_gemini(prompt, api_key):

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-2.5-flash:generateContent?key="
        + api_key
    )

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    request_data = json.dumps(data).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=request_data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

            return result["candidates"][0]["content"]["parts"][0]["text"]

    except urllib.error.HTTPError as error:

        error_message = error.read().decode("utf-8")

        return f"Gemini API Error:\n{error_message}"

    except Exception as error:

        return f"Error connecting to Gemini:\n{error}"


# ---------------------------------------------------------
# PDF TEXT EXTRACTION
# ---------------------------------------------------------

def extract_pdf_text(uploaded_file):

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("📚 AI StudyMate")

st.write(
    "Understand, revise and test yourself using AI-powered study tools."
)


# ---------------------------------------------------------
# API KEY
# ---------------------------------------------------------

st.sidebar.header("⚙️ Settings")

api_key = st.sidebar.text_input(
    "Gemini API Key",
    type="password",
    help="Enter your Gemini API key."
)

st.sidebar.info(
    "Your API key is used only to communicate with Gemini."
)


# ---------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------

option = st.selectbox(
    "Choose a feature:",
    [
        "📄 Upload Material",
        "📝 AI Notes",
        "❓ AI Quiz",
        "📊 Track Learning"
    ]
)


# =========================================================
# UPLOAD MATERIAL
# =========================================================

if option == "📄 Upload Material":

    st.header("📄 Upload Study Material")

    uploaded_file = st.file_uploader(
        "Upload your study PDF",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        with st.spinner("Reading PDF..."):

            text = extract_pdf_text(uploaded_file)

        if text.strip():

            st.session_state["pdf_text"] = text
            st.session_state["file_name"] = uploaded_file.name

            st.success(
                "PDF successfully processed! ✅"
            )

            st.info(
                f"Extracted approximately {len(text)} characters."
            )

        else:

            st.error(
                "Could not extract text from this PDF."
            )


# =========================================================
# AI NOTES
# =========================================================

elif option == "📝 AI Notes":

    st.header("📝 AI Notes Generator")

    uploaded_file = st.file_uploader(
        "Upload your study PDF",
        type=["pdf"],
        key="notes_upload"
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

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        if st.button("✨ Generate Notes"):

            if not api_key:

                st.error(
                    "Please enter your Gemini API key in the sidebar."
                )

            else:

                with st.spinner(
                    "Reading your PDF and generating notes..."
                ):

                    pdf_text = extract_pdf_text(
                        uploaded_file
                    )

                if not pdf_text.strip():

                    st.error(
                        "No readable text was found in the PDF."
                    )

                else:

                    # Limit text to avoid extremely large requests
                    pdf_text = pdf_text[:100000]

                    prompt = f"""
You are an expert study assistant.

Create {note_type} from the following study material.

Requirements:

1. Use simple student-friendly language.
2. Explain important concepts clearly.
3. Use headings and bullet points.
4. Highlight important definitions.
5. Include important formulas where applicable.
6. Include examples where useful.
7. For Exam-Focused Notes, emphasize likely exam questions and key points.
8. Do not add information that is unrelated to the supplied material.

Study Material:

{pdf_text}
"""

                    result = ask_gemini(
                        prompt,
                        api_key
                    )

                    st.markdown("## 📖 Generated Notes")

                    st.markdown(result)


# =========================================================
# AI QUIZ
# =========================================================

elif option == "❓ AI Quiz":

    st.header("❓ AI Quiz Generator")

    uploaded_file = st.file_uploader(
        "Upload your study PDF",
        type=["pdf"],
        key="quiz_upload"
    )

    number_of_questions = st.slider(
        "Number of questions",
        min_value=5,
        max_value=15,
        value=10
    )

    if uploaded_file:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        if st.button("🚀 Generate Quiz"):

            if not api_key:

                st.error(
                    "Please enter your Gemini API key in the sidebar."
                )

            else:

                with st.spinner(
                    "Generating your quiz..."
                ):

                    pdf_text = extract_pdf_text(
                        uploaded_file
                    )

                pdf_text = pdf_text[:100000]

                prompt = f"""
Create a multiple-choice quiz from the following study material.

Create exactly {number_of_questions} questions.

For every question provide:

Question:
A)
B)
C)
D)
Correct Answer:
Explanation:

Rules:

- Questions must be based only on the supplied material.
- Mix easy, medium and difficult questions.
- Avoid duplicate questions.
- Make the correct answers accurate.

Study Material:

{pdf_text}
"""

                result = ask_gemini(
                    prompt,
                    api_key
                )

                st.markdown("## 🧠 Your AI Quiz")

                st.markdown(result)


# =========================================================
# TRACK LEARNING
# =========================================================

elif option == "📊 Track Learning":

    st.header("📊 Track Learning")

    st.write(
        "Use this section to track your study progress."
    )

    col1, col2 = st.columns(2)

    with col1:

        topics_completed = st.number_input(
            "Topics completed",
            min_value=0,
            value=0
        )

    with col2:

        topics_total = st.number_input(
            "Total topics",
            min_value=1,
            value=10
        )

    progress = min(
        topics_completed / topics_total,
        1.0
    )

    st.progress(progress)

    st.write(
        f"### Progress: {progress * 100:.0f}%"
    )

    if progress == 1:

        st.success(
            "🎉 Excellent! You completed all topics!"
        )

    elif progress >= 0.5:

        st.info(
            "🔥 Great progress! Keep going!"
        )

    else:

        st.warning(
            "📚 Keep studying. You've got this!"
        )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "AI StudyMate | Built for students 🚀"
    )
