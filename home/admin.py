from django.contrib import admin

# Register your models here.

from .models import Batch, Mailing, Attachments, OTPMailing

admin.site.register(Batch)
admin.site.register(Mailing)
admin.site.register(Attachments)
admin.site.register(OTPMailing)
