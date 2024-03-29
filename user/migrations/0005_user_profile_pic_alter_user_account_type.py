# Generated by Django 4.1.2 on 2023-04-01 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_user_first_name_remove_user_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='user/profile_pics', verbose_name='profile picture'),
        ),
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.CharField(blank=True, choices=[('admin', 'Admin'), ('moderator', 'Moderator'), ('user', 'User')], default='user', max_length=30, verbose_name='account type'),
        ),
    ]
