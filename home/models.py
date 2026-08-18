from django.db import models
from decimal import Decimal

class GoldRate(models.Model):
    rate_24k = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # 24K purity percentage (99.5)
        base = GoldPurity.objects.get(purity="24K")

        # 24K MetalRate
        MetalRate.objects.update_or_create(
            metal="Gold",
            purity="24K",
            defaults={
                "rate": self.rate_24k,
                "unit": "10g",
            }
        )

        # 22K, 20K, 18K, 14K, 9K
        for gp in GoldPurity.objects.exclude(purity="24K"):

            new_rate = (
                self.rate_24k * gp.percentage
            ) / base.percentage

            MetalRate.objects.update_or_create(
                metal="Gold",
                purity=gp.purity,
                defaults={
                    "rate": round(new_rate, 2),
                    "unit": "10g",
                }
            )


    def __str__(self):
        return f"24K ₹{self.rate_24k}"



class Product(models.Model):

    CATEGORY_CHOICES = [
        ('Gold', 'Gold Jewellery'),
        ('Silver', 'Silver Jewellery'),
        ('Diamond', 'Diamond Jewellery'),
        ('Bridal', 'Bridal Collection'),
        ('Custom', 'Custom Jewellery'),
        ('Coins', 'Gold Coins'),
    ]
    PRODUCT_TYPE_CHOICES = [
    ('Ring', 'Ring'),
    ('Pendant', 'Pendant'),
    ('Necklace', 'Necklace'),
    ('Chain', 'Chain'),
    ('Bangles', 'Bangles'),
    ('Bracelet', 'Bracelet'),
    ('Earrings', 'Earrings'),
    ('Mangalsutra', 'Mangalsutra'),
    ('Nose Pin', 'Nose Pin'),
    ('Anklet', 'Anklet'),
    ('Jewellery Set', 'Jewellery Set'),
    ("Men's Jewellery", "Men's Jewellery"),
    ("Kids Jewellery", "Kids Jewellery"),
    ('Coins', 'Coins'),
    ('Idols', 'Idols'),
    ('Utensils', 'Utensils'),
    ('Other', 'Other'),
]

    PURITY_CHOICES = [
        ('18K', '18 Karat'),
        ('22K', '22 Karat'),
        ('24K', '24 Karat'),
        ('925', '925 Sterling Silver')
    ]

    name = models.CharField(max_length=200)

    product_code = models.CharField(max_length=50, unique=True)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )
    product_type = models.CharField(
    max_length=30,
    choices=PRODUCT_TYPE_CHOICES,
    default='Other'
    )
    
    STYLE_CHOICES = [
    ('Classic', 'Classic'),
    ('Traditional', 'Traditional'),
    ('Elegant', 'Elegant'),
    ('Floral', 'Floral'),
    ('Modern', 'Modern'),
    ('Minimal', 'Minimal'),
    ('Other', 'Other'),
]

    style = models.CharField(
    max_length=20,
    choices=STYLE_CHOICES,
    blank=True,
    default='Other'
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

    metal_price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0,
    help_text="Metal value before making charge, stone charge and GST"
)

    price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0,
    help_text="Final selling price"
)
    
    making_charge = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    default=0,
    help_text="Making charge percentage"
)

    stone_charge = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0,
    help_text="Stone charge amount"
)

    gst_percentage = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    default=3,
    help_text="GST Percentage"
)
    GENDER_CHOICES = (
    ('Women', 'Women'),
    ('Men', 'Men'),
    ('Kids', 'Kids'),
)

    gender = models.CharField(
    max_length=10,
    choices=GENDER_CHOICES,
    default='Women'
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
    
class MetalRate(models.Model):

    METAL_CHOICES = [
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
        ('Diamond', 'Diamond'),
    ]

    PURITY_CHOICES = [
        ('24K', '24K Gold'),
        ('22K', '22K Gold'),
        ('20K', '20K Gold'),
        ('18K', '18K Gold'),
        ('14K', '14K Gold'),
        ('9K', '9K Gold'),
        ('925', '925 Silver'),
        ('1CT', 'Diamond Per Carat'),
    ]

    UNIT_CHOICES = [
        ('10g', 'Per 10 Gram'),
        ('1kg', 'Per 1 Kilogram'),
        ('1ct', 'Per Carat'),
    ]

    metal = models.CharField(
        max_length=20,
        choices=METAL_CHOICES
    )

    purity = models.CharField(
        max_length=20,
        choices=PURITY_CHOICES
    )

    rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Enter the current market rate"
    )

    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default='10g'
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return f"{self.metal} ({self.purity}) - ₹{self.rate} / {self.unit}"    


    
class GoldPurity(models.Model):
    purity = models.CharField(max_length=10, unique=True)
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Purity Percentage"
    )

    def __str__(self):
        return f"{self.purity} ({self.percentage}%)"
    
class CustomEnquiry(models.Model):

    JEWELLERY_CHOICES = [

        ("Ring", "Ring"),
        ("Necklace", "Necklace"),
        ("Bridal Set", "Bridal Set"),
        ("Pendant", "Pendant"),
        ("Earrings", "Earrings"),
        ("Couple Ring", "Couple Ring"),

    ]


    name = models.CharField(
        max_length=100
    )


    phone = models.CharField(
        max_length=15
    )


    jewellery_type = models.CharField(
        max_length=50,
        choices=JEWELLERY_CHOICES
    )


    gold_purity = models.CharField(
        max_length=20,
        blank=True
    )


    budget = models.CharField(
        max_length=50,
        blank=True
    )


    design_idea = models.TextField(
        blank=True
    )


    reference_image = models.ImageField(
        upload_to="custom_designs/",
        blank=True,
        null=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return self.name
    

class CustomGallery(models.Model):

    CATEGORY_CHOICES = [

        ("ring", "Ring"),
        ("necklace", "Necklace"),
        ("bridal", "Bridal Set"),
        ("pendant", "Pendant"),
        ("earrings", "Earrings"),
        ("couple-ring", "Couple Ring"),

    ]

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    title = models.CharField(
        max_length=100
    )

    image = models.ImageField(
        upload_to="custom_gallery/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.category} - {self.title}"