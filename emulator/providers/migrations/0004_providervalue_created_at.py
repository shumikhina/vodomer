# Generated by Django 3.2.6 on 2021-08-18 07:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0003_alter_providervalue_sent_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='providervalue',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
