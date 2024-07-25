from django.db import models
from home.models import Mailing


class MailSeen(models.Model):
    token = models.UUIDField()
    mailing_id = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)