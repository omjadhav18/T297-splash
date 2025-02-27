from django.db import models
from user.models import User
from django.utils import timezone


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    institute = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.institute.username})"


class InstituteRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    institute = models.ForeignKey(User, on_delete=models.CASCADE, related_name="institute_requests")  
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="requests")  
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    approved_at = models.DateTimeField(blank=True, null=True) 
    rejected_at = models.DateTimeField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.institute.username} - {self.item.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        if self.status == 'Approved' and not self.approved_at:
            self.approved_at = timezone.now()
        elif self.status == 'Rejected' and not self.rejected_at:
            self.rejected_at = timezone.now()
        super().save(*args, **kwargs)