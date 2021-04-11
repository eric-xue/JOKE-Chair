from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.exc import OperationalError
from backend.db import db


class TrainingData(db.Model):
    __tablename__ = "trainingdata"

    uid = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(TIMESTAMP, primary_key=True)
    sensor1 = db.Column(db.Integer)
    sensor2 = db.Column(db.Integer)
    sensor3 = db.Column(db.Integer)
    sensor4 = db.Column(db.Integer)
    sensor5 = db.Column(db.Integer)
    sensor6 = db.Column(db.Integer)
    sensor7 = db.Column(db.Integer)
    sensor8 = db.Column(db.Integer)
    classification = db.Column(db.String(32))

    def __init__(self, uid, timestamp, sensor1, sensor2, sensor3,
                 sensor4, sensor5, sensor6, sensor7, sensor8, classification):
        self.uid = uid
        self.timestamp = timestamp
        self.sensor1 = sensor1
        self.sensor2 = sensor2
        self.sensor3 = sensor3
        self.sensor4 = sensor4
        self.sensor5 = sensor5
        self.sensor6 = sensor6
        self.sensor7 = sensor7
        self.sensor8 = sensor8
        self.classification = classification

    def __repr__(self):
        return "<TrainingData(uid=%s, timestamp=%s, sensor1=%s, sensor2=%s, sensor3=%s, sensor4=%s" \
               ", sensor5=%s, sensor6=%s, sensor7=%s, sensor8=%s, classification=%s)>" % (self.uid, self.timestamp,
        self.sensor1, self.sensor2, self.sensor3, self.sensor4, self.sensor5, self.sensor6, self.sensor7, self.sensor8,
                                                                                          self.classification)
    def serialize(self):
        aggregate_sensors = [self.sensor1, self.sensor2, self.sensor3, self.sensor4, self.sensor5, self.sensor6,
                             self.sensor7, self.sensor8]
        payload = {
            "uid": self.uid,
            "timestamp": self.timestamp,
            "sensor": aggregate_sensors,
            "classification":self.classification
        }
        return payload


class UserDataModel(db.Model):
    __tablename__ = "userdatamodel"

    uid = db.Column(db.Integer, primary_key=True)
    datamodel = db.Column(db.TEXT(64))

    def __init__(self, uid, datamodel):
        self.uid = uid
        self.datamodel = datamodel

    def __repr__(self):
        return "<UserDataModel(uid=%s, datamodel=%s)>" % (self.uid, self.datamodel)


if __name__ == "__main__":
    try:
        db.engine.execute("DROP DATABASE posturechair;")
    except OperationalError:
        print("DB does not exist")
    db.engine.execute("CREATE DATABASE posturechair;")
    db.engine.execute("USE posturechair;")

    db.create_all()

