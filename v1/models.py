from email.policy import default
from enum import auto
from django.db import models
from datetime import datetime
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    best_price = models.CharField(max_length=10)
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    image = models.CharField(max_length=100, blank=True)
    startech = models.OneToOneField('Startech', on_delete=models.CASCADE, blank=True, null=True)
    ryans = models.OneToOneField('Ryans', on_delete=models.CASCADE, blank=True, null=True)
    techland = models.OneToOneField('Techland', on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.best_price = min(self.ryans.price if self.ryans else 999999, self.startech.price if self.startech else 999999, self.techland.price if self.techland else 999999)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name



class Startech(models.Model):
    link = models.URLField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    regular_price = models.CharField(max_length=10, null = True, blank = True)
    status = models.CharField(max_length=100, null = True, blank = True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.last_updated = datetime.now()
        super(Startech, self).save(*args, **kwargs)

    def __str__(self):
        return self.link.replace("https://www.startech.com.bd/", "").replace("-", " ").title()


class Ryans(models.Model):
    link = models.URLField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    regular_price = models.CharField(max_length=10, null = True, blank = True)
    status = models.CharField(max_length=100, null = True, blank = True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.last_updated = datetime.now()
        super(Ryans, self).save(*args, **kwargs)

    def __str__(self):
        return self.Product.name


class Techland(models.Model):
    link = models.URLField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    regular_price = models.CharField(max_length=10, null = True, blank = True)
    status = models.CharField(max_length=100, null = True, blank = True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.last_updated = datetime.now()
        super(Techland, self).save(*args, **kwargs)

    def __str__(self):
        return self.Product.name


class Feature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.name