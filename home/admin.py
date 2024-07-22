from django.contrib import admin

# Register your models here.

from .models import Batch, Mailing, Attachments, OTPMailing, MailingToken


admin.site.register(Batch)
admin.site.register(Mailing, list_display=['email', 'subject', 'created_at','get_attachments'])
admin.site.register(Attachments)
admin.site.register(OTPMailing)
admin.site.register(MailingToken, list_display=['mailing', 'token', 'is_sent', 'created_at'])
