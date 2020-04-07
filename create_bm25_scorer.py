# TO DO
# 1. fetch all phrases
# 2. create bm25 scorer from phrases
# 3. save scorer
# from app import create_app
# app = create_app()
# app.app_context().push()
import os
from models.phrase import PhraseModel
from pythainlp.tokenize import word_tokenize
from gensim.summarization.bm25 import BM25
import pickle

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
    os.makedirs('./scorer',exist_ok=True)
    pickle.dump(bm25_scorer, open('./scorer/bm25_scorer.pkl','wb'))
    pickle.dump(itoid, open('./scorer/itoid.pkl','wb'))

if __name__ == '__main__':
    create_scorer()