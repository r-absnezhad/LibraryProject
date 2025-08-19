from django.contrib import admin
from .models import Notification
# Register your models here.

class NotificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Notification model.
    - Customizes how Notification records are displayed, filtered, searched, and ordered in the admin panel.
    """

    model = Notification
    list_display = ["profile", "message", "is_read"]
    list_filter = ["is_read"]
    search_fields = ["Last_Name","First_Name"]
    ordering = ["Last_Name","First_Name"]
    fieldsets = (
        ("Authentication", {"fields": ("First_Name", "Last_Name", "message")}),
    )  
    def get_first_name(self, obj):
        return obj.profile.last_name

    get_first_name.short_description = "First_Name"

    def get_last_name(self, obj):
        return obj.profile.last_name

    get_last_name.short_description = "Last_Name"

admin.site.register(Notification, NotificationAdmin)

