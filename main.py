import json
import os
import pymongo

from bson import json_util
from flask import Flask, request, Response, render_template, jsonify
from requests import post
from aylienapiclient import textapi

APP_ID = None
APP_KEY = None

if not APP_KEY or not APP_ID:
    print "Please specify APP_KEY and APP_ID for the Aylien client"
    exit()

AYLIEN_CLIENT = textapi.Client(APP_ID, APP_KEY)

app = Flask(__name__,
            template_folder='frontend')

# Set up mongo client and collections
CLIENT = pymongo.MongoClient()
DB = CLIENT['local']
RESULTS = DB['results']
RESULTS.ensure_index('url')

# Determine `pwd` of this executing file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/extract", methods=['GET', 'POST'])
def extract():
    url = request.args.get('url')
    callback_url = request.args.get('callback')

    if request.method == 'GET':
        result = RESULTS.find_one({'url': url})

        if not result:
            return render_template('error.html'), 404

        result.pop('_id')  # not particularly useful to the client

        return Response(json.dumps(result, default=json_util.default),
                        mimetype='application/json')

    elif request.method == 'POST':
        try:
            result = AYLIEN_CLIENT.Extract({"url": url})
        except:
            return "URL is invalid", 400

        result['url'] = url
        RESULTS.update({'url': url}, result, upsert=True)

        if callback_url:
            try:
                post(callback_url, result)  # send POST request to callback URL with result as JSON body
            except:
                return "Callback URL is invalid", 400

        return jsonify(**result)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5000')
