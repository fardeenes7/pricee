from django.db import models
from v2.models import Product, SubCategory
from user.models import User

# Create your models here.

class ProductView(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} viewed by {self.user.name if self.user else "Anonymous"}'

    class Meta:
        verbose_name = 'Product View'
        verbose_name_plural = 'Product Views'
        ordering = ['-date']

class CategoryView(models.Model):
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.category.name} viewed by {self.user.name if self.user else "Anonymous"}'

    class Meta:
        verbose_name = 'Category View'
        verbose_name_plural = 'Category Views'
        ordering = ['-date']
