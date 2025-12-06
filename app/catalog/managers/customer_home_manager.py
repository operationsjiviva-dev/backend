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
        categories = CategoryManager.get_categories()
        occasions = OccasionManager.get_occasions_with_products()

        filters["men"]["collections"] = collections.filter(gender_id=1)
        filters["men"]["categories"] = categories.filter(gender_id=1)
        filters["men"]["occasions"] = occasions.filter(gender_id=1)
        filters["women"]["collections"] = collections.filter(gender_id=2)
        filters["women"]["categories"] = categories.filter(gender_id=2)
        filters["women"]["occasions"] = occasions.filter(gender_id=2)
        filters["collections"] = collections
        filters["categories"] = categories
        filters["occasions"] = occasions
        if collections:
            top_collections = collections[:6]
        if categories:
            top_categories = categories[:6]
        home_data["top_collections"] = top_collections
        home_data["top_categories"] = top_categories
        home_data["filters"] = filters


        return home_data


        