from marshmallow import Schema, fields


class GetProductMetaSchema(Schema):
    attribute_name = fields.Str(required=True, data_key="attributeName")
