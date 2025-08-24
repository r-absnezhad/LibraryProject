from rest_framework import serializers
from ....models import BookRequest, Book

class BookRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRequest
        fields = ['id', 'book', 'profile', 'is_notified', 'notified_at', 'is_expired', 'created_date', 'updated_date']
        read_only_fields = ['profile', 'is_notified', 'notified_at', 'is_expired', 'created_date', 'updated_date']


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if isinstance(instance, BookRequest):
            rep['book'] = instance.book.title
            rep['profile'] = instance.profile.last_name + " " + instance.profile.first_name
        return rep