# Generated by Django 3.2.3 on 2022-05-26 12:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20220419_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='token',
            field=models.CharField(default=uuid.uuid4, max_length=36),
        ),
    ]