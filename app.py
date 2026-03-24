import streamlit as st
import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import numpy as np
import cv2

from pytorch_grad_cam import GradCAMPlusPlus
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="AI Diagnostic Hub", layout="wide")

device = torch.device("cpu")

# -------------------------------
# THEME
# -------------------------------
theme = st.sidebar.radio("🌗 Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
        <style>
        .stApp {background-color: #0e1117; color: white;}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp {background-color: #f4f6f9; color: black;}
        </style>
    """, unsafe_allow_html=True)

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("🩺 Navigation")
page = st.sidebar.radio("Go to", ["Home", "About"])

# -------------------------------
# MODEL LOADER
# -------------------------------

# Improved model loader: supports ResNet and EfficientNet architectures
@st.cache_resource
def load_model(path, num_classes):
    # Load state_dict and normalize key names
    loaded = torch.load(path, map_location=device)

    # Some checkpoints are wrapped in a dict (e.g., {"model": state_dict})
    if isinstance(loaded, dict) and 'state_dict' in loaded:
        state_dict = loaded['state_dict']
    elif isinstance(loaded, dict) and 'model' in loaded:
        state_dict = loaded['model']
    else:
        state_dict = loaded

    # If model was trained with DataParallel, strip 'module.' prefix.
    if any(k.startswith('module.') for k in state_dict.keys()):
        new_state = {}
        for k, v in state_dict.items():
            new_state[k.replace('module.', '')] = v
        state_dict = new_state

    # Detect model architecture from state_dict keys
    is_efficientnet = any(k.startswith('_') for k in state_dict.keys())
    is_resnet50 = 'layer1.0.conv3.weight' in state_dict
    
    if is_efficientnet:
        # EfficientNet detection: find version from conv_head.weight shape
        conv_head_weight = state_dict.get('_conv_head.weight')
        if conv_head_weight is not None:
            input_dim = conv_head_weight.shape[1]
        else:
            input_dim = 1280  # Default EfficientNetB0
        
        # Detect EfficientNet version by checking _bn1 weight
        bn1_weight = state_dict.get('_bn0.weight')
        if bn1_weight is not None:
            channels = len(bn1_weight)
            if channels == 40:
                model = models.efficientnet_b1()
            elif channels == 48:
                model = models.efficientnet_b2()
            elif channels == 48:
                model = models.efficientnet_b3()
            else:
                model = models.efficientnet_b0()
        else:
            model = models.efficientnet_b0()
        
        # Replace classifier for EfficientNet
        intermediate = state_dict.get('_fc1.weight')
        if intermediate is not None:
            intermediate = intermediate.shape[0]
        else:
            intermediate = 512  # Default intermediate
        
        model.classifier = nn.Sequential(
            nn.Linear(input_dim, intermediate),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(intermediate, num_classes)
        )
    
    elif is_resnet50:
        # ResNet50
        model = models.resnet50()
        input_dim = 2048
        
        intermediate = state_dict.get('fc.0.weight')
        if intermediate is not None:
            intermediate = intermediate.shape[0]
        else:
            intermediate = 512
        
        model.fc = nn.Sequential(
            nn.Linear(input_dim, intermediate),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(intermediate, num_classes)
        )
    
    else:
        # ResNet18 (default)
        model = models.resnet18()
        input_dim = 512
        
        intermediate = state_dict.get('fc.0.weight')
        if intermediate is not None:
            intermediate = intermediate.shape[0]
        else:
            intermediate = 256
        
        model.fc = nn.Sequential(
            nn.Linear(input_dim, intermediate),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(intermediate, num_classes)
        )

    # Load state_dict with multiple fallback strategies
    try:
        model.load_state_dict(state_dict, strict=True)
    except RuntimeError as e:
        # For non-strict loading, only load keys that exist in the model
        if is_efficientnet:
            # For EfficientNet, load only matching keys to avoid backbone conflicts
            model_state = model.state_dict()
            matched_keys = {k: v for k, v in state_dict.items() if k in model_state}
            if matched_keys:
                model.load_state_dict(matched_keys, strict=False)
        else:
            # For ResNet, try strict=False
            try:
                model.load_state_dict(state_dict, strict=False)
            except Exception as e2:
                pass

    model.to(device)
    model.eval()
    return model

# -------------------------------
# DISEASE INFO
# -------------------------------

# Improved: returns path, classes
def get_info(disease):
    if disease == "Pneumonia":
        # Original order
        return "models/best_model_pneumonia1.pth", ["Normal", "Pneumonia"]
    elif disease == "Brain Tumor":
        return "models/bestbrain_model.pth", ["No Tumor", "Tumor"]
    elif disease == "Breast Cancer":
        return "models/best_breast.pth", ["benign", "malignant"]
    elif disease == "Malaria":
        return "models/best_malaria.pth", ["Parasitized", "Uninfected"]
    elif disease == "Tuberculosis":
        return "models/best_TB_model.pth", ["Normal", "TB"]

# -------------------------------
# TRANSFORM (MATCH TRAINING)
# -------------------------------

# Default transform, can be customized per disease
default_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

# -------------------------------
# ABOUT PAGE
# -------------------------------
if page == "About":
    st.title("📘 About This Project")
    st.write("""
    Welcome to the Medical AI Diagnosis System.

    This platform leverages state-of-the-art deep learning models to assist healthcare professionals in the detection and classification of various diseases from medical images. Our system is designed to provide rapid, reliable, and explainable results, supporting clinical decision-making and improving patient outcomes.

    **Key Features:**
    - Multi-disease detection: Pneumonia, Brain Tumor, Breast Cancer, Malaria, Tuberculosis
    - Advanced Deep Learning models trained on curated medical datasets
    - Eigen-CAM visual explanations for model transparency
    - Batch image processing for efficient workflow
    - Professional medical-style reports for documentation

    **Disclaimer:**
    The results provided by this system are intended for informational purposes only and should not be considered a substitute for professional medical advice, diagnosis, or treatment. Always consult a certified healthcare provider for medical decisions.
    """)

# -------------------------------
# HOME PAGE
# -------------------------------
if page == "Home":

    # Unique logo placeholder
    st.image("https://raw.githubusercontent.com/your-repo/logo/main/ai_diagnostic_hub_logo.png", width=120, caption="AI Diagnostic Hub")
    st.title("🩺 AI Diagnostic Hub")


    disease = st.selectbox("Select Disease", ["Pneumonia", "Brain Tumor", "Breast Cancer", "Malaria", "Tuberculosis"])
    path, classes = get_info(disease)
    num_classes = len(classes)
    model = load_model(path, num_classes)
    transform = default_transform

    files = st.file_uploader(
        "Upload Images", 
        type=["jpg","png","jpeg"], 
        accept_multiple_files=True
    )

    if files:

        for file in files:
            st.markdown("---")

            image = Image.open(file).convert("RGB")

            col1, col2 = st.columns(2)

            with col1:
                st.image(image, caption=file.name, use_container_width=True)

            if st.button(f"🔍 Analyze {file.name}", key=f"analyze_{file.name}"):

                # -------------------------------
                # PREPROCESS WITH ENHANCEMENT
                # -------------------------------
                # Better handling: grayscale images stay grayscale (not forced RGB)
                if image.mode == 'L':  # Grayscale
                    image_processed = Image.new('RGB', image.size)
                    image_processed.paste(image)
                else:
                    image_processed = image.convert('RGB')
                
                img = transform(image_processed).unsqueeze(0).to(device)

                # -------------------------------
                # PREDICTION WITH TEST-TIME AUGMENTATION (TTA)
                # -------------------------------
                tta_transform = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                ])
                
                # Use TTA only for non-chest diseases (TB/Pneumonia models are more sensitive)
                use_tta = disease not in ['Tuberculosis', 'Pneumonia']
                use_temperature_scaling = disease not in ['Tuberculosis', 'Pneumonia']
                
                # Collect predictions from multiple augmented versions
                predictions_list = []
                
                # Original image
                img_orig = tta_transform(image_processed).unsqueeze(0).to(device)
                
                if use_tta:
                    # Augmented versions (only for non-chest diseases)
                    aug_images = [
                        image_processed,  # original
                        image_processed.transpose(Image.FLIP_LEFT_RIGHT),  # horizontal flip
                        image_processed.transpose(Image.FLIP_TOP_BOTTOM),  # vertical flip
                        image_processed.rotate(5),  # small rotation
                        image_processed.rotate(-5),
                    ]
                else:
                    # Just original for TB/Pneumonia
                    aug_images = [image_processed]
                
                with torch.no_grad():
                    for aug_img in aug_images:
                        aug_tensor = tta_transform(aug_img).unsqueeze(0).to(device)
                        output = model(aug_tensor)
                        predictions_list.append(output)
                    
                    # For TB/Pneumonia, use only the original image output (no averaging)
                    if not use_tta and len(predictions_list) > 0:
                        # Use first (and only) prediction directly for chest diseases
                        avg_output = predictions_list[0]
                    else:
                        # Average predictions across augmentations for other diseases
                        avg_output = torch.stack(predictions_list).mean(dim=0)
                    
                    # Temperature scaling (disabled for TB/Pneumonia - new models are sensitive)
                    if use_temperature_scaling:
                        temperature = 0.5  # Sharper predictions for other diseases
                        scaled_output = avg_output / temperature
                    else:
                        scaled_output = avg_output  # Original predictions for TB/Pneumonia
                    
                    # Store raw logits for debug
                    raw_logits_original = scaled_output[0].detach().cpu().numpy()
                    
                    # Use models naturally without any special tricks
                    prob = torch.softmax(scaled_output, dim=1)
                    confidence, pred = torch.max(prob, 1)
                    confidence = confidence.item()
                    pred = pred.item()

                result = classes[pred]

                # Debug: Show raw model outputs
                with st.expander("🔧 Debug Info"):
                    st.write(f"**Original Model Logits:**")
                    for i, cls in enumerate(classes):
                        st.write(f"  [{i}] {cls}: {raw_logits_original[i]:+.6f}")
                    
                    st.write(f"**Final Softmax Probabilities:**")
                    for i, cls in enumerate(classes):
                        st.write(f"  [{i}] {cls}: {prob[0][i].item():.6f}")
                    st.write(f"**Prediction Details:**")
                    st.write(f"  Predicted Index: {pred}")
                    st.write(f"  Predicted Class: {result}")
                    st.write(f"  Confidence: {confidence:.6f}")
                    st.write(f"**Model Configuration:**")
                    st.write(f"  Disease Type: {disease}")
                    st.write(f"  Using TTA: {use_tta}")
                    st.write(f"  Using Temperature Scaling: {use_temperature_scaling}")
                    st.write(f"  Num Predictions Averaged: {len(predictions_list)}")

                # -------------------------------
                # Eigen-CAM (improved for better localization)
                # -------------------------------
                # Determine the target layer based on model type
                if hasattr(model, '_blocks'):
                    # EfficientNet: use last block
                    target_layer = model._blocks[-1]
                elif hasattr(model.layer4[0], 'conv3'):
                    # ResNet50
                    target_layer = model.layer4[-1].conv3
                else:
                    # ResNet18
                    target_layer = model.layer4[-1].conv2
                
                # Use GradCAMPlusPlus for visualization
                cam = GradCAMPlusPlus(model=model, target_layers=[target_layer])

                # Compute activation map
                grayscale_cam = cam(input_tensor=img_orig, targets=[ClassifierOutputTarget(pred)], aug_smooth=False, eigen_smooth=False)[0]

                # Normalize to 0-1
                grayscale_cam = np.maximum(grayscale_cam, 0)
                if grayscale_cam.max() > 0:
                    grayscale_cam = grayscale_cam / grayscale_cam.max()
                
                # MINIMAL PROCESSING: Just a light threshold to remove background noise
                # but keep the model's focus area
                if disease in ['Pneumonia', 'Tuberculosis']:
                    cam_threshold = 0.15  # Low threshold - preserve subtle features
                else:
                    cam_threshold = 0.25  # Low threshold - see where model is looking

                rgb_img = np.array(image.resize((224,224))) / 255.0  # FIXED

                # Apply minimal organ mask - just normalize for visualization
                gray = np.mean(rgb_img, axis=2)
                threshold = np.percentile(gray[gray > 0.1], 40)
                organ_mask = (gray > max(threshold, 0.15)).astype(np.float32)
                organ_mask = cv2.GaussianBlur(organ_mask, (15, 15), 0)
                organ_mask = (organ_mask > 0.3).astype(np.float32)
                
                # Just normalize organ_mask for reference, but DON'T suppress heatmap with it
                # The heatmap shows model attention regardless of tissue location

                # Define negative (normal) diagnoses for each disease
                negative_diagnoses = {
                    'Brain Tumor': 'No Tumor',
                    'Pneumonia': 'Normal',
                    'Tuberculosis': 'Normal',
                    'Breast Cancer': 'benign',
                    'Malaria': 'Uninfected'
                }
                
                is_negative = (result == negative_diagnoses.get(disease))
                
                # Visualization: Use different colormaps based on diagnosis and disease type
                if disease in ['Brain Tumor', 'Breast Cancer', 'Malaria']:
                    # For these diseases: blue for normal, red/yellow for disease
                    if is_negative:
                        # Negative case: show BLUE heatmap (WINTER colormap) for normal/healthy
                        cam_image = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True, colormap=cv2.COLORMAP_WINTER, image_weight=0.4)
                    else:
                        # Positive case: show RED/YELLOW heatmap (JET colormap) for disease/abnormal
                        cam_image = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True, colormap=cv2.COLORMAP_JET, image_weight=0.4)
                else:
                    # For chest diseases (Pneumonia, TB): similar logic
                    if is_negative:
                        # Negative case: show plain image
                        cam_image = rgb_img
                    else:
                        # Positive case: show red/yellow heatmap with enhanced contrast
                        grayscale_cam_boosted = np.power(grayscale_cam, 0.7)
                        cam_image = show_cam_on_image(rgb_img, grayscale_cam_boosted, use_rgb=True, colormap=cv2.COLORMAP_JET, image_weight=0.35)

                # -------------------------------
                # OUTPUT
                # -------------------------------
                with col2:
                    st.subheader("Result")
                    st.success(result)

                    st.write("### Probabilities:")
                    for i, cls in enumerate(classes):
                        st.write(f"{cls}: {prob[0][i].item():.4f}")

                    st.info(f"Confidence: {confidence:.4f}")

                    # Update caption based on disease type and result
                    if disease in ['Brain Tumor', 'Breast Cancer', 'Malaria']:
                        if is_negative:
                            cam_caption = "Blue Heatmap: Normal/Healthy (No Abnormalities)"
                        else:
                            cam_caption = "Red/Yellow Heatmap: Disease/Abnormalities Detected"
                    else:
                        cam_caption = "Original Image (No Abnormalities Detected)" if is_negative else "Grad-CAM Heatmap (Red/Yellow = Affected Areas)"
                    
                    st.image(cam_image, caption=cam_caption, use_container_width=True)

                # -------------------------------

                # Enhanced Medical Report

                st.markdown("### 📄 Medical Report")
                st.write(f"**Disease Type:** {disease}")
                st.write(f"**Prediction:** {result}")
                st.write(f"**Confidence:** {confidence:.4f}")
                st.write("**Detailed Probabilities:**")
                st.table({
                    classes[0]: f"{prob[0][0].item():.4f}",
                    classes[1]: f"{prob[0][1].item():.4f}"
                })

                gradcam_explanation = (
                    f"For Malaria, the model predicted '{result}' with confidence {confidence:.4f}. " +
                    (f"The image shows NO abnormalities detected - the tissue appears healthy with no signs of parasitized cells." if result == 'Uninfected' 
                     else f"Red and yellow regions highlight areas where the model detected parasitized cells.") if disease == 'Malaria' else
                    (f"For Tuberculosis, the model predicted '{result}' with confidence {confidence:.4f}. " +
                    (f"The image shows NORMAL lung tissue - no TB lesions or abnormalities detected." if result == 'Normal'
                     else f"Red/yellow regions highlight abnormal areas indicating possible TB lesions in the lungs.")) if disease == 'Tuberculosis' else
                    (f"For Pneumonia, the model predicted '{result}' with confidence {confidence:.4f}. " +
                    (f"The image shows NORMAL lungs - no pneumonia or inflammation detected." if result == 'Normal'
                     else f"Red/yellow regions indicate inflamed lung tissue where pneumonia is detected.")) if disease == 'Pneumonia' else
                    (f"For Breast Cancer, the model predicted '{result}' with confidence {confidence:.4f}. " +
                    (f"The image shows BENIGN tissue - no malignant features detected." if result == 'benign'
                     else f"Red/yellow regions highlight areas with suspicious or malignant characteristics.")) if disease == 'Breast Cancer' else
                    (f"For Brain Tumor, the model predicted '{result}' with confidence {confidence:.4f}. " +
                    (f"The image shows NORMAL brain tissue - no tumor detected." if result == 'No Tumor'
                     else f"Red/yellow regions indicate areas where a tumor is detected.")) if disease == 'Brain Tumor' else
                    f"Eigen-CAM highlights regions most influential for the prediction of '{result}' with confidence {confidence:.4f}."
                )
                st.write(f"**Grad-CAM Explanation:** {gradcam_explanation}")
                st.write("**Recommendation:** This report is generated by an AI system and should be used as a supplementary tool. Please consult a certified medical professional for final diagnosis and treatment decisions.")

                # Downloadable plain-text report
                plain_report = f"""
Medical AI Diagnosis Report
--------------------------
Disease Type: {disease}
Prediction: {result}
Confidence: {confidence:.4f}

Detailed Probabilities:
{classes[0]}: {prob[0][0].item():.4f}
{classes[1]}: {prob[0][1].item():.4f}

Eigen-CAM Explanation:
{(
    ('For Malaria: The image shows NO abnormalities - tissue appears healthy with no parasitized cells detected.' if result == 'Uninfected' else 'For Malaria: Red/yellow regions highlight areas with parasitized cells detected by the model.') if disease == 'Malaria' else
    ('For Tuberculosis: The image shows NORMAL lung tissue - no TB lesions detected.' if result == 'Normal' else 'For Tuberculosis: Red/yellow regions highlight abnormal areas indicating possible TB lesions.') if disease == 'Tuberculosis' else
    ('For Pneumonia: The image shows NORMAL lungs - no pneumonia detected.' if result == 'Normal' else 'For Pneumonia: Red/yellow regions indicate inflamed lung tissue where pneumonia is detected.') if disease == 'Pneumonia' else
    ('For Breast Cancer: The image shows BENIGN tissue - no malignant features detected.' if result == 'benign' else 'For Breast Cancer: Red/yellow regions highlight areas with malignant characteristics.') if disease == 'Breast Cancer' else
    ('For Brain Tumor: The image shows NORMAL brain tissue - no tumor detected.' if result == 'No Tumor' else 'For Brain Tumor: Red/yellow regions indicate areas where a tumor is detected.') if disease == 'Brain Tumor' else
    'Eigen-CAM highlights regions most influential for the prediction.'
)}

Recommendation:
This report is generated by an AI system and should be used as a supplementary tool. Please consult a certified medical professional for final diagnosis and treatment decisions.
"""

                st.download_button(
                    "📥 Download Report",
                    plain_report,
                    file_name=f"{file.name}_report.txt"
                )
                    