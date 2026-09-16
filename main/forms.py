from django.forms import ModelForm, TextInput, Textarea, URLInput
from main.models import Skill

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