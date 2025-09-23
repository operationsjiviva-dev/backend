from marshmallow import Schema, fields


class MetaDataSubSchema(Schema):
    collection_name = fields.String(data_key="collectionName")
    fashion_line_id = fields.Integer(data_key="fashionLineId")
    category_name = fields.String(data_key="categoryName")
    parent_category_id = fields.Integer(data_key="parentCategoryId")
    occasion_name = fields.String(data_key="occasionName")
    tag_name = fields.String(data_key="tagName")


class PostProductMetaSchema(Schema):
    attribute_name = fields.Str(required=True, data_key="attributeName")
    data = fields.Nested(MetaDataSubSchema(), data_key="flashSaleDiscounts")

