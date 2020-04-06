from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.response import ResponseModel

class Response(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('value',
        type=str,
        required=True,
        help="Reponse of corresponded intent cannot be empty."
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
        help="Reponse of corresponded intent cannot be empty."
        )

    model = ResponseModel

    def post(self):
        payload = self.__class__.post_parser.parse_args()
        if self.model.find_by_value(payload['value']):
            return {'message': "A response '{}' already exists.".format(payload['value'])}, 400

        model_obj = self.model(**payload)

        try:
            model_obj.save_to_db()
        except:
            return {'message':"An error occurred inserting the response."}, 500
        
        return model_obj.json(), 201

    def get(self):
        payload = self.__class__.parser.parse_args()
        model_obj = self.model.find_by_value(payload['value'])
        if model_obj:
            return model_obj.json()
        return {'message': "Reponse not found"}, 404

    def delete(self):
        payload = self.__class__.parser.parse_args()
        model_obj = self.model.find_by_value(payload['value'])
        if model_obj:
            model_obj.delete_from_db()
            return {'message':'Response deleted.'}
        return {'message','Response not found.'}, 404