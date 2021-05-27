import pyrebase
import datetime


# Configuration goes here !!!
firebase_config = {

}


player = {
    'start_time': 0,
    'end_time': None,
    "payment": '',
    "name": '',
    "position": None,
    "earning": 0,
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()
