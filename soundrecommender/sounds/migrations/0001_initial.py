# Generated by Django 5.0.2 on 2024-02-10 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('bpm', models.IntegerField()),
                ('duration_in_seconds', models.IntegerField()),
                ('genres', models.JSONField()),
                ('credits', models.JSONField()),
            ],
        ),
    ]
