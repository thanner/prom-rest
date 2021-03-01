from flask import Blueprint
from flask import Flask
from flask_pymongo import PyMongo

from src.swagger import api
from src.util import logger_utils

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/prom"
mongo = PyMongo(app)

logger = logger_utils.get_logger()

from src.controller import package_manager_controller, param_controller, prom_controller, script_controller

def initialize_server():
    api_blueprint = Blueprint('api', __name__, url_prefix='/prom')
    api.init_app(api_blueprint)
    api.add_namespace(package_manager_controller.ns)
    api.add_namespace(prom_controller.ns)
    api.add_namespace(param_controller.ns)
    api.add_namespace(script_controller.ns)
    app.register_blueprint(api_blueprint)
    logger.info("Swagger running on http://localhost:5000/prom")
    app.run()


if __name__ == '__main__' or __name__ == 'prom.app':
    initialize_server()
