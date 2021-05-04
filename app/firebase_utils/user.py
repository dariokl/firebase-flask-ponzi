from .db import db, player, data

class User():
    def __init__(self):
        self.user_key = None


    # This method should be moved to database class but that class is obsolete so far.
    def create_new_game(self, db):
        new_game = db.child('game').set(data)
        return new_game


    # Creating new user
    def create_new_user(self, db, email):
        allowed_players = db.child('game').child("allowed_players").get()
        if email and allowed_players.val() != 0:
            player['payment'] = email
            db.child('game').child('players').update({allowed_players.val(): player})
            db.child('game').update({'allowed_players': allowed_players.val() - 1})
            return True
        else:
            False

    # Main method in class ever since we use the session email to "authorize" the user.
    def current_user(self, db, email):
        player = db.child("game").child('players').order_by_child('payment').equal_to(email).get()
        if player:
            for data in player.each():
                self.user_key = data.key()
                return data.key()
        else:
            return False
        
    # Initialize the timer when the player makes first guess
    def set_timer(self, db,time):
        user_key = self.user_key
        check_timer = db.child('game').child('players').child(user_key).get()
        try:
            if check_timer.val()['start_time'] == 0 or check_timer['']:
                db.child('game').child('players').child(user_key).update({"start_time": time})
            else:
                return False
        except TypeError:
            return False


    # Set the timer once player makes the guess
    def end_timer(self, db, time):
        user_key = self.user_key
        start_timer = db.child('game').child('players').child(user_key).get()
        db.child('game').child('players').child(user_key).update({"end_time": time - start_timer.val()['start_time']})

    def set_position(self, db):
        # Return firebase object oredered by end_time property.
        timed_result = db.child('game').child('players').order_by_child('end_time').get()

        # Each time a player finish the game the final result will be updated based on timed_result query
        # Looping over every player and chanign the position based on new results in database.
        position = 1
        for player in timed_result.each():
            end_time =  db.child('game').child('players').child(player.key()).get()
            try:
                # Check if the player has ended his game.
                if end_time.val()['end_time']:
                    db.child('game').child('players').child(player.key()).update({'position': position})
                    position += 1
            except KeyError:
                pass


crud_user = User()