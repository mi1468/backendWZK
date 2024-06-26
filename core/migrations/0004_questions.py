# Generated by Django 5.0.2 on 2024-03-20 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_patient_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('text', 'Text'), ('area', 'Area'), ('bool', 'Boolean')], max_length=10)),
                ('title', models.CharField(max_length=100)),
                ('input_text', models.CharField(blank=True, max_length=255, null=True)),
                ('input_area', models.TextField(blank=True, null=True)),
                ('input_bool', models.BooleanField(default=False)),
                ('order', models.IntegerField()),
                ('group', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
