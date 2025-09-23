from catalog.models import Product, Collection, Category, Occasion, Tag, FashionLine

class ProductMetaManager:
    def __init__(self):
        pass

    def create_fashion_line(self, fashion_line_name: str):
        fashion_line = FashionLine(name=fashion_line_name)
        fashion_line.save()
        return fashion_line
    
    def get_default_fashion_line(self):
        fashion_line = FashionLine.objects.filter(pk=1).first()
        return fashion_line

    def create_collection(self, collection_name: str, fashion_line_id: int = None):
        if not fashion_line_id:
            fashion_line_id = self.get_default_fashion_line().id
        collection = Collection.objects.filter(name=collection_name, fashion_line_id=fashion_line_id).first()
        if not collection: 
            collection = Collection(name=collection_name, fashion_line_id=fashion_line_id)
            collection.save()
        return collection
    
    def create_category(self, category_name: str, parent_id: int = 1):
        category = Category.objects.filter(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            category.parent_id = parent_id
            category.save()
        return category
    
    def create_occasion(self, occasion_name: str):
        occasion = Occasion.objects.filter(name=occasion_name).first()
        if not occasion:
            occasion = Occasion(name=occasion_name)
            occasion.save()
        return occasion
    
    def create_tag(self, tag_name: str):
        tag = Tag.objects.filter(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            tag.save()
        return tag
    
    def get_collections(self):
        collections = Collection.objects.all().order_by('created_on')
        response = []
        for collection in collections:
            response.append({
                "collectionName": collection.name,
                "collectionId": collection.id,
                "fashionLine": collection.fashion_line.name,
                "isActive": collection.is_active
            })
        return collections
    
    def get_occasions(self):
        occasions = Occasion.objects.all().order_by('created_on')
        response = []
        for occasion in occasions:
            response.append({
                "occasionName": occasion.name,
                "occasionId": occasion.id,
                "isActive": occasion.is_active
            })
        return occasions
    
    def get_tags(self):
        tags = Tag.objects.all().order_by('created_on')
        response = []
        for tag in tags:
            response.append({
                "tagName": tag.name,
                "tagId": tag.id,
                "isActive": tag.is_active
            })
        return tags
    
    def get_categories(self):
        categories = Category.objects.all().order_by('created_on')
        response = []
        for category in categories:
            response.append({
                "categoryName": category.name,
                "categoryId": category.id,
                "parentCategory": category.parent.name if category.parent else "",
                "parentCategoryId": category.parent.id if category.parent else "",
                "isActive": category.is_active
            })
        return categories

    