from flask import request, jsonify
from flask_restx import Resource, fields

from src.service import script_service as service
from src.swagger import api
from src.util import parser, script_parser
from src.util.script_parser import script_parser

ns = api.namespace("scripts", description="Script related operations")

param_model = api.model("param", {
    "name": fields.String(required=True, description="Param name"),
    "description": fields.String(required=True, description="Param description"),
    "expectedType": fields.String(required=True, description="Expected Param type"),
})

script_projection_model = api.model("script_projection", {
    "name": fields.String(required=True, description="The script unique identifier"),
    "description": fields.String(required=True, description="The script description"),
    "var_params": fields.List(fields.Nested(param_model, skip_none=True)),
    "file_params": fields.List(fields.Nested(param_model, skip_none=True)),
})

script_model = api.inherit("script", script_projection_model, {
    "source_code": fields.String(required=True, description="The source code"),
})

var_param_transformation_model = api.model('var_param_transformation', {
    "placeholder": fields.String(required=True, description="The script's param placeholder"),
    "value": fields.String(required=True, description="The param value"),
})

file_param_transformation_model = api.model('file_param_transformation', {
    "placeholder": fields.String(required=True, description="The script's param placeholder"),
    "file_param_id": fields.String(required=True, description="The file param unique identifier"),
})

param_transformations_model = api.model('param_transformations', {
    "var_params": fields.List(fields.Nested(var_param_transformation_model, skip_none=True)),
    "file_params": fields.List(fields.Nested(file_param_transformation_model, skip_none=True)),
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
            var_params = body["var_params"]
            request_file_params = body["file_params"]
            outputs = service.execute_script(script_name, var_params, request_file_params)
            return jsonify(outputs)
        except Exception as e:
            return str(e)
