import streamlit as st
from pypdf import PdfReader 
import os
from lyzr_functions import send_cold_email

# Save information on a text file that acts as memory for LLM
def save_to_text_file(text_value, mode):
    data_directory = "data"
    os.makedirs(data_directory, exist_ok=True)

    text_file_path = os.path.join(data_directory, 'instructions.txt')
    with open(text_file_path, mode) as file:
        file.write(text_value)

# Parse Resume
def read_pdf(pdf_file_path):
    reader = PdfReader(pdf_file_path) 
    extracted_text = ''.join(page.extract_text() for page in reader.pages)
    return extracted_text

# Resume Input
uploaded_file = st.file_uploader("Upload Resume", type='pdf')

# Job Description Input
job_description = st.text_area("Enter Job Description")

# List of Emails to Send Input
email_ids = st.text_input('List of Emails', placeholder='Email1, Email2,...')

# Name and Contact to sign the email
contact_info = st.text_input('Your contact info (to sign the email)', placeholder='Name, Phone Number')

# env Variables to send email
user_email_address = st.text_input('Your email address')
app_password = st.text_input('Your app password')

is_send_email = st.button('Send Email!')
if is_send_email:
    # If fields are empty
    if not email_ids or not job_description or not uploaded_file or not contact_info or not user_email_address or not app_password:
        st.error('Enter all the fields!')
    else:
        os.environ["PASSWORD"] = app_password
        os.environ["EMAIL"] = user_email_address
        email_list = email_ids.split(',')
        email_list = [email.strip() for email in email_list] # make a list of emails
        extracted_pdf_text = read_pdf(uploaded_file) # parse pdf
        save_to_text_file(text_value = extracted_pdf_text, mode = "w") # save pdf in txt file
        save_to_text_file(text_value = "\nJob Description : \n" + job_description, mode = "a") # save job desctiption in txt file
        send_cold_email(email_list, contact_info) # send email using Lyzr Automata
        st.success("Email sent!")