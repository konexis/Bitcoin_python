import requests
from twilio.rest import Client
import os
from infos import *
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
account_sid = os.environ['ACCOUNT_SID ']
auth_token = os.environ['AUTH_TOKEN']
to_number = os.environ['TELEPHONE_NUMBER']

def send_whatsapp_msg(msg='hello world'):
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=msg, from_ ='whatsapp:+14155238886', to = to_number)
    return message.sid

@sched.scheduled_job('interval', seconds=10)
def get_last_bitcoin_price(target=65000):
    res = requests.get('https://www.mercadobitcoin.net/api/BTC/ticker/')
    last_price = float(res.json().get('ticker').get('last'))
    if last_price <= target:

        return send_whatsapp_msg(f'Price is good to buy. Bitcoin price now: {last_price}')

sched.start()
