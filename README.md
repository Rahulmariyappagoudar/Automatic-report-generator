Automated Report Generator
Project Overview
The Automated Report Generator is a Streamlit-based application that uses the Google Gemini API to generate structured reports based on Python code input. It supports creating reports in various styles (Academic, Business, Technical) and languages (English, Kannada, Tamil, Telugu). Additionally, the application can generate workflow steps from Python code to assist in visualizing its execution.

Features
Section-Based Report Generation: Generate specific sections such as Abstract, Introduction, Methodology, Results and Discussion, Conclusion, and Literature Survey.
Multi-Language Support: Supports report generation in English, Kannada, Tamil, and Telugu.
Customizable Report Styles: Choose between Academic, Business, or Technical styles.
Workflow Generation: Provides step-by-step instructions for creating flowcharts from Python code.
Download Options: Export the generated report as a PDF, Word, or plain text file.
Prerequisites
Install Python (version 3.8 or later).
Install the required Python libraries:
bash
Copy
Edit
pip install streamlit google-generativeai python-docx reportlab python-dotenv
Set up the Google Gemini API:
Obtain an API key and save it in a .env file with the following format:
makefile
Copy
Edit
GEMINI_API_KEY=your_api_key
Usage
Run the Application:
bash
Copy
Edit
streamlit run app.py
Enter Input:
Provide a project title and the Python code you want to analyze.
Select the report style and language.
Choose the sections you want to include in the report.
Generate Report:
Click on the "Generate Report" button to create the report.
Download the report in the desired format (PDF, Word, or text).
Generate Workflow Steps:
Click on "Generate Workflow Steps" to view step-by-step instructions for creating a flowchart based on the code.
File Structure
bash
Copy
Edit
project-directory/
├── app.py                # Main application script
├── .env                  # Environment variables (API key)
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation
Example Workflow Generation
If the Python code is provided, the application will analyze and generate a sequence of steps that describe the workflow and dependencies between different tasks.

Contributing
Contributions are welcome! Please submit issues or pull requests to improve the project.

