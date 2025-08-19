from django.db import models
from books.models import Book
# Create your models here.

class Review(models.Model):
    """
    This Model represents a review given by a user to a book.
    Fields include user, book, review text, and a rating.
    """
    profile = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="reviews", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)  
    comment = models.TextField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("profile", "book")  # هر کاربر فقط یه نظر روی یه کتاب بده


    def __str__(self):
        return f"{self.profile} - {self.book} ({self.rating})"
