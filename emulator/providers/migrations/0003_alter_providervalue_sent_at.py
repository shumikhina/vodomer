# Generated by Django 3.2.6 on 2021-08-17 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0002_rename_received_at_providervalue_sent_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providervalue',
            name='sent_at',
            field=models.DateTimeField(null=True),
        ),
    ]