from catalog.models import Product, ProductVariant, ProductImage, Collection, Category, Occasion, Tag


class ProductManager:
    def __init__(self):
        pass

    @classmethod
    def get_products_using_filters():
        products = Product.objects.all().order_by('-created_on')
        
        return products
    
    @classmethod
    def single_product_response_data_for_crm(cls, product: Product):
        response_dict = {
            "productId": product.id,
            "displayName": product.display_name,
            "description": product.description if product.description else "",
            "urlSlug": product.url_slug if product.url_slug else "",
            "fabric": product.fabric if product.fabric else "",
            "color": product.color if product.color else "",
            "collectionNames": [collection.name for collection in product.collections.all()],
            "categoryNames": [category.name for category in product.categories.all()],
            "occasionNames": [occasion.name for occasion in product.occasions.all()],
            "tagNames": [tag.name for tag in product.tags.all()],
            "variants": []
        }
        variants = ProductVariant.objects.filter(product=product)
        #TODO: add sorting of variants based on size order
        for variant in variants:
            response_dict["variants"].append({
                "variantId": variant.id,
                "sku": variant.sku,
                "size": variant.size,
                "sellingPrice": variant.selling_price,
                "isPrimary": variant.is_primary,
                "isDeleted": variant.is_deleted,
                "inStock": variant.in_stock
            })
        return response_dict
    
    @classmethod
    def multiple_product_response_data_for_crm(cls, products):
        response_data = []
        for product in products:
            response_data.append(cls.single_product_response_data_for_crm(product))
        return product