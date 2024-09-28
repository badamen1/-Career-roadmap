# Generated by Django 5.0.7 on 2024-09-12 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('current_job', models.CharField(max_length=100)),
                ('dream_job', models.CharField(max_length=100)),
                ('skills', models.TextField(blank=True)),
            ],
        ),
    ]