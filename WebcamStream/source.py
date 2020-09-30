from flask import Flask
from flask_restful import Api
from WebcamStream.webcam_resource import StreamResource

# Flask setup
app = Flask(__name__)
api = Api(app)

# Register Resources
api.add_resource(StreamResource, "/webcam/<string:function>")

# Run Flask Server, if invoked on this module; on debug mode
if __name__ == "__main__":
    app.run(debug=True)
