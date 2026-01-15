import uuid
from typing import Any, Type

from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver

PAYMENT_STATUSES = [
    ("CREATED", "created"),
    ("PENDING", "pending"), 
    ("READY", "ready"), 
    ("GIVEN", "given"), 
    ("CANCELLED", "cancelled"),
]

class Payouts(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator('0.01')],
        db_index=True
    )
    currency = models.CharField(max_length=3, db_index=True, validators=[MinLengthValidator(3)])
    bank_details = models.TextField(validators=[MinLengthValidator(1)])
    status = models.CharField(max_length=10, choices=PAYMENT_STATUSES, default="CREATED", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    description = models.TextField(null=True, blank=True, validators=[MinLengthValidator(3)])
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector"]),
        ]


@receiver(post_save, sender=Payouts)
def update_search_vector(sender: Type[Model], instance: Model, **kwargs: Model) -> None:
    Payouts.objects.filter(pk=instance.pk).update(
        search_vector=SearchVector('description')
    )
