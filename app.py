import os
import streamlit as st
import google.generativeai as genai
import io
from time import sleep
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from docx import Document
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Google Gemini model configuration
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# Define prompt templates for each section
prompt_templates = {
    "Abstract": "Write a concise abstract for the project titled '{title}'. Provide an overview of the following Python code and summarize the key concepts, including any libraries or functions used:\n\n{code}\n\nPlease write the report in {language}.",
    "Introduction": "Introduce the project titled '{title}'. Describe its purpose and relevance based on the following Python code and explain any important components such as functions, loops, or conditionals:\n\n{code}\n\nPlease write the report in {language}.",
    "Methodology": "Explain the methodology used in the project titled '{title}'. Include a description of how the Python code works and discuss any important steps, like imports, functions, or algorithms used:\n\n{code}\n\nPlease write the report in {language}.",
    "Results and Discussion": "Summarize the results of running the following Python code and discuss any insights or outcomes related to the project titled '{title}':\n\n{code}\n\nPlease write the report in {language}.",
    "Conclusion": "Conclude the report for the project titled '{title}'. Summarize the findings and discuss the final outcome:\n\n{code}\n\nPlease write the report in {language}.",
    "Literature Survey": "Generate a literature survey for the project titled '{title}'. Provide relevant research papers and articles related to the concepts used in the code provided:\n\n{code}",
}

# Function to generate Gemini response
def get_gemini_response(prompt, retries=3):
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if attempt < retries - 1:
                sleep(2 ** attempt)  # Exponential backoff
            else:
                st.error(f"Failed after {retries} retries: {e}")
                return None

# Function to generate flowchart instructions
def generate_flowchart_from_gemini(code):
    try:
        prompt = f"""
        Analyze the following Python code and break it down into key tasks. 
        Describe the task, dependencies, and order of execution. 
        Return the workflow as a list of steps, with each step describing a task and its dependency.
        
        Python code:\n\n{code}
        """
        flowchart_instructions = get_gemini_response(prompt)
        if flowchart_instructions:
            return flowchart_instructions
        else:
            return "Unable to generate flowchart. Please try again."
    except Exception as e:
        st.error(f"Error generating flowchart: {e}")
        return "An error occurred while generating the flowchart."

# Function to generate a PDF file
def generate_pdf(content):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    text_object = c.beginText(30, 750)
    text_object.setFont("Times-Roman", 12)

    for line in content.split("\n"):
        text_object.textLine(line)
    c.drawText(text_object)
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer

# Function to generate a Word document
def generate_word(content):
    buffer = io.BytesIO()
    doc = Document()
    for line in content.split("\n"):
        doc.add_paragraph(line)
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Function to generate a plain text file
def generate_txt(content):
    buffer = io.BytesIO()
    buffer.write(content.encode("utf-8"))
    buffer.seek(0)
    return buffer

# Function to display the generated report
def display_generated_report(report_content, selected_sections):
    st.subheader("Generated Report")
    for section in selected_sections:
        # Find section content in the report
        section_start = report_content.find(f"### {section}")
        if section_start != -1:
            section_end = report_content.find("### ", section_start + len(section))
            section_content = report_content[section_start:section_end] if section_end != -1 else report_content[section_start:]
            st.markdown(section_content.strip())

# Streamlit UI
st.title("Automated Report Generator")

project_title = st.text_input("Project Title:")
project_code = st.text_area("Python Code:")
report_style = st.selectbox("Select Report Style:", ["Academic", "Business", "Technical"], index=0)

# Dropdown for sections
section_options = list(prompt_templates.keys())
selected_sections = st.multiselect("Select Sections to Generate:", section_options, default=section_options)

# Dropdown for selecting language
language = st.selectbox("Select Language for Report:", ["English", "Kannada", "Tamil", "Telugu"])

# Function to generate section reports
def generate_section_reports():
    complete_report = ""
    for section in selected_sections:
        prompt = prompt_templates[section].format(title=project_title, code=project_code, language=language)
        section_content = get_gemini_response(prompt)
        if section_content:
            complete_report += f"\n\n### {section}\n\n{section_content}"
    return complete_report

# Generate Report Button
if st.button("Generate Report"):
    if project_title and project_code:
        report_content = generate_section_reports()
        display_generated_report(report_content, selected_sections)

        # Provide options to download the report
        pdf_buffer = generate_pdf(report_content)
        word_buffer = generate_word(report_content)
        txt_buffer = generate_txt(report_content)

        st.download_button("Download as PDF", data=pdf_buffer, file_name="generated_report.pdf", mime="application/pdf")
        st.download_button("Download as Word", data=word_buffer, file_name="generated_report.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        st.download_button("Download as Text", data=txt_buffer, file_name="generated_report.txt", mime="text/plain")
    else:
        st.error("Please provide both a project title and code to generate the report.")

# Generate Workflow Steps Button
if st.button("Generate Workflow Steps"):
    if project_code:
        flowchart_instructions = generate_flowchart_from_gemini(project_code)
        st.subheader("Generated Workflow Steps")
        st.text(flowchart_instructions)
    else:
        st.error("Please provide Python code to generate the workflow steps.")
