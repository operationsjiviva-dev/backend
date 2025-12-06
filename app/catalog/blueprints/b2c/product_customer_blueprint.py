import os
import django
from flask import Blueprint, request
from common.handlers.error import ErrorHandler
from common.handlers.success import SuccessHandler
from common.handlers.pagination import PaginationHandler
from common.resource.base import CommonResource
from catalog.managers.bulk_uploader_manager import BulkUploaderManager
from common.managers.aws_csv_manager import AWSCSVManager
from catalog.celery.bulk_uploader import bulk_uploader_runner
from catalog.schemas.response_schema.bulk_uploader import GenericBulkUploaderRequestSchema
from common.miscellaneous_values.aws_buckets import AWSBuckets
from catalog.managers.customer_home_manager import CustomerHomeManager
from catalog.schemas.response_schema.home import CustomerHomeResponseSchema
from catalog.managers.product_manager import ProductManager
from catalog.schemas.get_requests.customer_product_listing import CustomerProductListingGetSchema
from catalog.schemas.response_schema.customer_product_listing import CustomerProductListingResponseSchema

product_customer_blueprint = Blueprint('product_customer_blueprint', __name__)


class HomeAPI(CommonResource):

    def get(self):
        home_data = CustomerHomeManager().get_customer_home_data()
        response = CustomerHomeResponseSchema().dump(home_data)
        return SuccessHandler(response, request_obj=request).success_response()
    
class CustomerProductListingAPI(CommonResource):

    def get(self):
        request_schema = CustomerProductListingGetSchema()
        errors = request_schema.validate(request.args)
        if errors:
            return ErrorHandler(errors).error_response()
      
        data = request_schema.load(request.args)
        page = data.get('page', 1)
        limit = data.get('limit', 10)
        print(data)
        products = ProductManager.get_products_with_filters(data)
        product_filters = ProductManager.get_filters_for_product_listing(products)
        pagination_handler = PaginationHandler(page, limit, request.path, request.args)
        pagination_data = pagination_handler.get_pagination_data(products)
        next_url = pagination_data.get("next_url")
        prev_url = pagination_data.get("prev_url")
        paginated_products = pagination_data.get("results")
        response_data = {"products": paginated_products, "filters": product_filters}
        response_schema = CustomerProductListingResponseSchema()
        response = response_schema.dump(response_data)
        return SuccessHandler(response, request_obj=request).success_response(
            paginate=True, next_url=next_url, prev_url=prev_url, total_count=products.count()
        )
