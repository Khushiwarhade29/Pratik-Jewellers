from django.contrib import admin
from .models import Product, Wishlist, Contact, MetalRate

from .models import CustomEnquiry
from .models import CustomGallery

@admin.register(CustomGallery)
class CustomGalleryAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "created_at"
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "title",
    )


from django.contrib import admin
from .models import GoldRate

from .models import GoldPurity

@admin.register(CustomEnquiry)
class CustomEnquiryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "jewellery_type",
        "budget",
        "created_at"
    )

@admin.register(GoldPurity)
class GoldPurityAdmin(admin.ModelAdmin):
    list_display = ('purity', 'percentage')

@admin.register(GoldRate)
class GoldRateAdmin(admin.ModelAdmin):
    list_display = ("rate_24k", "updated_at")


admin.site.register(Wishlist)
@admin.register(MetalRate)
class MetalRateAdmin(admin.ModelAdmin):

    list_display = (
        'metal',
        'purity',
        'rate',
        'unit',
        'updated_at',
    )

    list_filter = (
        'metal',
        'purity',
        'unit',
    )

    search_fields = (
        'metal',
        'purity',
    )

    ordering = (
        'metal',
        'purity',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
    'product_code',
    'name',
    'category',
    'product_type',
    'purity',
    'weight',
    'metal_price',
    'making_charge',
    'stone_charge',
    'price',
    'stock',
    'is_featured',
)
    

    list_filter = (
    'category',
    'product_type',
    'purity',
    'is_featured',
    'is_new_arrival',
    'is_best_seller',
)

    search_fields = (
    'name',
    'product_code',
    'category',
    'product_type',
    )

    list_per_page = 20
    
    class Media:
            js = (
                'home/js/admin.js',
            )
            
    
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