from rest_framework import viewsets, filters, status
from ...models import Loan
from rest_framework.decorators import action
from rest_framework.response import Response    
from books.models import BookRequest, Book
from django_filters.rest_framework import DjangoFilterBackend
from .loanserializers import LoanSerializer
from datetime import timedelta
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

class LoanModelViewSet(viewsets.ModelViewSet):

    """
    A viewset for viewing and editing Loan instances.
    """
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["is_returned",]
    search_fields = ['book__title', 'profile__last_name', 'profile__first_name']
    ordering_fields = ['borrowed_at', 'due_date', 'returned_at', 'book__title', 'profile__last_name',]
    # pagination_class


    def create(self, request, *args, **kwargs):
        book_id = request.data.get("book")
        profile = request.user.profile
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({"error": "کتاب پیدا نشد."}, status=status.HTTP_404_NOT_FOUND)
        
        if not book.is_available:
            return Response({"error": f"کتاب {book.title} در دسترس نیست."}, status=status.HTTP_400_BAD_REQUEST)

        if BookRequest.objects.filter(book=book, is_expired=False, is_notified=False):
            req = BookRequest.objects.filter(book=book, profile=profile, is_notified=True, is_expired=False).first()
            if not req:
                return Response({"error": "شما در صف این کتاب نیستید یا فرصت شما تمام شده."}, status=status.HTTP_400_BAD_REQUEST)
            req.is_expired = True
            req.save()
            return Response({"detail": f"شما نفر اول در صف این کتاب هستید.کتاب {book.title} برای شما ثبت خواهد شد."}, status=status.HTTP_200_OK)

        if Loan.objects.filter(profile=profile, book=book, is_returned=False).exists():
            return Response({"error": "شما قبلا این کتاب را قرض گرفته‌اید و هنوز برنگردانده‌اید."}, status=status.HTTP_400_BAD_REQUEST)
        
        loan = Loan.objects.create(
            profile=profile,
            book=book,
            due_date=(timezone.now() + timedelta(days=14)).date()
        )
        book.is_available = False
        book.save()

        # return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)
        return Response({
            "message": f"کتاب {book.title} با موفقیت برای شما ثبت شد.",
            "loan": LoanSerializer(loan).data
        }, status=status.HTTP_201_CREATED)

    # برگرداندن کتاب
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        loan = self.get_object()
        book = loan.book
        if loan.is_returned:
            return Response({"error": "این کتاب قبلا برگشت داده شده."}, status=status.HTTP_400_BAD_REQUEST)
        loan.is_returned = True
        loan.returned_at = timezone.now()
        
        book.is_available = True
        book.save()
        loan.save()

        # صف درخواست‌ها
        # همون لحظه نفر بعدی در صف نوتیف بشه
        BookRequest.notify_next_in_queue(book)


        # return Response(LoanSerializer(loan).data)
        return Response({
            "message": f"کتاب {book.title} با موفقیت برگردانده شد.",
            "loan": LoanSerializer(loan).data
        }, status=status.HTTP_200_OK)

    # تمدید کتاب
    @action(detail=True, methods=["post"])
    def renew(self, request, pk=None):
        loan = self.get_object()
        book = loan.book
        if loan.is_returned:
            return Response({"error": "کتاب برگشت داده شده و قابل تمدید نیست."}, status=status.HTTP_400_BAD_REQUEST)
 
        active_request = BookRequest.objects.filter(
            book=book, is_notified=False, is_expired=False
        ).exists()

        if active_request:
            return Response({"error": "درخواستی برای این کتاب ثبت شده است و قابل تمدید نیست."}, status=status.HTTP_400_BAD_REQUEST)
        
        loan.due_date += timedelta(days=7)
        loan.save()
        return Response({
            "message": f"کتاب {loan.book.title} با موفقیت تمدید شد.",
            "loan": LoanSerializer(loan).data
        }, status=status.HTTP_200_OK)
