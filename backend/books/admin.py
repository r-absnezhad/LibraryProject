from django.contrib import admin
from .models import Book, BookRequest,Genre
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = ["title", "author", "publisher", "language", ]
    list_filter = ["publisher", "language", "publication_year"]
    search_fields = ["title", "isbn"]
    ordering = ["title", "author", "publication_year", "page_count"]
    fieldsets = (
        ("Details", {"fields": ("title", "author", "publisher", "language", "page_count", "summary", "cover_image",)}),
        ("Important Dates", {"fields": ("publication_year", )}),
    )  
admin.site.register(Book, BookAdmin)
class BookRequestAdmin(admin.ModelAdmin):
    model = BookRequest
    list_display = ["book", "profile_name", "is_notified", "notified_at", "is_expired"]
    list_filter = ["is_notified", "is_expired",]
    search_fields = ["book", "profile__last_name"]
    ordering = ["created_date", "book", "profile__last_name"]
    fieldsets = (
        ("Details", {"fields": ("book", "profile", "notified_at", "is_expired",)}),
    )  
    def profile_name(self, instance):
        return instance.profile
    profile_name.short_description = "Name"

admin.site.register(BookRequest, BookRequestAdmin)

class GenreAdmin(admin.ModelAdmin):
    model = Genre
    list_display = ["id","name"]
    ordering = ["name"]
    fieldsets = (
        ("Details", {"fields": ("name",)}),
    )  
admin.site.register(Genre, GenreAdmin)