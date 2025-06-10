from django.db import models
from django.contrib.auth.models import User

class DocumentSet(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_sets')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Document(models.Model):
    document_set = models.ForeignKey(DocumentSet, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255, blank=True)  # Extracted from file or user input
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or self.file.name