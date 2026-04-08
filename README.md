---
title: Kawach Diagnostic Final
emoji: 🛡️
colorFrom: red
colorTo: red
sdk: streamlit
app_file: app.py
pinned: false
---
# 🧠 AI Diagnostic Hub - Medical Disease Detection System

AI Diagnostic Hub is an AI-powered medical image analysis system that detects multiple diseases using Deep Learning and provides explainable predictions using Grad-CAM.

🚀 Built with PyTorch & Streamlit
🔍 Supports multiple diseases
📊 Provides confidence scores + visual explanations

---

## 🚀 Features

* 🩺 Multi-disease detection:

  * Tuberculosis
  * Pneumonia
  * Brain Tumor
  * Breast Cancer
  * Malaria
* 🔍 Explainable AI using Grad-CAM
* 📊 Confidence score prediction
* 🖥️ Interactive UI with Streamlit
* 📄 Downloadable medical report

---

## 🛠️ Tech Stack

* Python
* PyTorch
* Streamlit
* OpenCV
* NumPy
* Grad-CAM

---

## 📁 Project Structure

```
disease_final/
│── app.py                    # Main application entry point
│── config.py                 # Configuration settings
│── models.py                 # Model loading and utilities
│── README.md
│── requirements.txt
│── __init__.py
│── components/
│   ├── ui.py                 # UI components (theme, sidebar)
│   └── __init__.py
│── pages/
│   ├── home.py               # Home page with disease detection
│   ├── about.py              # About page
│   └── __init__.py
│── utils/
│   ├── transforms.py         # Image transforms and utilities
│   └── __init__.py
└── models/                   # Pre-trained model files
    ├── best_breast.pth
    ├── best_malaria.pth
    ├── bestbrain_model.pth
    ├── nimobest_model (1).pth
    └── tb_final_generalized_model.pth
```

---

## ⚙️ Installation

## ⚙️ Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 🧪 Usage

1. Select disease type from sidebar
2. Upload medical image (`jpg`, `png`, `jpeg`)
3. Click **Analyze**
4. View prediction + Grad-CAM visualization
5. Download the generated report

---

## 🧠 Model Details

* Built using Convolutional Neural Networks (CNN)
* Trained on medical imaging datasets
* Supports both binary and multi-class classification

---

## 📌 Future Improvements

* 🌐 Deploy on cloud (Streamlit Cloud / AWS)
* 📊 Add evaluation metrics (accuracy, precision, recall)
* 🧬 Expand to more diseases
* 📱 Improve UI/UX for better usability

---

## 👩‍💻 Author

**Jagriti Arora**

---

## 📜 License

MIT License
