from flask import Flask

from src.controller.promController import prom_blueprint

app = Flask(__name__)
app.register_blueprint(prom_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
