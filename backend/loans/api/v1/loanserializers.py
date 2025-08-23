from rest_framework import serializers
from ...models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'profile', 'book', 'borrowed_at', 'due_date',
                  "is_returned", 'returned_at', 'fine_amount', 'created_date', 'updated_date']