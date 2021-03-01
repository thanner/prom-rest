from index import mongo
from src.util import logger_utils

collection = mongo.db["param"]
logger = logger_utils.get_logger()


def find_param(param_name):
    return collection.find_one_or_404({"name": param_name})


def find_all_params():
    return [param for param in collection.find({}, {"data": False})]


def remove_param(param_name):
    return collection.remove({"name": param_name})


def insert_param(param):
    if collection.find_one({"name": param["name"]}) is not None:
        return "Not Created"
    else:
        return str(collection.insert_one(param).inserted_id)


def update_param(param_name, param):
    param.pop('name', None)
    new_values = {"$set": param}
    return collection.update_one({"name": param_name}, new_values)
