import fitz
import re
import pandas as pd
import streamlit as st

def extract_text_from_pdf(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_email(text):
    email = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return email[0] if email else None

def extract_phone(text):
    phone = re.findall(r'\+?\d[\d\s\-()]{8,}\d', text)
    return phone[0] if phone else None

def extract_name(text):
    lines = text.split('\n')
    for line in lines:
        if line.strip() and line.strip().istitle():
            return line.strip()
    return None

def extract_skills(text):
    skills_list = ['Python', 'Java', 'SQL', 'Excel', 'C++', 'Data Analysis', 'Machine Learning']
    found_skills = []
    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    return found_skills

def parse_resume(file_path):
    text = extract_text_from_pdf(file_path)
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)

    data = {
        'Name': name,
        'Email': email,
        'Phone': phone,
        'Skills': ', '.join(skills)
    }
    return data

# Streamlit app
st.title("Resume Parser")

uploaded_file = st.file_uploader("Upload a Resume PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        result = parse_resume("temp.pdf")
        st.subheader("Extracted Information:")
        for key, value in result.items():
            st.write(f"**{key}:** {value}")
        
        save_csv = st.button("Save to CSV")
        if save_csv:
            df = pd.DataFrame([result])
            csv_name = st.text_input("Enter the name for the CSV file (without extension):", "parsed_resume")
            df.to_csv(f"{csv_name}.csv", index=False)
            st.success(f"Data saved to '{csv_name}.csv'")
    except Exception as e:
        st.error(f"Error: {e}")
