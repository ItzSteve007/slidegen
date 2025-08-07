# dashboard/image_analyzer.py

import torch
from PIL import Image
from torchvision import transforms
from transformers import CLIPProcessor, CLIPModel
import os

# Load model once
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def classify_images(image_paths, candidate_labels):
    images = [Image.open(path).convert("RGB") for path in image_paths]
    inputs = clip_processor(text=candidate_labels, images=images, return_tensors="pt", padding=True)
    outputs = clip_model(**inputs)

    logits_per_image = outputs.logits_per_image  # shape: [num_images, num_labels]
    probs = logits_per_image.softmax(dim=1)

    # Average the probabilities across all images
    avg_probs = probs.mean(dim=0)
    best_idx = avg_probs.argmax().item()
    return candidate_labels[best_idx], avg_probs[best_idx].item()
