from django.urls import path

from main.views import (
    show_main, show_experience, 
    show_skills, create_skill, get_skills_json, delete_skill, 
    show_education, get_education_json, create_education, edit_education, delete_education,
)

app_name = "main"

urlpatterns = [

# MAIN 
    path("", show_main, name="show_main"),

# EXPERIENCE
    path("experience/", show_experience, name="show_experience"),

# SKILLS
    path("skills/", show_skills, name="show_skills"),
    path("skills/add/", create_skill, name="create_skill"),
    path("api/skills/", get_skills_json, name="get_skills_json"),
    path("skills/<uuid:skill_id>/delete/", delete_skill, name="delete_skill"),

# EDUCATION
    path("education/", show_education, name="show_education"),
    path("api/education/", get_education_json, name="get_education_json"),
    path("education/add/", create_education, name="create_education"),
    path("education/edit/<uuid:id>/", edit_education, name="edit_education"),
    path("education/delete/<uuid:id>/", delete_education, name="delete_education"),
]