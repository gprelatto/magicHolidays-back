# Generated by Django 3.0.6 on 2020-06-01 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_notification_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='date_from',
        ),
        migrations.RemoveField(
            model_name='token',
            name='date_to',
        ),
        migrations.AddField(
            model_name='token',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
