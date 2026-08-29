from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from decimal import Decimal
from .models import Product, Wishlist, Contact, MetalRate
from .models import CustomEnquiry
from .models import CustomGallery
from urllib.parse import quote
from .models import SavingScheme, SchemeEnquiry


def calculate_product_price(product):

    calculated_price = None

    # ==========================================
    # GOLD
    # ==========================================

    if (
        product.category == "Gold"
        and product.purity in ["18K", "22K", "24K"]
    ):

        gold_rate = MetalRate.objects.filter(
            metal="Gold",
            purity=product.purity
        ).first()

        if gold_rate:

            # MetalRate = Per 10 grams
            rate_per_gram = gold_rate.rate / Decimal("10")

            # Gold value
            metal_value = rate_per_gram * product.weight

            # Making charge %
            making_amount = (
                metal_value
                * product.making_charge
                / Decimal("100")
            )

            # Hallmark
            hallmark_charge = Decimal("45")

            # Subtotal
            subtotal = (
                metal_value
                + making_amount
                + product.stone_charge
                + hallmark_charge
            )

            # GST
            gst_amount = (
                subtotal
                * product.gst_percentage
                / Decimal("100")
            )

            # Final price
            calculated_price = subtotal + gst_amount


    # ==========================================
    # SILVER
    # ==========================================

    elif (
        product.category == "Silver"
        and product.purity == "925"
    ):

        silver_rate = MetalRate.objects.filter(
            metal="Silver",
            purity="925"
        ).first()

        if silver_rate:

            # Silver rate = Per 1 kilogram
            rate_per_gram = silver_rate.rate / Decimal("1000")

            # 925 purity
            purity_rate = (
                rate_per_gram
                * Decimal("925")
                / Decimal("1000")
            )

            # Silver value
            metal_value = purity_rate * product.weight

            # Making charge %
            making_amount = (
                metal_value
                * product.making_charge
                / Decimal("100")
            )

            # Hallmark
            hallmark_charge = Decimal("45")

            # Subtotal
            subtotal = (
                metal_value
                + making_amount
                + product.stone_charge
                + hallmark_charge
            )

            # GST
            gst_amount = (
                subtotal
                * product.gst_percentage
                / Decimal("100")
            )

            # Final price
            calculated_price = subtotal + gst_amount


    # ==========================================
    # FALLBACK
    # ==========================================

    if calculated_price is None:
        calculated_price = product.price

    return calculated_price


def home(request):
    
    featured_products = Product.objects.filter(
        is_featured=True
    )[:4]

    # =====================================================
    # 20E — THE PRATIK EDIT
    # =====================================================

    pratik_edit_products = Product.objects.filter(
        is_new_arrival=True
    )[:4]

    # Calculate current price for The Pratik Edit
    for product in pratik_edit_products:
        product.calculated_price = calculate_product_price(product)

    
    
    gold_rate = MetalRate.objects.filter(
        metal="Gold",
        purity="24K"
    ).first()

    rate24 = rate22 = rate20 = rate18 = rate14 = rate9 = None

    if gold_rate:

         rate24 = MetalRate.objects.filter(
        metal="Gold",
        purity="24K"
    ).first()

    rate22 = MetalRate.objects.filter(
        metal="Gold",
        purity="22K"
    ).first()

    rate20 = MetalRate.objects.filter(
        metal="Gold",
        purity="20K"
    ).first()

    rate18 = MetalRate.objects.filter(
        metal="Gold",
        purity="18K"
    ).first()

    rate14 = MetalRate.objects.filter(
        metal="Gold",
        purity="14K"
    ).first()

    rate9 = MetalRate.objects.filter(
        metal="Gold",
        purity="9K"
    ).first()

    rate24 = rate24.rate if rate24 else None
    rate22 = rate22.rate if rate22 else None
    rate20 = rate20.rate if rate20 else None
    rate18 = rate18.rate if rate18 else None
    rate14 = rate14.rate if rate14 else None
    rate9 = rate9.rate if rate9 else None

    # Calculate current price for every featured product
    for product in featured_products:
        product.calculated_price = calculate_product_price(product)

    context = {
        "featured_products": featured_products,
        "pratik_edit_products": pratik_edit_products,
        "rate24": rate24,
        "rate22": rate22,
        "rate20": rate20,
        "rate18": rate18,
        "rate14": rate14,
        "rate9": rate9,
    }

    return render(request, "home/home.html", context)

def contact(request):

    if request.method == "POST":

        Contact.objects.create(

            name=request.POST.get("name"),

            email=request.POST.get("email"),

            phone=request.POST.get("phone"),

            message=request.POST.get("message"),

        )

        return render(request, "home/contact.html", {
            "success": True
        })

    return render(request, "home/contact.html")

from .models import Product

def gold(request):

    filter_type = request.GET.get("type", "all")
    product_type = request.GET.get("product_type", "all")
    weight_filter = request.GET.get("weight", "all")
    purity_filter = request.GET.get("purity", "all")
    
    category_filter = request.GET.get("category", "all")

    products = Product.objects.filter(category="Gold")
    
    
    if category_filter != "all":
        products = products.filter(product_type=category_filter)
    

    if filter_type != "all":
        products = products.filter(gender=filter_type)

    if product_type != "all":
        products = products.filter(product_type=product_type)
    
    if weight_filter == "under5":
       products = products.filter(weight__lt=5)

    elif weight_filter == "5to10":
       products = products.filter(weight__gte=5, weight__lte=10)

    elif weight_filter == "10to20":
       products = products.filter(weight__gt=10, weight__lte=20)

    elif weight_filter == "above20":
       products = products.filter(weight__gt=20)
       
    if purity_filter != "all":
       products = products.filter(purity=purity_filter)
       
    # Sidebar categories according to gender

    if filter_type == "Women":

      sidebar_categories = [
        "Ring",
        "Earrings",
        "Necklace",
        "Bangles",
        "Bracelet",
        "Chain",
        "Pendant",
        "Mangalsutra",
        "Nose Pin",
        "Nath",
    ]

    elif filter_type == "Men":

      sidebar_categories = [
        "Ring",
        "Chain",
        "Bracelet",
        "Kada",
        "Pendant",
    ]

    elif filter_type == "Kids":

       sidebar_categories = [
        "Ring",
        "Bracelet",
        "Chain",
        "Earrings",
        "Nazariya",
    ]

    else:

       sidebar_categories = [
        "Ring",
        "Earrings",
        "Necklace",
        "Bangles",
        "Bracelet",
        "Chain",
        "Pendant",
        "Mangalsutra",
        "Nose Pin",
        "Nath",
        "Kada",
        "Nazariya",
    ]

    # Calculate current price for every product
    product_prices = {}

    for product in products:
        product_prices[product.id] = calculate_product_price(product)

    context = {
    "products": products,
    "filter_type": filter_type,
    "product_type": product_type,
    "weight_filter": weight_filter,
    "purity_filter": purity_filter,
    "product_prices": product_prices,
    "sidebar_categories": sidebar_categories,
}

    return render(request, "home/gold.html", context)

def product_detail(request, id):

    product = get_object_or_404(Product, id=id)

    related_products = Product.objects.filter(
    category=product.category,
    product_type=product.product_type,
    gender=product.gender
    ).exclude(id=product.id)[:4]

    for item in related_products:
        item.calculated_price = calculate_product_price(item)

    wishlist_ids = Wishlist.objects.values_list(
        "product_id",
        flat=True
    )

    gold_rate_obj = MetalRate.objects.filter(
        metal="Gold",
        purity="24K"
    ).first()

    silver_rate_obj = MetalRate.objects.filter(
        metal="Silver",
        purity="925"
    ).first()

    calculated_price = None
    purity_rate = None
    metal_value = None
    subtotal = None
    gst_amount = None

    making_amount = Decimal("0")
    hallmark_charge = Decimal("45")

    # ---------------- GOLD ----------------

    if (
        product.category == "Gold"
        and gold_rate_obj
        and product.purity in ["18K", "22K", "24K"]
    ):

        metal_rate_obj = MetalRate.objects.filter(
        metal="Gold",
        purity=product.purity
        ).first()

        if metal_rate_obj:
         purity_rate = metal_rate_obj.rate / Decimal("10")

        metal_value = purity_rate * product.weight

        making_amount = (
            metal_value * product.making_charge / Decimal("100")
        )

        subtotal = (
            metal_value
            + making_amount
            + product.stone_charge
            + hallmark_charge
        )

        gst_amount = (
            subtotal * product.gst_percentage / Decimal("100")
        )

        calculated_price = subtotal + gst_amount

    # ---------------- SILVER ----------------

    elif (
        product.category == "Silver"
        and silver_rate_obj
        and product.purity == "925"
    ):

        rate_per_gram = silver_rate_obj.rate / Decimal("1000")

        purity_rate = (
            rate_per_gram * Decimal("925") / Decimal("1000")
        )

        metal_value = purity_rate * product.weight

        making_amount = (
            metal_value * product.making_charge / Decimal("100")
        )

        subtotal = (
            metal_value
            + making_amount
            + product.stone_charge
            + hallmark_charge
        )

        gst_amount = (
            subtotal * product.gst_percentage / Decimal("100")
        )

        calculated_price = subtotal + gst_amount

    else:
        calculated_price = product.price

    context = {
        "product": product,
        "related_products": related_products,
        "wishlist_ids": wishlist_ids,
        "gold_rate_obj": gold_rate_obj,
        "silver_rate_obj": silver_rate_obj,
        "purity_rate": purity_rate,
        "metal_value": metal_value,
        "subtotal": subtotal,
        "gst_amount": gst_amount,
        "calculated_price": calculated_price,
        "making_amount": making_amount,
        "hallmark_charge": hallmark_charge,
    }

    return render(
        request,
        "home/product_detail.html",
        context,
    )
def search(request):

    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    purity = request.GET.get('purity', '')
    sort = request.GET.get('sort', '')

    # Default: koi product nahi
    products = Product.objects.none()

    # ==========================================
    # SEARCH ONLY WHEN USER ENTERS SOMETHING
    # ==========================================

    if query:

        # Voice search / normal search query clean karo
        query = query.lower()

        query = (
            query.replace("jewellery", "")
                 .replace("jewelry", "")
                 .replace("collection", "")
                 .strip()
        )

        # Agar cleaning ke baad query empty ho gayi
        # toh bhi products show nahi honge
        if query:

            products = Product.objects.filter(
                Q(name__icontains=query) |
                Q(product_code__icontains=query) |
                Q(category__icontains=query) |
                Q(purity__icontains=query)
            )

            # Category filter
            if category:
                products = products.filter(category=category)

            # Purity filter
            if purity:
                products = products.filter(purity=purity)

            # Sorting
            if sort == "low":
                products = products.order_by("price")

            elif sort == "high":
                products = products.order_by("-price")


    # ==========================================
    # CONTEXT
    # ==========================================

    context = {
        "products": products,
        "query": query,
        "category": category,
        "purity": purity,
        "sort": sort,
    }

    return render(request, "home/search.html", context)


def silver(request):
    
    filter_type = request.GET.get("type", "all")
    product_type = request.GET.get("product_type", "all")
    weight_filter = request.GET.get("weight", "all")
    purity_filter = request.GET.get("purity", "all")

    products = Product.objects.filter(category="Silver")

    if filter_type != 'all':
        products = products.filter(gender=filter_type)
        
    if product_type != "all":
        products = products.filter(product_type=product_type)

    if weight_filter == "under5":
        products = products.filter(weight__lt=5)

    elif weight_filter == "5to10":
        products = products.filter(weight__gte=5, weight__lte=10)

    elif weight_filter == "10to20":
        products = products.filter(weight__gt=10, weight__lte=20)

    elif weight_filter == "above20":
        products = products.filter(weight__gt=20)

    if purity_filter != "all":
        products = products.filter(purity=purity_filter)
     
    # Sidebar categories according to gender

    if filter_type == "Women":

      sidebar_categories = [
        "Ring",
        "Chain",
        "Bracelet",
        "Pendant",
        "Earrings",
        "Anklet",
        "Bangle",
    ]

    elif filter_type == "Men":

      sidebar_categories = [
        "Ring",
        "Chain",
        "Bracelet",
    ]

    elif filter_type == "Kids":

      sidebar_categories = [
        "Ring",
        "Chain",
        "Bracelet",
        "Pendant",
    ]

    else:

        sidebar_categories = [
        "Ring",
        "Chain",
        "Bracelet",
        "Pendant",
        "Earrings",
        "Anklet",
        "Bangle",
    ]
 
    # Calculate current price for every product
    product_prices = {}

    for product in products:
        product_prices[product.id] = calculate_product_price(product)

    context = {
        "products": products,
        "filter_type": filter_type,
        "product_type": product_type,
        "weight_filter": weight_filter,
        "purity_filter": purity_filter,
        "product_prices": product_prices,
        "sidebar_categories": sidebar_categories,
}

    return render(request, 'home/silver.html', context)


def diamond(request):
    
    filter_type = request.GET.get("type", "all")
    product_type = request.GET.get("product_type", "all")
    weight_filter = request.GET.get("weight", "all")
    purity_filter = request.GET.get("purity", "all")

    products = Product.objects.filter(category="Diamond")

    
    # Top Navigation Filter

    if filter_type == "Bridal Sets":
        products = products.filter(product_type="Jewellery Set")

    elif filter_type == "Necklaces":
        products = products.filter(product_type="Necklace")

    elif filter_type == "Earrings":
        products = products.filter(product_type="Earrings")

    elif filter_type == "Bracelets":
        products = products.filter(product_type="Bracelet")
        
    if product_type != "all":
        products = products.filter(product_type=product_type)

    if weight_filter == "under5":
        products = products.filter(weight__lt=5)

    elif weight_filter == "5to10":
        products = products.filter(weight__gte=5, weight__lte=10)

    elif weight_filter == "10to20":
        products = products.filter(weight__gt=10, weight__lte=20)

    elif weight_filter == "above20":
        products = products.filter(weight__gt=20)

    if purity_filter != "all":
        products = products.filter(purity=purity_filter)
        
    sidebar_categories = [
       "Ring",
       "Jewellery Set",
       "Necklace",
       "Earrings",
       "Bracelet",
       "Pendant",
]

    context = {
    "products": products,
    "filter_type": filter_type,
    "product_type": product_type,
    "weight_filter": weight_filter,
    "purity_filter": purity_filter,
    "sidebar_categories": sidebar_categories,
}

    return render(request, 'home/diamond.html', context)

def bridal(request):

    filter_type = request.GET.get("type", "all")
    product_type = request.GET.get("product_type", "all")
    weight_filter = request.GET.get("weight", "all")
    purity_filter = request.GET.get("purity", "all")

    products = Product.objects.filter(category="Bridal")

    # Top Filter

    if filter_type == "Bridal Sets":
        products = products.filter(product_type="Jewellery Set")

    elif filter_type == "Necklaces":
        products = products.filter(product_type="Necklace")

    elif filter_type == "Bangles":
        products = products.filter(product_type="Bangles")

    elif filter_type == "Earrings":
        products = products.filter(product_type="Earrings")

    # Sidebar Filter

    if product_type != "all":
        products = products.filter(product_type=product_type)

    # Weight

    if weight_filter == "under5":
        products = products.filter(weight__lt=5)

    elif weight_filter == "5to10":
        products = products.filter(weight__gte=5, weight__lte=10)

    elif weight_filter == "10to20":
        products = products.filter(weight__gt=10, weight__lte=20)

    elif weight_filter == "above20":
        products = products.filter(weight__gt=20)

    # Purity

    if purity_filter != "all":
        products = products.filter(purity=purity_filter)

    # Sidebar Categories

    sidebar_categories = [
        "Jewellery Set",
        "Necklace",
        "Bangles",
        "Earrings",
    ]

    context = {
        "products": products,
        "filter_type": filter_type,
        "product_type": product_type,
        "weight_filter": weight_filter,
        "purity_filter": purity_filter,
        "sidebar_categories": sidebar_categories,
    }

    return render(request, "home/bridal.html", context)

def custom(request):

    custom_products = Product.objects.filter(category='Custom')

    context = {
        'products': custom_products
    }

    return render(request, 'home/custom.html', context)

def coins(request):

    filter_type = request.GET.get("type", "all")
    product_type = request.GET.get("product_type", "all")
    weight_filter = request.GET.get("weight", "all")
    purity_filter = request.GET.get("purity", "all")

    products = Product.objects.filter(category="Coins")

    # TOP FILTERS

    # Top Navigation Filter

    if filter_type == "Gold Coin":
        products = products.filter(purity="24K")

    elif filter_type == "Silver Coin":
        products = products.filter(purity="925")

    elif filter_type == "Lakshmi Ganesh":
        products = products.filter(name__icontains="Lakshmi") | products.filter(name__icontains="Ganesha")

    elif filter_type == "Gift Coin":
        products = products.filter(name__icontains="Gift")

    # SIDEBAR FILTERS

    if product_type != "all":
        products = products.filter(product_type=product_type)

    if weight_filter == "under5":
        products = products.filter(weight__lt=5)

    elif weight_filter == "5to10":
        products = products.filter(weight__gte=5, weight__lte=10)

    elif weight_filter == "10to20":
        products = products.filter(weight__gt=10, weight__lte=20)

    elif weight_filter == "above20":
        products = products.filter(weight__gt=20)

    if purity_filter != "all":
        products = products.filter(purity=purity_filter)

    sidebar_categories = [
        "Coins",
    ]

    context = {
        "products": products,
        "filter_type": filter_type,
        "product_type": product_type,
        "weight_filter": weight_filter,
        "purity_filter": purity_filter,
        "sidebar_categories": sidebar_categories,
    }

    return render(request, "home/coins.html", context)


def about(request):
    return render(request, "home/about.html")

def wishlist(request):

    wishlist_items = Wishlist.objects.all()

    context = {
        'wishlist_items': wishlist_items
    }

    return render(request, "home/wishlist.html", context)

def add_to_wishlist(request, id):

    product = get_object_or_404(Product, id=id)

    wishlist_item, created = Wishlist.objects.get_or_create(product=product)

    if created:
        return JsonResponse({
            "status": "added"
        })

    else:
        wishlist_item.delete()

        return JsonResponse({
            "status": "removed"
        })
        
def remove_from_wishlist(request, id):

    Wishlist.objects.filter(product_id=id).delete()

    return redirect("wishlist")

def about(request):
    return render(request, 'home/about.html')

def get_metal_rate(request):
    purity = request.GET.get("purity")

    if not purity:
        return JsonResponse({"rate": 0})

    metal = "Gold"

    if purity == "925":
        metal = "Silver"

    rate = MetalRate.objects.filter(
        metal=metal,
        purity=purity
    ).first()

    if rate:
        return JsonResponse({"rate": float(rate.rate)})

    return JsonResponse({"rate": 0})





            
def custom_category(request, jewellery_type):

    if request.method == "POST":

        enquiry = CustomEnquiry.objects.create(

            name=request.POST.get("name"),

            phone=request.POST.get("phone"),

            jewellery_type=jewellery_type,

            gold_purity=request.POST.get("gold_purity"),

            budget=request.POST.get("budget"),

            design_idea=request.POST.get("design_idea"),

        )


        if request.FILES.get("reference_image"):

            enquiry.reference_image = request.FILES.get("reference_image")

            enquiry.save()


    data = {

        "ring": {
            "title": "Custom Ring Designs",
            "icon": "💍"
        },

        "necklace": {
            "title": "Custom Necklace Designs",
            "icon": "📿"
        },

        "bridal": {
            "title": "Custom Bridal Sets",
            "icon": "👰"
        },

        "pendant": {
            "title": "Custom Pendant Designs",
            "icon": "💎"
        },

        "earrings": {
            "title": "Custom Earrings Designs",
            "icon": "👂"
        },

        "couple-ring": {
            "title": "Custom Couple Ring Designs",
            "icon": "💞"
        }

    }


    # Sirf reference images ke liye 4 images
    gallery = CustomGallery.objects.filter(
        category=jewellery_type
    )[:4]


    return render(
        request,
        "home/custom_category.html",
        {
            "category": data.get(jewellery_type),
            "gallery": gallery,
            "products": [],   # IMPORTANT - custom products hide honge
        }
    )    
# =====================================================
# EVERYDAY JEWELLERY
# =====================================================

def everyday(request):

    everyday_products = Product.objects.filter(
    is_everyday=True
    ).order_by("-id")

    for product in everyday_products:
        product.calculated_price = calculate_product_price(product)

    context = {
        "everyday_products": everyday_products,
    }

    return render(
        request,
        "home/everyday.html",
        context
    )
    
# =====================================================
# SAVING SCHEME
# =====================================================

def saving_scheme(request):

    schemes = SavingScheme.objects.all()

    if request.method == "POST":

        scheme_id = request.POST.get("scheme")

        scheme = SavingScheme.objects.get(id=scheme_id)

        enquiry = SchemeEnquiry.objects.create(

            scheme=scheme,

            name=request.POST.get("name"),

            phone=request.POST.get("phone"),

            message=request.POST.get("message"),

        )


        return render(
            request,
            "home/saving_scheme.html",
            {
                "schemes": schemes,
                "success": True
            }
        )


    return render(
        request,
        "home/saving_scheme.html",
        {
            "schemes": schemes
        }
    )