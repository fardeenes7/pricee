from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.


class Shop(models.Model):
    name = models.CharField(max_length=255)
    href = models.CharField(max_length=511)
    logo = models.ImageField(upload_to='logos', blank=True, null=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


def SET_OTHERS():
    return Category.objects.get_or_create(name="Others", slug="others")[0]


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    category = models.ForeignKey('Category', related_name='sub_categories', on_delete=models.SET(SET_OTHERS), null=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=511, default="N/A")
    slug = models.SlugField(max_length=511, null=True, blank=True)
    sub_category = models.ForeignKey('SubCategory', related_name='products', on_delete=models.CASCADE, null=True)
    best_price = models.IntegerField(default=0)
    brand = models.CharField(max_length=255, blank=True)
    model = models.CharField(max_length=511, blank=True)
    brand_slug = models.SlugField(max_length=255, blank=True)
    model_slug = models.SlugField(max_length=511, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.brand_slug = slugify(self.brand)
        self.model_slug = slugify(self.model)
        if self.brand:
            self.model_slug = self.model_slug.replace(self.brand_slug, '')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Link(models.Model):
    shop = models.ForeignKey(Shop, related_name='links', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', related_name='links', on_delete=models.CASCADE)
    href = models.CharField(max_length=511)
    price = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='N/A')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop.name + ': ' + self.product.name

    def save(self, *args, **kwargs):
        links = self.product.links.all()
        prices = [int(i.price) for i in links if (i.price and i.price>0)] + [self.price]
        self.product.best_price = min(prices) if prices else 0
        self.product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


class Image(models.Model):
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)
    href = models.URLField(max_length=511, blank=True, null=True)
    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.product.save()



class Feature(models.Model):
    product = models.ForeignKey(Product, related_name='features' ,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=2047)

    def __str__(self):
        return self.name

"""
@receiver(post_delete, sender=Product)
def submission_delete(sender, instance, **kwargs):
    if instance.startech:
        instance.startech.delete()
    if instance.ryans:
        instance.ryans.delete()
    if instance.techland:
        instance.techland.delete()
"""