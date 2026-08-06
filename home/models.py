from django.db import models

class Product(models.Model):

    CATEGORY_CHOICES = [
        ('Gold', 'Gold Jewellery'),
        ('Silver', 'Silver Jewellery'),
        ('Diamond', 'Diamond Jewellery'),
        ('Bridal', 'Bridal Collection'),
        ('Custom', 'Custom Jewellery'),
        ('Coins', 'Gold Coins'),
    ]

    PURITY_CHOICES = [
        ('18K', '18 Karat'),
        ('22K', '22 Karat'),
        ('24K', '24 Karat'),
    ]

    name = models.CharField(max_length=200)

    product_code = models.CharField(max_length=50, unique=True)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    purity = models.CharField(
        max_length=10,
        choices=PURITY_CHOICES,
        blank=True
    )

    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Weight in grams"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(default=1)

    image = models.ImageField(upload_to='products/')
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)

    image3 = models.ImageField(upload_to='products/', blank=True, null=True)

    image4 = models.ImageField(upload_to='products/', blank=True, null=True)

    description = models.TextField()

    is_featured = models.BooleanField(default=False)

    is_new_arrival = models.BooleanField(default=False)

    is_best_seller = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class Wishlist(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
    
class Contact(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=15)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name