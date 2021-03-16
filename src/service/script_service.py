import os
import tempfile

from index import mongo
from src.service import param_service, prom_service
from src.util import logger_utils

collection = mongo.db["script"]
logger = logger_utils.get_logger()


def find_script(script_name):
    return collection.find_one_or_404({"name": script_name})


def find_all_scripts():
    return [script for script in collection.find({}, {"source_code": False})]


def remove_script(script_name):
    return collection.remove({"name": script_name})


def insert_script(script):
    if collection.find_one({"name": script["name"]}) is not None:
        return "Not Created"
    else:
        add_exit_script(script)
        return str(collection.insert_one(script).inserted_id)


def update_script(script_name, script):
    script.pop('name', None)
    new_values = {"$set": script}
    add_exit_script(script)
    return collection.update_one({"name": script_name}, new_values)


def get_file_params(request_file_params):
    file_params = []
    for request_file_param in request_file_params:
        param_name = request_file_param["file_param_id"]
        param_base = param_service.find_param(param_name)

        # Create file param temp file
        fd, path = tempfile.mkstemp(text=True, suffix=param_base['type'])
        with os.fdopen(fd, "w") as tmp:
            tmp.write(param_base["data"])

        file_params.append({"placeholder": request_file_param["placeholder"], "filename": path, "file": fd})

    return file_params


def create_script_template(script_name, var_params, file_params):
    # Replace in template content
    template_content = find_script(script_name)["source_code"]
    for var_param in var_params:
        template_content = template_content.replace(var_param["placeholder"], var_param["value"])
    for file_param in file_params:
        template_content = template_content.replace(file_param["placeholder"], file_param["filename"])

    # Create template content temp file
    fd, path = tempfile.mkstemp(text=True, suffix=".txt")
    with os.fdopen(fd, "w") as tmp:
        tmp.write(template_content)

    return path


def execute_script(script_name, var_params, request_file_params):
    file_params = get_file_params(request_file_params)
    template_filename = create_script_template(script_name, var_params, file_params)

    command = f"-f {template_filename}"
    return prom_service.execute_command(command)


def add_exit_script(script):
    script["source_code"] = "try {\n" + script[
        "source_code"] + "\n} catch (Exception e) {\n\tSystem.out.println(e);\n}" + "finally {\n\tSystem.exit(0);\n}"