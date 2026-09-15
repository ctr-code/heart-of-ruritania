from django.shortcuts import render


def menu(request):
    """View for the menu page"""
    return render(
        request,
        "menu/menu.html",
    )
