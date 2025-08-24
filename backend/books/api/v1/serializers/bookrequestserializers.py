from rest_framework import serializers
from ....models import BookRequest

class BookRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRequest
        fields = ['id', 'book', 'profile', 'is_notified', 'notified_at', 'is_expired', 'created_date', 'updated_date']


        def to_represe