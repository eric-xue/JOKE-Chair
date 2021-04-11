from backend.webapi.routes.traindata_route import traindata_routes
from backend.webapi.routes.usermodel_route import usermodel_routes
from backend.webapi import app
from sqlalchemy import create_engine

app.register_blueprint(traindata_routes)
app.register_blueprint(usermodel_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)
