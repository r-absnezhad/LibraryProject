from rest_framework import viewsets, filters
from ...models import Loan
from django_filters.rest_framework import DjangoFilterBackend
from .loanserializers import LoanSerializer
# from .permissions import IsStaffOrReadOnly

class LoanModelViewSet(viewsets.ModelViewSet):

    """
    A viewset for viewing and editing Loan instances.
    """
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    # permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['book__title', 'returned_at']
    search_fields = ['book__title', 'profile__last_name', 'profile__first_name']
    ordering_fields = ['borrowed_at', 'due_date', 'returned_at']
    # pagination_class