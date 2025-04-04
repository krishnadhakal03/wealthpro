# Generated by Django 5.1.4 on 2025-03-23 21:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_appointment_businesscontact_contactus_videodirect'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZoomAvailableSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('meeting_id', models.CharField(blank=True, max_length=255, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ZoomCredentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(default='wealthProZoomApp', max_length=255)),
                ('account_id', models.CharField(default='Sn2rpXqFRmC7AitP028Xmg', max_length=255)),
                ('client_id', models.CharField(default='FC0NGNG7QfyRU7yLXHCrMw', max_length=255)),
                ('client_secret', models.CharField(default='68kBbdAS49mzxtvQebGl1BM5fzN6AgBp', max_length=255)),
                ('secret_token', models.CharField(default='Hapqqa_CRN2HzdT0R-kgiw', max_length=255)),
                ('verification_token', models.CharField(default='TdcWSKzkSV6J3PBjo1qVpQ', max_length=255)),
                ('access_token', models.TextField(blank=True, null=True)),
                ('refresh_token', models.TextField(blank=True, null=True)),
                ('token_expiry', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Zoom Credentials',
            },
        ),
        migrations.AddField(
            model_name='appointment',
            name='zoom_meeting_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='zoom_meeting_password',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='zoom_meeting_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='zoom_slot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointments', to='main.zoomavailableslot'),
        ),
    ]
