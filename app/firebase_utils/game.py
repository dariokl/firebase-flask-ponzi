class Game():

    # Creating new game and intializing room_key
    def create_new_game(self, db, data):
        new_game = db.child('game').push(data)
        return new_game
    
    def add_solved(self, db, room_key):
        counter = db.child('game').child(room_key).child('solved_n').get().val()
        db.child('game').child(room_key).update({"solved_n": counter + 1 })
    
    def check_game_status(self, db, room_key):
        max_players = db.child('game').child(room_key).child('max_players').get().val()
        counter = db.child('game').child(room_key).child('solved_n').get().val()

        if counter >= max_players:
            db.child('game').child(room_key).update({'status': 'CLOSED'})
    

crud_game = Game()
        