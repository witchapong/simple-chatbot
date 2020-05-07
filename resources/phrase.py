from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.phrase import PhraseModel
from rq import Queue
from worker import conn
from create_bm25_scorer import create_scorer

class Phrase(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('value',
        type=str,
        required=True,
        help="Example phrase of corresponded intent cannot be empty."
        )
    post_parser.add_argument('intent_id',
        type=int,
        required=True,
        help="Corresponded intent_id cannot be empty."
        )

    parser = reqparse.RequestParser()
    parser.add_argument('value',
        type=str,
        required=True,
        help="Example phrase of corresponded intent cannot be empty."
        )

    model = PhraseModel

    def post(self):
        payload = self.__class__.post_parser.parse_args()
        if self.model.find_by_value(payload['value']):
            return {'message': "A phrase '{}' already exists.".format(payload['value'])}, 400

        model_obj = self.model(**payload)

        try:
            model_obj.save_to_db()
        except:
            return {'message':"An error occurred inserting the phrase."}, 500
        
        return model_obj.json(), 201

    def get(self):
        payload = self.__class__.parser.parse_args()
        model_obj = self.model.find_by_value(payload['value'])
        if model_obj:
            return model_obj.json()
        return {'message': "Phrase not found"}, 404

    def delete(self):
        payload = self.__class__.parser.parse_args()
        model_obj = self.model.find_by_value(payload['value'])
        if model_obj:
            model_obj.delete_from_db()
            return {'message':'Phrase deleted.'}
        return {'message','Phrase not found.'}, 404

class FitPhrases(Resource):
    def post(self):
        q = Queue(connection=conn)
        q.enqueue(create_scorer)
        return {'message':'FitPhrase resource called!'}