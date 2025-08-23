from rest_framework import viewsets, filters, status
from ...models import Loan
from rest_framework.decorators import action
from rest_framework.response import Response    
from notifications.models import Notification
from books.models import BookRequest, Book
from django_filters.rest_framework import DjangoFilterBackend
from .loanserializers import LoanSerializer
from datetime import timedelta, datetime
from django.utils import timezone
# from .permissions import IsStaffOrReadOnly

class LoanModelViewSet(viewsets.ModelViewSet):

    """
    A viewset for viewing and editing Loan instances.
    """
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    # permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['book__title', 'returned_at', "is_returned"]
    search_fields = ['book__title', 'profile__last_name', 'profile__first_name']
    ordering_fields = ['borrowed_at', 'due_date', 'returned_at']
    # pagination_class


    def create(self, request, *args, **kwargs):
        book_id = request.data.get("book_id")
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({"error": "کتاب پیدا نشد."}, status=status.HTTP_404_NOT_FOUND)
        
        if not book.is_available:
            return Response({"error": "کتاب در دسترس نیست."}, status=status.HTTP_400_BAD_REQUEST)
        
        if BookRequest.objects.filter(
            book=book, expired=False, is_notified=False):
            profile = request.user.profile
            req = BookRequest.objects.filter(book=book, profile=profile, is_notified=True, expired=False).first()
            if not req:
                return Response({"error": "شما در صف این کتاب نیستید یا فرصت شما تمام شده."}, status=status.HTTP_400_BAD_REQUEST)
            if req.notified_at and datetime.now() > req.notified_at + timedelta(hours=24):
                req.expired = True
                req.save()
                return Response({"error": "مهلت شما برای گرفتن این کتاب تمام شد."}, status=status.HTTP_400_BAD_REQUEST)
 

        loan = Loan.objects.create(
            profile=profile,
            book=book,
            due_date=timezone.now() + timedelta(days=14)
        )
        book.is_available = False
        book.save()
        req.expired = True
        req.save()

        return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)

    # برگرداندن کتاب
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        loan = self.get_object()
        if loan.is_returned:
            return Response({"error": "این کتاب قبلا برگشت داده شده."}, status=status.HTTP_400_BAD_REQUEST)
        loan.returned = True
        loan.returned_at = timezone.now()
        loan.book.is_available = True
        loan.book.save()
        loan.save()

        # # همون لحظه نفر بعدی در صف نوتیف بشه
        # BookRequest.notify_next_in_queue(self.book)

         # صف درخواست‌ها
        waiting_requests = BookRequest.objects.filter(
            book=loan.book, expired=False, is_notified=False
        ).order_by("created_at")

        if waiting_requests.exists():
            first_request = waiting_requests.first()
            first_request.is_notified = True
            first_request.notified_at = datetime.now()
            first_request.save()

            Notification.objects.create(profile=first_request.profile, message=f"کتاب {loan.book.title} برای شما آزاد شد. ۲۴ ساعت فرصت دارید.")

        return Response(LoanSerializer(loan).data)
    
# تمدید کتاب
    @action(detail=True, methods=["post"])
    def renew(self, request, pk=None):
        loan = self.get_object()
        if loan.returned:
            return Response({"error": "کتاب برگشت داده شده و قابل تمدید نیست."}, status=status.HTTP_400_BAD_REQUEST)
 
        active_request = BookRequest.objects.filter(
            book=loan.book, is_notified=False, expired=False
        ).exists()

        if active_request:
            return Response({"error": "کتاب درخواستی فعال است و قابل تمدید نیست."}, status=status.HTTP_400_BAD_REQUEST)
        
        loan.due_date += timedelta(days=7)
        loan.save()
        return Response(LoanSerializer(loan).data)
