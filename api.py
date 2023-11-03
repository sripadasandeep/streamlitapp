import streamlit as st
from PIL import Image
import io
import base64
import cv2
import requests
import json


def testingfunc(base64_string):
    try:
        # base64_string = 
        # Convert the Base64 string to binary data
        binary_data = base64.b64decode(base64_string)
        url = 'http://164.52.201.54:18080/verify_liveness'
        headers = {
            "Content-Type": "image/jpeg",  
        }
        r = requests.post(url,data=binary_data, headers=headers)
        json_object = json.loads(r.text)
        # print("json_object:",json_object)
        return json_object
    except Exception as e:
        print(f"requesting backend api issue:{e}")
        return {"error":"backend api requesting error."}

# Set a title for the Streamlit app
st.title("FaceLiveness Testing App")

# Create a sidebar selection for image source
image_source = st.sidebar.selectbox("Select Image Source", ("Capture from Webcam", "Upload from Local"))

if image_source == "Capture from Webcam":
    st.subheader("Webcam Capture")
    
    # # Use st.empty() to create a placeholder for the webcam image
    # webcam_image_placeholder = st.empty()
    
    # # Use st.button() to trigger image capture
    # if st.button("Capture Image"):
    #     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    #     ret, frame = cap.read()
    #     cap.release()

    #     # Save the captured image to a file
    #     if ret:
    #         cv2.imwrite("captured_image.jpg", frame)
    #         st.write("Image captured and saved as 'captured_image.jpg'")
    #     # Open and display the captured image
    #     captured_image = Image.open("captured_image.jpg")
    #     webcam_image_placeholder.image(captured_image, caption="Captured Image", use_column_width=True)
    #     # Open the image file
    #     with open("captured_image.jpg", "rb") as image_file:
    #         # Read the binary data of the image
    #         image_binary = image_file.read()

    #     # Encode the binary data as base64
    #     image_base64 = base64.b64encode(image_binary).decode()

    #     response = testingfunc(image_base64)
    #     print(response)
    #     st.write(response)
        

    img_file_buffer = st.camera_input("Take a picture")

    if img_file_buffer is not None:
        # To read image file buffer as bytes:
        bytes_data = img_file_buffer.getvalue()
        # st.write(type(bytes_data))
        image_base64 = base64.b64encode(bytes_data).decode()
        st.write("Photo captured Successfully and waiting for response...")
        response = testingfunc(image_base64)
        # print(response)
        st.write(response)
        
else:
    # Upload an image from the local system
    st.subheader("Upload Image")
    
    # Create a file uploader widget
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    # print(f"uploaded_image:{uploaded_image}")
    if uploaded_image is not None:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        print(type(image))
        print(image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes = image_bytes.getvalue()

        # Encode bytes in base64
        image_base64 = base64.b64encode(image_bytes).decode()

        response = testingfunc(image_base64)
        # print(response)
        st.write(response)
    
    
# Run the Streamlit app
