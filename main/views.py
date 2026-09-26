from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from main.models import Experience, Skill, Education
from main.forms import SkillForm, EducationForm


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

# ===========================================================

def show_experience(request):
    context = {
        "name": "Karen Lim",
        "nickname": "Karen",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

# ===========================================================

def show_skills(request):
    json_response = get_skills_json(request)
    deserialized_skills = serializers.deserialize("json", json_response.content.decode("utf-8"))
    skills = [skill.object for skill in deserialized_skills]
    
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

def get_skills_json(request):
    tool_query = request.GET.get("tool", "").strip()
    skills = Skill.objects.all()
    
    if tool_query:
        skills = skills.filter(tool_name__icontains=tool_query)

    skills_json = serializers.serialize("json", skills)
    return HttpResponse(skills_json, content_type="application/json")

def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
  
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill successfully deleted!")
        return redirect("main:show_skills")
        
    return redirect("main:show_skills")

# ===========================================================

def get_education_json(request):
    educations = Education.objects.all()
    educations_json = serializers.serialize("json", educations)
    return HttpResponse(educations_json, content_type="application/json")


def show_education(request):
    json_response = get_education_json(request)
    educations_deserialized = serializers.deserialize("json", json_response.content.decode("utf-8"))
    educations = [edu.object for edu in educations_deserialized]
    
    context = {
        "name": "Karen Lim", 
        "nickname": "Karen",
        "educations": educations,
    }
    return render(request, "education.html", context)


def create_education(request):
    form = EducationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Education history added successfully!")
        return redirect("main:show_education")
        
    context = {
        "name": "Karen Lim",
        "nickname": "Karen",
        "form": form
    }
    return render(request, "education_form.html", context)


def edit_education(request, id):
    education = get_object_or_404(Education, pk=id)
    form = EducationForm(request.POST or None, instance=education)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Education history successfully updated!")
        return redirect("main:show_education")
        
    context = {
        "name": "Karen Lim",
        "nickname": "Karen",
        "form": form
    }
    return render(request, "education_form.html", context) 


def delete_education(request, id):
    education = get_object_or_404(Education, pk=id)
    if request.method == "POST":
        education.delete()
        messages.success(request, "Education history successfully deleted!")
        return redirect("main:show_education")
    
    return redirect("main:show_education")

# =======================================================================

def register(request): 
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.succes(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Karen",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("main: show_main")

    context = {
        "name": "Karen",
        "form": form,
    }