from django.shortcuts import render

from main.models import Experience


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