import tempfile

from flask import request, jsonify
from flask_restx import Resource, fields

from src.service import script_service as service
from src.service.prom_service import execute_command
from src.swagger import api
from src.util.file_manager import get_template_plugin

ns = api.namespace("scripts", description="Script related operations")

param_model = api.model('Param', {
    'name': fields.String(required=True, description='Param name'),
    'description': fields.String(required=True, description='Param value'),
    'type': fields.String(required=True, description='Param type'),
})

script_model = api.model('Script', {
    'name': fields.String(required=True, description='The script unique identifier'),
    'description': fields.String(required=True, description='The script description'),
    'source': fields.String(required=True, description='The source code'),
    'params': fields.List(fields.Nested(param_model, skip_none=True)),
})


@ns.route('/<script_name>')
@ns.response(200, 'Success')
@ns.response(404, 'Script not found')
@api.doc(params={"script_name": "Unique script identifier"})
class ScriptController(Resource):

    @ns.marshal_with(script_model)
    def get(self, script_name):
        """Get a script given its identifier"""
        return service.find_script(script_name)

    @ns.expect(script_model, validate=True)
    def put(self, script_name):
        """Update a script given its identifier"""
        script = request.get_json()
        service.update_script(script_name, script)

    @ns.response(204, 'Script deleted')
    def delete(self, script_name):
        """Delete a script given its identifier"""
        return service.remove_script(script_name)


@ns.route('/<script_name>/execute')
@ns.response(200, 'Success')
@ns.response(404, 'Script not found')
class ScriptExecutionController(Resource):

    def post(self, script_name):
        """
        Executes a script saved in the database
        """
        try:
            param_files = []
            for param_name in request.files:
                param_file = request.files[param_name]
                param_file_temp, param_filename_temp = tempfile.mkstemp(text=True,
                                                                        suffix=os.path.splitext(param_file.filename)[1])
                with os.fdopen(param_file_temp, 'w') as tmp:
                    tmp.write(param_file.read().decode("utf-8"))
                param_files.append({"name": param_name, "filename": param_filename_temp})

            template_content = get_template_plugin(script_name)
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


@ns.route('/')
@ns.response(200, 'Success')
@ns.response(404, 'Script not found')
class ScriptsController(Resource):

    @ns.marshal_with(script_model)
    def get(self):
        """Get all scripts"""
        return service.find_all_scripts()

    @ns.expect(script_model, validate=True)
    def post(self):
        """Create a script given its identifier"""
        script = request.get_json()
        return {"Script Id": service.insert_script(script)}
