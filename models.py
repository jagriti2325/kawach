import streamlit as st
import torch
import torch.nn as nn
import torchvision.models as models
from config import device

@st.cache_resource
def load_model(path, num_classes, disease_type):
    # Load the state dict first to map to CPU/GPU
    state_dict = torch.load(path, map_location=device)

    # 1. Handle Tuberculosis (DenseNet-201)
    if disease_type == "Tuberculosis":
        model = models.densenet201(weights=None)
        # Based on your error log, the TB model expects 1920 -> 512
        model.classifier = nn.Sequential(
            nn.Linear(1920, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )

    # 2. Handle Pneumonia (DenseNet-121)
    elif disease_type == "Pneumonia":
        model = models.densenet121(weights=None)
        num_ftrs = model.classifier.in_features # This will be 1024
        model.classifier = nn.Sequential(
            nn.Linear(num_ftrs, 256),
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.Dropout(0.4),
            nn.Linear(256, num_classes)
        )

    # 3. Handle Other Architectures (EfficientNet/ResNet)
    elif any(k.startswith('_') or 'efficientnet' in path.lower() for k in state_dict.keys()):
        model = models.efficientnet_b0()
        model.classifier = nn.Sequential(
            nn.Linear(1280, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )
    elif 'layer1.0.conv3.weight' in state_dict:
        model = models.resnet50()
        model.fc = nn.Sequential(
            nn.Linear(2048, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )
    else:
        # Default fallback (ResNet-18)
        model = models.resnet18()
        model.fc = nn.Sequential(
            nn.Linear(512, 256),
            # ... rest of your resnet18 logic
            nn.Linear(256, num_classes)
        )

    # Load weights into the correctly initialized architecture
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model

def get_info(disease):
    if disease == "Pneumonia":
        # Updated to your new best model path
        return r"D:\Disease_detection\models\nimobest_model (1).pth", ["Normal", "Pneumonia"]
    elif disease == "Brain Tumor":
        return "models/bestbrain_model.pth", ["No Tumor", "Tumor"]
    elif disease == "Breast Cancer":
        return "models/best_breast.pth", ["benign", "malignant"]
    elif disease == "Malaria":
        return "models/best_malaria.pth", ["Parasitized", "Uninfected"]
    elif disease == "Tuberculosis":
        return r"D:\Disease_detection\models\tb_final_generalized_model.pth", ["Normal", "TB"]