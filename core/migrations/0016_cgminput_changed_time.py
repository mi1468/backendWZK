# Generated by Django 5.0.2 on 2024-05-04 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_cgminput'),
    ]

    operations = [
        migrations.AddField(
            model_name='cgminput',
            name='changed_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
