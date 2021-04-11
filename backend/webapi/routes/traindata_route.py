from flask import Blueprint, request, jsonify
from backend.repository.repository import TrainingDataRepository
from backend.db.model import TrainingData
traindata_routes = Blueprint('traindata_routes', __name__, url_prefix='/user')

TrainingDataRepository = TrainingDataRepository()

@traindata_routes.route('/get_traindata',methods=['GET'])
def get_usrdata():
    """
    INPUT: Takes arg request from url
    URL format example: http://127.0.0.1:5000/user/get_traindata?uid=1
        for user with uid = 1

    Output: Returns all readings of user with corresponding uid

    TODO: Add user verification so can only use associated uid and cant access other data through url.
    :return:
    """
    uid = request.args.get('uid')
    if uid is None:
        return jsonify({"error": "Missing request parameters"}), 400
    if not uid.isdigit():
        return jsonify({"error": "Invalid id"}), 400

    usr_data = TrainingDataRepository.retrieve_user_trainingdata(uid=uid)
    formatted_data = []
    for data in usr_data:
        formatted_data.append(data.serialize())
    return jsonify(formatted_data), 200


@traindata_routes.route('/add_traindata',methods=['POST'])
def add_usrdata():
    """
    INPUT: Takes POST request + json object.
    Json format
    {
        "uid": INT
        "timestamp": MYSQL format timestamp
        "sensor": Array of sensor readings
        "classification": Classification of posture
    }
    Inserts json info into database
    OUTPUT: Outputs created TrainingData entry with code 200

    :return:
    """
    data = request.get_json()
    uid = data["uid"]
    timestamp = data["timestamp"]
    sensor = data["sensors"]
    classif = data["classification"]

    list_length = len(uid)
    if all(len(x) == list_length for x in [uid, timestamp, sensor, classif]):
        created_data = []
        for element in range(list_length):
            train_dat = TrainingData(uid[element], timestamp[element], sensor[element][0], sensor[element][1],
                                     sensor[element][2], sensor[element][3], sensor[element][4]
                                     , sensor[element][5], sensor[element][6], sensor[element][7], classif[element])
            TrainingDataRepository.insert_user_trainingdata(train_dat)
            created_data += [train_dat]
        return jsonify(str(created_data)), 200
    else:
        return jsonify("Wrong length."), 400



    # train_dat = TrainingData(uid, timestamp, sensor[0], sensor[1], sensor[2], sensor[3], sensor[4]
    #                          , sensor[5], sensor[6], sensor[7], classif)
    # TrainingDataRepository.insert_user_trainingdata(train_dat)
    # return jsonify(str(train_dat)), 200

@traindata_routes.route('/',methods=['DELETE'])
def clear_usrdata():
    """
    INPUT: Takes DELETE REQUEST
    OUTPUT: Outputs small string confirming deletion of data
    :return:
    """
    uid = request.args.get('uid')
    TrainingDataRepository.clear_user_trainingdata(uid=uid)
    return jsonify("DATA CLEARED FOR " + str(uid)), 200