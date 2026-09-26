from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm


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


@login_required
def profile(request):
    """View for the profile page"""

    if request.method == "POST":
        form = ProfileForm(data=request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data["email"]
            request.user.save()
    else:
        form = ProfileForm(initial={"email": request.user.email})

    return render(
        request,
        "core/profile.html",
        {
            "form": form,
        }
    )
