import os
import django
from flask import Blueprint, request
from common.handlers.error import ErrorHandler
from common.handlers.success import SuccessHandler
from common.resource.base import CommonResource
from order.managers.order_manager import OrderManager
from order.exceptions.order import CartDoesNotExist, CartIsEmpty, CartDeliveryAdrressNotSet, PaymentPreferenceNotSet
from order.models import Order
from order.schemas.response_schema.order import OrderDetailsResponseSchema


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'app.settings'
)
django.setup()

order_customer_blueprint = Blueprint('order_customer_blueprint', __name__)


class OrderAPI(CommonResource):
    def post(self):
        post_data = request.get_json(force=True)
        cart_id = post_data.get('cartId')

        try:
            order = OrderManager.create_order(cart_id)
            response = {
                "orderId": order.id
            }
            return SuccessHandler(response, request_obj=request).success_response()
        
        except (CartDoesNotExist, CartIsEmpty, CartDeliveryAdrressNotSet, PaymentPreferenceNotSet)  as e:
            return ErrorHandler(str(e)).error_response()
    
    def get(self, order_id: int):
        order = Order.objects.filter(pk=order_id).first()
        if not order:
            return ErrorHandler("Order does not exist").error_response()
        
        response_schema = OrderDetailsResponseSchema()
        response = response_schema.dump(order)
        return SuccessHandler(response, request_obj=request).success_response()
        

class OrderListAPI(CommonResource):
    def get(self):
        customer_id = request.headers.get('Customer-Id')
        orders = Order.objects.filter(customer_id=customer_id).order_by('-created_on')
        response_schema = OrderDetailsResponseSchema(many=True)
        response = response_schema.dump(orders)
        return SuccessHandler(response, request_obj=request).success_response()