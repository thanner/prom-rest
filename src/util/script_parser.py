import werkzeug
from flask_restx import reqparse


def param_parser(value):
    # param_schema = {'type': 'list',
    #                 'schema':
    #                     {
    #                         'name': {'required': True, 'type': 'string'},
    #                         'description': {'required': True, 'type': 'string'},
    #                         'document_type': {'required': True, 'type': 'string'}
    #                     }
    #                 }
    #
    # v = Validator(param_schema)
    # if v.validate(value):
    #     return value
    # else:
    #     raise ValueError(json.dumps(v.errors))
    return value


script_parser = reqparse.RequestParser()
script_parser.add_argument('name', location='form', required=True)
script_parser.add_argument('description', location='form')
script_parser.add_argument('source_code',
                           type=werkzeug.datastructures.FileStorage,
                           location='files',
                           required=True,
                           help='Script to update',
                           )

script_parser.add_argument('params', type=param_parser, location='form', action='append',
                           help='{"name": "@xesLog", "description": "Log received", "expectedType": "xes"}', )
