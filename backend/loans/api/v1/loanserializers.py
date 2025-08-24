from rest_framework import serializers
from ...models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'profile', 'book', 'borrowed_at', 'due_date',
                  "is_returned", 'returned_at', 'fine_amount', 'created_date', 'updated_date']
        read_only_fields = ['profile', 'due_date', "is_returned",'returned_at', 'fine_amount', 'created_date', 'updated_date']


    def to_representation(self, instance):
        if isinstance(instance, Loan):
            rep = super().to_representation(instance)
            rep['book'] = {
                'title': instance.book.title,
                'author': instance.book.author,
            }
            rep['profile'] = instance.profile.last_name + " " + instance.profile.first_name
        return rep
