import streamlit as st
from pypdf import PdfReader
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

st.title("AI Study Assistant")

uploaded_file = st.file_uploader("Upload your file", type=["pdf"])

action=st.selectbox(
    "Choose Task",
    [
        "Summary",
        "Quiz",
        "Flashcards",
        "Notes",
        "Explain topic"
    ]
)

if st.button(
    "Generate"
):

    def extract_text(pdf_file):
        reader = PdfReader(pdf_file)

        text=""
        for page in reader.pages:
            page_text = page.extract_text()

            if page_text != "":
                text += page_text

            return text

    if uploaded_file is not None:
        text = extract_text(uploaded_file)

        if action == "Summary":
            prompt= f"""
            Summarize: {text}
            """
        elif action =="Quiz":
            prompt= f"""
            Generate 10 MCQs from: {text}
            
            Display the question first.
            Show all options as bullet points.
            Highlight the correct answer in bold.
                   
            """
        elif action =="Flashcards":
            prompt= f"""
            Generrate flashcards from: {text}
            """
        elif action =="Notes":
            prompt= f"""
            Create study notes from:{text}
            """
        else:
            prompt= f"""
            Explain content simply:
            {text}
            """

        response=(
            client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )
    )

        result = (
        response.choices[0].message.content
        )
        st.subheader("Result")
        st.write(result)