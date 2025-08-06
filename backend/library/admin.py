from django.contrib import admin
from .models import Book, Genre
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = ["title", "author", "publisher", "language", "copies_total", "copies_available"]
    list_filter = ["publisher", "language", "publication_year"]
    search_fields = ["title", "isbn"]
    ordering = ["title", "author", "publication_year", "page_count"]
    fieldsets = (
        ("Details", {"fields": ("title", "author", "publisher", "language", "page_count", "summary", "cover_image", "copies_total", "copies_available")}),
        ("Important Dates", {"fields": ("publication_year", )}),
    )  
admin.site.register(Book, BookAdmin)
class GenreAdmin(admin.ModelAdmin):
    model = Genre
    list_display = ["id","name"]
    ordering = ["name"]
    fieldsets = (
        ("Details", {"fields": ("name",)}),
    )  
admin.site.register(Genre, GenreAdmin)