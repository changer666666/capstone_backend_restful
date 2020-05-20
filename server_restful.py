from flask import Flask, request, flash, redirect, url_for
from flask_restful import Resource, Api
from flask_cors import CORS
import altair as alt
import pandas as pd
import os
import json
import boto3

myPath = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
api = Api(app)
CORS(app)
app.secret_key = 'testkey'

list = {}

def read_file_from_cloud(bucket, filename):
    s3 = boto3.resource('s3',
                        aws_access_key_id='AKIAI3UJLE5E54WROCRA',
                        aws_secret_access_key='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')
    content_object = s3.Object(bucket, filename)
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    return json_content

def getChart(filename):
    onStateRes = calculate_data.calculate_data(filename)
    chart = alt.Chart(onStateRes, width=400, height=200).mark_line(point=True).encode(
        x='Time:T',
        y='ONStateRES:Q',
        tooltip=['Time', 'ONStateRES']
    ).configure_axis(
        labelColor='gray',
        titleColor='gray'
    ).interactive()
    return chart

class TestRun(Resource):
    """
    You can try this example as follow:
        $ curl http://localhost:5000/test -d "data=MOSFET#1" -X PUT
        $ curl http://localhost:5000/test
        {"test": "MOSFET#1"}
    """
    def get(self, list_id):
        return {list_id: list[list_id]}

    def put(self, list_id):
        list[list_id] = request.form['data']
        print(list[list_id])
        return {list_id: list[list_id]}

api.add_resource(TestRun, '/<string:list_id>')

if __name__ == '__main__':
    app.run(debug=True)


