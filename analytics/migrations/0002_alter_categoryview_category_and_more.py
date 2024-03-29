# Generated by Django 4.1.2 on 2023-05-06 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v2', '0002_alter_shop_logo'),
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryview',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categoryviewcount', to='v2.subcategory'),
        ),
        migrations.AlterField(
            model_name='productview',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewcount', to='v2.product'),
        ),
    ]
