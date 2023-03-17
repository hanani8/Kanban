from flask import Response
import time
import requests
from application.card_api import CardAPI
from application.lists_api import ListsAPI
from application.list_api import ListAPI
from application import workers
from application import tasks
import os

from flask import Flask, render_template_string, make_response, request
from flask_security import Security, current_user, auth_token_required, hash_password, \
    SQLAlchemySessionUserDatastore
from application.database import db
from application.models import User, Role
from flask_restful import Api
from application.config import LocalDevelopmentConfig
from flask_cors import CORS

from application.cache import cache

app = None
api = None
celery = None


def create_app():
    # Create app
    app = Flask(__name__)

    app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)

    app.app_context().push()

    CORS(app)

    app.app_context().push()

    # Setup Flask-Security
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    app.security = Security(app, user_datastore)

    api = Api(app)
    app.api = api
    app.app_context().push()

    celery = workers.celery
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND']
    )

    celery.Task = workers.ContextTask
    app.app_context().push()

    return app, api, celery


app, api, celery = create_app()
cache.init_app(app)

# Views


@app.route("/api")
def home():
    return "API_OPERATIONAL", 200


@app.route("/api/isloggedin")
def getIsLoggedIn():
    if current_user.__class__.__name__ == "User":
        return {"logged_in": True}
    elif current_user.__class__.__name__ == "AnonymousUser":
        return {"logged_in": False}


URL = "http://localhost:5000/"


@app.route("/api/login", methods=["POST"])
def login():
    data = request.form.to_dict(flat=False)
    credentials = {
        "email": data['username'],
        "password": data['password']
    }

    result = requests.post(URL + "/login?include_auth_token", json=credentials)

    result_json = result.json()

    response = make_response(result_json)

    return response


@app.route("/api/login", methods=["OPTIONS"])
def login_options():

    return True


@app.route("/api/export/card/<card_id>", methods=["GET"])
def export_csv_card(card_id):
    job = tasks.export_card.delay(card_id, current_user.id)
    return str(job), 200


@app.route("/api/export/list/<list_id>", methods=["GET"])
def export_csv_list(list_id):
    job = tasks.export_list.delay(list_id, current_user.id)
    return str(job), 200


# def get_message():
#     # '''this could be any function that blocks until data is ready'''
#     time.sleep(5.0)
#     s = time.ctime(time.time())
#     return s


# @app.route('/stream')
# def stream():
#     def eventStream():
#         while True:
#             # wait for source data to be available, then push it
#             yield 'data: {}\n\n'.format(get_message())
#     return Response(eventStream(), mimetype="text/event-stream")


api.add_resource(ListAPI, "/api/list", "/api/list/<int:id>",
                 "/api/list/<int:id>", "/api/list/<int:id>")

api.add_resource(ListsAPI, "/api/lists")


api.add_resource(CardAPI, "/api/card", "/api/card/<int:id>",
                 "/api/card/<int:id>", "/api/card/<int:id>")


@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run("0.0.0.0")
