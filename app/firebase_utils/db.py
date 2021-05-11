import pyrebase
import datetime


# Configuration goes here !!!
firebase_config = {



}


player = {
    'earned': 0,
    'start_time': 0,
    'end_time': None,
    'investment': "100",
    "payment": '',
    "name": '',
    "position": None,
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()
