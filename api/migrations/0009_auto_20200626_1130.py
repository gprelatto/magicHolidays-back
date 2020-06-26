# Generated by Django 3.0.6 on 2020-06-26 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_customer_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='contact_source',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='rez',
            name='people_count',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='rez',
            name='tickets_count',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='birth_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user_type',
            name='feePercentage',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]