# Generated by Django 4.1.2 on 2023-05-11 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_linkclick'),
    ]

    operations = [
        migrations.RenameField(
            model_name='linkclick',
            old_name='Link',
            new_name='link',
        ),
    ]