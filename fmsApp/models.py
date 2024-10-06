# models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse  # Import reverse for URL resolution
from cryptography.fernet import Fernet
from django.conf import settings
import base64
import os

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    file_path = models.FileField(upload_to='uploads/', blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    hashed_content = models.BinaryField(blank=True, null=True)  # New field for hashed content
    password = models.CharField(max_length=255, blank=True, null=True)  # Add this line

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.file_path:
            # Read file content and hash it
            try:
                with open(self.file_path.path, 'rb') as f:
                    content = f.read()
                    fernet = Fernet(settings.ID_ENCRYPTION_KEY)
                    self.hashed_content = fernet.encrypt(content)
            except Exception as e:
                print(f"Error hashing file content: {str(e)}")
                # Handle error as needed (e.g., log it, raise an exception)
        
        super().save(*args, **kwargs)

    def get_share_url(self):
        fernet = Fernet(settings.ID_ENCRYPTION_KEY)
        value = fernet.encrypt(str(self.pk).encode())
        value = base64.urlsafe_b64encode(value).decode()
        return reverse("share-file-id", kwargs={"id": value})


from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file_path = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    



    from django.db import models
from django.contrib.auth.models import User

class HiddenFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='hidden_files/')
    password = models.CharField(max_length=128)  # Store hashed passwords

