from flask_restful import Api
from main import app

from api import routes

#app = Flask(__name__)
api = Api(app)
#mysql = DBConfig.config(app)

routes(api)

if __name__ == "__main__":
    app.run(debug=True)