from django.db import models
from institute.models import InstituteRequest

from django.db import models
from django.utils import timezone

class AdminRequestQueue(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Processing', 'Processing'), ('Completed', 'Completed')]
    institute_request = models.ForeignKey(InstituteRequest, on_delete=models.CASCADE, related_name='admin_queue')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    added_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self): return f"Queue - {self.institute_request.institute.username} ({self.institute_request.item.name})"
    def mark_processing(self): self.status, self.processed_at = 'Processing', timezone.now(); self.save()
    def mark_completed(self): self.status, self.completed_at = 'Completed', timezone.now(); self.save()

