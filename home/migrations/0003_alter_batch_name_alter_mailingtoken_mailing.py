# Generated by Django 4.2.14 on 2024-07-15 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_mailing_message_mailingtoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='name',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='mailingtoken',
            name='mailing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mailing_token', to='home.mailing'),
        ),
    ]
