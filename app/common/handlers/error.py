from http import HTTPStatus
from typing import Union


class ErrorHandler:
    """
    Handler to send error responses
    """
    def __init__(self, errors: Union[dict, list] = {}, message: str = None, error_code: int = None, display_text: str = None, http_status: int = 400):
        self.errors = errors
        self.message = message
        self.error_code = error_code
        self.display_text = display_text

        if isinstance(http_status, HTTPStatus):
            self.http_status = http_status
        else:
            self.http_status = HTTPStatus(http_status)

    def error_response(self):
        response = dict(
            success=False,
        )

        if self.errors:
            if isinstance(self.errors, list):
                response['errors'] = self.errors

            elif isinstance(self.errors, dict):

                errors_list = []
                for key in self.errors:
                    if isinstance(self.errors[key], dict):
                        errors_list = self.errors[key]
                    else:
                        errors_list.append({
                            "message": self.errors[key][0],
                            "field": key
                        })

                response['errors'] = errors_list

        if self.message:
            if not self.errors:
                error_message = {
                    "message": self.message
                }
                if self.error_code:
                    error_message['error_code'] = self.error_code

                if self.display_text:
                    error_message['display_text'] = self.display_text

                response['errors'] = [error_message]
            else:
                response['message'] = self.message


        return response, self.http_status

    def abort_response(self):
        response, http_status = self.error_response()
        return response

