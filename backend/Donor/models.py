from django.db import models
from user.models import User
from django.utils.translation import gettext_lazy as _

class DonorPerson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    amount_donated = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    date_donated = models.DateTimeField(auto_now_add=True)  
    payment_status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Completed", "Completed")], default="Pending")

    def __str__(self):
        return f"{self.user.username} donated {self.amount_donated}"


class Donation(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        COMPLETED = 'Completed', _('Completed')
        FAILED = 'Failed', _('Failed')

    donor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="donations"
    )
    amount_donated = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Amount donated by the donor"
    )
    transaction_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Unique transaction ID from payment gateway"
    )
    payment_status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        help_text="Status of the payment"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Time when donation was made"
    )

    def __str__(self):
        return f"Donation of {self.amount_donated} by {self.donor.username} - {self.payment_status}"
