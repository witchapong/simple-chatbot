import os
import pickle
from pythainlp.tokenize import word_tokenize
import pandas as pd

def get_intent(sentence):
    # load bm25 scorer & id mapper
    print('cwd:',os.getcwd())
    print('files in dir:',os.listdir())
    bm25_scorer = pickle.load(open('bm25_scorer.pkl','rb'))
    itoid = pickle.load(open('itoid.pkl','rb'))

    tokenized_sent = word_tokenize(sentence)
    scores = bm25_scorer.get_scores(tokenized_sent)
    return int(pd.DataFrame({'scores':scores, 'intent_id': itoid}).groupby('intent_id').sum().idxmax()['scores'])