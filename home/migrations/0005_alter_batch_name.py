# Generated by Django 4.2.14 on 2024-07-24 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_mailing_tracking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
