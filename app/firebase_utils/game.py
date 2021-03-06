from .user import crud_user

from time import sleep

class Game():

    # Creating new game and intializing room_key
    def create_new_game(self, db, data):
        new_game = db.child('game').push(data)
        return new_game
    
    def add_solved(self, db, room_key):
        counter = db.child('game').child(room_key).child('solved_n').get().val()
        db.child('game').child(room_key).update({"solved_n": counter + 1 })
    
    def check_game_status(self, db, room_key):
        """
        Function to check if every player finished the game.

        Preparing the players data for "payouts" firebase collection ,
        so that collection can be consued by flask scheduler and paypal
        payout system in order to payout the players that have earned
        gain while playing the game.
        """
        max_players = db.child('game').child(room_key).child('max_players').get().val()
        counter = db.child('game').child(room_key).child('solved_n').get().val()
        n_losers = db.child('game').child(room_key).child('n_losers').get().val()

        # The amount of players that will lose the game.
        player_cutoff = max_players - n_losers
        
        payouts = []

        # Function to expel the players that might have been inactive from the begging 
        # and preventing the game to get closed.
        # Ideal solution for this problem would be implementing time based games.
        if max_players >= 5 and counter >= player_cutoff:
            db.child('game').child(room_key).update({'status': 'CLOSED'})
            players = db.child('game').child(room_key).child('players').shallow().get()

            for keys in players.val():
                player = db.child('game').child(room_key).child('players').child(keys).get().val()

                # Checking for players that still didnt finish game or participate at all.
                # end_time is indicator for it.
                if not player.get('end_time') :
                    crud_user.expel_player(keys)
            
            # Query once again to get updated player models with that contain 'earning'
            for keys in players.val():
                player = db.child('game').child(room_key).child('players').child(keys).get().val()

                if not player['earning'] <= 0:
                    player = player['earning'], player['payment']
                    payouts.append(player)

                
        elif counter >= max_players:
            db.child('game').child(room_key).update({'status': 'CLOSED'})

            # Preparing data for separated firebase collection "payouts"
            players = db.child('game').child(room_key).child('players').shallow().get()
            for keys in players.val():
                player = db.child('game').child(room_key).child('players').child(keys).get().val()
                # Limiting the collection of data only for players that earned gain
                if not player['earning'] <= 0:
                    player = player['earning'], player['payment']
                    payouts.append(player)
                
        payout_obj = {
                'payouts': payouts,
                'closed': False
                }
        
        if len(payouts) != 0:
            db.child('payouts').push(payout_obj)


crud_game = Game()
        