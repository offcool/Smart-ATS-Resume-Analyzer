# Smart ATS Resume Analyzer (Flask Backend + React Frontend)

[![Deployment Status](https://ats-modified-8ee4avlk4-semehs-projects.vercel.app/)]

## Overview

This project is a Smart Applicant Tracking System (ATS) Resume Analyzer designed to help job seekers optimize their search.  It evaluates resumes against job descriptions, providing a match percentage, identifying missing keywords, and generating a profile summary.

This repository is a modified version of an original Streamlit application.  The key enhancement is the separation of the application into a **Flask backend** and a **React frontend**. This architecture offers improved scalability, maintainability, and a better user experience, and is specifically configured for deployment on **Vercel**.

**Key Features:**

*   **ATS-Style Resume Analysis:**  Evaluates resumes against job descriptions, mimicking Applicant Tracking Systems.
*   **Google Gemini API Powered:**  Utilizes the advanced Google Gemini API for accurate and insightful resume analysis, specifically tailored for tech roles (Software Engineering, Data Science, Big Data Engineering, Data Analysis).
*   **Key Metrics:** Provides a "JD Match" percentage and identifies crucial "Missing Keywords" to help users tailor their resumes.
*   **Profile Summary:**  Generates a concise summary highlighting the resume's strengths and weaknesses in relation to the job description.
*   **Flask Backend (Python):**  Handles the resume analysis logic using the Gemini API and provides an API endpoint for the frontend.
*   **React Frontend:**  Offers a user-friendly interface for pasting job descriptions and uploading resumes (PDF format), displaying analysis results in a clear and organized manner.
*   **Vercel Deployment Ready:**  Configuration files (`vercel.json`) are included for easy deployment to the Vercel platform.

## Architecture

The application is structured with a clear separation of concerns:

*   **Frontend ( `resume-evaluator` directory):**
    *   Built with **React**.
    *   Handles user interface, input forms (job description text area, resume file upload), and displays results.
    *   Communicates with the backend API to send resume and job description data and receive analysis results.
    *   Uses `fetch` API to interact with the Flask backend.
    *   Located in the `resume-evaluator` directory.

*   **Backend ( `app.py` ):**
    *   Built with **Flask (Python)**.
    *   Exposes an API endpoint `/api/analyze` that receives resume and job description data.
    *   Uses `PyPDF2` to extract text from uploaded PDF resumes.
    *   Leverages the `google-generativeai` library and the Google Gemini API to perform resume analysis based on the provided prompt.
    *   Returns analysis results in **JSON format**.
    *   Located in the root directory as `app.py`.

*   **Deployment (Vercel):**
    *   Configured for deployment on **Vercel** using `vercel.json`.
    *   Vercel handles both the Flask backend and the React frontend deployment.

## Local Development

To run this application locally, you need to set up both the backend (Flask) and the frontend (React) separately.

**Backend (Flask API):**

1.  **Prerequisites:**
    *   Python 3.12 installed
    *   pip package installer
    *   Google Gemini API Key (Get one from [Google AI Studio](https://makersuite.google.com/app/apikey))

2.  **Set up Environment Variables:**
    *   Create a `.env` file in the root directory of the repository (where `app.py` is located).
    *   Add your Google Gemini API key to the `.env` file:
        ```
        GOOGLE_PRO_API_KEY=YOUR_API_KEY_HERE
        ```

3.  **Install Python Backend Dependencies:**
    Navigate to the root directory (where `app.py` is) in your terminal and run:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask Backend:**
    ```bash
    python app.py
    ```
    The Flask backend will start running locally (usually on `http://127.0.0.1:5000/`).

**Frontend (React App):**

1.  **Prerequisites:**
    *   Node.js and npm installed

2.  **Navigate to the Frontend Directory:**
    ```bash
    cd resume-evaluator
    ```

3.  **Install Frontend Dependencies:**
    ```bash
    npm install
    ```

4.  **Start the React Development Server:**
    ```bash
    npm start
    ```
    The React frontend will open in your browser (usually on `http://localhost:3000`).

**Accessing the Application Locally:**

*   Once both the backend and frontend are running, you can access the application by opening your browser and going to the address where your React frontend is running (usually `http://localhost:3000`). The React frontend will communicate with the Flask backend API running in the background.

## Deployment to Vercel

This application is configured for easy deployment to Vercel.

1.  **Vercel CLI:** Ensure you have the Vercel CLI installed. If not, install it following the instructions on the [Vercel website](https://vercel.com/docs/cli).

2.  **Vercel Account & Project:**  Make sure you have a Vercel account and have created a new project on Vercel.

3.  **Deploy from the Repository Root:**
    Navigate to the root directory of your repository (where `vercel.json` is located) in your terminal and run:
    ```bash
    vercel deploy
    ```

4.  **Follow Vercel CLI Prompts:** The Vercel CLI will guide you through the deployment process, linking your local project to your Vercel project.

5.  **Environment Variables on Vercel:**  After deployment, you need to set the `GOOGLE_PRO_API_KEY` environment variable in your Vercel project settings.
    *   Go to your Vercel project dashboard.
    *   Navigate to "Settings" -> "Environment Variables".
    *   Add a new environment variable:
        *   **Name:** `GOOGLE_PRO_API_KEY`
        *   **Value:** Your actual Google Gemini API key.

**After deployment is complete, Vercel will provide you with a deployment URL where your Smart ATS Resume Analyzer application will be live.**  Update the "Deployment Status" badge link at the top of this README with your Vercel project URL.

## Technologies Used

*   **Backend:**
    *   Python
    *   Flask
    *   google-generativeai
    *   PyPDF2
    *   dotenv

*   **Frontend:**
    *   React
    *   JavaScript
    *   HTML/CSS

*   **Deployment:**
    *   Vercel

## Future Improvements

*   **Enhanced Frontend Features:**  Add features like progress indicators, more detailed error handling, and improved result visualization.
*   **User Authentication:** Implement user accounts to save and manage resume analyses.
*   **Database Integration:**  Store analysis history and user data in a database.
*   **More Advanced ATS Features:**  Explore adding features like resume parsing for structured data extraction, job recommendation based on resume analysis, and integration with job boards.
*   **Model Fine-tuning:** Fine-tune the Gemini model for even better resume analysis accuracy in specific domains.

## License

[MIT License]

---
**Feel free to contribute to this project!**
