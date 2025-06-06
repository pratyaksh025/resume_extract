import fitz  # PyMuPDF
import re
import streamlit as st

# ------------ Extraction Functions ------------
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_email(text):
    matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return matches[0] if matches else "Not found"

def extract_phone(text):
    matches = re.findall(r'\+?\d[\d\s\-()]{8,}\d', text)
    return matches[0] if matches else "Not found"

def extract_name(text):
    lines = text.split('\n')
    for line in lines:
        if line.strip() and line.strip().istitle():
            return line.strip()
    return "Not found"

def extract_skills(text):
    skills_list = ['Python', 'Java', 'SQL', 'Excel', 'C++', 'Data Analysis', 'Machine Learning']
    found = [skill for skill in skills_list if skill.lower() in text.lower()]
    return ', '.join(found) if found else "Not found"

# ------------ Streamlit UI Setup ------------
st.set_page_config(page_title="Resume Parser", layout="centered")

st.markdown(
    """
    <style>
    .main { background-color: #f5f5f5; }
    .title { text-align: center; font-size: 40px; color: #4B8BBE; font-weight: bold; }
    .info-box { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px #e0e0e0; margin-top: 20px; }
    .footer { text-align: center; font-size: 13px; color: #888; margin-top: 50px; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">📄 Smart Resume Parser</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("⬆️ Upload your resume (PDF format only)", type=["pdf"])

if uploaded_file is not None:
    try:
        text = extract_text_from_pdf(uploaded_file)
        name = extract_name(text)
        email = extract_email(text)
        phone = extract_phone(text)
        skills = extract_skills(text)

        st.success("✅ Resume processed successfully!")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="info-box">🧑‍💼 <b>Name:</b><br>' + name + '</div>', unsafe_allow_html=True)
            st.markdown('<div class="info-box">📧 <b>Email:</b><br>' + email + '</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="info-box">📞 <b>Phone:</b><br>' + phone + '</div>', unsafe_allow_html=True)
            st.markdown('<div class="info-box">🛠️ <b>Skills:</b><br>' + skills + '</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("👈 Please upload a PDF file to extract resume information.")

st.markdown('<div class="footer">Made with ❤️ using Streamlit | © 2025</div>', unsafe_allow_html=True)
