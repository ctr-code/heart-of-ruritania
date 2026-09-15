from django.shortcuts import render


def index(request):
    """View for the home page"""
    return render(
        request,
        "core/index.html",
    )


def contact(request):
    """View for the contact page"""
    return render(
        request,
        "core/contact.html",
    )
