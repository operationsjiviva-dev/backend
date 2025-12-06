from catalog.namespaces.catalog_namespace import catalog_namespace
from catalog.blueprints.b2c.product_customer_blueprint import HomeAPI, CustomerProductListingAPI


def initialize_catalog_customer_routes():
    catalog_namespace.add_resource(HomeAPI, '/customer/home')
    catalog_namespace.add_resource(CustomerProductListingAPI, '/customer/products')
