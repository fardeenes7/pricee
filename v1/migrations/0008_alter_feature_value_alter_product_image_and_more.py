# Generated by Django 4.1.2 on 2022-10-30 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0007_alter_product_sub_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='value',
            field=models.CharField(max_length=1023),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(blank=True, max_length=511),
        ),
        migrations.AlterField(
            model_name='product',
            name='model',
            field=models.CharField(blank=True, max_length=511),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=511),
        ),
    ]
