# Generated by Django 5.0.2 on 2024-04-30 09:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField()),
                ('mobile_number', models.CharField(max_length=15)),
                ('verification_sms_code', models.CharField(blank=True, max_length=6)),
                ('verification_email_code', models.CharField(blank=True, max_length=6)),
                ('is_sms_verified', models.BooleanField(default=False)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('sms_time_for_valid', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('text', 'Text'), ('area', 'Area'), ('bool', 'Boolean'), ('radio', 'Radio Botton')], max_length=10)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('question_text', models.CharField(max_length=255)),
                ('order', models.IntegerField()),
                ('group', models.IntegerField()),
                ('page', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('required', models.BooleanField(default=False)),
                ('prerequisite', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinet_patient_form.questions')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerTemplateQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinet_patient_form.questions')),
            ],
        ),
        migrations.CreateModel(
            name='AssignedRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinet_patient_form.role')),
            ],
        ),
    ]
