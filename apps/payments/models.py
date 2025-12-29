from django.db import models

from apps.borrowing.models import Borrowing


# Create your models here.
class Payment(models.Model):
    status = models.BooleanField(default=False, choices=[
        ("PENDING", "PAID"),
    ])
    type = models.CharField(max_length=10, choices=[
        ("PAYMENT", "FINE"),
    ])
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE, related_name="payments")
    session_url = models.URLField(max_length=500, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment #{self.id} — ${self.money_to_pay}"
