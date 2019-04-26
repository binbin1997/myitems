from django.db import models
from uuslug import slugify
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    # db_index=True通过索引查找，增加搜索速度
    name = models.CharField(max_length=50, db_index=True)
    # unique商品名是唯一的，不能重复
    slug = models.SlugField(max_length=100, db_index=True, unique=True, default="1")

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:30]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, default="1")
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = '商品'
        verbose_name_plural = '商品'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:30]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
