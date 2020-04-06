from db import db


class IntentModel(db.Model):
    __tablename__ = 'intents'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100))

    responses = db.relationship('ResponseModel', lazy='dynamic')
    phrases = db.relationship('PhraseModel', lazy='dynamic')

    def __init__(self, value):
        self.value = value

    def json(self):
        return {'id':self.id ,
        'value':self.value,
        'responses': [response.json() for response in self.responses.all()],
        'phrases': [phrase.json() for phrase in self.phrases.all()]
        }

    @classmethod
    def find_by_value(cls, value):
        return cls.query.filter_by(value=value).first()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()