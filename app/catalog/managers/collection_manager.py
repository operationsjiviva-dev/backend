from catalog.models import Collection, Product


class CollectionManager:
    def __init__(self):
        pass

    @classmethod
    def get_collections(cls):
        collections_with_products = Collection.objects.filter(products__isnull=False).distinct()
        return collections_with_products

        
