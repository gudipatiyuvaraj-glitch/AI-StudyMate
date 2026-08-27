import streamlit as st
from pypdf import PdfReader


# -----------------------------
# PDF TEXT EXTRACTION FUNCTION
# -----------------------------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# -----------------------------
# APP CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="AI StudyMate",
    page_icon="📚",
    layout="wide"
)


# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("📚 AI StudyMate")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📝 AI Notes", "❓ Quiz"]
)


# -----------------------------
# HOME PAGE
# -----------------------------
if page == "🏠 Home":

    st.title("📚 AI StudyMate")
    st.subheader("Your Smart Study Companion 🚀")

    st.write(
        "Upload your study materials and use AI-powered tools "
        "to make studying easier and smarter."
    )

    st.divider()

    st.subheader("✨ Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📝 AI Notes\n\nGenerate useful notes from your study material.")

    with col2:
        st.info("❓ Quiz\n\nTest your knowledge with quizzes.")

    with col3:
        st.info("📚 Study Better\n\nOrganize your learning in one place.")


# -----------------------------
# AI NOTES PAGE
# -----------------------------
elif page == "📝 AI Notes":

    st.title("📝 AI Notes")

    st.write("Upload your study material below.")

    uploaded_file = st.file_uploader(
        "📄 Upload your study material",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.success(f"✅ Uploaded: {uploaded_file.name}")

        try:
            pdf_text = extract_text_from_pdf(uploaded_file)

            if pdf_text:

                st.success("✅ PDF text extracted successfully!")

                with st.expander("📖 Preview extracted text"):
                    st.write(pdf_text[:3000])

                note_type = st.selectbox(
                    "Choose note type",
                    ["Short Notes", "Detailed Notes", "Important Points"]
                )

                if st.button("✨ Generate Notes"):

                    st.info(
                        f"🤖 AI note generation for '{note_type}' "
                        "will be added in the next step!"
                    )

            else:
                st.warning(
                    "⚠️ Could not extract text from this PDF."
                )

        except Exception as e:
            st.error(f"❌ Error reading PDF: {e}")


# -----------------------------
# QUIZ PAGE
# -----------------------------
elif page == "❓ Quiz":

    st.title("❓ Quiz")

    st.write("Upload study material to generate quizzes in a future update.")

    st.info("🚀 AI Quiz generation will be added soon!")