# Generated by Django 5.0.2 on 2024-05-06 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinet_patient_form', '0003_delete_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='AnswerId',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='QuestionId',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
