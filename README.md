# Smart ATS Resume Analyzer V2

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) 

Smart ATS Resume Analyzer is a web application designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS).  By analyzing a resume against a job description using AI, this tool provides valuable insights to improve resume content and increase the chances of passing through automated screening processes.

This application is built as a **two-part system**:

*   **Backend (Flask):**  A Python Flask API that handles PDF resume processing, interacts with the Gemini AI model for analysis, and serves API endpoints.
*   **Frontend (React):** A user-friendly React web application that allows users to upload their resume (PDF) and paste a job description, then displays the AI-powered analysis results.

## Key Features

*   **Resume Upload (PDF):** Users can upload their resume in PDF format for analysis.
*   **Job Description Input:** Users can paste job descriptions to compare against their resume.
*   **AI-Powered Analysis:** Utilizes the Google Gemini AI model to analyze resume content and job description relevance.
*   **Job Description Match Score:** Provides a percentage-based score indicating how well the resume matches the job description.
*   **Missing Keywords Identification:**  Highlights keywords from the job description that are missing from the resume, indicating areas for improvement.
*   **Professional Profile Summary:** Generates a summary of the resume's strengths and weaknesses in relation to the job description.
*   **Clear and User-Friendly Frontend:**  Built with React for an intuitive user experience.

## Challenges and Solutions

During the development of this application, we encountered and successfully resolved several challenges:

*   **PDF Resume Processing:**
    *   **Challenge:** Extracting text content accurately from PDF resumes for AI analysis.
    *   **Solution:** Implemented PDF parsing in the Flask backend using the `PyPDF2` library to reliably extract text content from uploaded PDF files.  Error handling was added to manage potentially corrupted or unreadable PDFs.

*   **Cross-Origin Resource Sharing (CORS) Issues:**
    *   **Challenge:**  The React frontend running on `localhost:3000` was blocked from making API requests to the Flask backend running on `localhost:5000` due to browser CORS policies. This resulted in "fetch failed" errors and prevented communication between the frontend and backend.
    *   **Solution:** Enabled CORS in the Flask backend using the `flask-cors` library. Configured CORS to specifically allow requests from `http://localhost:3000` (for development) and the eventual Vercel frontend URL (for production).

*   **JSON Parsing Errors:**
    *   **Challenge:**  Initially, the React frontend was encountering "Unexpected token '<'..." errors when receiving responses from the Flask backend, even with a `200 OK` status. This indicated that the frontend was expecting JSON but receiving HTML or invalid JSON.
    *   **Solution:** Implemented more robust JSON cleaning in the Flask backend's `clean_and_parse_json` function. This involved using regular expressions to remove extra whitespace, markdown code block markers (like ```json), and ensure only valid JSON is returned to the frontend.  Detailed error logging was added in both frontend and backend to diagnose parsing issues effectively.

*   **Deployment to Vercel:**
    *   **Challenge:**  Deploying a full-stack application with a React frontend and a Flask backend API to Vercel required specific configuration.
    *   **Solution:** Created a `vercel.json` configuration file in the project root to define build settings for both the frontend and backend, and to correctly route API requests to the Flask backend when deployed on Vercel.  Environment variables were configured on Vercel to securely manage the Gemini API key.

## Technologies Used

*   **Frontend:**
    *   [React](https://reactjs.org/) - JavaScript library for building user interfaces
    *   [React Hooks](https://reactjs.org/docs/hooks-intro.html) - For managing state and side effects in functional components
    *   [Font Awesome](https://fontawesome.com/) - For icons
    *   [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) - For styling
*   **Backend:**
    *   [Flask](https://flask.palletsprojects.com/en/2.3.x/) - Python microframework for web development
    *   [Python](https://www.python.org/) - Programming language
    *   [PyPDF2](https://pypdf2.readthedocs.io/en/3.0.0/) - Python library for PDF manipulation and text extraction
    *   [google-generativeai](https://ai.google.dev/tutorials/python_quickstart) - Google Gemini API Python library
    *   [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/) - For enabling Cross-Origin Resource Sharing
*   **AI Model:**
    *   [Google Gemini API](https://ai.google.dev/) -  Large language model for resume analysis
*   **Deployment:**
    *   [Vercel](https://vercel.com/) - Platform for frontend and backend deployment
*   **Version Control:**
    *   [Git](https://git-scm.com/) & [GitHub](https://github.com/)

## Setup Instructions

**Before you begin:**

*   Make sure you have [Python](https://www.python.org/downloads/) and [Node.js](https://nodejs.org/) installed on your system.
*   You will need a Google Gemini API key.  Get one from [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey).

**Backend Setup (Flask API):**

1.  **Navigate to the backend directory** in your project (if you have a separate backend folder, otherwise stay in the project root).
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```
3.  **Activate the virtual environment:**
    *   **On Windows:** `.\venv\Scripts\activate`
    *   **On macOS/Linux:** `source venv/bin/activate`
4.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(If you don't have `requirements.txt` yet, create it by running `pip freeze > requirements.txt` after installing the required libraries: `flask`, `PyPDF2`, `google-generativeai`, `flask-cors`)*
5.  **Set your Gemini API key as an environment variable:**
    *   **Option 1 (using `.env` file - recommended for local development):**
        *   Create a `.env` file in your backend directory.
        *   Add the following line to `.env`, replacing `YOUR_API_KEY` with your actual Gemini API key:
            ```
            GOOGLE_PRO_API_KEY=YOUR_API_KEY
            ```
        *   You might need to install `python-dotenv` if you don't have it already: `pip install python-dotenv` and ensure you are loading it in your `app.py` as shown in the code.
    *   **Option 2 (exporting in terminal - less persistent):**
        *   **On Linux/macOS:** `export GOOGLE_PRO_API_KEY=YOUR_API_KEY`
        *   **On Windows (Command Prompt):** `set GOOGLE_PRO_API_KEY=YOUR_API_KEY`
        *   **On Windows (PowerShell):** `$env:GOOGLE_PRO_API_KEY="YOUR_API_KEY"`
6.  **Run the Flask backend:**
    ```bash
    flask run
    ```
    The backend API will start running at [http://127.0.0.1:5000](http://127.0.0.1:5000).

**Frontend Setup (React):**

1.  **Navigate to the frontend directory** in your project (if you have a separate frontend folder, otherwise stay in the project root).
2.  **Install Node.js dependencies:**
    ```bash
    npm install  # or yarn install
    ```
3.  **Start the React development server:**
    ```bash
    npm start  # or yarn start
    ```
    The React frontend will open in your browser, usually at [http://localhost:3000](http://localhost:3000).

**Deployment to Vercel:**

1.  **Push your code to a GitHub repository** (you've already done this).
2.  **Create a Vercel account** at [https://vercel.com/](https://vercel.com/).
3.  **Import your project** from your GitHub repository to Vercel.
4.  **Configure Environment Variable:** In your Vercel project settings, add an environment variable named `GOOGLE_PRO_API_KEY` and set its value to your Gemini API key.
5.  **Vercel should automatically deploy** your application. You will get a `*.vercel.app` URL when deployment is complete.

## Usage Instructions

1.  **Access the application** in your browser at the URL provided by Vercel after deployment (or `http://localhost:3000` if running locally).
2.  **Paste the Job Description** into the "Job Description" textarea.  The more detailed the job description, the better the analysis.
3.  **Upload your Resume PDF** by clicking the "Upload Your Resume (PDF)" button and selecting your resume file.
4.  **Click the "Analyze My Resume" button.**
5.  **Wait for the analysis to complete.**  The application will display:
    *   **Job Description Match Score:** A percentage indicating resume-job description alignment.
    *   **Key Improvement Areas:** A list of keywords from the job description that are missing from your resume.
    *   **Professional Summary Highlights:** A summary of your resume's profile in relation to the job description.

## Contributing

Feel free to contribute to this project by submitting pull requests, reporting issues, or suggesting improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

