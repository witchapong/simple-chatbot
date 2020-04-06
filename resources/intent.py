from flask_restful import Resource
from models.intent import IntentModel


class Intent(Resource):
    model = IntentModel
    def get(self, value):
        model_obj = self.model.find_by_value(value)
        if model_obj:
            return model_obj.json()
        return {'message':'Intent not found'}, 404

    def post(self, value):
        if self.model.find_by_value(value):
            return {'message': "An intent with value '{}' already exists".format(value)}, 400

        model_obj = self.model(value)
        try:
            model_obj.save_to_db()
        except:
            return {'message': "An error occurred creating the intent."}, 500

        return model_obj.json(), 201

    def delete(self, value):
        model_obj = self.model.find_by_value(value)
        if model_obj:
            model_obj.delete_from_db()

        return {'message': "Intent deleted"}


class IntentList(Resource):
    model = IntentModel
    def get(self):
        return {'intents': list(map(lambda x: x.json(), self.model.query.all()))}