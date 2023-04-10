from django.db import models

# Create models here.
 
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    is_encrypted = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)
    STATUS_CHOICES = [
        ('SENT', 'Sent'),
        ('DELIVERED', 'Delivered'),
        ('READ', 'Read'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SENT')   


    class Meta:
        ordering = ['-sent_at']
    def __id__(self):
        return self.id
    def __str__(self):
        return self.content

class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_users')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_by_users')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, blank=True, null=True)
    reason = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.reporter} reported {self.reported_user} for {self.reason}' 

 
