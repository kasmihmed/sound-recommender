# Generated by Django 5.0.2 on 2024-02-10 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sounds', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('sounds', models.ManyToManyField(to='sounds.sound')),
            ],
        ),
    ]
