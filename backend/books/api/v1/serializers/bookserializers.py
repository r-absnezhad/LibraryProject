from rest_framework import serializers
from ....models import Book
from .genreserializers import GenreSerializer

class BookSerializer(serializers.ModelSerializer):
    # genre = GenreSerializer(many=True)
    class Meta:
        model = Book
        fields = ['id','title', 'author', 'isbn', 'genre', 'publisher', 'publication_year',
                   'language', 'page_count', 'summary', "is_available", 'cover_image', 'created_date', 'updated_date']
        

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['genre'] = [genre.name for genre in instance.genre.all()]
        return rep