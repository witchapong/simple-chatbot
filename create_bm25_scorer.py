# TO DO
# 1. fetch all phrases
# 2. create bm25 scorer from phrases
# 3. save scorer
# from app import create_app
# app = create_app()
# app.app_context().push()
import os
import requests
from models.phrase import PhraseModel
from pythainlp.tokenize import word_tokenize
from gensim.summarization.bm25 import BM25
import pickle
import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

def upload_to_aws(local_file, bucket, s3_file):
    s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    try:
        s3_resource.Object(bucket, local_file).upload_file(Filename=s3_file)
        print("Upload successfully...")
        return True
    except FileNotFoundError:
        print("File is not founded...")
        return False
    except NoCredentialsError:
        print("Credentials are not available...")
        return False  

def create_scorer():
    from app import create_app
    app = create_app()
    app.app_context().push()
    # 1. fetch all phrases
    phrases = list(map(lambda x: x.value, PhraseModel.query.all()))
    itoid = list(map(lambda x: x.intent_id, PhraseModel.query.all()))

    # 2. tokenize phrases
    tokenized_phrase = [word_tokenize(sent) for sent in phrases]

    # 3. initialise BM25 scorer
    bm25_scorer = BM25(tokenized_phrase)

    # 4. save scorer & corresponded intent id
    pickle.dump(bm25_scorer, open('bm25_scorer.pkl','wb'))
    pickle.dump(itoid, open('itoid.pkl','wb'))
    print('uploading to S3...')
    upload_to_aws(local_file='bm25_scorer.pkl', bucket=BUCKET_NAME, s3_file='bm25_scorer.pkl')
    upload_to_aws(local_file='itoid.pkl', bucket=BUCKET_NAME, s3_file='itoid.pkl')

    # 5. request intent classifier service to fetch weight from S3
    resp = requests.get(url='https://bm25-classifier-api.herokuapp.com/fetch_classifier')
    print(resp.json())

# for testing locally
if __name__ == '__main__':
    create_scorer()