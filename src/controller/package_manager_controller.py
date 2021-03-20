from flask import jsonify, request
from flask_restx import Resource, fields

from src.service.package_manager_service import list_packages, install_packages, update_packages, \
    remove_packages, install_all_packages
from src.swagger import api

ns = api.namespace("packages", description="Package Manager related operations")

package_model = api.model('Package', {
    'packages': fields.List(fields.String(required=True, description='The package name')),
})


@ns.route('/')
@ns.response(200, 'Success')
@ns.response(404, 'Package not found')
class PackageController(Resource):

    def get(self):
        """Get all packages"""
        try:
            outputs = list_packages()
            return jsonify(outputs)
        except Exception as e:
            return str(e)

    @ns.expect(package_model, validate=True)
    def post(self):
        """Create packages given its identifiers"""
        try:
            body = request.get_json()
            packages = body["packages"]
            install_packages(packages)
            return 'OK'
        except Exception as e:
            return str(e)

    @ns.expect(package_model, validate=True)
    @ns.response(204, 'Package deleted')
    def delete(self):
        """Delete packages given its identifiers"""
        try:
            body = request.get_json()
            packages = body["packages"]
            remove_packages(packages)
            return 'OK'
        except Exception as e:
            return str(e)


@ns.route('/update')
@ns.response(200, 'Success')
@ns.response(404, 'Package not found')
class PackageUpdateController(Resource):
    def post(self):
        """Update all packages"""
        try:
            outputs = update_packages()
            return jsonify(outputs)
        except Exception as e:
            return str(e)

@ns.route('/install-all')
@ns.response(200, 'Success')
@ns.response(404, 'Package not found')
class PackageFullInstallController(Resource):
    def post(self):
        """Install all packages"""
        try:
            outputs = install_all_packages()
            return jsonify(outputs)
        except Exception as e:
            return str(e)
