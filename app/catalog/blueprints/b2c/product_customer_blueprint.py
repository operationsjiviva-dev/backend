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

product_customer_blueprint = Blueprint('product_customer_blueprint', __name__)


class HomeAPI(CommonResource):

    def get(self):
        home_data = CustomerHomeManager().get_customer_home_data()
        response = CustomerHomeResponseSchema().dump(home_data)
        return SuccessHandler(response, request_obj=request).success_response()