from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'category'
        verbose_name_plural = "categories"

    def __str__(self):
        return f"Category {self.name}"

    def get_absolute_url(self):
        return reverse("shop:category_products",args=[self.slug])




class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(default="No description")
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f"Product {self.name}"

    def get_absolute_url(self):
        return reverse("shop:details",args=[self.id,self.slug])
