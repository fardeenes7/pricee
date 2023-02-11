# Generated by Django 4.1.2 on 2023-02-09 13:30

from django.db import migrations, models
import v1.models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0012_product_last_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='best_price',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(v1.models.SET_OTHERS), related_name='subcategories', to='v1.category'),
        ),
    ]
