from db import db


class PhraseModel(db.Model):
    __tablename__ = 'phrases'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(200))

    intent_id = db.Column(db.Integer, db.ForeignKey('intents.id'))
    intent = db.relationship('IntentModel')

    def __init__(self, value, intent_id):
        self.value = value
        self.intent_id = intent_id

    def json(self):
        return {'id':self.id,
        'value':self.value,
        'intent_id':self.intent_id}

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