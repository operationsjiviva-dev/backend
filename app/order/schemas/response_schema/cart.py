from marshmallow import fields, Schema, pre_dump


class CartProductResponseSchema(Schema):
    class Meta:
        ordered = True

    product_id = fields.Integer(data_key="productId")
    variant_id = fields.Integer(data_key="variantId")
    quantity = fields.Integer(data_key="quantity")
    selling_price = fields.Float(data_key="sellingPrice", attribute="variant.selling_price")
    image = fields.String(data_key="image", attribute="product.primary_image")
    name = fields.String(data_key="name", attribute="product.name")
    size = fields.String(data_key="size", attribute="variant.size")


class CartResponseSchema(Schema):
    class Meta:
        ordered = True
    
    cart_id = fields.Integer(data_key="cartId")
    cart_products = fields.Nested(CartProductResponseSchema(many=True), data_key="cartProducts")
    delivery_address = fields.Dict(data_key="deliveryAddress")
    payment_preference = fields.String(data_key="paymentPreference")
    total_bill = fields.Float(data_key="totalBill")
