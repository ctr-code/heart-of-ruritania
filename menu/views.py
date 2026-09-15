from django.shortcuts import render
from .models import Course


def menu(request):
    """View for the menu page"""

    courses = Course.objects.all()

    return render(
        request,
        "menu/menu.html",
        {
            "courses": courses,
        },
    )
