from django.db import models

# Create your models here.

class Attachments(models.Model):
    file = models.FileField(upload_to='attachments/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name

class Mailing(models.Model):
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    attachment = models.ManyToManyField(Attachments, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'

class OTPMailing(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Batch(models.Model):
    name = models.IntegerField(max_length=4)
    recipients = models.CharField(max_length=2000)