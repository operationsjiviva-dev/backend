from marshmallow import Schema, fields


class filterBySchema(Schema):
    key = fields.Str(data_key="key")
    values = fields.List(fields.Str(), data_key="values")


class CustomerProductListingGetSchema(Schema):
    page = fields.Int(default=1, data_key="page")
    limit = fields.Int(default=10, data_key="limit")
    collections = fields.Str(data_key="collections")
    categories = fields.Str(data_key="categories")
    occasions = fields.Str(data_key="occasions")
    tags = fields.Str(data_key="tags")
    sort_by = fields.List(fields.Str(), data_key="sortBy")
    filter_by = fields.Dict(keys=fields.Str(), values=fields.List(fields.Str()), data_key="filterBy")