import os
import django
from flask import Blueprint, request
from common.handlers.error import ErrorHandler
from common.handlers.success import SuccessHandler
from common.resource.base import CommonResource
from customer.managers.customer_manager import CustomerManager
from customer.managers.otp_manager import OTPManager


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'app.settings'
)
django.setup()

customer_blueprint = Blueprint('customer_blueprint', __name__)


class SendOtpAPI(CommonResource):

    def post(self) -> dict:
        request_data = request.get_json(force=True)
        phone_number = request_data.get('phoneNumber')
        name = request_data.get('name')
        gender = request_data.get('gender')
        CustomerManager.send_otp(phone_number, name, gender)

        return SuccessHandler({}, request_obj=request).success_response()
    
class LoginAPI(CommonResource):

    def post(self) -> dict:
        request_data = request.get_json(force=True)
        phone_number = request_data.get('phoneNumber')
        otp = request_data.get('otp')
        if not OTPManager().is_otp_valid(phone_number, otp):
            return ErrorHandler("Invalid OTP").error_response()
        else:
            customer = CustomerManager.get_customer_using_phone_number(phone_number)
            response_data = CustomerManager.get_single_customer_data(customer)

            return SuccessHandler(response_data, request_obj=request).success_response()

