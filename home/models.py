from django.db import models
from tinymce.models import HTMLField
import re

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
    tracking = models.BooleanField(default=False)
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
    name = models.CharField(max_length=30)
    recipients = models.CharField(max_length=2000)

    def __str__(self):
        return str(self.name)
    @property
    def recipients_as_list(self):
        return [ recipient.strip() for recipient in self.recipients.split(',') ]
    
    class Meta:
        verbose_name = 'Batch'
        verbose_name_plural = 'Batches'

    def is_valid_email(self, email):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(email_regex, email))

    def save(self, *args, **kwargs):
        unique_recipients = list(set(
            email.strip() for email in self.recipients_as_list
            if email.strip() and self.is_valid_email(email)
        ))

        # Join the valid recipients back into a string
        self.recipients = ','.join(unique_recipients)

        # Call the superclass save method
        super().save(*args, **kwargs)

    
class MailingToken(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mailing_token')
    token = models.CharField(max_length=100)
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token
    
    @property
    def is_sent(self):
        return self.sent
