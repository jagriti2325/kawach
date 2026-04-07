import torch

# Device configuration
device = torch.device("cpu")

# Page configuration
PAGE_CONFIG = {
    "page_title": "Kawach - AI Medical Diagnostic Hub",
    "layout": "wide"
}

# Theme options
THEMES = {
    "Light": {
        "background": "#f4f6f9",
        "color": "black"
    },
    "Dark": {
        "background": "#0e1117",
        "color": "white"
    }
}

# Navigation options
PAGES = ["Home", "About"]