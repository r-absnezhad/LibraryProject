from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from notifications.models import Notification
# Create your models here.


class Loan(models.Model):
    """
    This model represents a loan in the library.
    It includes fields for the loan date, return date, and the associated book.
    It also includes a foreign key to the user who borrowed the book.
    """
    profile = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE, related_name='loans')
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE, related_name='loans')
    borrowed_at = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)


    class Meta:
        ordering = ['-borrowed_at']
        constraints = [
            models.UniqueConstraint(
                fields=['book', 'profile', 'returned_at'],
                name='unique_active_loan_per_book'
            )
        ]

    # Properties
    @property
    def is_returned(self):
        return self.returned_at is not None
    
    @property
    def is_overdue(self):
        """بررسی دیرکرد"""
        return not self.is_returned and timezone.now() > self.due_date

    # Methods 
    def calculate_fine(self, daily_rate=100):
        """محاسبه جریمه به ازای هر روز دیرکرد"""
        if self.is_overdue:
            days_late = (timezone.now() - self.due_date).days
            self.fine_amount = daily_rate * days_late
            self.save()
        return self.fine_amount
    
    def send_overdue_notification(self):
        """ارسال نوتیفیکیشن برای دیرکرد"""
        if self.is_overdue:
            message = f"کتاب '{self.book.title}' شما دیر برگشت داده شده! جریمه فعلی: {self.fine_amount} تومان."
            Notification.objects.create(profile=self.profile, message=message)

    def mark_returned(self):
        """علامت گذاری برگشت کتاب"""
        self.returned_at = timezone.now()
        self.calculate_fine()
        self.send_overdue_notification()
        self.save()

    
    def clean(self):
        """بررسی اینکه کاربر بدهی دارد یا خیر"""
        if self.profile.has_active_fines():
            raise ValidationError("کاربر جریمه فعال دارد و نمی‌تواند کتاب جدید قرض بگیرد.")
        

    def save(self, *args, **kwargs):
        # اگر due_date مشخص نشده، خودکار ۲ هفته از امروز تنظیم کن
        if not self.due_date:
            self.due_date = timezone.now() + timedelta(days=14)
        self.clean()
        super().save(*args, **kwargs)    

    def __str__(self):
        status = "Returned" if self.is_returned else "Borrowed"
        return f"{self.book.title} by {self.profile} ({status})"