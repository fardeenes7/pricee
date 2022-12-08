from email.policy import default
from enum import auto
from django.db import models
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_delete
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=511)
    sub_category = models.ForeignKey('SubCategory', related_name='products', on_delete=models.CASCADE, null=True)
    best_price = models.CharField(max_length=10)
    brand = models.CharField(max_length=255, blank=True)
    model = models.CharField(max_length=511, blank=True)
    image = models.CharField(max_length=511, blank=True)
    startech = models.OneToOneField('Startech', on_delete=models.CASCADE, blank=True, null=True)
    ryans = models.OneToOneField('Ryans', on_delete=models.CASCADE, blank=True, null=True)
    techland = models.OneToOneField('Techland', on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        st = self.startech.price if self.startech else 0
        ry = self.ryans.price if self.ryans else 0
        tl = self.techland.price if self.techland else 0

        best_price = [i for i in [st, ry, tl] if i>0]
        try:
            self.best_price = min(best_price)
        except:
            self.best_price = 0
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, null = True, blank = True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE, null = True, blank = True)
    name = models.CharField(max_length=255, null = True, blank = True)

    def __str__(self):
        return self.name


class Startech(models.Model):
    link = models.URLField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    regular_price = models.CharField(max_length=255, null = True, blank = True)
    status = models.CharField(max_length=255, null = True, blank = True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.last_updated = datetime.now()
        super(Startech, self).save(*args, **kwargs)

    def __str__(self):
        return self.link.replace("https://www.startech.com.bd/", "").replace("-", " ").title()



class Ryans(models.Model):
    link = models.URLField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    regular_price = models.CharField(max_length=10, null = True, blank = True)
    status = models.CharField(max_length=255, null = True, blank = True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.last_updated = datetime.now()
        super(Ryans, self).save(*args, **kwargs)

    def __str__(self):
        return self.link.replace("https://www.ryanscomputers.com/", "").replace("-", " ").title()



class Techland(models.Model):
    link = models.URLField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    regular_price = models.CharField(max_length=255, null = True, blank = True)
    status = models.CharField(max_length=255, null = True, blank = True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.last_updated = datetime.now()
        super(Techland, self).save(*args, **kwargs)

    def __str__(self):
        return self.link.replace("https://www.techlandbd.com/", "").replace("-", " ").title()
    


class Feature(models.Model):
    product = models.ForeignKey(Product, related_name='features' ,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=1023)

    def __str__(self):
        return self.name


@receiver(post_delete, sender=Product)
def submission_delete(sender, instance, **kwargs):
    if instance.startech:
        instance.startech.delete()
    if instance.ryans:
        instance.ryans.delete()
    if instance.techland:
        instance.techland.delete()
