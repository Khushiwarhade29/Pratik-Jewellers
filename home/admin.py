from django.contrib import admin
from django.contrib import admin
from decimal import Decimal
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

@admin.register(CustomEnquiry)
class CustomEnquiryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "jewellery_type",
        "gold_purity",
        "budget",
        "created_at",
    )

    list_filter = (
        "jewellery_type",
        "gold_purity",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
    )

from django.contrib import admin
from .models import GoldRate

from .models import GoldPurity



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
    class Media:
        js = (
            'home/js/product_price.js',
        )

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

    def save_model(self, request, obj, form, change):
        obj.weight = Decimal(str(obj.weight))
        obj.making_charge = Decimal(str(obj.making_charge))
        obj.stone_charge = Decimal(str(obj.stone_charge))
        obj.gst_percentage = Decimal(str(obj.gst_percentage))

        # =====================================================
        # GOLD
        # =====================================================

        if (
            obj.category == "Gold"
            and obj.purity in ["18K", "22K", "24K"]
        ):

            metal_rate = MetalRate.objects.filter(
            metal="Gold",
            purity=obj.purity
            ).first()

            if not metal_rate:
             print("NO METAL RATE FOUND")

            if metal_rate:

                # MetalRate = Per 10 Gram
                rate_per_gram = (
                    metal_rate.rate / Decimal("10")
                )

                obj.metal_price = (
                    rate_per_gram * obj.weight
                )

                # Making charge %
                making_amount = (
                    obj.metal_price
                    * obj.making_charge
                    / Decimal("100")
                )

                hallmark_charge = Decimal("45")

                subtotal = (
                    obj.metal_price
                    + making_amount
                    + obj.stone_charge
                    + hallmark_charge
                )

                gst_amount = (
                    subtotal
                    * obj.gst_percentage
                    / Decimal("100")
                )

                obj.price = subtotal + gst_amount

        # =====================================================
        # SILVER
        # =====================================================

        elif (
            obj.category == "Silver"
            and obj.purity == "925"
        ):

            metal_rate = MetalRate.objects.filter(
                metal="Silver",
                purity="925"
            ).first()

            if metal_rate:

                # Silver rate = Per 1 KG
                rate_per_gram = (
                    metal_rate.rate / Decimal("1000")
                )

                # 925 purity
                purity_rate = (
                    rate_per_gram
                    * Decimal("925")
                    / Decimal("1000")
                )

                obj.metal_price = (
                    purity_rate * obj.weight
                )

                # Making charge %
                making_amount = (
                    obj.metal_price
                    * obj.making_charge
                    / Decimal("100")
                )

                hallmark_charge = Decimal("45")

                subtotal = (
                    obj.metal_price
                    + making_amount
                    + obj.stone_charge
                    + hallmark_charge
                )

                gst_amount = (
                    subtotal
                    * obj.gst_percentage
                    / Decimal("100")
                )

                obj.price = subtotal + gst_amount

        # =====================================================
        # SAVE PRODUCT
        # =====================================================

        super().save_model(
            request,
            obj,
            form,
            change
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