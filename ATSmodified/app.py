from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import re
from flask_cors import CORS

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_PRO_API_KEY"))

app = Flask(__name__)

# Function to extract text from PDF (Corrected to handle file object)
def input_pdf_text(resume_file_object): # Expecting a file object now
    text = ""
    try:
        reader = pdf.PdfReader(resume_file_object) # Pass the file object directly
        text = " ".join([page.extract_text() or "" for page in reader.pages])
    except pdf.errors.PdfReadError as e: # Catch PyPDF2 specific errors
        print(f"PyPDF2 Error reading PDF: {e}")
        return "Error: Could not read PDF content due to PDF format issue." # More specific error message
    except Exception as e: # Catch any other potential errors
        print(f"Error extracting text from PDF: {e}")
        return "Error: Could not extract text from PDF." 
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

# Function to clean and validate JSON response (No changes needed)
def clean_and_parse_json(response_text):
    print("Raw Response Text before JSON parsing:", response_text) # Debug print

    # 1. Remove any text BEFORE the first '{' and AFTER the last '}'
    cleaned_text = re.search(r'\{.*\}', response_text, re.DOTALL)
    if cleaned_text:
        cleaned_text = cleaned_text.group(0)
    else:
        print("Warning: No JSON-like content with curly braces found.")
        return None # Or handle as error

    # 2. Remove any ```json or ``` markers if present (for markdown code blocks)
    cleaned_text = cleaned_text.replace("```json", "").replace("```", "")

    # 3. Remove leading/trailing whitespace and newlines within the JSON string itself
    cleaned_text = cleaned_text.strip()

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error AFTER Cleaning: {e}") # More specific error message
        print("Problematic JSON string:", cleaned_text) # Print the string that failed to parse
        return None # Or handle as error
    
CORS(app, resources={r"/api/analyze": {"origins": "http://localhost:3000"}})


@app.route('/api/analyze', methods=['POST'])
def analyze():
    print("API Key:", os.getenv("GOOGLE_PRO_API_KEY")) # for debugging

    if 'resume' not in request.files or 'job_description' not in request.form: # Check for file and form data
        return jsonify({"error": "Invalid input: 'resume' file and 'job_description' text are required."}), 400

    resume_file_object = request.files['resume'] # Get the uploaded file object
    job_description = request.form['job_description'] # Get job description from form data

    if resume_file_object and job_description:
        if resume_file_object.filename == '': # Check if file was selected
            return jsonify({"error": "No selected resume file"}), 400
        if resume_file_object and not allowed_file(resume_file_object.filename): # Check allowed file type
            return jsonify({"error": "Invalid file type. Only PDF files are allowed."}), 400

        resume_text = input_pdf_text(resume_file_object) # Pass the file object to PDF text extraction

        if resume_text.startswith("Error:"): # Check if input_pdf_text returned an error message
            return jsonify({"error": resume_text}), 400 # Return PDF processing error to frontend

        response_text = get_gemini_response(resume_text, job_description)
        response_data = clean_and_parse_json(response_text)
        return jsonify(response_data)

    return jsonify({"error": "Invalid input"}), 400

# Function to check allowed file types (PDF only)
ALLOWED_EXTENSIONS = {'pdf'} # Set of allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)