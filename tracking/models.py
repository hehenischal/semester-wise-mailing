from django.db import models
from home.models import Mailing


class MailSeen(models.Model):
    token = models.UUIDField()
    mailing_id = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    count = models.IntegerField()

    def increasecount(self):
        self.count = self.count + 1 