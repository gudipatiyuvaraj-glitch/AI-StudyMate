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
# SIDEBAR
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

        # Extract text
        extracted_text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text + "\n"

        extracted_text = extracted_text.strip()

        # --------------------------------------------------
        # CHECK PDF TEXT
        # --------------------------------------------------

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

                if not gemini_api_key:

                    st.warning(
                        "Please enter your Gemini API key in Settings."
                    )

                else:

                    try:

                        client = genai.Client(
                            api_key=gemini_api_key
                        )

                        summary_prompt = f"""
You are an AI study assistant.

Analyze the following study material and create
a clear and student-friendly summary.

STUDY MATERIAL:
{extracted_text}

Provide:

## 📌 Main Topic
Identify the main topic.

## 🧠 Important Concepts
Explain the important concepts simply.

## 🔑 Key Points
List the most important points.

## 📚 Summary
Give a concise overall summary.

Important:
- Only use information from the study material.
- Do not invent facts.
- Use simple language.
- Use headings and bullet points.
"""

                        with st.spinner(
                            "🤖 Generating summary..."
                        ):

                            response = client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=summary_prompt
                            )

                        st.success(
                            "Summary generated successfully! ✅"
                        )

                        st.markdown(response.text)

                    except Exception as e:

                        st.error(
                            f"Gemini error: {e}"
                        )


            # --------------------------------------------------
            # QUIZ SECTION
            # --------------------------------------------------

            st.divider()

            st.header("🧠 Practice Quiz")

            st.write(
                "Test your knowledge with 10 questions "
                "generated from your uploaded PDF."
            )

            # --------------------------------------------------
            # GENERATE QUIZ BUTTON
            # --------------------------------------------------

            if st.button(
                "🎯 Generate 10-Question Quiz",
                use_container_width=True
            ):

                if not gemini_api_key:

                    st.warning(
                        "Please enter your Gemini API key in Settings."
                    )

                else:

                    try:

                        client = genai.Client(
                            api_key=gemini_api_key
                        )

                        quiz_prompt = f"""
You are an AI study assistant.

Create a quiz containing exactly 10 questions
based ONLY on the study material below.

STUDY MATERIAL:
{extracted_text}

For each question:

1. Write the question.
2. Give four multiple-choice options:
   A
   B
   C
   D
3. Clearly identify the correct answer.
4. Give a short explanation of why the answer is correct.

Use this exact format:

## Question 1
Question text

A. Option A
B. Option B
C. Option C
D. Option D

**Answer:** B

**Explanation:** Short explanation.

## Question 2
Question text

A. Option A
B. Option B
C. Option C
D. Option D

**Answer:** A

**Explanation:** Short explanation.

Continue this format until Question 10.

Important:
- Create exactly 10 questions.
- Use ONLY information from the PDF.
- Do not invent information.
- Make the questions useful for studying.
- Mix easy, medium, and difficult questions.
- Make sure each question has exactly one correct answer.
"""

                        with st.spinner(
                            "🧠 Creating your 10-question quiz..."
                        ):

                            quiz_response = client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=quiz_prompt
                            )

                        st.success(
                            "Quiz generated successfully! 🎉"
                        )

                        st.markdown(
                            quiz_response.text
                        )

                    except Exception as e:

                        st.error(
                            f"Gemini error: {e}"
                        )

        else:

            st.warning(
                "The PDF was uploaded, but no readable text "
                "could be extracted."
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
