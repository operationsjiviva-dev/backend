from catalog.namespaces.catalog_namespace import catalog_namespace
from catalog.blueprints.crm.bulkuploader import BulkUploadAPI, BulkUploadMetaDataAPI


def initialize_bulk_uploader_routes():
    catalog_namespace.add_resource(BulkUploadAPI, '/crm/bulk-uploader')
    catalog_namespace.add_resource(BulkUploadMetaDataAPI, '/crm/bulk-uploader/meta-data')