from .db import db, player


class User():
    def __init__(self):
        self.user_key = None
        self.room_key = None

    # Creating new user
    def create_new_user(self, db, email, name, room_key):
        allowed_players = db.child('game').child(
            room_key).child("allowed_players").get()
        if email and allowed_players.val() != 0:
            player['payment'] = email
            player['name'] = name
            db.child('game').child(room_key).child(
                'players').update({allowed_players.val(): player})
            db.child('game').child(room_key).update(
                {'allowed_players': allowed_players.val() - 1})
            return True
        else:
            False

    # Main method in class ever since we use the session email to "authorize" the user.
    def current_user(self, db, email, room_key):
        player = db.child("game").child(room_key).child(
            'players').order_by_child('payment').equal_to(email).get()
        if player:
            for data in player.each():
                self.user_key = data.key()
                self.room_key = room_key
                return data.key()
        else:
            return False

    # Initialize the timer when the player makes first guess
    def set_timer(self, db, time):
        user_key = self.user_key
        check_timer = db.child('game').child(
            self.room_key).child('players').child(user_key).get()
        try:
            if check_timer.val()['start_time'] == 0 or check_timer['']:
                db.child('game').child(self.room_key).child(
                    'players').child(user_key).update({"start_time": time})
            else:
                return False
        except TypeError:
            return False

    # Set the timer once player makes the guess

    def end_timer(self, db, time, failed=False):
        user_key = self.user_key
        start_timer = db.child('game').child(
            self.room_key).child('players').child(user_key).get()
        if failed != True:
            db.child('game').child(self.room_key).child('players').child(user_key).update(
                {"end_time": int(time - start_timer.val()['start_time'])})
        else:
            # This should be maximum time set for the game to be solved.
            db.child('game').child(self.room_key).child('players').child(user_key).update(
                {"end_time": 9999})


    def set_position(self, db, room_key):
        # Return firebase object oredered by end_time property.
        player_keys = db.child('game').child(
            room_key).child('players').shallow().get()
        gain = db.child('game').child(
            room_key).child('distribution').get()

        # Stroing every users key and time into a tumple
        results_list = []
        for keys in player_keys.val():
            player = db.child('game').child(room_key).child(
                'players').child(keys).get().val()
            # This is just a value inside the loop its not stored in firebase
            tup = keys, player.get('end_time', 9999999999999999999999999999999)
            results_list.append(tup)

        # Sorting a list by end time.
        sorted_by_time = sorted(results_list, key=lambda tup: tup[1])

        position = 1
        for player in sorted_by_time:
            db.child('game').child(room_key).child('players').child(
                player[0]).update({'position': position})
            self.distribute_gain(db, player[0], position, room_key)
            position += 1

    def distribute_gain(self, db, player_key, position, room_key):
        """
        Distribution function , even tough it looks pretty huge
        the purpouse of this function is pretty simple to compare
        key value from distribution with position of player and update
        the gain and earning property based on distribution value.
        """
        distribution = db.child('game').child(
            room_key).child('distribution').get()
        contribution = db.child('game').child(
            room_key).child('contribution').get()
        try:
            whole = contribution.val()
            part = distribution.val()[position]
            earning = int((part * whole)+whole)
            if earning > 0:
                db.child('game').child(room_key).child('players').child(
                    player_key).update({'gain': distribution.val()[position]})
                db.child('game').child(room_key).child('players').child(player_key).update(
                    {'earning': earning})
            else:
                db.child('game').child(room_key).child('players').child(
                    player_key).update({'gain': distribution.val()[position]})
                db.child('game').child(room_key).child('players').child(player_key).update(
                    {'earning': 0})

        except KeyError:
            db.child('game').child(room_key).child(
                'players').child(player_key).update({'gain': -1})


crud_user = User()
