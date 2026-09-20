from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput
from main.models import Skill, Education

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            "tool_name",
            "category_title",
            "description",
            "tool_logo_url",
            "sub_skills",
        ]
        labels = {
            "tool_name": "Nama Alat / Skill",
            "category_title": "Kategori",
            "description": "Deskripsi",
            "tool_logo_url": "URL Logo Alat",
            "sub_skills": "Sub-skills / Bahasa Pemrograman",
        }
        widgets = {
            "tool_name": TextInput(
                attrs={
                    "placeholder": "Visual Studio Code",
                    "maxlength": 100,
                }
            ),
            "category_title": TextInput(
                attrs={
                    "placeholder": "Development Tools",
                    "maxlength": 100,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan kegunaan skill ini...",
                    "rows": 3,
                }
            ),
            "tool_logo_url": TextInput(
                attrs={
                    "placeholder": "https://upload.wikimedia.org/...",
                }
            ),
            "sub_skills": Textarea(
                attrs={
                    "placeholder": "Python, Java, Git",
                    "rows": 2,
                }
            ),
        }

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ["school_name", "start_year", "end_year", "description"]
        
        labels = {
            "school_name": "Nama Institusi / Sekolah",
            "start_year": "Tahun Mulai",
            "end_year": "Tahun Selesai",
            "description": "Deskripsi",
        }
        
        widgets = {
            "school_name": TextInput(
                attrs={"placeholder": "Universitas Indonesia", "class": "form-input"}
            ),
            "start_year": NumberInput(
                attrs={"placeholder": "2025", "class": "form-input"}
            ),
            "end_year": TextInput(
                attrs={"placeholder": "Present atau 2029", "class": "form-input"}
            ),
            "description": Textarea(
                attrs={"placeholder": "Fokus pada software engineering...", "rows": 3, "class": "form-input"}
            ),
        }