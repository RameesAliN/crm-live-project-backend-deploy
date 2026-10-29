from django.conf import settings
from django.db import models

class Task(models.Model):
    TASK_TYPE_CHOICES = [
        ("call", "Call"),
        ("email", "Email"),
        ("meeting", "Meeting"),
        ("follow-up", "Follow Up"),
        ("reminder", "Reminder"),
    ]

    PRIORITY_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
        ("urgent", "Urgent"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    task_name = models.CharField(max_length=255)
    due_date = models.DateField()
    due_time = models.TimeField()
    note = models.TextField()
    task_type = models.CharField(max_length=20,choices=TASK_TYPE_CHOICES,)
    priority = models.CharField(max_length=10,choices=PRIORITY_CHOICES,)

    

    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,
        null=True,blank=True,related_name="assigned_tasks",)
    
    lead = models.ForeignKey("leads.Lead",on_delete=models.CASCADE,
        null=True,blank=True,related_name="tasks",)

    company = models.ForeignKey("companies.Company",on_delete=models.CASCADE,
        null=True,blank=True,related_name="tasks",)

    deal = models.ForeignKey("deals.Deal",on_delete=models.CASCADE,
        null=True,blank=True,related_name="tasks",)

    ticket = models.ForeignKey("tickets.Ticket",on_delete=models.CASCADE,
        null=True,blank=True,related_name="tasks",)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="pending",)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_name