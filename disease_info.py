from datetime import datetime

DISEASE_INFO = {
    "Pneumonia": {
        "description": "Pneumonia is an infection that inflames the air sacs in one or both lungs. The air sacs may fill with fluid or pus.",
        "symptoms": [
            "Cough (productive or dry)",
            "Fever or chills",
            "Difficulty breathing",
            "Chest pain",
            "Fatigue"
        ],
        "severity_low": "No pneumonia detected. Lungs appear normal.",
        "severity_high": "Pneumonia detected. Immediate medical consultation recommended.",
        "recommendations": [
            "Consult with a pulmonologist for confirmation",
            "Get chest X-ray imaging for verification",
            "Follow prescribed antibiotic treatment if pneumonia is confirmed",
            "Rest and maintain hydration"
        ]
    },
    "Brain Tumor": {
        "description": "A brain tumor is an abnormal growth of cells in the brain. It can be benign (non-cancerous) or malignant (cancerous).",
        "symptoms": [
            "Headaches",
            "Vision or hearing problems",
            "Balance and coordination issues",
            "Nausea or vomiting",
            "Cognitive changes"
        ],
        "severity_low": "No tumor detected. Brain imaging appears normal.",
        "severity_high": "Brain tumor detected. Urgent neurological consultation required.",
        "recommendations": [
            "Consult with a neurosurgeon immediately",
            "Get advanced imaging (MRI/CT) for confirmation",
            "Biopsy may be required for accurate diagnosis",
            "Treatment options: surgery, radiation, or chemotherapy"
        ]
    },
    "Breast Cancer": {
        "description": "Breast cancer occurs when malignant cells form in the breast tissue. Early detection is crucial for treatment.",
        "symptoms": [
            "Lump in the breast",
            "Skin irritation or dimpling",
            "Redness or scaliness",
            "Nipple discharge",
            "Breast pain"
        ],
        "severity_low": "No malignancy detected. Breast tissue appears benign.",
        "severity_high": "Malignant cells detected. Urgent oncology consultation recommended.",
        "recommendations": [
            "Consult with an oncologist for confirmation",
            "Additional mammography or ultrasound imaging",
            "Biopsy for definitive diagnosis",
            "Treatment options: surgery, chemotherapy, or radiation"
        ]
    },
    "Malaria": {
        "description": "Malaria is a parasitic infection transmitted through mosquito bites. Early diagnosis and treatment are critical.",
        "symptoms": [
            "High fever with chills",
            "Headache and muscle pain",
            "Nausea and vomiting",
            "Fatigue",
            "Jaundice in severe cases"
        ],
        "severity_low": "No parasites detected. Blood sample appears normal.",
        "severity_high": "Malarial parasites detected. Immediate treatment required.",
        "recommendations": [
            "Consult with an infectious disease specialist",
            "Blood tests for parasite confirmation",
            "Start antimalarial medication immediately",
            "Maintain hydration and rest"
        ]
    },
    "Tuberculosis": {
        "description": "Tuberculosis is a serious infection affecting the lungs, caused by the bacterium Mycobacterium tuberculosis.",
        "symptoms": [
            "Persistent cough lasting 3+ weeks",
            "Coughing up blood or phlegm",
            "Chest pain",
            "Fatigue and weakness",
            "Night sweats and chills"
        ],
        "severity_low": "No TB detected. Lungs appear normal. Regular check-ups recommended.",
        "severity_high": "TB infection detected. Immediate pulmonary consultation and treatment required.",
        "recommendations": [
            "Consult with a pulmonologist or TB specialist",
            "Confirmatory tests: Sputum smear microscopy, culture, GeneXpert",
            "Start anti-tuberculous therapy (ATT) immediately",
            "Infection control measures to prevent transmission",
            "Regular follow-up and monitoring"
        ]
    }
}

POSITIVE_LABELS = {
    "Pneumonia": {"Pneumonia"},
    "Brain Tumor": {"Tumor"},
    "Breast Cancer": {"malignant"},
    "Malaria": {"Parasitized"},
    "Tuberculosis": {"TB"}
}


def get_disease_info(disease_name):
    """Return metadata for a known disease."""
    return DISEASE_INFO.get(disease_name, {})


def generate_report(disease, prediction, confidence, probabilities):
    """Generate a detailed medical report for the selected disease."""
    disease_data = get_disease_info(disease)
    prediction_text = str(prediction)
    confidence_value = float(confidence)

    if disease in POSITIVE_LABELS:
        if disease == "Breast Cancer":
            is_positive = prediction_text.lower() in POSITIVE_LABELS[disease]
        else:
            is_positive = prediction_text in POSITIVE_LABELS[disease]
    else:
        is_positive = any(label in prediction_text or label.lower() in prediction_text.lower()
                          for label in {"Pneumonia", "Tumor", "malignant", "Parasitized", "TB"})

    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "disease_screened": disease,
        "prediction": prediction_text,
        "confidence": f"{confidence_value * 100:.2f}%",
        "status": "⚠️ POSITIVE" if is_positive else "✅ NEGATIVE",
        "description": disease_data.get("description", ""),
        "finding": disease_data.get("severity_high", "") if is_positive else disease_data.get("severity_low", ""),
        "key_symptoms": disease_data.get("symptoms", []),
        "recommendations": disease_data.get("recommendations", []),
        "probabilities": probabilities,
        "disclaimer": "⚠️ DISCLAIMER: This is an AI-assisted diagnostic tool for preliminary screening. Results must be confirmed by a qualified healthcare professional. Do not use as the sole basis for medical diagnosis.",
    }

    return report


def format_report_display(report):
    """Return a display-ready report structure."""
    return report
