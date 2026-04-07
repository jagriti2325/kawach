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
                st.image(image, caption=file.name, use_container_width=True)

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
                        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
                        border-radius: 16px;
                        padding: 24px;
                        border: 2px solid #e2e8f0;
                        margin-bottom: 20px;
                    }
                    .prediction-title {
                        font-size: 1.4rem;
                        font-weight: 700;
                        color: #0f172a;
                        margin-bottom: 16px;
                    }
                    .prediction-value {
                        font-size: 1.3rem;
                        font-weight: 600;
                        color: #1e293b;
                        margin: 12px 0;
                    }
                    .confidence-badge {
                        background: linear-gradient(135deg, #dbeafe 0%, #e0f2fe 100%);
                        border: 2px solid #0ea5e9;
                        border-radius: 12px;
                        padding: 12px 16px;
                        font-weight: 600;
                        color: #0c4a6e;
                        margin: 12px 0;
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

                st.markdown("""
                <style>
                .report-card {
                    background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
                    border-radius: 16px;
                    padding: 28px;
                    border: 2px solid #e2e8f0;
                    margin-bottom: 24px;
                }
                .report-title {
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: #0f172a;
                    margin-bottom: 20px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                .report-section {
                    margin-bottom: 20px;
                }
                .section-header {
                    font-size: 1.1rem;
                    font-weight: 700;
                    color: #1e293b;
                    margin-bottom: 12px;
                    padding-bottom: 8px;
                    border-bottom: 2px solid #e2e8f0;
                }
                .report-item {
                    color: #475569;
                    margin-bottom: 10px;
                    padding: 8px 0;
                    line-height: 1.6;
                }
                .status-badge {
                    display: inline-block;
                    background: linear-gradient(135deg, #dbeafe 0%, #e0f2fe 100%);
                    border: 2px solid #0ea5e9;
                    border-radius: 12px;
                    padding: 8px 16px;
                    font-weight: 600;
                    color: #0c4a6e;
                    margin-bottom: 16px;
                }
                </style>
                <div class='report-card'>
                    <div class='report-title'>📄 Medical Diagnostic Report</div>
                    <div class='status-badge'>Status: {report['status']}</div>
                    
                    <div class='report-section'>
                        <div class='section-header'>🔍 Finding</div>
                        <div class='report-item'>{report['finding']}</div>
                    </div>
                    
                    <div class='report-section'>
                        <div class='section-header'>📋 Description</div>
                        <div class='report-item'>{report['description']}</div>
                    </div>
                    
                    <div class='report-section'>
                        <div class='section-header'>⚠️ Key Symptoms</div>
                        {"".join([f"<div class='report-item'>• {symptom}</div>" for symptom in report['key_symptoms']])}
                    </div>
                    
                    <div class='report-section'>
                        <div class='section-header'>💊 Recommendations</div>
                        {"".join([f"<div class='report-item'>• {rec}</div>" for rec in report['recommendations']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("**Class Probabilities:**")
                st.table(report['probabilities'])
                st.caption(report['disclaimer'])
                st.caption(f"Report generated: {report['timestamp']}")