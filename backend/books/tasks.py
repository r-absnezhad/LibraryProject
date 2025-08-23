from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import BookRequest


@shared_task
def process_expired_requests():
    """
    همه‌ی درخواست‌هایی که ۲۴ ساعت گذشته و هنوز کتاب نگرفتن → expire
    و بعد نفر بعدی توی صف notify بشه
    """
    requests = BookRequest.objects.filter(is_notified=True, expired=False)

    for req in requests:
        if req.notified_at and timezone.now() > req.notified_at + timedelta(hours=24):
            req.expired = True
            req.save()
            # حالا نوبت نفر بعدی
            BookRequest.notify_next_in_queue(req.book)