import os
import pickle
from flask import Flask
from flask_restful import Api, Resource, reqparse
from pythainlp.tokenize import word_tokenize
import pandas as pd
import boto3

ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

# download from bucket to local
s3_resource = boto3.resource('s3')
print('Downloading from S3...')
s3_resource.Object(BUCKET_NAME, 'bm25_scorer.pkl').download_file(f'bm25_scorer.pkl')
s3_resource.Object(BUCKET_NAME, 'itoid.pkl').download_file(f'itoid.pkl')

# load from local
bm25_scorer = pickle.load(open('bm25_scorer.pkl','rb'))
itoid = pickle.load(open('itoid.pkl','rb'))
    
def get_intent(sentence):
    tokenized_sent = word_tokenize(sentence)
    scores = bm25_scorer.get_scores(tokenized_sent)
    return int(pd.DataFrame({'scores':scores, 'intent_id': itoid}).groupby('intent_id').sum().idxmax()['scores'])

def create_app():
    app = Flask(__name__)
    app.secret_key = 'mick'
    return app

def create_api(app):
    api = Api(app)
    api.add_resource(IntentClassifier, '/intent_classifier')

class IntentClassifier(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('value',
        type=str,
        required=True,
        help="Sentence to send to chatbot agent cannot be empty."
        )

    def get(self):
        payload = self.__class__.parser.parse_args()
        # 1. get intent
        intent_id = get_intent(payload['value'])

        return {'intent_id':intent_id}

if __name__ == "__main__":
    app = create_app()
    create_api(app)
    app.run(port=8080, debug=True)