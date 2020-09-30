from flask import Flask
from flask_restful import Api
from Lottery.rest_flask_api.resource.common_game import CommonGameResources
from Lottery.rest_flask_api.resource.daily_lotto import DailyLotto

# Flask setup
app = Flask(__name__)
api = Api(app)

# Register Resources
api.add_resource(CommonGameResources, "/<string:game_name>/<string:function>")
api.add_resource(DailyLotto, "/daily_lotto/<string:function>")


def start_server(host="localhost", port=5000, debug=True):
    app.run(host=host, port=port, debug=debug)
    return app


# Run Flask Server, if invoked on this module; on debug mode
if __name__ == "__main__":
    start_server()
