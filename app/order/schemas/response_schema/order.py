from marshmallow import fields, Schema, pre_dump


class PaymentOrderDetailsSchema(Schema):
    class Meta:
        ordered = True

    mode = fields.String(data_key="mode", default="CASH")
    status = fields.String(data_key="status", default="PENDING")
    bill_total = fields.Float(data_key="billTotal", default=0)
    discount = fields.Float(data_key="discount", default=0)
    amount_payable = fields.Float(data_key="amountPayable")
    amount_paid = fields.Float(data_key="amountPaid")
    amount_refunded = fields.Float(data_key="amountRefunded")
    refund_in_process = fields.Float(data_key="refundInProcess")


class OrderProductDetailsSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(data_key="OrderProductId", attribute="id")
    product_id = fields.Integer(data_key="productId", attribute="product.id")
    variant_id = fields.Integer(data_key="variantId", attribute="variant.id")
    quantity = fields.Integer(data_key="quantity")
    selling_price = fields.Float(data_key="sellingPrice")
    status = fields.String(data_key="status", default="UNALTERED")


class OrderDetailsResponseSchema(Schema):
    class Meta:
        ordered = True

    order_id = fields.Integer(data_key="orderId", attribute="id")
    delivery_status = fields.String(data_key="deliveryStatus")
    delivery_address = fields.Dict(data_key="deliveryAddress", default={})
    created_on = fields.DateTime(data_key="createdOn")
    modified_on = fields.DateTime(data_key="modifiedOn")
    payment = fields.Nested(PaymentOrderDetailsSchema())
    order_products = fields.Nested(OrderProductDetailsSchema(many=True), data_key="retailerProducts")
    product_count = fields.Int(data_key="productCount")


    @pre_dump
    def set_order_products(self, data, **kwargs):
        data.product_count = data.orderproduct_set.count()
        data.order_products = data.orderproduct_set.all()
        return data

