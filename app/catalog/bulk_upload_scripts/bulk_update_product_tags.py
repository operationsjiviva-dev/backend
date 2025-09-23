from catalog.bulk_upload_scripts.base import BulkUploadeBaseClass
from catalog.models import Product, Tag


class BULK_UPDATE_PRODUCT_TAGS_MAPPING(BulkUploadeBaseClass):
    required_headers = ["product_id", "tag_id", "action"]
    optional_headers = []

    def process_row(self, row: dict, **kwargs):
        fail_reasons = []
        action = row.get("action", "").strip().lower()
        if action not in ["add", "remove"]:
            fail_reasons.append("Action must be either 'add' or 'remove'.")
        product_id = row.get("product_id", "").strip()
        if not product_id or not product_id.isdigit() or not Product.objects.filter(id=int(product_id)).exists():
            fail_reasons.append("Valid product_id is required.")
        
        tag_id = row.get("tag_id", "").strip()
        if not tag_id or not tag_id.isdigit() or not Tag.objects.filter(id=int(tag_id)).exists():
            fail_reasons.append("Valid tag_id is required.")
        
        if action == "add":
            if Product.objects.filter(id=int(product_id), tags__id=int(tag_id)).exists():
                fail_reasons.append(f"Product {product_id} is already tagged with tag {tag_id}.")
        elif action == "remove":
            if not Product.objects.filter(id=int(product_id), tags__id=int(tag_id)).exists():
                fail_reasons.append(f"Product {product_id} is not tagged with tag {tag_id}.")
        
        if fail_reasons:
            return False, fail_reasons
        product = Product.objects.filter(id=int(product_id)).first()
        tag = Tag.objects.filter(id=int(tag_id)).first()
        if action == "add":
            product.tags.add(tag)
        elif action == "remove":
            product.tags.remove(tag)
        product.save()
        return True, row

    def post_upload_changes(self, response_list_of_dict, **kwargs):
        pass