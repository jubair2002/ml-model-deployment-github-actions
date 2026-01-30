"""
Plant Disease Detection — Streamlit app.
Predicts: Corn-Common_rust, Potato-Early_blight, Tomato-Bacterial_spot.
"""
import os
import numpy as np
import streamlit as st
import cv2
from tensorflow.keras.models import load_model

# Same folder as this script (self-contained app folder)
_APP_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.environ.get(
    "MODEL_PATH",
    os.path.join(_APP_DIR, "plant_disease_model.h5"),
)
IMG_SIZE = 256
CLASS_NAMES = (
    "Corn-Common_rust",
    "Potato-Early_blight",
    "Tomato-Bacterial_spot",
)


@st.cache_resource
def load_predictor():
    """Load model once and cache."""
    if not os.path.isfile(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    return load_model(MODEL_PATH)


def preprocess(image_bgr, size=(IMG_SIZE, IMG_SIZE)):
    """Resize and shape for model: (1, H, W, 3)."""
    resized = cv2.resize(image_bgr, size)
    return resized.reshape(1, *size, 3)


def main():
    st.set_page_config(page_title="Plant Disease Detection", page_icon="🌱")
    st.title("Plant Disease Detection")
    st.markdown("Upload a leaf image to predict disease (Corn, Potato, Tomato).")

    try:
        model = load_predictor()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    plant_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    submit = st.button("Predict disease")

    if submit and plant_image is not None:
        file_bytes = np.asarray(bytearray(plant_image.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if opencv_image is None:
            st.error("Could not decode image. Try another file.")
            return

        st.image(opencv_image, channels="BGR", use_container_width=True)

        with st.spinner("Predicting..."):
            X = preprocess(opencv_image)
            Y_pred = model.predict(X, verbose=0)
            idx = int(np.argmax(Y_pred[0]))
            label = CLASS_NAMES[idx]
            confidence = float(Y_pred[0][idx])

        plant_name = label.split("-")[0]
        disease_name = label.split("-", 1)[1].replace("_", " ")
        st.success(f"This is a **{plant_name}** leaf with **{disease_name}**.")
        st.caption(f"Confidence: {confidence:.2%}")


if __name__ == "__main__":
    main()
