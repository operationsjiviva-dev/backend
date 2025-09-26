import os
import django
from flask import Blueprint, request
from common.handlers.error import ErrorHandler
from common.handlers.success import SuccessHandler
from common.resource.base import CommonResource
from order.managers.cart_manager import CartManager
from order.exceptions.cart import CartDoesNotExist, ProductDoesNotExist, ProductOutOfStock, \
    CartProductQuantityLimitExceeded, InvalidPaymentPreference
from order.schemas.response_schema.cart import CartResponseSchema
from order.schemas.post_schema.cart import DeliveryAddressSchema, UpdateDeliveryAddressSchema


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'app.settings'
)
django.setup()

cart_blueprint = Blueprint('cart_blueprint', __name__)


class CartProductAPI(CommonResource):
    def post(self, cart_id: int):
        post_data = request.get_json(force=True)
        product_id = post_data.get('productId')
        variant_id = post_data.get('variantId')
        quantity = post_data.get('quantity')

        try:
            cart_manager = CartManager(cart_id)
            cart_product = cart_manager.add_product(product_id, quantity, variant_id)
            cart_data = cart_manager.get_cart_data()
            response_schema = CartResponseSchema()
            response = response_schema.dump(cart_data)
            return SuccessHandler(response, request_obj=request).success_response()
        
        except(CartDoesNotExist, ProductDoesNotExist, 
               ProductOutOfStock, CartProductQuantityLimitExceeded, InvalidPaymentPreference) as e:
            return ErrorHandler(str(e)).error_response()
    
    def patch(self, cart_id: int):
        post_data = request.get_json(force=True)
        product_id = post_data.get('productId')
        variant_id = post_data.get('variantId')
        quantity = post_data.get('quantity')

        try:
            cart_manager = CartManager(cart_id)
            cart_product = cart_manager.update_product(product_id, quantity, variant_id)
            cart_data = cart_manager.get_cart_data()
            response_schema = CartResponseSchema()
            response = response_schema.dump(cart_data)
            return SuccessHandler(response, request_obj=request).success_response()
        
        except(CartDoesNotExist, ProductDoesNotExist, 
               ProductOutOfStock, CartProductQuantityLimitExceeded, InvalidPaymentPreference) as e:
            return ErrorHandler(str(e)).error_response()


class UpdatePaymentPreferenceAPI(CommonResource):
    def patch(self, cart_id: int):
        post_data = request.get_json(force=True)
        payment_preference = post_data.get('paymentPreference')

        try:
            cart_manager = CartManager(cart_id)
            cart_manager.update_payment_preference(payment_preference)
            cart_data = cart_manager.get_cart_data()
            response_schema = CartResponseSchema()
            response = response_schema.dump(cart_data)
            return SuccessHandler(response, request_obj=request).success_response()
        
        except(CartDoesNotExist, ProductDoesNotExist, 
               ProductOutOfStock, CartProductQuantityLimitExceeded, InvalidPaymentPreference) as e:
            return ErrorHandler(str(e)).error_response()


class DeliveryAddressAPI(CommonResource):
    def post(self, cart_id: int):
        request_schema = DeliveryAddressSchema()
        post_data = request.get_json(force=True)
        errors = request_schema.validate(post_data)
        if errors:
            return ErrorHandler(errors).error_response()
        delivery_address = request_schema.load(post_data)
        try:
            cart_manager = CartManager(cart_id)
            cart_manager.add_delivery_address(delivery_address)
            cart_data = cart_manager.get_cart_data()
            response_schema = CartResponseSchema()
            response = response_schema.dump(cart_data)
            return SuccessHandler(response, request_obj=request).success_response()
        
        except(CartDoesNotExist, ProductDoesNotExist, 
               ProductOutOfStock, CartProductQuantityLimitExceeded, InvalidPaymentPreference) as e:
            return ErrorHandler(str(e)).error_response()
    
    def patch(self, cart_id: int):
        request_schema = UpdateDeliveryAddressSchema()
        post_data = request.get_json(force=True)
        errors = request_schema.validate(post_data)
        if errors:
            return ErrorHandler(errors).error_response()
        post_data = request_schema.load(post_data)
        try:
            id = post_data.get('id')
            delivery_address = post_data.get('delivery_address')
            cart_manager = CartManager(cart_id)
            cart_manager.update_delivery_address(id, delivery_address)
            cart_data = cart_manager.get_cart_data()
            response_schema = CartResponseSchema()
            response = response_schema.dump(cart_data)
            return SuccessHandler(response, request_obj=request).success_response()
        
        except(CartDoesNotExist, ProductDoesNotExist, 
               ProductOutOfStock, CartProductQuantityLimitExceeded, InvalidPaymentPreference) as e:
            return ErrorHandler(str(e)).error_response()
    



        
