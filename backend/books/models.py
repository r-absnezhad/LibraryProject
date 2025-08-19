from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.



class Book(models.Model):
    """
    This Model represents a book in the library.
    Fields include title, author, ISBN, publication date, a brief description and more information about the book.
    """
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    genre = models.ManyToManyField("Genre", related_name='books')
    publisher = models.CharField(max_length=500)
    publication_year = models.PositiveIntegerField()
    language = models.CharField(max_length=155)
    page_count = models.PositiveIntegerField()
    summary = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='book_covers/',blank=True, null=True)
    

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def average_rating(self):
        return self.reviews.aggregate(models.Avg("rating"))["rating__avg"] or 0



    def __str__(self):
        return f"{self.title} by {self.author}"
    



class Genre(models.Model):
    """
    This Model represents a genre of books in the library.
    Fields include name.
    """
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name