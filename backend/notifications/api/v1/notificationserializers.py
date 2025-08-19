from rest_framework import serializers
from ...models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification  # Replace with the actual model
        fields = ['profile', 'message', 'is_read', 'created_date']

