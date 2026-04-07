import streamlit as st
import torch
import numpy as np
import cv2
from PIL import Image
from pytorch_grad_cam import GradCAMPlusPlus
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from torchvision import transforms

from disease_info import generate_report
from models import load_model, get_info
from utils.transforms import default_transform
from config import device

def show_home_page():
    st.markdown("<div class='field-label'>Select Disease</div>", unsafe_allow_html=True)
    disease = st.selectbox("", ["Pneumonia", "Brain Tumor", "Breast Cancer", "Malaria", "Tuberculosis"], key="disease_select", label_visibility="collapsed")
    path, classes = get_info(disease)

    model = load_model(path, len(classes), disease)
    st.markdown("<div class='field-label'>Upload Images</div>", unsafe_allow_html=True)
    files = st.file_uploader("", type=["jpg","png","jpeg"], accept_multiple_files=True, key="file_upload")

    if files:
        for file in files:
            st.markdown("---")
            image = Image.open(file).convert("RGB")
            col1, col2 = st.columns(2)
            with col1:
                st.image(image, caption=file.name, width=500)

            if st.button(f"🔍 Analyze {file.name}", key=f"btn_{file.name}"):
                img_tensor = default_transform(image).unsqueeze(0).to(device)

                # CRITICAL FIX: Disable TTA and Scaling for TB to match Colab exactly
                use_tta = False if disease == "Tuberculosis" else True
                temp_scale = 1.0 if disease == "Tuberculosis" else 0.5

                with torch.no_grad():
                    if use_tta:
                        # Simple TTA for other models
                        flipped = transforms.RandomHorizontalFlip(p=1.0)(img_tensor)
                        out_orig = model(img_tensor)
                        out_flip = model(flipped)
                        output = (out_orig + out_flip) / 2
                    else:
                        output = model(img_tensor)

                    scaled_output = output / temp_scale
                    prob = torch.softmax(scaled_output, dim=1)
                    confidence, pred = torch.max(prob, 1)
                    result = classes[pred.item()]

                # Determine if disease is detected
                disease_detected = False
                if disease == "Malaria":
                    # For Malaria: Parasitized (index 0) = disease
                    disease_detected = (pred.item() == 0)
                else:
                    # For other diseases: disease is typically index 1
                    disease_detected = (pred.item() != 0)

                # -------------------------------
                # GRAD-CAM (Always show; grayscale overlay for normal results)
                # -------------------------------
                if hasattr(model, 'features'): # DenseNet (TB)
                    target_layer = model.features[-1]
                elif hasattr(model, 'layer4'): # ResNet
                    target_layer = model.layer4[-1]
                else: # EfficientNet
                    target_layer = model.conv_head if hasattr(model, 'conv_head') else model._blocks[-1]

                cam = GradCAMPlusPlus(model=model, target_layers=[target_layer])
                grayscale_cam = cam(input_tensor=img_tensor, targets=[ClassifierOutputTarget(pred.item())])[0]
                rgb_img = np.array(image.resize((224, 224))) / 255.0

                if disease_detected:
                    cam_image = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)
                else:
                    heatmap = np.uint8(255 * grayscale_cam)
                    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_GRAY2BGR)
                    rgb_uint8 = np.uint8(rgb_img * 255)
                    cam_image = cv2.addWeighted(rgb_uint8, 0.65, heatmap, 0.35, 0)

                probabilities = {cls: prob[0][i].item() for i, cls in enumerate(classes)}
                report = generate_report(disease, result, confidence.item(), probabilities)

                with col2:
                    st.markdown("""
                    <style>
                    .result-card {
                        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                        border-radius: 16px;
                        padding: 24px;
                        border: 2px solid #38bdf8;
                        margin-bottom: 20px;
                    }
                    .prediction-title {
                        font-size: 1.5rem;
                        font-weight: 900;
                        color: #38bdf8;
                        margin-bottom: 16px;
                    }
                    .prediction-value {
                        font-size: 1.3rem;
                        font-weight: 600;
                        color: #e2e8f0;
                        margin: 12px 0;
                    }
                    .confidence-badge {
                        background: linear-gradient(135deg, #06b6d4 0%, #0ea5e9 100%);
                        border: 2px solid #38bdf8;
                        border-radius: 12px;
                        padding: 12px 16px;
                        font-weight: 700;
                        color: #0f172a;
                        margin: 12px 0;
                        font-size: 1.1rem;
                        display: inline-block;
                    }
                    </style>
                    <div class='result-card'>
                        <div class='prediction-title'>🔍 Prediction Result</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if disease_detected:
                        st.error(f"⚠️ **Prediction:** {result}")
                    else:
                        st.success(f"✅ **Prediction:** {result}")
                    
                    confidence_pct = confidence.item() * 100
                    st.markdown(f"""<div class='confidence-badge'>📊 Confidence: {confidence_pct:.2f}%</div>""", unsafe_allow_html=True)
                    
                    st.image(cam_image, caption="AI Grad-CAM Analysis", use_container_width=True)
                    if disease_detected:
                        st.warning("🔴 **Red areas indicate regions of concern**")

                # Build the report HTML with proper variable interpolation
                st.markdown("""
                <style>
                .report-card {
                    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                    border-radius: 16px;
                    padding: 28px;
                    border: 2px solid #38bdf8;
                    margin-bottom: 24px;
                    box-shadow: 0 8px 24px rgba(56, 189, 248, 0.15);
                }
                .report-title {
                    font-size: 1.6rem;
                    font-weight: 900;
                    color: #38bdf8;
                    margin-bottom: 20px;
                    border-bottom: 3px solid #38bdf8;
                    padding-bottom: 12px;
                }
                .report-section {
                    margin-bottom: 24px;
                }
                .section-header {
                    font-size: 1.15rem;
                    font-weight: 800;
                    color: #06b6d4;
                    margin-bottom: 12px;
                    padding-bottom: 10px;
                    border-bottom: 2px solid #0ea5e9;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }
                .report-item {
                    color: #e2e8f0;
                    margin-bottom: 10px;
                    padding: 10px 12px;
                    line-height: 1.7;
                    background: rgba(15, 23, 42, 0.5);
                    border-left: 3px solid #0ea5e9;
                    border-radius: 4px;
                }
                .status-badge {
                    display: inline-block;
                    background: linear-gradient(135deg, #06b6d4 0%, #0ea5e9 100%);
                    border: 2px solid #38bdf8;
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-weight: 700;
                    color: #0f172a;
                    margin-bottom: 20px;
                    font-size: 1.05rem;
                    box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
                }
                </style>
                <div class='report-card'>
                    <div class='report-title'>📄 Medical Diagnostic Report</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Status badge
                st.markdown(f"<div style='display: inline-block; background: linear-gradient(135deg, #06b6d4 0%, #0ea5e9 100%); border: 2px solid #38bdf8; border-radius: 12px; padding: 12px 24px; font-weight: 700; color: #0f172a; font-size: 1.05rem;'>✓ Status: {report['status']}</div>", unsafe_allow_html=True)
                
                st.markdown("")
                
                # Finding
                st.markdown("<div class='section-header'>🔍 Finding</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='report-item'>{report['finding']}</div>", unsafe_allow_html=True)
                
                # Description
                st.markdown("<div class='section-header'>📋 Description</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='report-item'>{report['description']}</div>", unsafe_allow_html=True)
                
                # Key Symptoms
                st.markdown("<div class='section-header'>⚠️ Key Symptoms</div>", unsafe_allow_html=True)
                for symptom in report['key_symptoms']:
                    st.markdown(f"<div class='report-item'>• {symptom}</div>", unsafe_allow_html=True)
                
                # Recommendations
                st.markdown("<div class='section-header'>💊 Recommendations</div>", unsafe_allow_html=True)
                for rec in report['recommendations']:
                    st.markdown(f"<div class='report-item'>• {rec}</div>", unsafe_allow_html=True)
                
                st.markdown("**Class Probabilities:**")
                st.table(report['probabilities'])
                st.caption(report['disclaimer'])
                st.caption(f"Report generated: {report['timestamp']}")