from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(upload_file):
    if upload_file is not None:
        bytes_data=upload_file.getvalue()
        image_parts=[
            {
                "mime_type": upload_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
st.set_page_config(page_title="Invoice Extractor")

st.header("Gemini Applicartion")
input=st.text_input("Input prompt: ",key="input")
upload_file= st.file_uploader("choose an image...",type=["jpg","jpeg","png","WEBP"])
image=""
if upload_file is not None:
    image=Image.open(upload_file)
    st.image(image,caption="Uploaded image.",use_column_width=True)
    
submit=st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoice.You will 
receive input image as invoice and you will have to 
answer question based on the input image.

"""
if submit:
    image_data=input_image_setup(upload_file)
    response=get_gemini_response(input_prompt,image_data,input)

    st.subheader("The Repsonse is")
    st.write(response)