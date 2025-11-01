from catalog.bulk_upload_scripts.base import BulkUploadeBaseClass 
from catalog.models import GenericBulkUploadRequest
from common.helpers.datetime_helper import get_start_date_end_date_in_datetime


class BulkUploaderManager:
    UPLOAD_TYPE_CLASS_MAP = {x.__name__.upper(): x for x in BulkUploadeBaseClass.__subclasses__()}

    @classmethod
    def get_uploader_class(cls, upload_type: str):
        return cls.UPLOAD_TYPE_CLASS_MAP[upload_type.upper()]
    
    @classmethod
    def get_bulk_upload_requests(cls, upload_type: str = "", upload_requeat_id: int = None, start_date: str = None, end_date: str = None):
        if start_date and end_date:
            start_date, end_date = get_start_date_end_date_in_datetime(start_date, end_date)

        query_set = GenericBulkUploadRequest.objects.all()
        if upload_requeat_id:
            query_set = query_set.filter(pk=upload_requeat_id)
        if upload_type:
            query_set = query_set.filter(upload_type=upload_type.upper())
        if start_date and end_date:
            query_set = query_set.filter(created_on__gte=start_date, created_on__lte=end_date)
        
        return query_set.order_by('-created_on')
    
    @classmethod
    def add_bulk_upload_request(cls, csv_link: str, admin_user: str, upload_type: str):
        generic_bulk_request = GenericBulkUploadRequest.objects.create(
            upload_type=upload_type.upper(),
            request_file_link=csv_link,
            admin_user=admin_user
        )

        return generic_bulk_request

    

