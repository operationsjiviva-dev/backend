from io import BytesIO, StringIO
import pandas
from datetime import datetime, timedelta
import re
import string
import csv
from common.managers.aws_client import AWSS3
from boto3.exceptions import S3UploadFailedError


class AWSCSVManager:
    CSV_EXPIRE_IN_DAYS = 7

    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.base_s3_url = "https://{}.s3.amazonaws.com/{}"

    @classmethod
    def get_csv_buffer_from_list_of_dict(cls, list_of_dict: list):
        csv_dataframe = pandas.DataFrame(list_of_dict)
        csv_buffer = BytesIO()
        csv_dataframe.to_csv(csv_buffer, index=False)

        return csv_buffer

    @classmethod
    def get_dynamic_file_name_for_csv(cls):
        file_name = datetime.now().strftime('%m%d%Y%H%M%S%f') + '.csv'
        return file_name

    def upload_to_aws(self, list_of_dict: list, file_name: str = '', expire_in_days:int = CSV_EXPIRE_IN_DAYS):
        if not file_name:
            file_name = self.get_dynamic_file_name_for_csv()

        csv_buffer = self.get_csv_buffer_from_list_of_dict(list_of_dict)
        expires = datetime.now() + timedelta(days=expire_in_days)

        s3_client = AWSS3.get_client()
        try:
            s3_client.put_object(
                Body=csv_buffer.getvalue(),
                ContentType='application/vnd.ms-excel',
                Bucket=self.bucket_name,
                Key='{}'.format(file_name),
                ACL='public-read',
                Expires=expires
            )
        except S3UploadFailedError as exception:
            raise exception

        aws_csv_url = self.base_s3_url.format(self.bucket_name, file_name)
        return aws_csv_url
    
    @classmethod
    def get_clean_header_string(cls, header_string: str):
        header_string = header_string.replace('_', ' ').strip().lower()
        header_string = re.sub("[.\(\[].*?[\)\]]", "", header_string)
        header_string = header_string.translate(string.punctuation)
        header_string = header_string.strip().replace(' ', '_').replace('__', '_')
        return header_string

    @classmethod
    def get_csv_data_in_list_of_dict_with_clean_header(cls, csv_file: csv):
        stream = StringIO(csv_file.stream.read().decode("UTF8"), newline='')
        rows = list(csv.reader(stream, delimiter=','))
        headers = [cls.get_clean_header_string(x) for x in rows[0]]    
        
        data_dict_list = []
        for row in rows[1:]:
            data_dict = {headers[index]: col for index, col in enumerate(row)}
            data_dict_list.append(data_dict)
            
        return data_dict_list
    
    @classmethod
    def download_csv_and_get_in_list_of_dict(cls, csv_file):
        csv_df = pandas.read_csv(csv_file, keep_default_na=False)
        return csv_df.to_dict('records')

