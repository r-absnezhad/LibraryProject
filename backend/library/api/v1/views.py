from rest_framework import viewsets, filters
from ...models import Book, Genre
from .permissions import IsStaffOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BookSerializer, GenreSerializer

class BookModelViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genre', 'publication_year']
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