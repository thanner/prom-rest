import os
import tempfile

from flask import request, jsonify
from flask_restx import Resource, fields

from src.service import script_service as service, param_service, prom_service
from src.swagger import api
from src.util import parser, script_parser
from src.util.script_parser import script_parser

ns = api.namespace("scripts", description="Script related operations")

param_model = api.model("param", {
    "name": fields.String(required=True, description="Param name"),
    "description": fields.String(required=True, description="Param value"),
    "type": fields.String(required=True, description="Param type"),
})

script_projection_model = api.model("script_projection", {
    "name": fields.String(required=True, description="The script unique identifier"),
    "description": fields.String(required=True, description="The script description"),
    "params": fields.List(fields.Nested(param_model, skip_none=True)),
})

script_model = api.inherit("script", script_projection_model, {
    "source_code": fields.String(required=True, description="The source code"),
})

param_transformation_model = api.model('param_transformation', {
    "name": fields.String(required=True, description="The param unique identifier"),
    "placeholder": fields.String(required=True, description="The script's param placeholder"),
})

param_transformations_model = api.model('param_transformations', {
    "params": fields.List(fields.Nested(param_transformation_model, skip_none=True)),
})


@ns.route("/<script_name>")
@ns.response(200, "Success")
@ns.response(404, "Script not found")
@api.doc(params={"script_name": "Unique script identifier"})
class ScriptController(Resource):

    @ns.marshal_with(script_model)
    def get(self, script_name):
        """Get a script given its identifier"""
        return service.find_script(script_name)

    @ns.response(204, "Script deleted")
    def delete(self, script_name):
        """Delete a script given its identifier"""
        return service.remove_script(script_name)


@ns.route("/")
@ns.response(200, "Success")
@ns.response(404, "Script not found")
class ScriptsController(Resource):

    @ns.marshal_with(script_projection_model)
    def get(self):
        """Get all scripts"""
        return service.find_all_scripts()

    @ns.expect(script_parser, validate=True)
    def post(self):
        """Create a script given its identifier"""
        args = script_parser.parse_args()

        params = parser.parse_params(args["params"])
        source_code = args["source_code"]

        script = {"name": args["name"],
                  "description": args["description"],
                  "params": params,
                  "source_code": source_code.read().decode("utf-8")}
        return {"Script Id": service.insert_script(script)}


@ns.route("/<script_name>/execute")
@ns.response(200, "Success")
@ns.response(404, "Script not found")
class ScriptExecutionController(Resource):

    @ns.expect(param_transformations_model)
    def post(self, script_name):
        """
        Executes a script saved in the database
        """
        try:
            body = request.get_json()
            params = body["params"]

            param_files = []
            for param in params:
                param_name = param["name"]
                param_base = param_service.find_param(param_name)
                param_file_temp, param_filename_temp = tempfile.mkstemp(text=True,
                                                                        suffix=os.path.splitext(param_name)[1])
                with os.fdopen(param_file_temp, "w") as tmp:
                    tmp.write(param_base["data"])
                param_files.append({"name": param["placeholder"], "filename": param_filename_temp})

            template_content = service.find_script(script_name)["source_code"]
            for param_file in param_files:
                template_content = template_content.replace(param_file["name"], param_file["filename"])
            template_file, template_filename = tempfile.mkstemp(text=True, suffix=".txt")
            with os.fdopen(template_file, "w") as tmp:
                tmp.write(template_content)

            command = f"-f {template_filename}"
            outputs = prom_service.execute_command(command)
            return jsonify(outputs)
        except Exception as e:
            return str(e)
