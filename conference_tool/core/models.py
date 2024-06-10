from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import qrcode
import io
import uuid


class Conference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    presenter = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(unique=True, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code_path = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = f"http://localhost:8000/conference/{self.id}/"
        super().save(*args, **kwargs)
        self.generate_qr_code()

    def generate_qr_code(self):
        qr = qrcode.make(self.link)
        qr_content = io.BytesIO()
        qr.save(qr_content, format='PNG')
        self.qr_code.save(f"qr_{self.id}.png", ContentFile(qr_content.getvalue()), save=False)

    def __str__(self):
        return self.title

class Question(models.Model):
    conference = models.ForeignKey(Conference, related_name='questions', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.text}"
