import pyrebase
import datetime


# Configuration goes here !!!
firebase_config = {

    "apiKey": "AIzaSyCulR0OlEN-dCRPxVsx16paDmbZef-x1gI",
    "authDomain": "test-90b1b.firebaseapp.com",
    "databaseURL": "https://test-90b1b-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "test-90b1b",
    "storageBucket": "test-90b1b.appspot.com",
    "messagingSenderId": "1085178731342",
    "appId": "1:1085178731342:web:56a11a11b07b25916fdc1f"

}


player = {
    'earned': 0,
    'start_time': 0,
    'end_time': None,
    'investment': "100",
    "payment": '',
    "position": None,
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()
