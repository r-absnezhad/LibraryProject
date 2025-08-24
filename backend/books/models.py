from django.db import models
# from django.core.exceptions import ValidationError
from datetime import timedelta, datetime
from django.utils import timezone
from notifications.models import Notification
# Create your models here.




class BookRequest(models.Model):
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE, related_name="requests")
    profile = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    is_notified = models.BooleanField(default=False)
    notified_at = models.DateTimeField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def check_expired(self):
        if self.is_notified and self.notified_at:
            if datetime.now() > self.notified_at + timedelta(hours=24):
                self.is_expired = True
                self.save()
                return True
        return False
    

    @classmethod
    def notify_next_in_queue(cls, book):
        next_request = cls.objects.filter(
            book=book, is_expired=False, is_notified=False
        ).order_by("created_date").first()

        if next_request:
            next_request.is_notified = True
            next_request.notified_at = timezone.now()
            next_request.save()
            # اینجا مثلاً می‌تونی ایمیل بزنی
            # print(f"📢 اطلاع‌رسانی شد به {next_request.profile.user.email}")
            Notification.objects.create(profile=next_request.profile ,message=f"کتاب {next_request.book.title} برای شما رزرو شد. ۲۴ ساعت فرصت دارید." ,)
            return next_request
        return None



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
    is_available = models.BooleanField(default=True)
    

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
    
