from flask_restx import Resource, fields

from src.service import param_service as service
from src.swagger import api
from src.util.param_parser import param_parser

ns = api.namespace("params", description="Param related operations")

param_projection_model = api.model("Param Projection", {
    "name": fields.String(required=True, description="Param name"),
    "description": fields.String(required=True, description="Param value"),
    "type": fields.String(required=True, description="Param type"),
})

param_model = api.inherit("Param", param_projection_model, {
    "data": fields.String(required=True, description="The param data"),
})


@ns.route("/<param_name>")
@ns.response(200, "Success")
@ns.response(404, "Param not found")
@api.doc(params={"param_name": "Unique param identifier"})
class ParamController(Resource):

    @ns.marshal_with(param_model)
    def get(self, param_name):
        """Get a param given its identifier"""
        return service.find_param(param_name)

    @ns.response(204, "Param deleted")
    def delete(self, param_name):
        """Delete a param given its identifier"""
        return service.remove_param(param_name)


@ns.route("/")
@ns.response(200, "Success")
@ns.response(404, "Param not found")
class ParamsController(Resource):

    @ns.marshal_with(param_projection_model)
    def get(self):
        """Get all params"""
        return service.find_all_params()

    @ns.expect(param_parser, validate=True)
    def post(self):
        """Create a param given its identifier"""
        args = param_parser.parse_args()

        data = args["data"]

        param = {"name": args["name"],
                 "description": args["description"],
                 "type": args["type"],
                 "data": data.read().decode("utf-8")}
        return {"Param Id": service.insert_param(param)}
