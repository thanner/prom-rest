from flask import jsonify, Blueprint, request

from src.service.package_manager_service import list_packages, install_packages, update_packages, \
    remove_packages

package_manager_blueprint = Blueprint('package_manager_blueprint', __name__)


@package_manager_blueprint.route("/packages", methods=['GET'])
def get_packages():
    try:
        outputs = list_packages()
        return jsonify(outputs)
    except Exception as e:
        return str(e)


@package_manager_blueprint.route("/packages", methods=['PUT'])
def put_packages():
    try:
        outputs = update_packages()
        return jsonify(outputs)
    except Exception as e:
        return str(e)


@package_manager_blueprint.route("/packages", methods=['POST'])
def post_packages():
    try:
        body = request.get_json()
        packages = body["packages"]
        install_packages(packages)
        return 'OK'
    except Exception as e:
        return str(e)


@package_manager_blueprint.route("/packages", methods=['DELETE'])
def delete_packages():
    try:
        body = request.get_json()
        packages = body["packages"]
        remove_packages(packages)
        return 'OK'
    except Exception as e:
        return str(e)
