from django.shortcuts import render, get_object_or_404, reverse
from django.db import transaction
from django.db.models import Max
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from .forms import DishForm
from .models import Course, Dish


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
def menu_admin(request):
    """View for the menu admin page"""

    courses = Course.objects.order_by('order')

    return render(
        request,
        "menu/menu_admin.html",
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
            return HttpResponseRedirect(reverse('menu_admin'))
    else:
        dish_form = DishForm()

    return render(
        request,
        "menu/add_dish.html",
        {
            "course": course,
            "dish_form": dish_form,
        },
    )


@staff_member_required
def edit_dish(request, dish_id):
    """View to edit the given dish"""
    dish = get_object_or_404(Dish, pk=dish_id)

    if request.method == "POST":
        dish_form = DishForm(instance=dish, data=request.POST)
        if dish_form.is_valid():
            dish = dish_form.save(commit=False)
            dish.save()
            messages.add_message(
                request, messages.SUCCESS,
                f'Edited {dish.name}'
            )
            return HttpResponseRedirect(reverse('menu_admin'))
    else:
        dish_form = DishForm(instance=dish)

    return render(
        request,
        "menu/edit_dish.html",
        {
            "dish": dish,
            "dish_form": dish_form,
        },
    )


@staff_member_required
def delete_dish(request, dish_id):
    """
    The delete_dish endpoint, which deletes a dish and redirects
    to the menu page
    """
    if request.method == "POST":
        dish = get_object_or_404(Dish, pk=dish_id)
        dish.delete()
        messages.add_message(
            request, messages.SUCCESS,
            f'{dish.name} deleted.'
        )

    return HttpResponseRedirect(reverse('menu_admin'))


@staff_member_required
def toggle_dishes(request, course_id):
    """View to toggle dishes for the given course atomically"""
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
        # The POST data contains names of the form dish_<id> and active_<id>.

        # Parse the POST data for the ids of dishes that were present
        exists_set = set(int(id[5:])
                         for id in request.POST if id.startswith("dish_"))

        # Parse the POST data for the ids of dishes that were selected
        active_set = set(int(id[7:])
                         for id in request.POST if id.startswith("active_"))

        # Update the active menu items in one go
        with transaction.atomic():
            for dish in course.dishes.all():
                if dish.id in exists_set:
                    dish.active = dish.id in active_set
                    dish.save()

        messages.add_message(
            request, messages.SUCCESS,
            f'Updated dishes in {course.name}.'
        )
        return HttpResponseRedirect(reverse('menu_admin'))

    return render(
        request,
        "menu/toggle_dishes.html",
        {
            "course": course,
        },
    )


@staff_member_required
def arrange_dishes(request, course_id):
    """View to rearrange the order of dishes in a course"""
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
        # The POST data contains key-value pairs of the form:
        # dish_<id>=<order>
        # Parse the pairs to create a map from id to order.
        order_map = {
            int(id[5:]): int(order)
            for (id, order) in request.POST.items() if id.startswith("dish_")
        }
        # Update all the dishes in the course in one go
        with transaction.atomic():
            for dish in course.dishes.all():
                if dish.id in order_map:
                    dish.order = order_map[dish.id]
                    dish.save()

        messages.add_message(
            request, messages.SUCCESS,
            f'Arranged dishes in {course.name}.'
        )
        return HttpResponseRedirect(reverse('menu_admin'))

    return render(
        request,
        "menu/arrange_dishes.html",
        {
            "course": course,
        },
    )
