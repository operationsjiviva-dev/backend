import os
import django
from flask import Blueprint, request
from common.handlers.error import ErrorHandler
from common.handlers.success import SuccessHandler
from common.handlers.pagination import PaginationHandler
from common.resource.base import CommonResource
from catalog.schemas.post_requests.product_meta import PostProductMetaSchema
from catalog.miscellaneous_values.product import ProductMetaAtrributes
from catalog.managers.product_meta_manager import ProductMetaManager


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'app.settings'
)
django.setup()

product_blueprint = Blueprint('product_blueprint', __name__)


class ProductMetaAPI(CommonResource):

    def post(self) -> dict:
        request_schema = PostProductMetaSchema()
        post_data = request.get_json(force=True)
        errors = request_schema.validate(post_data)
        if errors:
            return ErrorHandler(errors).error_response()
        
        post_data = request_schema.load(post_data)
        attribute_name = post_data.get('attribute_name')
        meta_data = post_data.get('data')
        if attribute_name == ProductMetaAtrributes.COLLECTION:
            collection_name = meta_data.get('collection_name')
            fashion_line_id = meta_data.get('fashion_line_id', None)
            collection = ProductMetaManager().create_collection(collection_name, fashion_line_id)
            return SuccessHandler({}, request_obj=request).success_response()
        
        if attribute_name == ProductMetaAtrributes.CATEGORY:
            category_name = meta_data.get('category_name')
            parent_category_id = meta_data.get('parent_category_id', None)
            category = ProductMetaManager().create_category(category_name, parent_category_id)
            return SuccessHandler({}, request_obj=request).success_response()
        
        if attribute_name == ProductMetaAtrributes.OCCASION:
            occasion_name = meta_data.get('occasion_name')
            occasion = ProductMetaManager().create_occasion(occasion_name)
            return SuccessHandler({}, request_obj=request).success_response()
        
        if attribute_name == ProductMetaAtrributes.TAG:
            tag_name = meta_data.get('tag_name')
            tag = ProductMetaManager().create_tag(tag_name)
            return SuccessHandler({}, request_obj=request).success_response()
        
    def get(self) -> dict:
        param_json = request.args.to_dict()
        attribute_name = param_json.get('attributeName')
        if attribute_name == ProductMetaAtrributes.COLLECTION:
            response = ProductMetaManager().get_collections()
            return SuccessHandler(response, request_obj=request).success_response()
        
        if attribute_name == ProductMetaAtrributes.CATEGORY:
            response = ProductMetaManager().get_categories()
            return SuccessHandler(response, request_obj=request).success_response()
        
        if attribute_name == ProductMetaAtrributes.OCCASION:
            response = ProductMetaManager().get_occasions()
            return SuccessHandler(response, request_obj=request).success_response()
        
        if attribute_name == ProductMetaAtrributes.TAG:
            response = ProductMetaManager().get_tags()
            return SuccessHandler(response, request_obj=request).success_response()
        
        return ErrorHandler(message="Invalid attribute name").error_response()
    

