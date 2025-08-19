from django.db import models
from accounts.models import Profile
# Create your models here.

class Notification(models.Model):
    """
    This Models represents a notification in the library system.
    It includes fields for the notification type, message, and the user it is associated with.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"Notification for {self.profile}"

    def save(self, *args, **kwargs):
        """
        ایجاد Notification فقط اگر مشابه آن قبلاً فرستاده نشده
        و هنوز خوانده نشده باشد.
        """
        exists = Notification.objects.filter(
            profile=self.profile,
            message=self.message,
            is_read=False
        ).exists()
        if not exists:
            super().save(*args, **kwargs)  # فقط اگر وجود نداشت ذخیره کن
        # اگر پیام قبلاً وجود داشت، هیچ کاری انجام نمی‌دهد
