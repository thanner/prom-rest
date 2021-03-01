from index import mongo
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
        return str(collection.insert_one(script).inserted_id)


def update_script(script_name, script):
    script.pop('name', None)
    new_values = {"$set": script}
    return collection.update_one({"name": script_name}, new_values)
