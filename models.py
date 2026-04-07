import streamlit as st
import torch
import torch.nn as nn
import torchvision.models as models
from config import device
import gdown
import os

# ✅ Download function
def download_model(file_id, output):
    if not os.path.exists(output):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output, quiet=False)


@st.cache_resource
def load_model(path, num_classes, disease_type):

    # ✅ FILE ID mapping
    FILE_IDS = {
        "best_breast.pth": "1m4qUmlR2ZsCLKsHwxAvUv3QYN-yafDfs",
        "bestbrain_model.pth": "1xOy8OFwcoZnVadUkp1e5aKPTKeOEtKqb",
        "best_malaria.pth": "1_KeqAG8T3ZAVnVEca834hZr8DXau3WlS",
        "nimobest_model.pth": "1M9yZEJe6QwCxhhh2kLj483J7A5pX314k",
        "tb_final_generalized_model.pth": "1gW-_JZsHvQm25snAypUgHDdaOuhgEYGZ"
    }

    # ✅ Download model first
    download_model(FILE_IDS[path], path)

    # ✅ Load state dict AFTER download
    state_dict = torch.load(path, map_location=device)

    # 1. Tuberculosis (DenseNet-201)
    if disease_type == "Tuberculosis":
        model = models.densenet201(weights=None)
        model.classifier = nn.Sequential(
            nn.Linear(1920, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )

    # 2. Pneumonia (DenseNet-121)
    elif disease_type == "Pneumonia":
        model = models.densenet121(weights=None)
        num_ftrs = model.classifier.in_features
        model.classifier = nn.Sequential(
            nn.Linear(num_ftrs, 256),
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.Dropout(0.4),
            nn.Linear(256, num_classes)
        )

    # 3. EfficientNet
    elif any(k.startswith('_') or 'efficientnet' in path.lower() for k in state_dict.keys()):
        model = models.efficientnet_b0()
        model.classifier = nn.Sequential(
            nn.Linear(1280, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )

    # 4. ResNet50
    elif 'layer1.0.conv3.weight' in state_dict:
        model = models.resnet50()
        model.fc = nn.Sequential(
            nn.Linear(2048, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    # 5. Default (ResNet18)
    else:
        model = models.resnet18()
        model.fc = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, num_classes)
        )

    # ✅ Load weights
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    return model


# ✅ FIXED get_info (NO local paths anymore)
def get_info(disease):
    if disease == "Pneumonia":
        return "nimobest_model.pth", ["Normal", "Pneumonia"]
    elif disease == "Brain Tumor":
        return "bestbrain_model.pth", ["No Tumor", "Tumor"]
    elif disease == "Breast Cancer":
        return "best_breast.pth", ["benign", "malignant"]
    elif disease == "Malaria":
        return "best_malaria.pth", ["Parasitized", "Uninfected"]
    elif disease == "Tuberculosis":
        return "tb_final_generalized_model.pth", ["Normal", "TB"]