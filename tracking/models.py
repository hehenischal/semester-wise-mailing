from django.db import models
from home.models import Mailing
import uuid

class MailSeen(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    mailing_id = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mail_seen')
    count = models.IntegerField(default=0)

    def increase_count(self):
        self.count += 1
        self.save()

    def total_recipients(self):
        recipients = sum(batch.recipients.count(',') + 1 for batch in self.mailing_id.batches.all())
        return recipients

    def __str__(self):
        return self.mailing_id.subject
    
    class Meta:
        verbose_name = 'Mail Seen'
        verbose_name_plural = 'Mail Seen'
