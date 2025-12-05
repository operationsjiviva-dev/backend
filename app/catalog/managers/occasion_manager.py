from catalog.models import Occasion


class OccasionManager:
    def __init__(self):
        pass

    @classmethod
    def get_occasions_with_products(cls):
        occasion_with_products = Occasion.objects.filter(products__isnull=False).distinct()
        return occasion_with_products
    
        