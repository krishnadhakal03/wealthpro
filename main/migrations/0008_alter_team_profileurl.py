# Generated by Django 5.1.4 on 2025-01-06 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_team_profileurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='profileUrl',
            field=models.ImageField(default='images/default.jpg', upload_to='images/'),
        ),
    ]
