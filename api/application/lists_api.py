from flask_restful import Resource, Api
from flask_restful import fields, marshal
from flask_restful import reqparse
from application.models import List
from application.database import db
from flask import current_app as app
from flask_security import auth_token_required, current_user
import json

from application.cache import cache


card_resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'created_at': fields.String,
    'completed': fields.Boolean,
    'list_id': fields.Integer,
    'deadline': fields.DateTime,
    'completed_at': fields.DateTime
}

list_resource_fields = {
    'id': fields.Integer,
    'user_id':   fields.Integer,
    'title':    fields.String,
    'description': fields.String,
    'cards': fields.List(fields.Nested(card_resource_fields))
}


class ListsAPI(Resource):
    @auth_token_required
    @cache.memoize(timeout=40)
    def get(self):

        # Current User's ID
        current_user_id = current_user.id

        # Get all the lists with user_id as current_user_id
        lists = List.query.filter_by(user_id=current_user_id).all()

        # return marshal(list, list_resource_fields)

        lists_ = []

        for i in lists:
            print(i.cards)
            lists_.append(marshal(i, list_resource_fields))

            # print(i.cards)

        return lists_
