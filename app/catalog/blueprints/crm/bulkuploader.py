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

bulk_uploader_blueprint = Blueprint('bulk_uploader_blueprint', __name__)


class BulkUploadAPI(CommonResource):

    def get(self):
        data = request.args.to_dict()
        upload_type = data.get('uploadType', "").upper()
        page = data.get('page', 1)
        limit = data.get('limit', 10)
        upload_request_id = data.get('uploadRequestId', None)
        start_date = data.get('startDate', None)
        end_date = data.get('endDate', None)
        
        if upload_type and upload_type not in BulkUploaderManager.UPLOAD_TYPE_CLASS_MAP.keys():
            return ErrorHandler(message="Invalid upload type").error_response()
        
        upload_requests = BulkUploaderManager.get_bulk_upload_requests(upload_type, upload_request_id, start_date, end_date)
        pagination_handler = PaginationHandler(page, limit, request.path, request.args)
        pagination_data = pagination_handler.get_pagination_data(upload_requests)
        next_url = pagination_data.get("next_url")
        prev_url = pagination_data.get("prev_url")
        paginated_upload_requests = pagination_data.get("results")
        response_schema = GenericBulkUploaderRequestSchema(many=True)
        response = response_schema.dump(paginated_upload_requests)
        return SuccessHandler(response, request_obj=request).success_response(
            paginate=True, next_url=next_url, prev_url=prev_url, total_count=upload_requests.count())
    
    def post(self):
        form_data = request.form.to_dict()
        csv_file = request.files.get("data")
        upload_type = form_data.get('uploadType', '').upper()
        admin_user = request.headers.get('Client-User', '')
        if upload_type and upload_type not in BulkUploaderManager.UPLOAD_TYPE_CLASS_MAP.keys():
            return ErrorHandler(message="Invalid upload type").error_response()
        
        list_of_dict = AWSCSVManager.get_csv_data_in_list_of_dict_with_clean_header(csv_file)
        _class = BulkUploaderManager.UPLOAD_TYPE_CLASS_MAP[upload_type]
        is_valid_csv, message_list = _class.validate_csv_file(
            list_of_dict=list_of_dict, upload_type=upload_type)
        if not is_valid_csv:
            return ErrorHandler(message=message_list).error_response()
        
        csv_link = AWSCSVManager(bucket_name=AWSBuckets.GENERIC_BULK_UPLOAD).upload_to_aws(list_of_dict=list_of_dict)
        bulk_upload_request = BulkUploaderManager.add_bulk_upload_request(csv_link, admin_user, upload_type)
        bulk_uploader_runner(upload_type=upload_type, upload_request_id=bulk_upload_request.pk)
        response_schema = GenericBulkUploaderRequestSchema()
        response = response_schema.dump(bulk_upload_request)
        return SuccessHandler(response, request_obj=request).success_response()


class BulkUploadMetaDataAPI(CommonResource):
    def get(self):
        admin_user = request.headers.get('Client-User', '')
        meta_data = [{key: _class.get_schema_dict(admin_user=admin_user)} for key, _class
                        in BulkUploaderManager.UPLOAD_TYPE_CLASS_MAP.items()]
        return SuccessHandler({"meta_data": meta_data}, request_obj=request).success_response()