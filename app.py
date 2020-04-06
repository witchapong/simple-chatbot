import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from resources.intent import Intent, IntentList
from resources.response import Response
from resources.phrase import Phrase, FitPhrases
from resources.chat import Chat
from resources.user import UserRegister

# jwt = JWT(app ,authenticate, identity)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.secret_key = 'mick'

    db.init_app(app)
    return app

def create_api(app):
    api = Api(app)
    api.add_resource(Intent, '/intent/<string:value>')
    api.add_resource(IntentList, '/intents')
    api.add_resource(Response, '/response')
    api.add_resource(Phrase, '/phrase')
    api.add_resource(Chat, '/chat')
    api.add_resource(FitPhrases,'/fit_phrases')
    api.add_resource(UserRegister, '/register')

app = create_app()
create_api(app)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app = create_app()
    create_api(app)

    @app.before_first_request
    def create_tables():
        db.create_all()
    
    app.run(port=5000, debug=True)