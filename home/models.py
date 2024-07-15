from django.db import models
from tinymce.models import HTMLField

class Attachments(models.Model):
    file = models.FileField(upload_to='attachments/')
    mailing = models.ForeignKey('Mailing', related_name='attachments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name

class Mailing(models.Model):
    email = models.EmailField(max_length=254)
    batches = models.ManyToManyField('Batch')
    subject = models.CharField(max_length=100)
    message = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    @property
    def get_attachments(self):
        return self.attachments.all()

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'

class OTPMailing(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Batch(models.Model):
    name = models.IntegerField()
    recipients = models.CharField(max_length=2000)

    def __str__(self):
        return str(self.name)
    
class MailingToken(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mailing_token')
    token = models.CharField(max_length=100)
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token
