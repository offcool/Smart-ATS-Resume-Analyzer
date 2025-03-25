from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
import json
import re
from flask_cors import CORS
import logging
import time
from typing import Optional, Dict, List, Union, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app, resources={r"/api/analyze": {"origins": "*"}}) #allow all origins

# Load environment variables
load_dotenv()
# Get the API key; raise an error if it's missing
GOOGLE_PRO_API_KEY = os.getenv("GOOGLE_PRO_API_KEY")
if not GOOGLE_PRO_API_KEY:
    raise ValueError("GOOGLE_PRO_API_KEY environment variable not set!")
genai.configure(api_key=GOOGLE_PRO_API_KEY)


def extract_text_from_pdf(pdf_file_object: fitz.Document) -> str:
    """Extracts text from a PDF file object using PyMuPDF (fitz)."""
    text = ""
    try:
        doc = fitz.open(stream=pdf_file_object.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        logging.error(f"Error extracting text with PyMuPDF: {e}")
        return "Error: Could not extract text from PDF."
    return text.strip()

def call_gemini_api(prompt: str, model_name: str = 'gemini-1.5-pro-latest', max_retries: int = 3) -> str:
    """Calls the Gemini API with retries."""
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Gemini API error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return f"Error: Gemini API error after multiple retries: {e}"

def extract_job_keywords(job_description: str) -> str:
    """Extracts key skills and requirements from the job description."""
    prompt = f"""
    You are a highly skilled HR professional. Analyze the following job description and extract the key skills, technologies, and requirements.
    Return a comma-separated list of keywords and phrases. Be concise and specific. Focus on technical skills.

    Job Description:
    {job_description}

    Keywords:
    """
    return call_gemini_api(prompt)

def create_analysis_prompt(resume_text:str, job_keywords:str)->str:
    prompt = f"""
    Act as an **advanced Applicant Tracking System (ATS)** specialized in **Software Engineering, Data Science, and Big Data Engineering**.
    Evaluate the resume against the provided job keywords, considering a **highly competitive job market**.
    Provide an ATS-style evaluation with **high accuracy**, listing missing keywords and percentage match.

    📌 **Expected Response Format (STRICT JSON FORMAT, NO EXTRA TEXT)**:
    ```json
    {{
        "JD Match": "XX%",
        "MissingKeywords": ["keyword1", "keyword2"],
        "Profile Summary": "A concise summary tailored to the job, highlighting relevant experience. Focus on quantifiable achievements and key skills."
    }}
    ```
    ❗ **IMPORTANT:**
    - **Return ONLY valid JSON** (no extra comments, explanations, or markdown).
    - **Do NOT include escape characters** (`\\n`, `\\t`, etc.).
    - **Do NOT include text before or after the JSON output.**
    - **Ensure all percentage values contain `%` (e.g., `"85%"`).**
    - If the resume is very short or lacks relevant information, provide a "Profile Summary" indicating this.
    - Be critical and realistic in the "JD Match" percentage.
    - Prioritize technical skills in "MissingKeywords".

    Resume Content:
    {resume_text}

    Job Keywords:
    {job_keywords}
    """
    return prompt

def clean_and_parse_json(response_text: str) -> Optional[Dict]:
    """Cleans and parses the JSON response from Gemini."""
    logging.info(f"Raw Response Text before JSON parsing: {response_text}")
    cleaned_text = re.search(r'\{.*\}', response_text, re.DOTALL)
    if cleaned_text:
        cleaned_text = cleaned_text.group(0)
    else:
        logging.warning("Warning: No JSON-like content found.")
        return None
    cleaned_text = cleaned_text.replace("`json", "").replace("`", "").strip()

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        logging.error(f"JSON Decode Error AFTER Cleaning: {e}")
        logging.error(f"Problematic JSON string: {cleaned_text}")
        return None

@app.route('/api/analyze', methods=['POST'])
async def analyze():
    """Analyzes a resume against a job description."""
    logging.info("Received request to /api/analyze")

    if 'resume' not in request.files or 'job_description' not in request.form:
        return jsonify({"error": "Invalid input: 'resume' file and 'job_description' text are required."}), 400

    resume_file_object = request.files['resume']
    job_description = request.form['job_description']

    if not resume_file_object or resume_file_object.filename == '':
        return jsonify({"error": "No selected resume file"}), 400
    if not allowed_file(resume_file_object.filename):
        return jsonify({"error": "Invalid file type. Only PDF files are allowed."}), 400

    resume_text = extract_text_from_pdf(resume_file_object)
    if resume_text.startswith("Error:"):
        return jsonify({"error": resume_text}), 400

    job_keywords = extract_job_keywords(job_description)
    prompt = create_analysis_prompt(resume_text, job_keywords)
    response_text = call_gemini_api(prompt)

    if response_text.startswith("Error:"):
        return jsonify({"error": response_text}), 500

    response_data = clean_and_parse_json(response_text)
    if response_data is None:
        return jsonify({"error": "Failed to parse Gemini API response."}), 500

    return jsonify(response_data)

ALLOWED_EXTENSIONS = {'pdf'}
def allowed_file(filename: str) -> bool:
    """Checks if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))