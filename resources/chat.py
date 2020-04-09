from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import requests
from models.response import ResponseModel
from numpy.random import choice

class Chat(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('value',
        type=str,
        required=True,
        help="Sentence to send to chatbot agent cannot br empty."
        )

    def post(self):
        payload = self.__class__.parser.parse_args()
        # 1. get intent
        resp = requests.get(url="http://127.0.0.1:8080/intent_classifier",json=payload)
        intent_id = resp.json()['intent_id']

        # 2. get intent response
        model_obj = choice(ResponseModel.query.filter_by(intent_id=intent_id).all())

        return model_obj.json()