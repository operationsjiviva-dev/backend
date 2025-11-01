from catalog.namespaces.catalog_namespace import catalog_namespace
from catalog.blueprints.crm.product import ProductMetaAPI, ProductsAPI


def initialize_catalog_routes():
    catalog_namespace.add_resource(ProductMetaAPI, '/crm/product/meta')
    catalog_namespace.add_resource(ProductsAPI, '/crm/products')

