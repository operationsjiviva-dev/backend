from flask_restx import Resource
from django.db import connection
from flask import request


class CommonResource(Resource):

    def dispatch_request(self, *args, **kwargs):
        connection.connect()
        return super(CommonResource, self).dispatch_request(*args, **kwargs)
