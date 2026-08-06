from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Wishlist, Contact


def home(request):

    featured_products = Product.objects.all()[:4]

    context = {
        "featured_products": featured_products
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

def gold(request):

    gold_products = Product.objects.filter(category='Gold')

    context = {
        'products': gold_products
    }

    return render(request, 'home/gold.html', context)

def product_detail(request, id):

    product = get_object_or_404(Product, id=id)

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    wishlist_ids = Wishlist.objects.values_list('product_id', flat=True)

    context = {
        'product': product,
        'related_products': related_products,
        'wishlist_ids': wishlist_ids,
    }

    return render(request, 'home/product_detail.html', context)


def search(request):

    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    purity = request.GET.get('purity', '')
    sort = request.GET.get('sort', '')

    products = Product.objects.all()
    if query:

    # Voice search / normal search query ko clean karo
     query = query.lower()

    query = (
        query.replace("jewellery", "")
             .replace("jewelry", "")
             .replace("collection", "")
             .strip()
    )

    products = products.filter(
        Q(name__icontains=query) |
        Q(product_code__icontains=query) |
        Q(category__icontains=query) |
        Q(purity__icontains=query)
    )

    if category:
        products = products.filter(category=category)

    if purity:
        products = products.filter(purity=purity)

    if sort == "low":
        products = products.order_by("price")

    elif sort == "high":
        products = products.order_by("-price")

    context = {
        "products": products,
        "query": query,
        "category": category,
        "purity": purity,
        "sort": sort,
    }

    return render(request, "home/search.html", context)

def silver(request):

    silver_products = Product.objects.filter(category='Silver')

    context = {
        'products': silver_products
    }

    return render(request, 'home/silver.html', context)

def diamond(request):

    diamond_products = Product.objects.filter(category='Diamond')

    context = {
        'products': diamond_products
    }

    return render(request, 'home/diamond.html', context)

def bridal(request):

    bridal_products = Product.objects.filter(category='Bridal')

    context = {
        'products': bridal_products
    }

    return render(request, 'home/bridal.html', context)

def custom(request):

    custom_products = Product.objects.filter(category='Custom')

    context = {
        'products': custom_products
    }

    return render(request, 'home/custom.html', context)

def coins(request):

    coin_products = Product.objects.filter(category='Coins')

    context = {
        'products': coin_products
    }

    return render(request, 'home/coins.html', context)

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