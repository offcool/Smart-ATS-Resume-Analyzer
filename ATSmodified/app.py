from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_PRO_API_KEY"))

app = Flask(__name__)

# Function to extract text from PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = " ".join([page.extract_text() or "" for page in reader.pages])
    return text.strip()

# Function to get response from Gemini API
def get_gemini_response(resume_text, job_description):
    model = genai.GenerativeModel('gemini-2.0-flash')
    input_prompt = f"""
    Act as an **advanced Applicant Tracking System (ATS)** specialized in **Software Engineering, Data Science, and Big Data Engineering**.
    Evaluate the resume against the provided job description, considering a **highly competitive job market**.
    Provide an ATS-style evaluation with **high accuracy**, listing missing keywords and percentage match.

    📌 **Expected Response Format (STRICT JSON FORMAT, NO EXTRA TEXT)**:
    ```json
    {{
        "JD Match": "XX%",
        "MissingKeywords": ["keyword1", "keyword2"],
        "Profile Summary": "..."
    }}
    ```
    ❗ **IMPORTANT:**  
    - **Return ONLY valid JSON** (no extra comments, explanations, or markdown).  
    - **Do NOT include escape characters** (`\\n`, `\\t`, etc.).  
    - **Do NOT include text before or after the JSON output.**  
    - **Ensure all percentage values contain `%` (e.g., `"85%"`).**

    **Resume Content:**
    {resume_text}

    **Job Description:**
    {job_description}
    """

    response = model.generate_content(input_prompt)
    return response.text

# Function to clean and validate JSON response
def clean_and_parse_json(response_text):
    try:
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            cleaned_json = json_match.group(0)
            return json.loads(cleaned_json)
        else:
            return None
    except json.JSONDecodeError:
        return None

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    resume_file = data.get('resume')
    job_description = data.get('job_description')

    if resume_file and job_description:
        resume_text = input_pdf_text(resume_file)
        response_text = get_gemini_response(resume_text, job_description)
        response_data = clean_and_parse_json(response_text)
        return jsonify(response_data)
    return jsonify({"error": "Invalid input"}), 400

if __name__ == '__main__':
    app.run(debug=True)