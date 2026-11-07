from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.response import Response

from main.models import Skill, Education, Experience
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import SkillSerializer, EducationSerializer, ExperienceSerializer



#SKILL API VIEW

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def skill_list(request):
    # GET: Menampilkan semua skill (bisa difilter lewat ?tool=...)
    if request.method in ("GET", "HEAD"):
        skills = Skill.objects.prefetch_related("starred_by").order_by("tool_name", "id")
        tool_query = request.query_params.get("tool", "").strip()
        
        if tool_query:
            skills = skills.filter(tool_name__icontains=tool_query)
            
        serializer = SkillSerializer(skills, many=True, context={"request": request})
        return Response(serializer.data)

    # POST: Menambah skill baru
    elif request.method == "POST":
        serializer = SkillSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def skill_detail(request, skill_id):
    skill = get_object_or_404(
        Skill.objects.prefetch_related("starred_by"), pk=skill_id
    )

    if request.method in ("GET", "HEAD"):
        serializer = SkillSerializer(skill, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = SkillSerializer(
        skill,
        data=request.data,
        partial=(request.method == "PATCH"),
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def skill_star(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    if skill.starred_by.filter(pk=request.user.pk).exists():
        skill.starred_by.remove(request.user)
    else:
        skill.starred_by.add(request.user)

    serializer = SkillSerializer(skill, context={"request": request})
    return Response(serializer.data)



#EDUCATION API VIEWS

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_list(request):
    if request.method in ("GET", "HEAD"):
        educations = Education.objects.prefetch_related("starred_by").order_by("-start_year", "school_name", "id")
        query = request.query_params.get("q", "").strip()

        if query:
            educations = educations.filter(school_name__icontains=query)

        serializer = EducationSerializer(educations, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = EducationSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_detail(request, education_id):
    education = get_object_or_404(
        Education.objects.prefetch_related("starred_by"), pk=education_id
    )

    if request.method in ("GET", "HEAD"):
        serializer = EducationSerializer(education, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = EducationSerializer(
        education,
        data=request.data,
        partial=(request.method == "PATCH"),
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def education_star(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    if education.starred_by.filter(pk=request.user.pk).exists():
        education.starred_by.remove(request.user)
    else:
        education.starred_by.add(request.user)

    serializer = EducationSerializer(education, context={"request": request})
    return Response(serializer.data)



#EXPERIENCE API VIEWS

@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list(request):
    if request.method == "GET":
        # Fitur Pencarian berdasarkan nama perusahaan (company)
        company_query = request.query_params.get("company", "").strip()
        experiences = Experience.objects.prefetch_related("starred_by").all()
        
        if company_query:
            experiences = experiences.filter(company__icontains=company_query)
            
        serializer = ExperienceSerializer(experiences, many=True, context={"request": request})
        return Response(serializer.data)
        
    elif request.method == "POST":
        serializer = ExperienceSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Detail, Edit (PUT/PATCH), dan Hapus (DELETE)
@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(Experience.objects.prefetch_related("starred_by"), pk=experience_id)
    
    if request.method in ("GET", "HEAD"):
        serializer = ExperienceSerializer(experience, context={"request": request})
        return Response(serializer.data)
        
    if request.method == "DELETE":
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    serializer = ExperienceSerializer(
        experience, 
        data=request.data, 
        partial=(request.method == "PATCH"),
        context={"request": request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


# Memberikan/Menghapus Star
@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)
        
    serializer = ExperienceSerializer(experience, context={"request": request})
    return Response(serializer.data)