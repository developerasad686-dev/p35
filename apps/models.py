import uuid

from django.urls import reverse
from slugify import slugify
from django.db.models import CharField, Model, DecimalField, ImageField, CASCADE, ForeignKey, PositiveIntegerField, SlugField, TextField, ManyToManyField, DateTimeField, JSONField
from django_ckeditor_5.fields import CKEditor5Field


class Category(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Tag(Model):
    name = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
            if not self.slug:
                original_slug = slugify(self.name)
                # Agar bazada shunday slug bo'lsa, oxiriga tasodifiy kod qo'shamiz
                if Tag.objects.filter(slug=original_slug).exists():
                    self.slug = f"{original_slug}-{uuid.uuid4().hex[:6]}"
                else:
                    self.slug = original_slug
                    
            super().save(*args, **kwargs)


    def __str__(self):
        return self.name
     

class Product(Model):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    slug = SlugField(unique=True, blank=True)
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    discount = DecimalField(max_digits=5, decimal_places=2, default=0)
    like_count = PositiveIntegerField(default=0)
    quantity = PositiveIntegerField(default=0)
    short_description = CKEditor5Field()
    description = CKEditor5Field()
    tags = ManyToManyField('apps.Tag', related_name='products', blank=True)
    updated_at = DateTimeField(auto_now_add=True)
    created_at = DateTimeField(auto_now=True)
    shipping_cost = DecimalField(max_digits=10, decimal_places=2, default=0)
    specifications = JSONField(blank=True)

    def discounted_price(self): 
        return self.price * (1 - self.discount / 100)

    def get_absolute_url(self):
        return reverse('product_detail_page', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.name)
            # Agar bazada shunday slug bo'lsa, oxiriga tasodifiy kod qo'shamiz
            if Product.objects.filter(slug=original_slug).exists():
                self.slug = f"{original_slug}-{uuid.uuid4().hex[:6]}"
            else:
                self.slug = original_slug
                
        super().save(*args, **kwargs)

class ProductImage(Model):
    product = ForeignKey('apps.Product', CASCADE, related_name='images')
    image = ImageField(upload_to='static/products/%Y/%m/%d/')

    def __str__(self):
        return f"Image for {self.product.name}"