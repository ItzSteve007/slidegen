from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

# Load model & processor only once
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# List of common theme labels
CANDIDATE_LABELS = [
    "cars", "jdm cars", "sports", "landscapes", "food", "buildings", "people", "animals",
    "technology", "nature", "anime", "architecture", "travel", "interior design"
]

def classify_theme(image_paths):
    image_inputs = []

    for img_path in image_paths:
        image = Image.open(img_path).convert("RGB")
        inputs = processor(text=CANDIDATE_LABELS, images=image, return_tensors="pt", padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1).cpu().numpy()[0]
            image_inputs.append(probs)

    # Average the scores across all images
    avg_probs = sum(image_inputs) / len(image_inputs)
    best_idx = avg_probs.argmax()
    return CANDIDATE_LABELS[best_idx]
