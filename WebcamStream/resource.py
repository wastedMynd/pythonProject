from flask_restful import Resource
from WebcamStream.webcam import Streamer


class StreamResource(Resource):
    def get(self, function):
        if function == "capture":
            return {
                "request": function,
                "response": "ok",
                "stream": Streamer().get_captured_stream()
            }
        else:
            return {
                "request": function,
                "response": "not supported"
            }
