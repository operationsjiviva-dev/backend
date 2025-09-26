from django.db import models

# Create your models here.

from common.models import TimeStampedModel


class DeliveryAddress(TimeStampedModel):
    customer = models.ForeignKey("customer.Customer", on_delete=models.CASCADE)
    address = models.TextField(default='{}')
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)


class Cart(TimeStampedModel):
    customer = models.ForeignKey("customer.Customer", null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=256, default='PENDING')
    payment_preference = models.CharField(max_length=18, default='DIGITAL')
    delivery_address = models.ForeignKey(DeliveryAddress, null=True, on_delete=models.CASCADE)


class CartProduct(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    variant = models.ForeignKey('catalog.ProductVariant', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class OrderPayment(TimeStampedModel):
    bill_total = models.DecimalField(decimal_places=4, max_digits=16)
    discount = models.DecimalField(decimal_places=4, max_digits=16, default=0)
    amount_payable = models.DecimalField(decimal_places=4, max_digits=16)
    amount_paid = models.DecimalField(decimal_places=4, max_digits=16, default=0)
    amount_refunded = models.DecimalField(decimal_places=4, max_digits=16, default=0)
    refund_in_process = models.DecimalField(decimal_places=4, max_digits=16, default=0)
    mode = models.CharField(default='CASH', max_length=32)
    status = models.CharField(default='PENDING', max_length=32)


class Order(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    customer = models.ForeignKey("customer.Customer", on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=256, default='PENDING')
    payment = models.ForeignKey(OrderPayment, on_delete=models.CASCADE) 
    delivery_address = models.TextField(default='{}')


class OrderProduct(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    variant = models.ForeignKey('catalog.ProductVariant', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    selling_price = models.DecimalField(decimal_places=4, max_digits=16)
    status = models.CharField(max_length=256, default='UNALTERED')
