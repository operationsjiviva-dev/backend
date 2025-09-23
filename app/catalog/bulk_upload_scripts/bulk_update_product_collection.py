from catalog.bulk_upload_scripts.base import BulkUploadeBaseClass
from catalog.models import Product, Collection


class BULK_UPDATE_PRODUCT_COLLECTION_MAPPING(BulkUploadeBaseClass):
    required_headers = ["product_id", "collection_id", "action"]
    optional_headers = []

    def process_row(self, row: dict, **kwargs):
        fail_reasons = []
        action = row.get("action", "").strip().lower()
        if action not in ["add", "remove"]:
            fail_reasons.append("Action must be either 'add' or 'remove'.")
        product_id = row.get("product_id", "").strip()
        if not product_id or not product_id.isdigit() or not Product.objects.filter(id=int(product_id)).exists():
            fail_reasons.append("Valid product_id is required.")
        
        collection_id = row.get("collection_id", "").strip()
        if not collection_id or not collection_id.isdigit() or not Collection.objects.filter(id=int(collection_id)).exists():
            fail_reasons.append("Valid collection_id is required.")
        
        if action == "add":
            if Product.objects.filter(id=int(product_id), collections__id=int(collection_id)).exists():
                fail_reasons.append(f"Product {product_id} is already in collection {collection_id}.")
        elif action == "remove":
            if not Product.objects.filter(id=int(product_id), collections__id=int(collection_id)).exists():
                fail_reasons.append(f"Product {product_id} is not in collection {collection_id}.")
        
        if fail_reasons:
            return False, fail_reasons
        product = Product.objects.filter(id=int(product_id)).first()
        collection = Collection.objects.filter(id=int(collection_id)).first()
        if action == "add":
            product.collections.add(collection)
        elif action == "remove":
            product.collections.remove(collection)
        product.save()

        return True, row    
    

    def post_upload_changes(self, response_list_of_dict, **kwargs):
        pass