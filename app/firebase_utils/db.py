import pyrebase
import datetime


# Configuration goes here !!!
firebase_config = {
  "apiKey": "AIzaSyAqruys1IIGxdu9yOIIvxM6dAuPT_Y4Cic",
  "authDomain": "ponzi-b40a8.firebaseapp.com",
  "databaseURL": "https://ponzi-b40a8-default-rtdb.firebaseio.com",
  "projectId": "ponzi-b40a8",
  "storageBucket": "ponzi-b40a8.appspot.com",
  "messagingSenderId": "475670648946",
  "appId": "1:475670648946:web:70d30ab9a2dc86846a4aeb"

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
