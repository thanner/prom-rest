from flask import jsonify, request, Blueprint
from flask_restx import Resource, fields

from src.service.prom_service import execute_commands, execute_command
from src.swagger import api

ns = api.namespace("prom", description="ProM related operations")

prom_blueprint = Blueprint('prom_blueprint', __name__)


@ns.route('/plugins')
@ns.response(200, 'Success')
@ns.response(404, 'Script not found')
class PromPluginsController(Resource):

    def get(self):
        """
        List all plugins (name, inputs and outputs)
        """
        try:
            command = "-l"
            outputs = execute_command(command)
            return jsonify(outputs)
        except Exception as e:
            return str(e)


command_model = api.model("Command", {
    'commands': fields.List(fields.String(required=True, description='Command')),
})


@ns.route('/commands')
@ns.response(200, 'Success')
@ns.response(404, 'Script not found')
class PromCommandsController(Resource):

    @ns.expect(command_model, validate=True)
    def post(self):
        """
        Execute a generic command in ProM
        """
        try:
            body = request.get_json()
            commands = body["commands"]
            outputs = execute_commands(commands)
            return jsonify(outputs)
        except Exception as e:
            return str(e)
