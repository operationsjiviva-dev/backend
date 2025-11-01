from order.models import Cart, CartProduct, DeliveryAddress
from order.exceptions.cart import CartDoesNotExist, ProductDoesNotExist, ProductOutOfStock, \
    CartProductQuantityLimitExceeded, InvalidPaymentPreference
from catalog.models import Product, ProductVariant
from order.miscellaneous_values.cart import CartPaymentPreference
import json
from order.miscellaneous_values.cart import CartStatus


class CartManager:
    SKU_LEVEL_QUANTITY_LIMIT = 10
    def __init__(self, cart_id: int):
        self.cart = Cart.objects.filter(pk=cart_id).first()
        if not self.cart:
            raise CartDoesNotExist
    
    def validate_product(self, variant_id: int):
        variant = ProductVariant.objects.filter(pk=variant_id).first()
        if not variant:
            raise ProductDoesNotExist
        if not variant.in_stock:
            raise ProductOutOfStock
    
    def validate_quantity(self, quantity: int, existing_quantity: int = 0):
        if existing_quantity + quantity > self.SKU_LEVEL_QUANTITY_LIMIT:
            raise CartProductQuantityLimitExceeded
        
    
    def add_product(self, product_id: int, quantity: int, variant_id: int):
        self.validate_product(variant_id)
        cart_product = CartProduct.objects.filter(cart=self.cart, product_id=product_id, variant_id=variant_id).first()
        if not cart_product:
            cart_product = CartProduct.objects.create(cart=self.cart, product_id=product_id, variant_id=variant_id, quantity=quantity)
        else:
            self.validate_quantity(quantity, cart_product.quantity)
            cart_product.quantity = quantity
            cart_product.save()
        
        return cart_product
    
    def update_product(self, product_id: int, quantity: int, variant_id: int):
        self.validate_product(variant_id)
        cart_product = CartProduct.objects.filter(cart=self.cart, product_id=product_id, variant_id=variant_id).first()
        if not cart_product:
            self.add_product(product_id, quantity, variant_id)
        elif quantity == 0:
            cart_product.delete()
        else:
            self.validate_quantity(quantity)
            cart_product.quantity = quantity
            cart_product.save()
        
        return cart_product
    
    def update_payment_preference(self, payment_preference: str):
        if payment_preference not in CartPaymentPreference.values():
            raise InvalidPaymentPreference

        self.cart.payment_preference = payment_preference
        self.cart.save()
    

    def add_delivery_address(self, delivery_address_dict: dict):
        delivery_address = DeliveryAddress()
        delivery_address.address = json.dumps(delivery_address_dict)

        self.cart.delivery_address = delivery_address
        self.cart.save()

        return delivery_address
    
    def update_delivery_address(self, delivery_address_id: int, delivery_address_dict: dict):
        delivery_address = DeliveryAddress.objects.filter(pk=delivery_address_id).first()
        delivery_address.address = json.dumps(delivery_address_dict)
        delivery_address.save()

        return delivery_address
    
    def remove_delivery_address(self, delivery_address_id: int):
        delivery_address = DeliveryAddress.objects.filter(pk=delivery_address_id).first()
        delivery_address.delete()

        return True
    
    def calculate_cart_bill(selfm, cart_products: list):
        cart_bill = 0
        for cart_product in cart_products:
            cart_bill += cart_product.variant.selling_price * cart_product.quantity

        return cart_bill


    def get_cart_data(self):
        cart_products = CartProduct.objects.filter(cart=self.cart)
        total_bill = self.calculate_cart_bill(cart_products)
        cart_data = {
            "cart": self.cart,
            'cart_id': self.cart.pk,
            'cart_products': CartProduct.objects.filter(cart=self.cart),
            'delivery_address': json.loads(self.cart.delivery_address.address) if self.cart.delivery_address else {},
            'payment_preference': self.cart.payment_preference,
            'total_bill': total_bill
        }

        return cart_data
    
    @classmethod
    def get_cart_by_id(cls, cart_id: int):
        return Cart.objects.filter(pk=cart_id).first()
    
    @classmethod
    def get_or_create_cart(cls, customer_id: int):
        cart = Cart.objects.filter(customer_id=customer_id, status=CartStatus.OPEN).first()
        if not cart:
            cart = Cart.objects.create(customer_id=customer_id)
        
        return cart
    
    def mark_cart_as_closed(self):
        self.cart.status = CartStatus.CLOSED
        self.cart.save()
        return True
       

    