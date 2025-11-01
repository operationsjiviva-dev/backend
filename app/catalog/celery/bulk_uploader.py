# from celery import shared_task
from catalog.bulk_upload_scripts.base import BulkUploadeBaseClass


# @shared_task(queue="default")
def bulk_uploader_runner(upload_type: str, upload_request_id: int):
    UPLOAD_TYPE_CLASS_MAP = {
        x.__name__.upper(): x for x in BulkUploadeBaseClass.__subclasses__()}
    uploader_class = UPLOAD_TYPE_CLASS_MAP[upload_type.upper()]
    if uploader_class:
        uploader_class(upload_request_id).run()