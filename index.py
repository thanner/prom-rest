from flask import Flask

from src.controller.package_manager_controller import package_manager_blueprint
from src.controller.prom_controller import prom_blueprint

app = Flask(__name__)
app.register_blueprint(prom_blueprint, url_prefix="/prom")
app.register_blueprint(package_manager_blueprint, url_prefix="/package-manager")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
