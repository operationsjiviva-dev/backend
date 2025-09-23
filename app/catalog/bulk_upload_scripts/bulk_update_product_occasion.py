from catalog.bulk_upload_scripts.base import BulkUploadeBaseClass
from catalog.models import Product, Occasion


class BULK_UPDATE_PRODUCT_OCCASION_MAPPING(BulkUploadeBaseClass):
    required_headers = ["product_id", "occasion_id", "action"]
    optional_headers = []

    def process_row(self, row: dict, **kwargs):
        fail_reasons = []
        action = row.get("action", "").strip().lower()
        if action not in ["add", "remove"]:
            fail_reasons.append("Action must be either 'add' or 'remove'.")
        product_id = row.get("product_id", "").strip()
        if not product_id or not product_id.isdigit() or not Product.objects.filter(id=int(product_id)).exists():
            fail_reasons.append("Valid product_id is required.")
        
        occasion_id = row.get("occasion_id", "").strip()
        if not occasion_id or not occasion_id.isdigit() or not Occasion.objects.filter(id=int(occasion_id)).exists():
            fail_reasons.append("Valid occasion_id is required.")
        
        if action == "add":
            if Product.objects.filter(id=int(product_id), occasions__id=int(occasion_id)).exists():
                fail_reasons.append(f"Product {product_id} is already in occasion {occasion_id}.")
        elif action == "remove":
            if not Product.objects.filter(id=int(product_id), occasions__id=int(occasion_id)).exists():
                fail_reasons.append(f"Product {product_id} is not in occasion {occasion_id}.")
        
        if fail_reasons:
            return False, fail_reasons
        product = Product.objects.filter(id=int(product_id)).first()
        occasion = Occasion.objects.filter(id=int(occasion_id)).first()
        if action == "add":
            product.occasions.add(occasion)
        elif action == "remove":
            product.occasions.remove(occasion)
        product.save()
        return True, row

    def post_upload_changes(self, response_list_of_dict, **kwargs):
        pass