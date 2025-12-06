from catalog.models import Category


class CategoryManager:
    def __init__(self):
        pass

    @classmethod
    def get_categories(cls):
        categories_with_products = Category.objects.filter(products__isnull=False, parent_id=1).distinct()
        return categories_with_products