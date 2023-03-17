from flask_restful import Resource, Api
from flask_restful import fields, marshal
from flask_restful import reqparse
from application.models import Card
from application.database import db
from flask import current_app as app
from flask_security import auth_token_required, current_user

# lists_resource_fields = {
#     'id': fields.Integer,
#     'user_id':   fields.Integer,
#     'title':    fields.String,
# }

class CardsAPI(Resource):
    @auth_token_required
    def get(self, list_id):

        # Current User's ID
        current_user_id = current_user.id

        # Get all the lists with user_id as current_user_id
        cards = Card.query.filter_by(list_id = list_id, user_id = current_user_id).all()

        # return marshal(list, list_resource_fields)

        return cards