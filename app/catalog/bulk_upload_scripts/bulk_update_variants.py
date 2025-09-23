from catalog.bulk_upload_scripts.base import BulkUploadeBaseClass
from catalog.models import ProductVariant, Product

from catalog.miscellaneous_values.product import ProductSizes


class BULK_UPDATE_PRODUCT_VARIANTS(BulkUploadeBaseClass):
    required_headers = ["variant_id"]
    optional_headers = ['price', 'size', 'in_stock', 'is_deleted']
    
    def process_row(self, row: dict, **kwargs):
        fail_reasons = []
        variant_id = row.get("variant_id", "").strip()
        if not variant_id or not variant_id.isdigit() or not ProductVariant.objects.filter(id=int(variant_id)).exists():
            fail_reasons.append("Valid variant_id is required.")
        size = row.get("size", "").strip()
        if size and size not in ProductSizes.ALL_SIZES_ORDER:
            fail_reasons.append(f"Size must be one of {ProductSizes.values}.")
        selling_price = row.get("price", "").strip()
        if selling_price:
            try:
                float(selling_price)
            except ValueError:
                fail_reasons.append("Price must be a valid number.")
        
        in_stock = row.get("in_stock", True)
        is_deleted = row.get("is_deleted", False)
        variant = ProductVariant.objects.filter(id=int(variant_id)).first()
        all_variants = ProductVariant.objects.filter(product_id=variant.product_id).exclude(id=variant.id)
        sizes_available = [v.size for v in all_variants]
        if size and size in sizes_available:
            fail_reasons.append(f"Variant with size '{size}' already exists for product_id {variant.product_id}.")
        
        if fail_reasons:
            return False, fail_reasons
        
        if selling_price:
            variant.selling_price = float(selling_price)
        if size:
            variant.size = size
        
        variant.in_stock = in_stock
        variant.is_deleted = is_deleted
        variant.save()
        
        return True, row

    def post_upload_changes(self, response_list_of_dict, **kwargs):
        pass