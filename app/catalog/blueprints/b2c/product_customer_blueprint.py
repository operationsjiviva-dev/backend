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

product_customer_blueprint = Blueprint('product_customer_blueprint', __name__)


class HomeAPI(CommonResource):

    def get(self):
        data = request.args.to_dict()
        upload_type = data.get('uploadType', "").upper()
        page = data.get('page', 1)
        limit = data.get('limit', 10)
        upload_request_id = data.get('uploadRequestId', None)
        start_date = data.get('startDate', None)
        end_date = data.get('endDate', None)