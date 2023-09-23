from flask import Blueprint, current_app
from flask_restx import Api

from background_noise_removal.improve_audio import imporve_audio_ns

blueprint = Blueprint('api_1_0', __name__)


api = Api(
    blueprint,
    doc=current_app.config['API_DOCS_URL'],
    catch_all_404s=True
)
api.namespaces.clear()
api.add_namespace(imporve_audio_ns)
