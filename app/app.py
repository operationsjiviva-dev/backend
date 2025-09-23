from flask import Flask
from flask_restx import Api
from flask_cors import CORS
import os
import django

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'app.settings'
)
django.setup()


# from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
CORS(app)

# csrf = CSRFProtect()
# csrf.init_app(app)

# app.register_blueprint(user_auth_blueprint)

api = Api(app)
# api.add_namespace(user_namespace)

# initialize_user_routes()


if __name__ == "__main__":
    env = os.getenv("ENVIRONMENT", "development")
    if env == "development":
        app.run(debug=True, port=5000)
    elif env == "production":
        app.run(host='0.0.0.0',debug=False, port=5000)