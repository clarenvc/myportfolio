from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience
from main.models import Skill
from main.forms import SkillForm


def show_main(request):
    context = {
        "nickname": "Karen",
        "name": "Karen Lim",
        "npm": "2506623982",
        "study_program": "S1 Information Systems",
        "bio": (
            "2nd Year student of Universitas Indonesia's Information System"
            " program. Currently pursuing my degree with interests in game"
            " development and web development."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Karen Lim",
        "nickname": "Karen",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_skills(request):
    skills = Skill.objects.all()
    context = {
        'name': 'Karen Lim',
        'nickname': 'Karen',
        'skills': skills,
    }
    return render(request, 'skills.html', context)

def create_skill(request):
    form = SkillForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill baru berhasil ditambahkan!")
        return redirect("main:show_skills")
        
    context = {
        "name": "Karen Lim",
        "nickname": "Karen",
        "form": form,
    }
    return render(request, "skills_form.html", context)