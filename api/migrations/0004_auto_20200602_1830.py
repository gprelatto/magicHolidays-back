# Generated by Django 3.0.6 on 2020-06-02 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200601_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='transactionNumber',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
