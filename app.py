import streamlit as st
import os
import io
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import PyPDF2 as pdf



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input_text, pdf_text, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input_text, pdf_text, prompt])
    return response.text

#Input setup of pdf
def input_pdf_setup(uploaded_file):
  if uploaded_file is not None:
      pdf_reader = pdf.PdfReader(uploaded_file)
      pdf_text = ""
      for page_num in range(len(pdf_reader.pages)):
          page = pdf_reader.pages[page_num]
          pdf_text += page.extract_text()

      return pdf_text
  else:
        raise FileNotFoundError("No file uploaded")


# app setup
st.set_page_config(page_title="SkillMatch",
page_icon=":clipboard:", )

# Navigation Bar with Tabs
# st.sidebar.image("images/resume.ico", use_column_width=True)
navigation = st.sidebar.title("Select Role")
# st.image(""C:\Users\harsh\Downloads\skillmatch-high-resolution-logo-transparent (1).png" , use_column_width=True)
st.header("SKILLMATCH📋")
st.markdown("Where Talent Meets Opportunity!")


selected_tab = st.sidebar.selectbox("", ["HR", "Applicant"])

     #-------------------------------------------------------------------#



# Setup  for HR part

#Select Role
if selected_tab == "HR":
    st.header("HR - Resume Advisor")
    st.markdown("Find your perfect match  for the job role.")
    input_text = st.text_area("Job Description:", key="input")
    uploaded_file = st.file_uploader("Upload your Resume (PDF only):", type=["pdf"])

    def display_buttons_hr():
        if uploaded_file is not None:
            st.write("PDF Uploaded Successfully")

        submit1 = st.button("Resume Summary")
        submit2 = st.button("Percentage Match for job description")
        return {
            "submit1": submit1,
            "submit2": submit2
        }



    def show_response_hr(buttons, input_prompts):
        if buttons["submit1"] and uploaded_file is not None:
            with st.spinner("Generating response..."):  # Add progress bar
                pdf_text = input_pdf_setup(uploaded_file)
                try:
                    response = get_gemini_response(input_prompts["HR_Summary"], pdf_text, input_text)
                except KeyError:
                    st.error("Prompt for 'Resume Summary' not found. Please check the code.")
                    return
                st.subheader("The Response is")
                st.write(response)

        elif buttons["submit2"] and uploaded_file is not None:
            with st.spinner("Generating response..."):  # Added progress bar
                pdf_text = input_pdf_setup(uploaded_file)
                try:
                    response = get_gemini_response(input_prompts["HR_Match"], pdf_text, input_text)
                except KeyError:
                    st.error("Prompt for 'Percentage Match' not found. Please check the code.")
                    return
                st.subheader("The Response is")
                st.write(response)

        else:
            if uploaded_file is None:
                st.write("Please upload the resume")

    buttons_hr = display_buttons_hr()
    input_prompts = {
        "HR_Summary": """
           your task is to review the provided pdf of  resume against the job description and give summary of the resume. 
  if job description not given then dont compare with anything , just give summary of the resume. Also provide any links mentioned in Resume , if any 
  if job description given then only tell Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
        """,
        "HR_Match": """
            You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
            your task is to evaluate the resume against the provided job description. Give me the percentage match in big fonts and bold if the resume matches
            the job description. also write a small review """
     }
    show_response_hr(buttons_hr, input_prompts)



             #------------------------------------------------------------#



        #Applicant part setup
if selected_tab == "Applicant":
    st.header("Applicant - Resume Advisor")
    st.markdown("Elevate your resume from ordinary to extraordinary with Resume Advisor's personalized tips.")
    input_text = st.text_area("Job Description:", key="input")
    uploaded_file = st.file_uploader("Upload your Resume (PDF only):", type=["pdf"])

    # Function to display success message and buttons for HR
    def display_buttons_app():
        if uploaded_file is not None:
            st.write("PDF Uploaded Successfully")

        submit3 = st.button("How to Enhance my resume ")
        return {
            "submit3": submit3,
        }


    # Function to display response based on button clicked for HR
    def show_response_app(buttons, input_prompts):
        if buttons["submit3"] and uploaded_file is not None:
            with st.spinner("Generating response..."):  # Added progress bar
                pdf_text = input_pdf_setup(uploaded_file)
                try:
                    response = get_gemini_response(input_prompts["APP_IMP"], pdf_text, input_text)
                except KeyError:
                    st.error("Prompt for 'Improvement' not found. Please check the code.")
                    return
                st.subheader("The Response is")
                st.write(response)


        else:
            if uploaded_file is None:
                st.write("Please upload the resume")

    buttons_app = display_buttons_app()
    input_prompts = {
        "APP_IMP": """
            You are an experienced technical human resource manager your task is to review the provided resume(PDF) againts the job desciption and  Tell what points to be improved by compairing the resume with job description only, what skills are missing, what should be the improvement. 
            First mention what are the missing skills and skills need to be added (in  rows and cloumns format) , there should be 2 columns 1st coloumn will be Missing Skills and 2nd will be Skill to be added(remember give this rows and columns) . then atlast give some recommendations """

    }
    show_response_app(buttons_app, input_prompts )
        #-----------------------------------------------------#


footer_col1, footer_col2, footer_col3 = st.columns([1, 6, 1])
with footer_col2:
    st.write('Gemini AI powered Resume Advisor model  build by Harsh')

# Display link for users to connect with you using emojis
    st.write("Connect with me 👉 [here](https://kumarharsh.vercel.app/)")




