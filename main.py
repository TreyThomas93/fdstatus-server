from assets.multifilehandler import MultiFileHandler
from assets.extensions import mongo, bcrypt
from api.routes import api
from auth.routes import auth
from assets.timeformatter import Formatter
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import certifi
ca = certifi.where()

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

load_dotenv(dotenv_path="config.env")


def create_app():

    app = Flask(__name__)

    CORS(app)

    app.config["MONGO_URI"] = os.getenv('MONGO_URI')

    app.config["ENV"] = os.getenv('ENV')

    app.config["DEBUG"] = os.getenv('DEBUG')

    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

    mongo.init_app(app, tlsCAFile=ca)

    bcrypt.init_app(app)

    # setup logger only if not in debug mode
    if not app.debug:

        limiter = Limiter(app, key_func=get_remote_address)

        # 10 requests per minute allowed for all app/api extensions
        limiter.limit("10/minute")(api)

        # 5 requests per minute allowed for all app/auth extensions
        limiter.limit("5/minute")(auth)

        file_handler = MultiFileHandler(filename='logs/error.log', mode='a')

        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler.setFormatter(formatter)

        app.logger.addHandler(file_handler)

        limiter.logger.addHandler(file_handler)

    app.register_blueprint(api)

    app.register_blueprint(auth)

    return app


if __name__ == "__main__":

    app = create_app()

    app.run()
