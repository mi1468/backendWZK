# Generated by Django 5.0.2 on 2024-05-03 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinet_patient_form', '0002_remove_assignedrule_role_remove_assignedrule_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Patient',
        ),
    ]
