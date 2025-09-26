from order.miscellaneous_values.cart import CartStatus
from order.exceptions.order import CartDoesNotExist, CartIsEmpty, CartDeliveryAdrressNotSet, PaymentPreferenceNotSet


class PreOrderCartValidationHandler:
    def __init__(self, cart_data: dict):
        self.cart_data = cart_data
    
    def validate_data(self):
        cart = self.cart_data.get('cart')
        if cart.status != CartStatus.OPEN:
            raise CartDoesNotExist
        cart_products = self.cart_data.get('cart_products')
        if not cart_products:
            raise CartIsEmpty
        delivery_address = self.cart_data.get('delivery_address')
        if not delivery_address:
            raise CartDeliveryAdrressNotSet
        payment_preference = self.cart_data.get('payment_preference')
        if not payment_preference:
            raise PaymentPreferenceNotSet

        return self.cart_data



