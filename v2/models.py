from django.db import models
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.template.defaultfilters import slugify
# Create your models here.

class Shop(models.Model):
    name = models.CharField(max_length=255)
    href = models.CharField(max_length=511)
    logo = models.ImageField(upload_to='logos', blank=True, null=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Shop, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=511)
    slug = models.SlugField(max_length=511, null=True, blank=True)
    sub_category = models.ForeignKey('SubCategory', related_name='products', on_delete=models.CASCADE, null=True)
    best_price = models.CharField(max_length=10, default=0)
    brand = models.CharField(max_length=255, blank=True)
    model = models.CharField(max_length=511, blank=True)
    last_updated = models.DateTimeField(auto_now=True)


class Link(models.Model):
    shop = models.ForeignKey(Shop, related_name='links', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', related_name='links', on_delete=models.CASCADE)
    href = models.CharField(max_length=511)
    price = models.CharField(max_length=10, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop.name + ' - ' + self.product.name

    def save(self, *args, **kwargs):
        super(Link, self).save(*args, **kwargs)
        self.product.save()

    def delete(self, *args, **kwargs):
        super(Link, self).delete(*args, **kwargs)
        self.product.save()


class Image(models.Model):
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/products', blank=True, null=True)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)
        self.product.save()

    def delete(self, *args, **kwargs):
        super(Image, self).delete(*args, **kwargs)
        self.product.save()











class Product(models.Model):
    name = models.CharField(max_length=511)
    slug = models.SlugField(max_length=511, null=True, blank=True)
    sub_category = models.ForeignKey('SubCategory', related_name='products', on_delete=models.CASCADE, null=True)
    best_price = models.CharField(max_length=10, default=0)
    brand = models.CharField(max_length=255, blank=True)
    model = models.CharField(max_length=511, blank=True)
    image = models.CharField(max_length=511, blank=True)
    startech = models.OneToOneField('Startech', on_delete=models.CASCADE, blank=True, null=True)
    ryans = models.OneToOneField('Ryans', on_delete=models.CASCADE, blank=True, null=True)
    techland = models.OneToOneField('Techland', on_delete=models.CASCADE, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        st = self.startech.price if self.startech else 0
        ry = self.ryans.price if self.ryans else 0
        tl = self.techland.price if self.techland else 0
        
        best_price = [i for i in [st, ry, tl] if i>0]
        self.best_price = min(best_price) if best_price else 0
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, null = True, blank = True)
    slug = models.SlugField(max_length=255, null = True, blank = True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


def SET_OTHERS():
    return Category.objects.get_or_create(name="Others", slug="others")[0]

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete = models.SET(SET_OTHERS), null = True, blank = True)
    name = models.CharField(max_length=255, null = True, blank = True)
    slug = models.SlugField(max_length=255, null = True, blank = True)

    def __str__(self):
        return self.name



    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)


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
