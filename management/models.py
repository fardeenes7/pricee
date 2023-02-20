from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

class BannerAd(models.Model):
    SIZE_CHOICES = (
        ('1x1', '1x1'),
        ('3x1', '3x1'),
    )
    image = models.ImageField(upload_to='bannerads/')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    body = models.TextField(null=True, blank=True)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, default='1x1')
    active = models.BooleanField(default=True)
    scheduledFrom = models.DateTimeField(null=True, blank=True)
    scheduledTo = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.url

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Banner Ads'
    
    def save(self, *args, **kwargs):
        if self.size == '1x1' and self.active == True:
            banners = BannerAd.objects.filter(size='1x1', active=True).exclude(id=self.id).order_by('-id')[3:]
            for banner in banners:
                banner.active = False
                banner.save()
        elif self.size == '3x1' and self.active == True:
            banners = BannerAd.objects.filter(size='3x1', active=True).exclude(id=self.id).order_by('-id')[1:]
            for banner in banners:
                banner.active = False
                banner.save()
        self.slug = slugify(self.title)
        super(BannerAd, self).save(*args, **kwargs)

    #on delete method
    def delete(self, *args, **kwargs):
        if self.size == '1x1':
            banner = BannerAd.objects.filter(size='1x1', active=False).order_by('-id')[:1]
            banner.active = True
            banner.save()
        elif self.size == '3x1':
            banner = BannerAd.objects.filter(size='3x1', active=False).order_by('-id')[:1]
            banner.active = True
            banner.save()
                
        super(BannerAd, self).delete(*args, **kwargs)

