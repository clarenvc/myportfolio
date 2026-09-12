import uuid
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tool_name = models.CharField(max_length=100) # Contoh: VS Code
    category_title = models.CharField(max_length=100) # Contoh: Programming
    description = models.TextField() # Contoh: Short description of how I use VS Code...
    tool_logo_url = models.URLField(blank=True, null=True) # Untuk logo software di kiri (misal logo VS Code)
    
    # Kamu bisa menyimpan daftar bahasa pemrograman/ikon terkait (misal menggunakan Font Awesome classes atau teks)
    sub_skills = models.TextField(blank=True, null=True) # Contoh: Java, Python (bisa dirender dengan ikon)

    def __str__(self):
        return f"{self.tool_name} - {self.category_title}"