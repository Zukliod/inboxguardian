from transformers import pipeline

# Load the text classification model
classifier = pipeline("text-classification", model="distilbert-base-uncased")

def prioritize_notification(content):
    """
    Predict the priority of a notification based on its content.
    """
    result = classifier(content)  # Get model prediction
    label = result[0]["label"]    # Extract the predicted label

    # Map model labels to priority levels
    if label == "LABEL_0":  # Example: Assume LABEL_0 = "low priority"
        return "low"
    elif label == "LABEL_1":  # Example: Assume LABEL_1 = "medium priority"
        return "medium"
    else:
        return "high"  # Default to "high" for other cases
if __name__ == "__main__":
    test_content = "Urgent meeting with the team at 3 PM"
    priority = prioritize_notification(test_content)
    print(f"Predicted priority: {priority}")