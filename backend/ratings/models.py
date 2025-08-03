from django.db import models

# Create your models here.

class Rating(models.Model):
    """
    This Model represents a rating given by a user to a book.
    Fields include user, book, rating score, and a comment.
    """
    pass


class Review(models.Model):
    """
    This Model represents a review given by a user to a book.
    Fields include user, book, review text, and a rating.
    """
    pass
