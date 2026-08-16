from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("contact/", views.contact, name="contact"),
    path('gold/', views.gold, name='gold'),
    
    path('search/', views.search, name='search'),
    path('silver/', views.silver, name='silver'),
    path('diamond/', views.diamond, name='diamond'),
    path('bridal/', views.bridal, name='bridal'),
    path('custom/', views.custom, name='custom'),
    path('coins/', views.coins, name='coins'),
    path("about/", views.about, name="about"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("wishlist/add/<int:id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path(
    "wishlist/remove/<int:id>/",
    views.remove_from_wishlist,
    name="remove_from_wishlist"
),
    path(
    "get-metal-rate/",
    views.get_metal_rate,
    name="get_metal_rate",
),
    path('about/', views.about, name='about'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    
    path('custom/<str:jewellery_type>/', views.custom_category, name='custom_category'),
    # Product Detail Page
    path('product/<int:id>/', views.product_detail, name='product_detail'),
]