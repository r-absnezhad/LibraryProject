from rest_framework import viewsets
from ...models import Notification
from .notificationserializers import NotificationSerializer
from .permissions import IsStaffOrReadOnly

class NotificationModelViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing notification instances.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsStaffOrReadOnly]