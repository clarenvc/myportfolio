from django.urls import path
from main import api_views

app_name = "api"

urlpatterns = [
    #SKILL
    path("skills/", api_views.skill_list, name="skill-list"),
    path("skills/<uuid:skill_id>/", api_views.skill_detail, name="skill-detail"),
    path("skills/<uuid:skill_id>/star/", api_views.skill_star, name="skill-star"),

    #EDUCATION
    path("education/", api_views.education_list, name="education-list"),
    path("education/<uuid:education_id>/", api_views.education_detail, name="education-detail"),
    path("education/<uuid:education_id>/star/", api_views.education_star, name="education-star"),

    #EXPERIENCE
    path("experiences/", api_views.experience_list, name="experience-list"),
    path("experiences/<uuid:experience_id>/", api_views.experience_detail, name="experience-detail"),
    path("experiences/<uuid:experience_id>/star/", api_views.experience_star, name="experience-star"),
]