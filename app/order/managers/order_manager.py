from order.models import Order, OrderPayment, OrderProduct
import secrets
from order.managers.cart_manager import CartManager
from order.handlers.pre_order_cart_validation import PreOrderCartValidationHandler
from order.exceptions.order import OrderDoesNotExist
from datetime import datetime


class OrderManager:

    def __init__(self, order_id: int):
        self.order = Order.objects.filter(pk=order_id).first()
        if not self.order:
            raise OrderDoesNotExist

    @classmethod
    def create_order_id(cls):
        while True:
            order_id = secrets.choice(range(10000000, 99999999))
            existing_order = Order.objects.filter(id=order_id).first()
            if not existing_order:
                return order_id
    
    @classmethod
    def create_order_products(cls, cart_products: list):
        for cart_product in cart_products:
            OrderProduct.objects.create(
                order=cart_product.order,
                product=cart_product.product,
                variant=cart_product.variant,
                quantity=cart_product.quantity,
                selling_price=cart_product.variant.selling_price
            )
        
        return True
    
    @classmethod
    def create_order_payment(cls, payment_preference: str, total_bill: float):
        payment = OrderPayment()
        payment.mode = payment_preference.upper()
        payment.amount_payable = total_bill
        payment.save()

        return payment

    @classmethod
    def create_order(cls, cart_id: int, order_id: int = None):
        if not order_id:
            order_id = cls.create_order_id()
        
        cart_manager = CartManager(cart_id)
        cart_data = cart_manager.get_cart_data()
        pre_order_validation_handler = PreOrderCartValidationHandler(cart_data)
        pre_order_validation_handler.validate_data()

        cart_products = cart_data.get('cart_products')
        delivery_address = cart_data.get('delivery_address')
        payment_preference = cart_data.get('payment_preference')
        total_bill = cart_data.get('total_bill')

        order = Order()
        order.id = order_id
        order.customer = cart_data.get('cart').customer
        order.cart = cart_data.get('cart')
        order.payment = cls.create_order_payment(payment_preference, total_bill)
        order.delivery_address = delivery_address

        order.save()
        cart_manager.mark_cart_as_closed()
        cls.create_order_products(cart_products)

        return order
    
    @classmethod
    def get_orders_with_filters(cls, parameters: dict):
        filters = {}
        if 'phone_number' in parameters:
            filters['customer__phone_number'] = parameters.get('phone_number')
        if 'order_id' in parameters:
            filters['id'] = parameters.get('order_id')
        if 'start_date' in parameters and 'end_date' in parameters:
            start_date = datetime.fromtimestamp(int(parameters.get('start_date'))/1000)
            end_date = datetime.fromtimestamp(int(parameters.get('end_date'))/1000)
            filters['created_on__range'] = (start_date, end_date)
        if 'delivery_status' in parameters:
            filters['delivery_status'] = parameters.get('delivery_status').upper()

        orders = Order.objects.filter(**filters).order_by('-created_on')
        return orders
    


        
        
        

