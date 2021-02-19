from flask import jsonify, request, Blueprint

from src.service.promService import execute_commands, execute_command

prom_blueprint = Blueprint('prom_blueprint', __name__)


@prom_blueprint.route("/commands", methods=['POST'])
def execute_prom_commands():
    body = request.get_json()
    commands = body["commands"]

    try:
        outputs = execute_commands(commands)
        return jsonify(outputs)
    except Exception as e:
        return str(e)


@prom_blueprint.route("/plugins", methods=['GET'])
def list_plugins():
    command = "-l"
    try:
        outputs = execute_command(command)
        return jsonify(outputs)
    except Exception as e:
        return str(e)
