from django.db import models


class Course(models.Model):
    """A course that appears on the menu"""
    name = models.CharField()
    order = models.PositiveBigIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"


class Dish(models.Model):
    """A dish that appears within a course on the menu"""
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='dishes')
    active = models.BooleanField()
    price = models.PositiveIntegerField(help_text='Price in pence')
    name = models.CharField()
    description = models.CharField()
    order = models.PositiveBigIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({'Active' if self.active else 'Inactive'})"
