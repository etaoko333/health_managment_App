from dotenv import load_dotenv
import streamlit as st
import os
import boto3
from PIL import Image

load_dotenv()  # Load all the environment variables

# Initialize AWS Rekognition client
rekognition_client = boto3.client('rekognition', region_name='your-region',
                                   aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                                   aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))

## Function to analyze image with AWS Rekognition
def analyze_image(image):
    response = rekognition_client.detect_labels(
        Image={
            'Bytes': image
        },
        MaxLabels=10,
        MinConfidence=75
    )
    return response['Labels']

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return bytes_data
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize our Streamlit app
st.set_page_config(page_title="Health Management App")

st.header("Health Management App")
input_prompt = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image_data = ""

if uploaded_file is not None:
    image_data = input_image_setup(uploaded_file)
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Analyze Image")

if submit:
    labels = analyze_image(image_data)
    st.subheader("Detected Items:")
    for label in labels:
        st.write(f"{label['Name']} - {label['Confidence']:.2f}% confidence")