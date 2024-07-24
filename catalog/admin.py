from django.contrib import admin
from catalog.models import Product, Category
@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
