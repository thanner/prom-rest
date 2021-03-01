import werkzeug
from flask_restx import reqparse


def param_parser(value):
    return value


script_execution_parser = reqparse.RequestParser()

# script_execution_parser.add_argument('param_input',
#                                      type=werkzeug.datastructures.FileStorage,
#                                      location='files',
#                                      action='append',
#                                      help='Param to input',
#                                      )

script_execution_parser.add_argument("images",
                                     type=werkzeug.datastructures.FileStorage,
                                     location="files",
                                     required=True,
                                     help="Person images",
                                     action='append')

# script_execution_parser.add_argument('params', type=param_parser, location='form', action='append',
#                                      help='{"filename": "log.xes", "param_name": "@xeslog"}', )
