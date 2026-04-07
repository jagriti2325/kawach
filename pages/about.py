import streamlit as st
from utils.transforms import get_disease_info

def show_about_page():
    # Header is now in main app.py

    st.markdown("""
    ### Welcome to the AI Diagnostic Hub

    Our platform leverages cutting-edge artificial intelligence and deep learning technologies
    to provide preliminary screening assistance for various medical conditions. We are committed
    to democratizing access to medical image analysis tools.

    ---

    #### 🎯 Our Mission

    To assist healthcare professionals in early disease detection and provide accessible preliminary
    screening tools for common medical conditions through advanced AI technologies.

    ---

    #### 🔬 How It Works

    1. **Image Upload**: Upload a medical image (X-ray, scan, etc.)
    2. **AI Analysis**: Our deep learning models analyze the image
    3. **Grad-CAM Visualization**: Visual explanation of AI decision (Red=Disease Areas, Green=Healthy)
    4. **Detailed Report**: Comprehensive analysis with confidence scores and recommendations

    ---

    #### 🏆 Supported Diseases

    """)

    # Display disease information
    diseases = ["Pneumonia", "Brain Tumor", "Breast Cancer", "Malaria", "Tuberculosis"]

    cols = st.columns(len(diseases))
    for idx, disease in enumerate(diseases):
        with cols[idx]:
            with st.expander(f"ℹ️ {disease}"):
                info = get_disease_info(disease)
                st.write(info.get("description", ""))

    st.markdown("""
    ---

    #### 📊 Technology Stack

    - **Deep Learning Frameworks**: PyTorch, TensorFlow
    - **Model Architectures**: ResNet, DenseNet, EfficientNet
    - **Visualization**: Grad-CAM++ for explainability
    - **Interface**: Streamlit for rapid deployment

    ---

    #### ⚠️ Important Disclaimer

    **This is a preliminary screening tool only.** Results should always be:
    - Verified by qualified healthcare professionals
    - Used in conjunction with clinical examination
    - Never used as the sole basis for medical diagnosis or treatment
    - Treated as supplementary to professional medical opinion

    **For medical emergencies, please contact your local healthcare provider immediately.**

    ---

    #### 🔒 Data Privacy & Security

    - All images are processed locally on your device
    - No images are stored on our servers
    - Your privacy is our top priority

    ---

    #### 📞 Contact & Support

    For questions, feedback, or technical issues, please contact our support team.

    **Version**: 2.0 | **Last Updated**: 2026
    """)