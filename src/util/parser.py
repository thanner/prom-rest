import ast
import json


def parse_params(params):
    if params is None:
        return None
    param_obj = ast.literal_eval(params[0])

    if type(param_obj) == str:
        return list([json.loads(param_obj)])

    if type(param_obj) == tuple:
        params_list = []
        for param in param_obj:
            param_dict = json.loads(param)
            params_list.append(param_dict)
        return params_list

    return None
