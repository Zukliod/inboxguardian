from transformers import pipeline
import os

# Set Hugging Face cache directory
os.environ["TRANSFORMERS_CACHE"] = os.getenv("TRANSFORMERS_CACHE", "./cache")

classifier = pipeline("text-classification", model="distilbert-base-uncased")

def prioritize_notification(content):
    result = classifier(content)
    label = result[0]["label"]
    if label == "LABEL_0":
        return "low"
    elif label == "LABEL_1":
        return "medium"
    else:
        return "high"