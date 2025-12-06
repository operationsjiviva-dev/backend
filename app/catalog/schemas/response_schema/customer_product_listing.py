from marshmallow import fields, Schema, pre_dump
from catalog.miscellaneous_values.customer_product_listing import ProductSortByOptions

class ProductDetailsSchema(Schema):
    id = fields.Int(data_key="productId")
    display_name = fields.Str(data_key="name")
    primary_price = fields.Int(data_key="sellingPrice")
    primary_image = fields.Str(data_key="image")


class CustomerProductListingResponseSchema(Schema):
    products = fields.List(fields.Nested(ProductDetailsSchema), data_key="products")
    sort_by_options = fields.List(fields.Str(), data_key="sortByOptions")
    filters = fields.Dict(data_key="filters")


    @pre_dump
    def set_sort_by_options(self, data, **kwargs):
        data['sort_by_options'] = ProductSortByOptions.values()
        return data

    