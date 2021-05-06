import pyrebase


# Configuration goes here !!!
firebase_config = {

}


player = {
    'earned': 0,
    'start_time': 0,
    'end_time': None,
    'id' : '',
    'investment': "100",
    "payment": '',
    "position": None,
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()
