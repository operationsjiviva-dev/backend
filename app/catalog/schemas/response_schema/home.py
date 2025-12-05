from marshmallow import fields, Schema, pre_dump


class CollectionSchema(Schema):
    id = fields.Int(data_key="id")
    fashion_line_id = fields.Int(data_key="fashionLineId")
    name = fields.Str(data_key="name")
    gender_id = fields.Int(data_key="genderId")


class CategorySchema(Schema):
    id = fields.Int(data_key="id")
    name = fields.Str(data_key="name")
    gender_id = fields.Int(data_key="genderId")

class OccasionSchema(Schema):
    id = fields.Int(data_key="id")
    name = fields.Str(data_key="name")
    gender_id = fields.Int(data_key="genderId")

class MenSubSchema(Schema):
    collections = fields.Nested(CollectionSchema(many=True), data_key="collections")
    categories = fields.Nested(CategorySchema(many=True), data_key="categories")
    occasions = fields.Nested(OccasionSchema(many=True), data_key="occasions")

class WomenSubSchema(Schema):
    collections = fields.Nested(CollectionSchema(many=True), data_key="collections")
    categories = fields.Nested(CategorySchema(many=True), data_key="categories")
    occasions = fields.Nested(OccasionSchema(many=True), data_key="occasions")

class filtersSubSchema(Schema):
    men = fields.Nested(MenSubSchema(), data_key="men")
    women = fields.Nested(WomenSubSchema(), data_key="women")
    collections = fields.Nested(CollectionSchema(many=True), data_key="collections")
    categories = fields.Nested(CategorySchema(many=True), data_key="categories")
    occasions = fields.Nested(OccasionSchema(many=True), data_key="occasions")


class CustomerHomeResponseSchema(Schema):
    top_collections = fields.Nested(CollectionSchema(many=True), data_key="topCollections")
    top_categories = fields.Nested(CategorySchema(many=True), data_key="topCategories")
    filters = fields.Nested(filtersSubSchema(), data_key="filters")