from django.db import models

# Create your models here.


class Loan(models.Model):
    """
    This model represents a loan in the library.
    It includes fields for the loan date, return date, and the associated book.
    It also includes a foreign key to the user who borrowed the book.
    """
    pass