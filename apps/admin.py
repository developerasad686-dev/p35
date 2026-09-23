from django.contrib import admin

from apps.models import Product, Category, ProductImage, Tag

# Register your models here.
@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    min_num = 1
    max_num = 10
    extra = 0

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    pass


