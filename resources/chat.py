from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from intent_classifier import get_intent
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
        intent_id = get_intent(payload['value'])

        # 2. get intent response
        model_obj = choice(ResponseModel.query.filter_by(intent_id=intent_id).all())

        return model_obj.json()