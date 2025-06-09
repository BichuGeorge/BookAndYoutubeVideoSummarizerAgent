import streamlit as st
from pdf_utils import extract_chapters
from lang_support import generate_prompt
from questions import generate_questions
from exporter import export_to_json, export_to_csv

st.set_page_config(page_title="📘 Book Chapter Summarizer", layout="wide")

st.title("📘 Book Chapter Summarizer with EURI AI")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

language = st.selectbox("Select Summary Language", ["English", "Hindi", "Spanish"])
lang_code = {"English": "en", "Hindi": "hi", "Spanish": "es"}[language]

if uploaded_file:
    with st.spinner("Extracting chapters..."):
        with open("data/uploads/temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        chapters = extract_chapters("data/uploads/temp.pdf")
        results = {}

        for chapter, text in chapters.items():
            st.subheader(f"📄 {chapter}")
            summary = generate_prompt("summarize", lang=lang_code, text=text[:3000], title=chapter)
            st.markdown("**Summary:**")
            st.write(summary)

            st.markdown("**Bloom Questions:**")
            questions = generate_questions(chapter, text[:3000])
            st.write(questions)

            results[chapter] = {
                "summary": summary,
                "questions": questions
            }

        export_to_json(results)
        export_to_csv(results)

        st.success("✅ Done! Results exported as `output.json` and `output.csv`.")
        st.download_button("📥 Download JSON", data=open("output.json", "rb"), file_name="chapter_summary.json")
        st.download_button("📥 Download CSV", data=open("output.csv", "rb"), file_name="chapter_summary.csv")
st.header("📹 YouTube Video Summarizer")

video_link = st.text_input("Paste YouTube Video Link Here")

if st.button("Summarize Video") and video_link:
    with st.spinner("Analyzing video..."):
        from yoputube_summary  import summarize_youtube_video_full
        print("Summarizing video:", video_link)
        summary = summarize_youtube_video_full(video_link)
        st.markdown("### 📘 Video Summary")
        st.write(summary)