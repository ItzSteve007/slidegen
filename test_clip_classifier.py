from dashboard.image_analyzer import classify_images

# Replace with real file paths (ensure these images exist on disk)
image_paths = [
    "media/uploads/sample1.jpg",
    "media/uploads/sample2.jpg",
    "media/uploads/sample3.jpg",
]

candidate_labels = [
    "JDM cars", "sports cars", "animals", "landscapes", "food", "people"
]

theme, confidence = classify_images(image_paths, candidate_labels)

print(f"🔍 Detected Theme: {theme} ({confidence * 100:.2f}% confidence)")
