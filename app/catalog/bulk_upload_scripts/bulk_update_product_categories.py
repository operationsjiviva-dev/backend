from catalog.bulk_upload_scripts.base import BulkUploadeBaseClass
from catalog.models import Product, Category


class BULK_UPDATE_PRODUCT_CATEGORIES_MAPPING(BulkUploadeBaseClass):
    required_headers = ["product_id", "category_id", "action"]
    optional_headers = []

    def process_row(self, row, **kwargs):
        fail_reasons = []
        action = row.get("action", "").strip().lower()
        if action not in ["add", "remove"]:
            fail_reasons.append("Action must be either 'add' or 'remove'.")
        product_id = row.get("product_id", "").strip()
        if not product_id or not product_id.isdigit() or not Product.objects.filter(id=int(product_id)).exists():
            fail_reasons.append("Valid product_id is required.")
        
        category_id = row.get("category_id", "").strip()
        if not category_id or not category_id.isdigit() or not Category.objects.filter(id=int(category_id)).exists():
            fail_reasons.append("Valid category_id is required.")
        if action == "add":
            if Product.objects.filter(id=int(product_id), categories__id=int(category_id)).exists():
                fail_reasons.append(f"Product {product_id} is already in category {category_id}.")
        elif action == "remove":
            if not Product.objects.filter(id=int(product_id), categories__id=int(category_id)).exists():
                fail_reasons.append(f"Product {product_id} is not in category {category_id}.")
        
        if fail_reasons:
            return False, fail_reasons
        product = Product.objects.filter(id=int(product_id)).first()
        category = Category.objects.filter(id=int(category_id)).first()
        if action == "add":
            product.categories.add(category)
        elif action == "remove":
            product.categories.remove(category)
        product.save()
        return True, row

    def post_upload_changes(self, response_list_of_dict, **kwargs):
        pass