from flask_restx import Namespace

from background_noise_removal.improve_audio import views as bg_views

imporve_audio_ns = Namespace("Improve_Audio", path="/improve_audio")
imporve_audio_ns.add_resource(bg_views.ImproveAudio, "")
