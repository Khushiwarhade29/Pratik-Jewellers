from decimal import Decimal
from .models import MetalRate

def metal_rates(request):

    gold_rate = MetalRate.objects.filter(
        metal="Gold",
        purity="24K"
    ).first()

    silver_rate = MetalRate.objects.filter(
        metal="Silver",
        purity="925"
    ).first()

    rate24 = rate22 = rate20 = rate18 = rate14 = rate9 = None

    if gold_rate:
        rate24 = gold_rate.rate
        rate22 = round(rate24 * Decimal("0.93"), 2)
        rate20 = round(rate24 * Decimal("0.90"), 2)
        rate18 = round(rate24 * Decimal("0.85"), 2)
        rate14 = round(rate24 * Decimal("0.5833"), 2)
        rate9 = round(rate24 * Decimal("0.375"), 2)

    return {
        "gold_rate": gold_rate,
        "silver_rate": silver_rate,
        "rate24": rate24,
        "rate22": rate22,
        "rate20": rate20,
        "rate18": rate18,
        "rate14": rate14,
        "rate9": rate9,
    }