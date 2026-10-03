from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.core import serializers
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied 
from django.views.decorators.http import require_POST

from main.models import Experience, Skill, Education
from main.forms import SkillForm, EducationForm

import datetime

# LANDING PAGE (MAIN) ==================================================

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'No login sessions found.')
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
        "last_login": last_login,
    }
    return render(request, "index.html", context)

# EXPERIENCE ===========================================================

def show_experience(request):
    context = {
        "name": "Karen Lim",
        "nickname": "Karen",
    }
    return render(request, "experience.html", context)

def get_experience_json(request):
    q = request.GET.get("q", "").strip()
    experiences = Experience.objects.all()

    if q:
        experiences = experiences.filter(title__icontains=q)
    
    data = []
    for exp in experiences:
        data.append({
            "pk": str(exp.id),
            "fields": {
                "title": exp.title,
                "description": exp.description,
                "is_ongoing": exp.is_ongoing,
                # Mengambil teks display dari field choices (misal: "Organisasi", "Kepanitiaan")
                "category_display": exp.get_category_display(), 
            }
        })
        
    return JsonResponse(data, safe=False)

# SKILLS ===========================================================

def show_skills(request):
    tool_query = request.GET.get("tool", "").strip()
    
    context = {
        "nickname": "Karen",
        "tool_query": tool_query,
        "form": SkillForm(),
        # Variabel 'skills' diurus JavaScript
    }
    return render(request, "skills.html", context)

@login_required(login_url="/login/")
def create_skill(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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
    
    skills = Skill.objects.prefetch_related('starred_by').all()
    
    if tool_query:
        skills = skills.filter(tool_name__icontains=tool_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for skill in skills:
        starred_users = skill.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(skill.id),
            "fields": {
                "tool_name": skill.tool_name,
                "category_title": skill.category_title,
                "description": skill.description,
                "tool_logo_url": skill.tool_logo_url,
                "sub_skills": skill.sub_skills,
                
                # Masukkan data logika Star ke dalam JSON
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })
        
    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def delete_skill(request, skill_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    skill = get_object_or_404(Skill, pk=skill_id)
  
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill successfully deleted!")
        return redirect("main:show_skills")
        
    return redirect("main:show_skills")

@login_required(login_url="/login/")
def toggle_star_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        if request.user in skill.starred_by.all():
            skill.starred_by.remove(request.user)
        else:
            skill.starred_by.add(request.user)

    return redirect("main:show_skills")

def create_skill_ajax(request):
    # Pengecekan keamanan: hanya superuser yang bisa menambah skill
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan skill."},
            status=403,
        )
        
    # Memasukkan data POST ke dalam form Django
    form = SkillForm(request.POST)
    
    if form.is_valid():
        skill = form.save()
        return JsonResponse(
            {"message": "Skill berhasil ditambahkan.", "pk": str(skill.id)},
            status=201,
        )
        
    # Jika form tidak valid (misal ada field yang kurang), kirim pesan error
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

# EDUCATION ===========================================================

def get_education_json(request):
    q = request.GET.get("q", "").strip()
    educations = Education.objects.prefetch_related('starred_by').all()
    
    if q:
        educations = educations.filter(school_name__icontains=q)
    
    data = []
    for edu in educations:
        starred_users = edu.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False

        data.append({
            "pk": str(edu.id),
            "fields": {
                "school_name": edu.school_name,
                "start_year": edu.start_year,
                "end_year": edu.end_year,
                "description": edu.description,
                
                # Informasi Star
                "star_count": starred_users.count(),
                "is_starred": is_starred,
            }
        })
        
    return JsonResponse(data, safe=False)


def show_education(request):
    context = {
        "name": "Karen Lim", 
        "nickname": "Karen",
        # Gunakan pengecekan aman agar tidak error jika user belum login
        "is_editor": is_editor(request.user) if request.user.is_authenticated else False, 
    }
    return render(request, "education.html", context)

@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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

@login_required(login_url="/login/") 
def edit_education(request, id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied

    education = get_object_or_404(Education, pk=id)
    form = EducationForm(request.POST or None, instance=education)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Education history successfully updated!")
        return redirect("main:show_education")
        
    context = {
        "name": "Karen Lim",
        "nickname": "Karen",
        "form": form,
    }
    return render(request, "education_form.html", context) 

@login_required(login_url="/login/")
def delete_education(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    education = get_object_or_404(Education, pk=id)
    if request.method == "POST":
        education.delete()
        messages.success(request, "Education history successfully deleted!")
        return redirect("main:show_education")
    
    return redirect("main:show_education")

@login_required(login_url="/login/")
def toggle_star_education(request, id):
    education = get_object_or_404(Education, pk=id)

    if request.method == "POST":
        if request.user in education.starred_by.all():
            education.starred_by.remove(request.user)
        else:
            education.starred_by.add(request.user)

    return redirect("main:show_education")

# USER =======================================================================

def register(request): 
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "nickname": "Karen",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, form.get_user())
        response = redirect("main:show_main")
        response.set_cookie("last_login", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "nickname": "Karen",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

def is_editor(user):
    return user.groups.filter(name="Editor").exists()