# Generated by Django 4.1.2 on 2022-10-25 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0002_remove_product_ryans_remove_product_startech_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ryans',
            name='product',
        ),
        migrations.RemoveField(
            model_name='startech',
            name='product',
        ),
        migrations.RemoveField(
            model_name='techland',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='ryans',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='v1.ryans'),
        ),
        migrations.AddField(
            model_name='product',
            name='startech',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='v1.startech'),
        ),
        migrations.AddField(
            model_name='product',
            name='techland',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='v1.techland'),
        ),
    ]
