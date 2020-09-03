from flask import Flask
from flask_restful import Api
from Lottery.rest_flask_api.resource.lotto import Lotto
from Lottery.rest_flask_api.resource.lotto_plus1 import LottoPlus1
from Lottery.rest_flask_api.resource.lotto_plus2 import LottoPlus2
from Lottery.rest_flask_api.resource.daily_lotto import DailyLotto
from Lottery.rest_flask_api.resource.powerball import PowerBall
from Lottery.rest_flask_api.resource.powerball_plus import PowerBallPlus

# Flask setup
app = Flask(__name__)
api = Api(app)

# Register Resources
api.add_resource(Lotto, "/lotto/<string:function>")
api.add_resource(LottoPlus1, "/lotto_plus1/<string:function>")
api.add_resource(LottoPlus2, "/lotto_plus2/<string:function>")
api.add_resource(DailyLotto, "/daily_lotto/<string:function>")
api.add_resource(PowerBall, "/powerball/<string:function>")
api.add_resource(PowerBallPlus, "/powerball_plus/<string:function>")

# Run Flask Server, if invoked on this module; on debug mode
if __name__ == "__main__":
    app.run(debug=True)
