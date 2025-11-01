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
from common.handlers.pagination import PaginationHandler
from order.schemas.get_requests.order_crm import OrderListRequestSchema


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'app.settings'
)
django.setup()

order_crm_blueprint = Blueprint('order_crm_blueprint', __name__)


class OrderCRMAPI(CommonResource):
    def get(self, order_id: int):
        order = Order.objects.filter(pk=order_id).first()
        if not order:
            return ErrorHandler("Order does not exist").error_response()
        
        response_schema = OrderDetailsResponseSchema()
        response = response_schema.dump(order)
        return SuccessHandler(response, request_obj=request).success_response()

class OrderCRMListAPI(CommonResource):
    def get(self):
        request_schema = OrderListRequestSchema()
        errors = request_schema.validate(request.args)
        if errors:
            return ErrorHandler(errors).error_response()
      
        data = request_schema.load(request.args)
        page = data.get('page', 1)
        limit = data.get('limit', 10)
        orders = OrderManager.get_orders_with_filters(data)
        pagination_handler = PaginationHandler(page, limit, request.path, request.args)
        pagination_data = pagination_handler.get_pagination_data(orders)
        next_url = pagination_data.get("next_url")
        prev_url = pagination_data.get("prev_url")
        paginated_orders = pagination_data.get("results")
        response_schema = OrderDetailsResponseSchema(many=True)
        response = response_schema.dump(paginated_orders)
        return SuccessHandler(response, request_obj=request).success_response(
            paginate=True, next_url=next_url, prev_url=prev_url, total_count=orders.count())
