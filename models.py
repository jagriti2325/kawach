import streamlit as st
import torch
import torch.nn as nn
import torchvision.models as models
import gdown
import os

# ------------------- DEVICE SETUP -------------------
device = torch.device("cpu") 

# ------------------- DOWNLOAD FUNCTION -------------------
@st.cache_resource(show_spinner=False)
def download_model(file_id, output):
    if not os.path.exists(output):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output, quiet=False)
    return True

# ------------------- LOAD MODEL FUNCTION -------------------
@st.cache_resource(show_spinner=False)
def load_model(path, num_classes, disease_type):
    FILE_IDS = {
        "best_breast.pth": "1m4qUmlR2ZsCLKsHwxAvUv3QYN-yafDfs",
        "bestbrain_model.pth": "1xOy8OFwcoZnVadUkp1e5aKPTKeOEtKqb",
        "best_malaria.pth": "1_KeqAG8T3ZAVnVEca834hZr8DXau3WlS",
        "nimobest_model.pth": "1M9yZEJe6QwCxhhh2kLj483J7A5pX314k",
        "tb_final_generalized_model.pth": "1gW-_JZsHvQm25snAypUgHDdaOuhgEYGZ"
    }

    # Safe download
    download_model(FILE_IDS[path], path)

    try:
        state_dict = torch.load(path, map_location=device)
    except Exception as e:
        return None

    try:
        if disease_type == "Tuberculosis":
            model = models.densenet201(weights=None)
            model.classifier = nn.Sequential(
                nn.Linear(1920, 512),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(512, num_classes)
            )
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
        elif 'layer1.0.conv3.weight' in state_dict:
            model = models.resnet50(weights=None)
            model.fc = nn.Sequential(
                nn.Linear(2048, 256),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(256, num_classes)
            )
        else:
            model = models.resnet18(weights=None)
            model.fc = nn.Sequential(
                nn.Linear(512, 256),
                nn.ReLU(),
                nn.Linear(256, num_classes)
            )

        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()
        return model
    except Exception as e:
        return None

def get_info(disease):
    mapping = {
        "Pneumonia": ("nimobest_model.pth", ["Normal", "Pneumonia"]),
        "Brain Tumor": ("bestbrain_model.pth", ["No Tumor", "Tumor"]),
        "Breast Cancer": ("best_breast.pth", ["benign", "malignant"]),
        "Malaria": ("best_malaria.pth", ["Parasitized", "Uninfected"]),
        "Tuberculosis": ("tb_final_generalized_model.pth", ["Normal", "TB"])
    }
    return mapping.get(disease)