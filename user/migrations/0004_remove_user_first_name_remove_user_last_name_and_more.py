# Generated by Django 4.1.2 on 2023-03-31 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_account_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='auth_provider',
            field=models.CharField(blank=True, choices=[('email', 'Email'), ('google', 'Google'), ('facebook', 'Facebook')], default='email', max_length=30, verbose_name='auth provider'),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=30, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=30, verbose_name='username'),
        ),
    ]