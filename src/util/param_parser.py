import werkzeug
from flask_restx import reqparse

param_parser = reqparse.RequestParser()
param_parser.add_argument('name', location='form', required=True)
param_parser.add_argument('description', location='form')
param_parser.add_argument('type', location='form')
param_parser.add_argument('data',
                          type=werkzeug.datastructures.FileStorage,
                          location='files',
                          required=True,
                          help='Param to update',
                          )
