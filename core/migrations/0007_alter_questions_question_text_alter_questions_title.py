# Generated by Django 5.0.2 on 2024-03-20 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_questions_page_questions_prerequisite_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='question_text',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='questions',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
