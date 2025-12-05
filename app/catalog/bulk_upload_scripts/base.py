from abc import ABC, abstractmethod
from catalog.models import GenericBulkUploadRequest, GenericBulkUploadResponse
from common.managers.aws_csv_manager import AWSCSVManager
from datetime import datetime
import traceback
from common.miscellaneous_values.aws_buckets import AWSBuckets
from common.models import SystemSettings
import json


class BulkUploadeBaseClass(ABC):
    """
    Abstract base class for bulk uploader
    """
    optional_headers = []
    required_headers = []
    upload_access_to_user_group = ['SUPER_ADMIN']
    upload_access_to_user_in_having_permission = [
        'GENERAL_GENERIC_BULK_UPLOADER']

    def __init__(self, upload_request_id: int):
        bulk_request = GenericBulkUploadRequest.objects.get(
            pk=upload_request_id)
        self.user = bulk_request.admin_user
        self.bulk_request = bulk_request
        self.bulk_response = GenericBulkUploadResponse.objects.create()
        self.bulk_response.genericbulkuploadrequest = self.bulk_request
        self.bulk_response.save()
        self.bulk_request.response = self.bulk_response
        self.bulk_request.save()

        self.meta_dict = bulk_request.params_dict
        request_list_of_dict = AWSCSVManager.download_csv_and_get_in_list_of_dict(
            bulk_request.request_file_link)
        self.request_list_of_dict = request_list_of_dict
        self.response_list_of_dict = []
        self.response_file_link = ''
        self.success_rows = 0
        self.total_rows = len(self.request_list_of_dict)

    @abstractmethod
    def process_row(self, row: dict, **kwargs):
        """
        :param row: single csv row to process
        :param kwargs:

        Abstract method to be implemented by every sub class(every uploader)
        for writing the data processing logic for single row
        """
        pass

    @abstractmethod
    def post_upload_changes(self, response_list_of_dict: list, **kwargs):
        """
        :param response_list_of_dict: bulk upload response data 

        Abstract method to be implemented if needed by sub class(uploader)
        for writing any logic after bulk uploade is completed
        """
        pass

    def pre_upload_changes(self, response_list_of_dict: list, **kwargs):
        """
        :param response_list_of_dict: bulk upload response data 

        Method to be implemented by sub class(uploader) if needed
        for writing any logic before bulk upload is started
        """
        return response_list_of_dict

    def start(self, request_list_of_dict: list, **kwargs):
        """
        :param request_list_of_dict: bulk upload request data

        This will take csv data as list of dicts and process each row
        and update status for each row i.e. either True or False, if status is False
        then it will also update the reason for failure for that specific row.

        :returns completion status and list of rows with status and reason in the form of list of dicts   
        """
        try:
            request_list_of_dict = self.pre_upload_changes(request_list_of_dict, **kwargs)
        except Exception as e:
            print(e, str(self.__class__))
        for index, request_dict in enumerate(request_list_of_dict):
            request_dict['status'] = False
            request_dict['reason'] = request_dict.get('reason', '')
            request_dict['warning'] = ''
            try:
                success, result = self.process_row(request_dict)
                if success:
                    request_dict['status'] = True
                    request_dict.update(result)
                else:
                    if isinstance(result, list):
                        result = ' | '.join(result)
                    request_dict['reason'] = str(result)

            except Exception as e:
                request_dict['reason'] = 'EXCEPTION {}'.format(str(e))

        try:
            self.post_upload_changes(request_list_of_dict, **kwargs)
        except Exception as e:
            print(e, str(self.__class__))

        return True, request_list_of_dict

    def run(self):
        """
        Starting function to run the bulk upload. It will run the bulk upload
        request and update the status of bulk upload request and bulk upload response
        """
        self.bulk_response.process_start_time = datetime.now()
        self.bulk_response.save()
        self.bulk_request.status = 'PROCESSING'
        self.bulk_request.save()

        try:
            status, resp_list_of_dicts = self.start(
                self.request_list_of_dict
            )
            self.bulk_response.status = status
            self.response_list_of_dict = resp_list_of_dicts
            if resp_list_of_dicts and isinstance(resp_list_of_dicts, list):
                self.success_rows = sum(
                    [
                        x['status'] for x in resp_list_of_dicts
                        if 'status' in x and isinstance(x['status'], bool)]
                )
                response_file_link = AWSCSVManager(
                    AWSBuckets.GENERIC_BULK_UPLOAD).upload_to_aws(resp_list_of_dicts)
                self.response_file_link = response_file_link
                self.bulk_response.response_file_link = self.response_file_link
        except Exception as e:
            print(e, str(self.__class__))
            self.bulk_response.error_trace = traceback.format_exc()
            self.bulk_response.status = 'SERVER_ERROR'

        self.bulk_response.process_end_time = datetime.now()
        self.bulk_response.is_completed = True
        self.bulk_request.status = 'COMPLETED : {}/{}'.format(
            self.total_rows, self.success_rows)
        self.bulk_request.save()
        self.bulk_response.save()

    @classmethod
    def validate_batch_size(cls, list_of_dict, upload_type):
        """
        This will validate the batch size for any bulk uploader
        """
        settings = SystemSettings.objects.filter(
            key='bulk_uploader_batch_size').first()
        maximum_batch_size = 1000
        if settings and settings.value:
            settings = json.loads(settings.value)
            if maximum_batch_size :=settings.get(upload_type):
                if len(list_of_dict) > maximum_batch_size:
                    return False, maximum_batch_size
        return True, maximum_batch_size

    @classmethod
    def validate_csv_file(cls, list_of_dict, upload_type=None):
        """
        This will validate the csv file headers for any bulk uploader
        """
        is_valid = True
        message_list = []

        # Validate Batch Size
        is_batch_size_allowed = True
        is_batch_size_allowed, maximum_batch_size = cls.validate_batch_size(
            list_of_dict, upload_type=upload_type)
        if not is_batch_size_allowed:
            is_valid = False
            message_list.append('Maximum batch size allowed is {}. The current value {} exceeds it.'.format(
                maximum_batch_size, len(list_of_dict)))
            return False, message_list

        # Validate Headers
        headers_list = list(list_of_dict[0].keys())
        optional_headers_set = set(cls.optional_headers)
        required_headers_set = set(cls.required_headers)
        validate_required_headers_set = required_headers_set.issubset(
            set(headers_list))
        if not validate_required_headers_set:
            is_valid = False
            message_list.append('headers [{}] not found'.format(
                ', '.join(required_headers_set - set(
                    headers_list) - optional_headers_set)
            ))

            extra_passed_header = set(headers_list) - set(headers_list) \
                .intersection(required_headers_set) - optional_headers_set

            if len(extra_passed_header) > 0:
                message_list.append(
                    ',  if any of the following headers [{}] means same '
                    'replace their name '
                    .format(', '.join(extra_passed_header))
                )
            return False, message_list

        return is_valid, message_list

    