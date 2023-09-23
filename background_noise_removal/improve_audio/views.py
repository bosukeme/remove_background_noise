from flask_restx import Resource, Api
from flask import request
from background_noise_removal.swagger_util import upload_parser
# from sites_scrapper.swagger_doc import sales_parser

api = Api()


class ImproveAudio(Resource):

    @api.expect(upload_parser)
    def post(self):
        from background_noise_removal.improve_audio.services import start_noise_removing_script
        from background_noise_removal import Base

        logger = Base.logger_func()

        try:
            data = request.files

            input_file = data['file'].filename

            result = start_noise_removing_script(input_file)

            return result
        except Exception as reason:
            logger.exception(reason)
            return {
                "status": False,
                "message": str(reason),
                "data": {}
            }, 500
