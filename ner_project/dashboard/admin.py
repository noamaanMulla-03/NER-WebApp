from django.contrib import admin
from .models import DocumentSet, Document

@admin.register(DocumentSet)
class DocumentSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')  # Columns to display
    list_filter = ('user', 'created_at')  # Filters for sidebar
    search_fields = ('name',)  # Search by name

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_set', 'file', 'uploaded_at')  # Columns to display
    list_filter = ('document_set', 'uploaded_at')  # Filters for sidebar
    search_fields = ('title', 'file')  # Search by title or file path