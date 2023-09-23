from flask import Flask
from flask_cors import CORS


ROOT_URL = '/api'


def create_app(config_name):
    from background_noise_removal.config import app_config

    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config["APPLICATION_ROOT"] = ROOT_URL
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    with app.app_context():
        from background_noise_removal.api_v1 import blueprint as api
        from background_noise_removal.healthcheck import healthcheck

        app.register_blueprint(api, url_prefix=ROOT_URL + '/v1.0/remove-noise')
        app.register_blueprint(healthcheck, url_prefix=ROOT_URL + '/version')
    return app
