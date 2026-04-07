from torchvision import transforms

# Default image transform
default_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Disease information
def get_disease_info(disease):
    info = {
        "Pneumonia": {
            "description": "Pneumonia is an infection that inflames the air sacs in one or both lungs. It can be caused by bacteria, viruses, or fungi. Symptoms include cough, fever, chills, and difficulty breathing."
        },
        "Brain Tumor": {
            "description": "A brain tumor is a mass or growth of abnormal cells in the brain. It can be benign or malignant. Symptoms may include headaches, seizures, nausea, and changes in cognitive function."
        },
        "Breast Cancer": {
            "description": "Breast cancer is a type of cancer that forms in the cells of the breasts. It can occur in both men and women, though it is far more common in women. Early detection is crucial for successful treatment."
        },
        "Malaria": {
            "description": "Malaria is a life-threatening disease caused by parasites transmitted through the bites of infected mosquitoes. Symptoms include fever, chills, and flu-like illness."
        },
        "Tuberculosis": {
            "description": "Tuberculosis (TB) is a potentially serious infectious disease that mainly affects the lungs. It is caused by the bacterium Mycobacterium tuberculosis and can spread through the air when infected people cough or sneeze."
        }
    }
    return info.get(disease, {"description": "Information not available."})