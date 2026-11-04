from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.response import Response

from main.models import Skill
from main.permissions import IsPortfolioOwnerOrReadOnly
from main.serializers import SkillSerializer

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
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
@permission_classes([IsPortfolioOwnerOrReadOnly])
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