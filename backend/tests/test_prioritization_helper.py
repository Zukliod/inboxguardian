from utils.prioritization_helper import prioritize_notification

def test_prioritize_notification():
    # Test case 1: High-priority content
    content = "Urgent meeting at 3 PM"
    priority = prioritize_notification(content)
    assert priority in ["high", "medium", "low"], "Invalid priority returned"

    # Test case 2: Low-priority content
    content = "Reminder to water the plants"
    priority = prioritize_notification(content)
    assert priority in ["high", "medium", "low"], "Invalid priority returned"