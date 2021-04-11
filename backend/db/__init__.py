from flask_sqlalchemy import SQLAlchemy
from backend.webapi import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/posturechair'
app.config['MYSQL_DATABASE_PASSWORD'] = "123456"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)