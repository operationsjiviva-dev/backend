from catalog.managers.collection_manager import CollectionManager
from catalog.managers.category_manager import CategoryManager
from catalog.managers.occasion_manager import OccasionManager


class CustomerHomeManager:
    def __init__(self):
        pass

    def get_customer_home_data(self):
        top_collections = []
        top_categories = []
        filters = {
                "men": {
                    "collections": [], "categories": [], "occasions": []
                }, 
                "women": {
                    "collections": [], "categories": [], "occasions": []
                }, 
                "collections": {
                    "collections": []
                }, 
                "occasions": {
                    "occasions": []
                }, 
                "categories":{
                    "categories": []
                } 
            }
        home_data = {}

        collections = CollectionManager.get_collections()
        if collections:
            top_collections = collections[:6]

        categories = CategoryManager.get_categories()
        if categories:
            top_categories = categories[:6]
        
        occasions = OccasionManager.get_occasions_with_products()
        
        home_data["top_collections"] = top_collections
        home_data["top_categories"] = top_categories

        filters["men"]["collections"] = collections.objects.filter(gender_id=1)
        filters["men"]["categories"] = categories.objects.filter(gender_id=1)
        filters["men"]["occasions"] = occasions.objects.filter(gender_id=1)
        filters["women"]["collections"] = collections.objects.filter(gender_id=2)
        filters["women"]["categories"] = categories.objects.filter(gender_id=2)
        filters["women"]["occasions"] = occasions.objects.filter(gender_id=2)
        filters["collections"] = collections
        filters["categories"] = categories
        filters["occasions"] = occasions


        return home_data


        