from django.contrib import admin
from .models import Product, Wishlist, Contact


admin.site.register(Wishlist)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'product_code',
        'name',
        'category',
        'purity',
        'weight',
        'price',
        'stock',
        'is_featured',
    )

    list_filter = (
        'category',
        'purity',
        'is_featured',
        'is_new_arrival',
        'is_best_seller',
    )

    search_fields = (
        'name',
        'product_code',
    )

    list_per_page = 20
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'phone',
        'created_at',
    )

    search_fields = (
        'name',
        'email',
        'phone',
    )

    list_filter = (
        'created_at',
    )

    ordering = ('-created_at',)