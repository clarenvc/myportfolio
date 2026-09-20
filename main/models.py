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
    tool_name = models.CharField(max_length=100)
    category_title = models.CharField(max_length=100) 
    description = models.TextField() 
    tool_logo_url = models.URLField(blank=True, null=True) # Untuk logo software di kiri 
    
    sub_skills = models.TextField(blank=True, null=True) # Contoh: Java, Python (bisa dirender dengan ikon)

    def __str__(self):
        return f"{self.tool_name} - {self.category_title}"
    
class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_name = models.CharField(max_length=255)
    start_year = models.IntegerField()
    end_year = models.CharField(max_length=50) # Memakai CharField agar bisa diisi angka "2025" atau teks "Present"
    description = models.TextField()

    def __str__(self):
        return self.school_name