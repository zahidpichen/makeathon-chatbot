import streamlit as st
import time
import os
import PyPDF2
import google.generativeai as genai

# Define the directory containing PDF files
files = "Materials"
genai.configure(api_key="AIzaSyCE3tcMsUGVmI1-HM6G_tju1mpwlDnIvnA")

# Function to extract text from a single PDF file
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        extracted_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text
        return extracted_text


# Iterate over all files in the directory
for file in os.listdir(files):
    if file.endswith('.pdf'):
        pdf_path = os.path.join(files, file)  # Get the full path of the PDF file
        material_text = extract_text_from_pdf(pdf_path)  # Extract text from the PDF file

def stream_data(text:str):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)



def chatbot(material:str, user_prompt:str):
    chat_template = f"""
    
        You are a doubt clearing assistant, You clear students doubts based on the materials provided. 

        Steps to follow:
        1. Get the materials: {material}
        2. And, get the user prompt: {user_prompt}
        3. Analyze the user prompt and get the realevent data from the material
        4. Display it accordingly.

      """
    model = genai.GenerativeModel(
        model_name = "gemini-1.5-pro",
        system_instruction = chat_template
        )
    # generated_text = model.generate_content(user_prompt)
    chat = model.start_chat(
            history=[
                {"role": "user", "parts": user_prompt},
                {"role": "model", "parts": chat_template},
            ]
    )
    response = chat.send_message(user_prompt)
    text = response.text
    return text


st.title("Doubt Clearer")
prompt = st.chat_input("Enter your question")

if prompt:
    response = chatbot(material=material_text, user_prompt=prompt)
    flow = stream_data(text=response)
    st.write_stream(flow)
