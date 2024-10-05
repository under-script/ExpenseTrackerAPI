from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class Category(TimeStampedModel):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name


class Expense(TimeStampedModel):
    description = models.CharField(max_length=200)
    amount = models.IntegerField()
    owner = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'description'], name='unique_expense_per_user')
        ]

    def __str__(self):
        return self.description
