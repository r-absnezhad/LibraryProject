from rest_framework import viewsets
from ...models import Book, Genre


class BookModelViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing book instances.
    """
    queryset = Book.objects.all()
    serializer_class = 'BookSerializer'  
    # permission_classes 

class GenreModelViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing genre instances.
    """
    queryset = Genre.objects.all()
    serializer_class = 'GenreSerializer'
    # permission_classes 