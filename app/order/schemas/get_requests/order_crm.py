from marshmallow import Schema, fields


class OrderListRequestSchema(Schema):
    page = fields.Integer(default=1)
    limit = fields.Integer(default=10)
    start_date = fields.Integer(data_key="startDate")
    end_date = fields.Integer(data_key="endDate")
    phone_number = fields.String(data_key="phoneNumber")
    order_id = fields.Integer(data_key="orderId")
    delivery_status = fields.String(data_key="deliveryStatus")
    