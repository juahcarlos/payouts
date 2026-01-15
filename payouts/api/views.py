from django.db import transaction
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import BaseSerializer

from payouts.models import Payouts
from payouts.tasks import process_payout

from .serializers import PayoutSerializer



class PayoutViewSet(viewsets.ModelViewSet[Payouts]):
    renderer_classes = [JSONRenderer]
    queryset = Payouts.objects.all()
    serializer_class = PayoutSerializer

    def perform_create(self, serializer: BaseSerializer[Payouts]) -> None:
        """
        Create a payout and trigger async processing after DB commit.
        Using transaction.atomic ensures data integrity.
        """
        with transaction.atomic():
            instance = serializer.save()
            # Using lambda to defer the .delay() execution until 
            # the transaction is successfully committed to the database.
            # This prevents the worker from failing with DoesNotExist.
            instance = serializer.save()
            transaction.on_commit(lambda: process_payout.delay(instance.id))

