from catalog.bulk_upload_scripts.base import BulkUploadeBaseClass
from catalog.models import Product, ProductVariant
from catalog.miscellaneous_values.product import ProductSizes
from catalog.managers.product_variant_manager import ProductVariantManager


class BULK_UPLOAD_PRODUCT_VARIANTS(BulkUploadeBaseClass):
    required_headers = ["product_id", "size", "price"]
    optional_headers = ["is_primary"]
    
    def process_row(self, row: dict, **kwargs):
        fail_reasons = []
        product_id = row.get("product_id", "")
        if not product_id or not Product.objects.filter(id=int(product_id)).exists():
            fail_reasons.append("Valid product_id is required.")
        size = row.get("size", "").strip()
        if not size or size not in ProductSizes.ALL_SIZES_ORDER:
            fail_reasons.append(f"Size is required and must be one of {ProductSizes.ALL_SIZES_ORDER}.")
        
        selling_price = row.get("price", "")
        if not selling_price:
            fail_reasons.append("Price is required.")

        is_primary =  bool(row.get("is_primary", False))
        
        if fail_reasons:
            return False, fail_reasons
        
        
        variant = ProductVariant.objects.filter(product_id=int(product_id), size=size).first()
        if variant:
            fail_reasons.append(f"Variant with size '{size}' already exists for product_id {product_id}.")
            return False, fail_reasons
        
        all_variants = ProductVariant.objects.filter(product_id=int(product_id))
        sizes_available = [v.size for v in all_variants]
        if size in sizes_available:
            fail_reasons.append(f"Variant with size '{size}' already exists for product_id {product_id}.")
            return False, fail_reasons
        
        variant = ProductVariant()
        variant.product_id = int(product_id)
        variant.size = size
        variant.selling_price = float(selling_price)
        variant.sku = ProductVariantManager.generate_sku_code()
        variant.is_primary = is_primary
        variant.save()
        row["variant_id"] = variant.id
        return True, row

    def post_upload_changes(self, response_list_of_dict, **kwargs):
        pass