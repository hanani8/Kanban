from flask_restful import Resource, Api
from flask_restful import fields, marshal
from flask_restful import reqparse
from application.models import List
from application.database import db
from flask import current_app as app
from flask_security import auth_token_required, current_user
from application.cache import cache


list_resource_fields = {
    'id': fields.Integer,
    'user_id':   fields.Integer,
    'title':    fields.String,
    'description': fields.String
}

create_list_parser = reqparse.RequestParser()
create_list_parser.add_argument('title')
create_list_parser.add_argument('description')


class ListAPI(Resource):
    @auth_token_required
    def post(self):
        args = create_list_parser.parse_args()
        title = args.get("title", None)
        description = args.get("description", None)
        user_id = current_user.id  # current user

        # Do all the validation
        new_list = List(title=title, user_id=user_id, description=description)

        try:
            db.session.add(new_list)
            db.session.flush()
        except:
            db.session.rollback()
            return "Internal Server Error", 500

        db.session.commit()

        return marshal(new_list, list_resource_fields), 201

    @auth_token_required
    @cache.memoize(timeout=40)
    def get(self, id):
        current_user_id = current_user.id

        list = List.query.filter_by(id=id, user_id=current_user_id).first()

        if list is None:
            return "No such list", 404
        else:
            return marshal(list, list_resource_fields)

    @auth_token_required
    def delete(self, id):
        current_user_id = current_user.id

        list = List.query.filter_by(id=id, user_id=current_user_id).first()

        if list is None:
            return "No such list", 404

        else:
            try:
                db.session.delete(list)
                db.session.flush()
            except:
                db.session.rollback()
                return "Internal Server Error", 500
            db.session.commit()
            return "List successfully deleted", 200

    @auth_token_required
    def put(self, id):
        current_user_id = current_user.id

        list = List.query.filter_by(id=id, user_id=current_user_id).first()

        if list is None:
            return "No such list", 404

        else:
            args = create_list_parser.parse_args()

            title = args.get("title", None)
            description = args.get("description", None)

            if title is None:
                return "Can only update title in List", 400

            else:
                list.title = title

                if description is not None:
                    list.description = description

                try:
                    db.session.add(list)
                    db.session.flush()
                except:
                    db.session.rollback()

                db.session.commit()

                return "List successfully patched", 200
