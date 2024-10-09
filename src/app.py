import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

API_URL = "http://127.0.0.1:8000/predict/"

def predict_image(image: Image.Image) -> requests.Response:
    """
    Send the given image to the backend API for malaria prediction.

    Args:
        image (Image.Image): The input image to be predicted.

    Returns:
        requests.Response: The response from the backend API.
    """
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    response = requests.post(API_URL, json={"image": img_str})
    return response

def main():
    """
    Main function to run the Streamlit app for malaria detection.
    """
    st.set_page_config(page_title="Malaria Detection", page_icon="🩺", layout="centered")
    st.title("🩺 Malaria Detection")
    st.markdown("Upload a blood cell image to check for malaria infection.")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Predict"):
            with st.spinner("Analyzing the image..."):
                response = predict_image(image)
                if response.status_code == 200:
                    prediction = response.json().get("prediction")
                    if prediction == 1:
                        st.success("The image indicates **malaria infection**.", icon="🔬")
                    else:
                        st.success("The image does not indicate malaria infection.", icon="✅")
                else:
                    st.error("Failed to process the image. Please try again.", icon="🚨")

if __name__ == "__main__":
    main()
