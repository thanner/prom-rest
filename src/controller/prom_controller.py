import os
import tempfile

from flask import jsonify, request, Blueprint

from src.service.prom_service import execute_commands, execute_command
from src.util.file_manager import get_template_plugin

prom_blueprint = Blueprint('prom_blueprint', __name__)


@prom_blueprint.route("/commands", methods=['POST'])
def execute_prom_commands():
    try:
        body = request.get_json()
        commands = body["commands"]
        outputs = execute_commands(commands)
        return jsonify(outputs)
    except Exception as e:
        return str(e)


@prom_blueprint.route("/installed-plugins", methods=['GET'])
def list_installed_plugins():
    try:
        command = "-l"
        outputs = execute_command(command)
        return jsonify(outputs)
    except Exception as e:
        return str(e)


@prom_blueprint.route("/execute-plugin/<plugin_name>", methods=['POST'])
def execute_plugin(plugin_name):
    try:
        # Recover params
        param_files = []
        for param_name in request.files:
            param_file = request.files[param_name]

            param_file_temp, param_filename_temp = tempfile.mkstemp(text=True,
                                                                    suffix=os.path.splitext(param_file.filename)[1])
            with os.fdopen(param_file_temp, 'w') as tmp:
                tmp.write(param_file.read().decode("utf-8"))

            param_files.append({"name": param_name, "filename": param_filename_temp})

        # Generate and execute template plugin
        template_content = get_template_plugin(plugin_name)

        for param_file in param_files:
            template_content = template_content.replace(param_file["name"], param_file["filename"])

        template_file, template_filename = tempfile.mkstemp(text=True, suffix=".txt")
        with os.fdopen(template_file, 'w') as tmp:
            tmp.write(template_content)

        command = f"-f {template_filename}"
        outputs = execute_command(command)
        return jsonify(outputs)
    except Exception as e:
        return str(e)
