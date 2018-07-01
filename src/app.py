from __future__ import absolute_import, print_function
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import requests
import oauth2
import tweepy
from time import gmtime,strftime
import os

# Get env 
DBIP = os.environ.get('DBIP')
DBPORT = os.environ.get('DBPORT')
DBURL = "http://" + str(DBIP) + ":" + str(DBPORT)
DBUSER = os.environ.get('DBUSER')
DBPASSWORD = os.environ.get('DBPASSWORD')

### DB init
from pyArango.connection import *
conn = Connection(arangoURL=DBURL, username=DBUSER, password=DBPASSWORD)

if not conn.hasDatabase("twitterapi"):
    db = conn.createDatabase("twitterapi")
else:
    db = conn["twitterapi"]

if not db.hasCollection('events'):
    collection = db.createCollection(name='events')
else:
    collection = db.collections['events']

app = Flask(__name__)
flaskapi = Api(app)
parser = reqparse.RequestParser()

CONSUMER_KEY = "consumer key"
CONSUMER_SECRET = "consumer secret"
ACCESS_TOKEN = "token"
ACCESS_SECRET = "secret"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

class Friendship(Resource):
    def get(self):
        parser.add_argument('user_a', type=str, help='Username', required=False)
        parser.add_argument('user_b', type=str, help='Username', required=False)
        args = parser.parse_args()
        user_a = args['user_a']
        user_b = args['user_b']

        status = api.show_friendship(source_id=user_a, target_id=user_b)

        event = collection.createDocument()
        event['timestamp'] = date = str(strftime("%Y/%m/%d %H:%M:%S", gmtime()))
        event['user_a'] = user_a
        event['user_b'] = user_b
        event['friendship'] = status[1].following
        event.save()

        print (event)

        return status[1].following

flaskapi.add_resource(Friendship, '/friendship')

@app.route('/friendship/<user_a>/<user_b>')
def get_status(user_a, user_b):
    status = api.show_friendship(source_id=user_a, target_id=user_b)
    return str(status[1].following)

@app.route('/proximity/<user_a>/<user_b>')
def get_proximity(user_a, user_b):
    followers_a = api.followers_ids(user_id=user_a)
    followers_b = api.followers_ids(user_id=user_b)
    proximity = collection.createDocument()
    proximity['timestamp'] = date = str(strftime("%Y/%m/%d %H:%M:%S", gmtime()))
    proximity['user_a'] = user_a
    proximity['user_b'] = user_b

    result = list(set(followers_a) & set(followers_b))
    proximity['proximity'] = len(result)
    proximity.save()

    return str(len(result))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
