from rest_framework import viewsets, filters, status
from rest_framework import serializers
from ...models import Book, Genre, BookRequest
from .permissions import IsStaffOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BookSerializer, GenreSerializer, BookRequestSerializer
from rest_framework.response import Response   
from datetime import timedelta, datetime


class BookRequestModelViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing book request instances.
    """
    queryset = BookRequest.objects.all()
    serializer_class = BookRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_notified', 'is_expired']
    search_fields = ['book__title', 'profile__last_name', 'profile__first_name']
    ordering_fields = ['created_at', 'book__title', 'profile__last_name',]
    # pagination_class


    def perform_create(self, serializer):
        book = serializer.validated_data["book"]
        profile = self.request.user.profile

        if book.is_available:
            return Response({"error": "این کتاب الان موجوده و نیاز به رزرو نیست."}, status=status.HTTP_400_BAD_REQUEST)

        # جلوگیری از ثبت درخواست تکراری
        if BookRequest.objects.filter(book=book, profile=profile, is_expired=False).exists():
            raise serializers.ValidationError("شما قبلاً برای این کتاب درخواست ثبت کرده‌اید.")
        
        serializer.save(profile=profile)


class BookModelViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genre', 'publication_year', "is_available"]
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'author', 'publication_year']
    # pagination_class


class GenreModelViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing genre instances.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']
    # pagination_class