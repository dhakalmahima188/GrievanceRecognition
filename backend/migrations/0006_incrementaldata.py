# Generated by Django 4.2.7 on 2024-03-09 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_audiorecording_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncrementalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]