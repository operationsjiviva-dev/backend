from http import HTTPStatus
from flask import url_for
from flask import request
from urllib import parse



class SuccessHandler:
    """
    Handler to send success responses
    """
    def __init__(self, data, http_status: int = 200, extra_data: dict = None, request_obj: request = None):
        self.data = data
        self.request_obj = request_obj
        self.extra_data = extra_data

        if isinstance(http_status, HTTPStatus):
            self.http_status = http_status
        else:
            self.http_status = HTTPStatus(http_status)

    def build_url(self, parameters: dict = {}):
        path = self.request_obj.path
        if parameters:
            params = '&'.join([f"{str(key)}={parse.quote(str(value), safe='')}" for key, value in parameters.items()])
            path += "?" + params
        return path

    def success_response(
            self, paginate: bool = False, current_page: int = 1,
            next_url: str = None, prev_url: str = None, total_count=None):
        response = dict(
            success=True,
        )

        if self.data:
            response['data'] = self.data
        else:
            if isinstance(self.data, list):
                response['data'] = []
            else:
                response['data'] = {}

        if isinstance(self.data, list):
            response['count'] = len(self.data)

        if total_count:
            response['count'] = total_count

        if self.extra_data:
            response.update(**self.extra_data)

        if paginate:
            if next_url or prev_url or type(next_url) == str:
                response['next'] = next_url
                response['prev'] = prev_url
            elif current_page:
                args = self.request_obj.args.to_dict()
                if current_page == 1:
                    response['prev'] = ""
                else:
                    args['page'] = current_page - 1
                    response['prev'] = self.build_url(args)

                args['page'] = current_page + 1
                response['next'] = self.build_url(args)

        return response, self.http_status
