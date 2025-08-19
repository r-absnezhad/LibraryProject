from django.contrib import admin
from .models import Loan
# Register your models here.
class LoanAdmin(admin.ModelAdmin):
    model = Loan
    list_display = ["id","profile","book", "borrowed_at", "due_date", "returned_at", "fine_amount"]
    ordering = ["profile", "borrowed_at"]
    fieldsets = (
        ("Details", {"fields": ("profile", "book", "borrowed_at", "due_date", "returned_at", "fine_amount")}),
    )
admin.site.register(Loan, LoanAdmin)