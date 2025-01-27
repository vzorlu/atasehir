from datetime import timezone
from apps.notification.models import Notification


def process_detection(results, cls):
    detected_class = results[0].names[int(cls)]

    # Check if notification exists for this class
    notification = Notification.objects.filter(class_field=detected_class, enabled=True).first()

    if notification:
        # Trigger notification
        notification.notification_history.append({"timestamp": timezone.now().isoformat(), "class": detected_class})
        notification.save()
        return notification
