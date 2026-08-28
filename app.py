import streamlit as st
from pypdf import PdfReader
from google import genai


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI StudyMate",
    page_icon="📚",
    layout="wide"
)


# --------------------------------------------------
# SIDEBAR - SETTINGS
# --------------------------------------------------

with st.sidebar:
    st.header("⚙️ Settings")

    gemini_api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Enter your Gemini API key"
    )

    st.info(
        "Your API key is used only to communicate with Gemini."
    )


# --------------------------------------------------
# MAIN TITLE
# --------------------------------------------------

st.title("📚 AI StudyMate")

st.write(
    "Upload your study material and use AI to understand it faster."
)


# --------------------------------------------------
# PDF UPLOAD
# --------------------------------------------------

st.header("📄 Upload Study Material")

uploaded_file = st.file_uploader(
    "Upload your study PDF",
    type=["pdf"]
)


# --------------------------------------------------
# PROCESS PDF
# --------------------------------------------------

if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    try:
        # Read PDF
        reader = PdfReader(uploaded_file)

        # Extract text from all pages
        extracted_text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text + "\n"

        # Remove unnecessary spaces
        extracted_text = extracted_text.strip()

        # Check whether text was extracted
        if extracted_text:

            st.success("PDF successfully processed! ✅")

            st.info(
                f"Extracted approximately {len(extracted_text)} characters."
            )

            # --------------------------------------------------
            # AI STUDY ASSISTANT
            # --------------------------------------------------

            st.divider()

            st.header("🤖 AI Study Assistant")

            # --------------------------------------------------
            # SUMMARY BUTTON
            # --------------------------------------------------

            if st.button(
                "📝 Generate Summary",
                use_container_width=True
            ):

                # Check API key
                if not gemini_api_key:

                    st.warning(
                        "Please enter your Gemini API key in the Settings section."
                    )

                else:

                    try:

                        # Create Gemini client
                        client = genai.Client(
                            api_key=gemini_api_key
                        )

                        # Prompt
                        prompt = f"""
You are an AI study assistant.

Analyze the following study material and create a
clear and student-friendly summary.

STUDY MATERIAL:
{extracted_text}

Please provide:

## 📌 Main Topic
Identify the main topic of the material.

## 🧠 Important Concepts
List the most important concepts and explain them simply.

## 🔑 Key Points
Give the most important points a student should remember.

## 📚 Summary
Give a concise overall summary that is easy for a student to understand.

Important instructions:
- Only use information from the study material.
- Do not invent facts.
- Use simple language.
- Use headings and bullet points where helpful.
"""

                        # Generate AI response
                        with st.spinner(
                            "🤖 AI is generating your summary..."
                        ):

                            response = client.models.generate_content(
                                model="gemini-3.7-flash",
                                contents=prompt
                            )

                        # Display result
                        st.success(
                            "Summary generated successfully! ✅"
                        )

                        st.markdown(response.text)

                    except Exception as e:

                        st.error(
                            f"Gemini error: {e}"
                        )

        else:

            st.warning(
                "The PDF was uploaded, but no readable text could be extracted."
            )

    except Exception as e:

        st.error(
            f"Error processing PDF: {e}"
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI StudyMate | Built for students 🚀"
)