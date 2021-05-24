#from flask_apscheduler import APScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from app.firebase_utils.db import db

from datetime import datetime

from paypal_payout import payout


#def register_scheduler(app):


    # The body of payouts request , checking python paypal-checkouts-serversdk documation,
    # holds more information about the request body and details that should body cointain.
    #body = {
    #"sender_batch_header": {
    #    "recipient_type": "EMAIL",
    #    "email_message": "Generic message.",
    #    "note": "Enjoy your Payout!",
    #    "sender_batch_id": "",
    #    "email_subject": "Your Ponzi.com payout enjoy your earnings !"
    #},
    #"items": [],
    #}

    #scheduler = APScheduler()  # Use default scheduler: BackgroundScheduler
    #scheduler.init_app(app)
    #scheduler.start()




scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', id='do_db_payout', days=5)
def db_payout():
    """
    Scheduled payout function that will be ran on desired interval.
    Main focus of this task is to collect every object from firebase
    that has propery "closed" set to false wich means that payments
    for players in those collections are not issued.
    """
    body = {
    "sender_batch_header": {
        "recipient_type": "EMAIL",
        "email_message": "Generic message.",
        "note": "Enjoy your Payout!",
        "sender_batch_id": "",
        "email_subject": "Your Ponzi.com payout enjoy your earnings !"
    },
    "items": [],
    }
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    body['sender_batch_header']['sender_batch_id'] = date_time
    payouts = db.child('payouts').order_by_child('closed').equal_to(False).get()
     # Using counter for unique ides for every sender item
    id_count = 0
    for payout_obj in payouts.each():
        print(payout_obj.val()['closed'])
        for player_data in payout_obj.val()['payouts']:
            item_obj = {
                "note": f"Your Ponzi Payout!",
                "amount": {
                    "currency": "USD",
                    "value": ""
                },
                "receiver": "",
                "sender_item_id": ""
            }
            item_obj['amount']['value'] = player_data[0]
            item_obj['receiver'] = player_data[1]
            item_obj['sender_item_id'] = id_count
            id_count += 1
            body['items'].append(item_obj)

    payout(body)
    body['items'].clear()

    for payout_obj in payouts.each():
        game = db.child('payouts').child(payout_obj.key()).update({'closed':True})


    print('Payout task completed !')


scheduler.start()
