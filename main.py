from flask import Flask, render_template, request
from google.cloud import datastore
import datetime
import json
import random
import requests
app = Flask(__name__)

datastore_client = datastore.Client()


def update_config(data):
    entity = datastore.Entity(key=datastore_client.key('config_data'))
    entity['created'] = datetime.datetime.now()
    entity['name'] = data['name']
    entity['props'] = json.dumps(data['data'], indent=4)
    # entity['props']['emailid'] = data['data']['emailid']
    # entity['props']['password'] = data['data']['password']
    # entity['props']['displayName'] = data['data']['displayName']
    # entity['props']['server'] = data['data']['server']
    datastore_client.put(entity)


def fetch_config(cursor=None):
    query = datastore_client.query(kind='config_data')
    # query.order = ['-update']
    data = query.fetch(start_cursor=cursor, limit=5)
    return data


def get_one_page_of_tasks(cursor=None):
    query = client.query(kind='Task')
    query_iter = query.fetch(start_cursor=cursor, limit=5)
    page = next(query_iter.pages)

    tasks = list(page)
    next_cursor = query_iter.next_page_token

    return tasks, next_cursor

@app.route("/", methods=['GET', 'POST'])
def index():
    if not request.args.get("update"):
        data = fetch_config(10)
        return render_template('index.html', data=data, json=json)
    else:
        names = json.loads(requests.get(
            "https://raw.githubusercontent.com/cyrilpillai/SuperHeroes/master/list.json").text)
        name = random.choice(names)['character_name']
        email = ''.join(e.lower() for e in name if e.isalnum())
        email = email+"@yopmail.com"
        password = random.randint(100000, 999999)
        data = {'name': name, 'data': {"emailid": email,
                                       "password": password, "displayName": name, "server": "gae"}}
        update_config(data)
        data = fetch_config(10)
        return render_template('index.html', data=data, json=json)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
