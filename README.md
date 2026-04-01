# Kawach - AI Medical Disease Detection

## Overview

Kawach is an AI-powered medical image diagnosis platform built with Streamlit and PyTorch. It supports detection of:

- Pneumonia
- Brain Tumor
- Breast Cancer
- Malaria
- Tuberculosis

The app loads trained `.pth` models from `models/`, applies preprocessing and visualization (GradCAM), and displays class prediction confidence with a downloadable report.

## Repository Structure

- `app.py` - Streamlit web app interface and inference pipeline.
- `models/` - pre-trained model weights (PyTorch `.pth`).
  - `best_model_pneumonia1.pth`
  - `bestbrain_model.pth`
  - `best_breast.pth`
  - `best_malaria.pth`
  - `tb_model.pth`
- `inspect_tb_model.py` - helper script to inspect model state dict keys.
- `README.md` - this file.

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

If you don't have `requirements.txt`, run:

```bash
pip install streamlit torch torchvision pillow numpy opencv-python pytorch-grad-cam
```

## Run the app

```bash
streamlit run app.py
```

## Usage

1. Choose disease from sidebar.
2. Upload one or more images (`jpg`, `png`, `jpeg`).
3. Click Analyze and inspect prediction + Grad-CAM visualization.
4. Download the generated medical report.

## TB-specific note

The `Tuberculosis` option uses `models/tb_model.pth`. Class mapping is handled via:

- default: `["Normal", "TB"]`
- if inverted, toggle `Flip TB class labels` in sidebar.



## Contributing

1. Fork the repository.
2. Create a branch `feature/your-feature`.
3. Make changes and commit.
4. Open a Pull Request.

## License

MIT License
