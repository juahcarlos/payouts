from decimal import Decimal, InvalidOperation

from rest_framework import serializers

from payouts.models import Payouts


class PayoutSerializer(serializers.ModelSerializer[Payouts]):
    # We remove 'min_value' from here and move it
    # to self.validate_amount() method to prevent the TypeError
    # between string and Decimal during internal DRF validation
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Payouts
        fields = ['id', 'amount', 'currency', 'bank_details', 'status', 'description']
        read_only_fields = ['id']

    def validate_amount(self, value: Decimal|str|float) -> Decimal:
        """
        Explicitly convert value to Decimal and validate.
        """
        try:
            amount_val = Decimal(str(value))
        except (ValueError, InvalidOperation):
            raise serializers.ValidationError("Invalid number format.")

        if amount_val <= Decimal('0.00'):
            raise serializers.ValidationError("Amount must be greater than zero.")
            
        return amount_val
