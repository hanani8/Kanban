from flask_restful import Resource, Api
from flask_restful import fields, marshal
from flask_restful import reqparse
from application.models import Card
from application.database import db
from flask import current_app as app
from flask_security import auth_token_required, current_user
from datetime import datetime
from application.cache import cache

card_resource_fields = {
    'id': fields.Integer,
    'user_id':   fields.Integer,
    'list_id': fields.Integer,
    'title':    fields.String,
    'content': fields.String,
    'deadline': fields.String,
    'completed': fields.Boolean
}

create_card_parser = reqparse.RequestParser()
create_card_parser.add_argument('title')
create_card_parser.add_argument('content')
create_card_parser.add_argument('deadline')
create_card_parser.add_argument('list_id')
create_card_parser.add_argument('completed')


class CardAPI(Resource):
    @auth_token_required
    def post(self):
        args = create_card_parser.parse_args()

        title = args.get("title", None)

        content = args.get("content", None)

        deadline = args.get("deadline", None)

        list_id = int(args.get("list_id", 0))

        completed = args.get("completed", None)

        if title is None or content is None or deadline is None or list_id is None or completed is None:
            return "Incomplete Date", 400

        deadline_datetime = datetime.strptime(deadline, "%Y-%m-%d %H:%M")

        user_id = current_user.id  # current user

        completed_boolean = False

        if completed == "True":
            completed_boolean = True
        else:
            completed_boolean = False

        # Do all the validation
        if completed_boolean:
            new_card = Card(title=title, content=content,
                            deadline=deadline_datetime, list_id=list_id, user_id=user_id, completed=completed_boolean, completed_at=datetime.now())
        else:
            new_card = Card(title=title, content=content,
                            deadline=deadline_datetime, list_id=list_id, user_id=user_id, completed=completed_boolean)

        try:
            db.session.add(new_card)
            db.session.flush()
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Internal Server Error", 500

        db.session.commit()

        return marshal(new_card, card_resource_fields), 201

    @auth_token_required
    @cache.memoize(timeout=40)
    def get(self, id):
        current_user_id = current_user.id

        card = Card.query.filter_by(id=id, user_id=current_user_id).first()

        if card is None:
            return "No such list", 404
        else:
            return marshal(card, card_resource_fields)

    @auth_token_required
    def delete(self, id):
        current_user_id = current_user.id

        card = Card.query.filter_by(id=id, user_id=current_user_id).first()

        if card is None:
            return "No such list", 404

        else:
            try:
                db.session.delete(card)
                db.session.flush()
            except:
                db.session.rollback()
                return "Internal Server Error", 500
            db.session.commit()
            return "Card successfully deleted", 200

    @auth_token_required
    def put(self, id):

        current_user_id = current_user.id

        card = Card.query.filter_by(
            id=id, user_id=current_user_id).first()

        if card is None:
            return "No such card", 404

        else:
            args = create_card_parser.parse_args()

            title = args.get("title", None)

            content = args.get("content", None)

            deadline = args.get("deadline", None)

            if title is None or content is None or deadline is None:
                return "Incomplete Date", 400

            deadline_datetime = datetime.strptime(
                deadline, "%Y-%m-%d %H:%M:%S")

            card.title = title
            card.content = content
            card.deadline = deadline
            card.deadline = deadline_datetime

            try:
                db.session.add(card)
                db.session.flush()
            except:
                db.session.rollback()
                return "Internal Server Error", 500

            db.session.commit()

            return "Card successfully updated", 200

    @auth_token_required
    def patch(self, id):

        current_user_id = current_user.id

        card = Card.query.filter_by(
            id=id, user_id=current_user_id).first()

        if card is None:
            return "No such card", 404

        else:
            args = create_card_parser.parse_args()

            list_id = args.get("list_id", None)

            completed = args.get("completed", None)

            completed_boolean = False

            if completed == "True":
                completed_boolean = True
            else:
                completed_boolean = False

            if list_id is not None:
                card.list_id = list_id
            if completed is not None:
                card.completed = completed_boolean
                if completed_boolean == True:
                    card.completed_at = datetime.now()

            try:
                db.session.add(card)
                db.session.flush()
            except:
                db.session.rollback()
                return "Internal Server Error", 500

            db.session.commit()

            return "Card successfully Patched", 200
