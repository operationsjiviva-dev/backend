from catalog.models import Product, ProductVariant, \
    ProductImage, Collection, Category, Occasion, Tag
from django.db.models import Min, Q, Count, Max



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
    
    @classmethod
    def get_products_with_filters(cls, filters: dict):
        products = Product.objects.all()

        if "collections" in filters:
            products = products.filter(collections__in=filters["collections"])

        if "categories" in filters:
            products = products.filter(categories__in=filters["categories"])

        if "occasions" in filters:
            products = products.filter(occasions__in=filters["occasions"])

        if "tags" in filters:
            products = products.filter(tags__in=filters["tags"])

        #sort
        products = (
            Product.objects
            .annotate(primary_price=Min("variants__selling_price", filter=Q(variants__is_primary=True)))
            .order_by("primary_price")
        )
        print(products.values()[0])
        return products
    
    @classmethod
    def get_filters_for_product_listing(cls, products: list):
        occasions = (
            Occasion.objects
            .filter(products__in=products)
            .annotate(count=Count('products', distinct=True))
            .values('id', 'name', 'count')
        )
        categories = (
            Category.objects
            .filter(products__in=products)
            .annotate(count=Count('products', distinct=True))
            .values('id', 'name', 'count')
        )
        color = (
            Product.objects
            .values("color")
            .annotate(count=Count("id"))
        )
        size = (
            ProductVariant.objects
            .filter(product__in=products)
            .values("size")
            .annotate(count=Count("id"))
        )
        highest_price = (
            ProductVariant.objects
            .filter(product__in=products)
            .aggregate(max_price=Max("selling_price"))
        )["max_price"]
        price = [{"maxPrice": int(highest_price)}]
        
        return {
            "occasions": list(occasions),
            "categories": list(categories),
            "color": list(color),
            "size": list(size),
            "price": list(price)
        }
