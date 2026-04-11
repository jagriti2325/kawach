import streamlit as st
import torch
import torch.nn as nn
import torchvision.models as models
import os

# ------------------- DEVICE SETUP -------------------
device = torch.device("cpu")

# ------------------- LOAD MODEL FUNCTION -------------------
@st.cache_resource(show_spinner=False)
def load_model(path, num_classes, disease_type):
    try:
        # Load directly from the uploaded 'models/' folder
        state_dict = torch.load(path, map_location=device)
    except Exception as e:
        st.error(f"Error loading {path}: {e}")
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
            if 'fc.3.weight' in state_dict or 'fc.3.bias' in state_dict:
                model.fc = nn.Sequential(
                    nn.Linear(512, 256),
                    nn.ReLU(),
                    nn.Dropout(0.5),
                    nn.Linear(256, num_classes)
                )
            else:
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
        st.error(f"Architecture mismatch: {e}")
        return None

def get_info(disease):
    mapping = {
        "Pneumonia": ("models/nimobest_model (1).pth", ["Normal", "Pneumonia"]),
        "Brain Tumor": ("models/bestbrain_model.pth", ["No Tumor", "Tumor"]),
        "Breast Cancer": ("models/best_breast.pth", ["benign", "malignant"]),
        "Malaria": ("models/best_malaria.pth", ["Parasitized", "Uninfected"]),
        "Tuberculosis": ("models/tb_final_generalized_model.pth", ["Normal", "TB"])
    }
    return mapping.get(disease)