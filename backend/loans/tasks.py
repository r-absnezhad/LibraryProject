from celery import shared_task
from django.utils import timezone
from .models import Loan

@shared_task
def process_overdue_loans():
    today = timezone.now().date()
    overdue_loans = Loan.objects.filter(is_returned=False, due_date__lt=today)
    
    for loan in overdue_loans:
        loan.calculate_fine()
        loan.send_overdue_notification()




# @shared_task
# def test_celery_task():
#     print("✅ Celery is working!")
#     return "Hello from Celery"