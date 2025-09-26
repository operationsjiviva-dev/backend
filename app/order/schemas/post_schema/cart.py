from marshmallow import fields, Schema

class DeliveryAddressSchema(Schema):
    flat_number = fields.String(data_key="flatNumber")
    locality_name = fields.String(data_key="localityName", required=True)
    building_name = fields.String(data_key="buildingName", required=True)
    street_name = fields.String(data_key="streetName")
    address_text = fields.String(data_key="addressText", default="")
    pin_code = fields.String(data_key="pinCode", required=True)
    landmark = fields.String(default="")

class UpdateDeliveryAddressSchema(Schema):
    delivery_address = fields.Nested(DeliveryAddressSchema(), data_key="deliveryAddress")
    id = fields.Integer(data_key="deliveryAddressId", required=True)
