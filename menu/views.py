from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Max
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import DishForm
from .models import Course


def menu(request):
    """View for the menu page"""

    courses = Course.objects.order_by('order')

    return render(
        request,
        "menu/menu.html",
        {
            "courses": courses,
        },
    )


@staff_member_required
def add_dish(request, course_id):
    """View to add a dish to the given course"""
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
        dish_form = DishForm(data=request.POST)
        if dish_form.is_valid():
            dish = dish_form.save(commit=False)
            dish.course = course
            dish.order = \
                course.dishes.aggregate(Max('order'))["order__max"] + 1
            dish.save()
            messages.add_message(
                request, messages.SUCCESS,
                f'Added {dish.name}'
            )
            return HttpResponseRedirect(reverse('menu'))

    dish_form = DishForm()

    return render(
        request,
        "menu/add_dish.html",
        {
            "course": course,
            "dish_form": dish_form,
        },
    )
