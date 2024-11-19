import os
from flask import Flask

#create an instance of a flask app and indicating its location
app_path = os.path.dirname(__file__)
app = Flask(__name__)#, static_folder=app_path+'/static'
#creating a secret key for security
app.config['SECRET_KEY'] = 'ce61f6a09b3840c5a6a1e0bfe8aca300'
#locating the database in our directory
#db_path = os.path.join(os.path.dirname(__file__), 'Kanban.db')
#URI = 'sqlite:///{}'.format(db_path)
#app.config['SQLALCHEMY_DATABASE_URI'] = URI
#db = SQLAlchemy(app)

