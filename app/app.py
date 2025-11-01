from flask import Flask
from flask_restx import Api
from flask_cors import CORS
import os
import django
from flask_wtf.csrf import CSRFProtect

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'app.settings'
)
django.setup()


from catalog.namespaces.catalog_namespace import catalog_namespace


from catalog.blueprints.crm.bulkuploader import bulk_uploader_blueprint
from catalog.blueprints.crm.product import product_blueprint


from catalog.routes.catalog_crm_routes import initialize_catalog_routes
from catalog.routes.bulk_uploader_routes import initialize_bulk_uploader_routes



app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
CORS(app)

csrf = CSRFProtect()
csrf.init_app(app)

api = Api(app)

app.register_blueprint(bulk_uploader_blueprint)
app.register_blueprint(product_blueprint)

api.add_namespace(catalog_namespace)

initialize_catalog_routes()
initialize_bulk_uploader_routes()



if __name__ == "__main__":
    env = os.getenv("ENVIRONMENT", "development")
    if env == "development":
        app.run(debug=True, port=5000)
    elif env == "production":
        app.run(host='0.0.0.0',debug=False, port=5000)