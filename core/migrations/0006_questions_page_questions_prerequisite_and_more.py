# Generated by Django 5.0.2 on 2024-03-20 09:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_input_text_questions_question_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='page',
            field=models.IntegerField(default=bool),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questions',
            name='prerequisite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.questions'),
        ),
        migrations.AddField(
            model_name='questions',
            name='required',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='questions',
            name='type',
            field=models.CharField(choices=[('text', 'Text'), ('area', 'Area'), ('bool', 'Boolean'), ('radio', 'Radio Botton')], max_length=10),
        ),
    ]
