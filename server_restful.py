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
datasetList = [{'value': 'NASA_Ames_MOSFET_Data', 'label': 'NASA_Ames_MOSFET_Data'}]
testRunList = [{'value': 'MOSFET#1', 'label': 'Select...'},
               {'value': 'MOSFET#1', 'label': 'MOSFET#1'}, 
               {'value': 'MOSFET#2', 'label': 'MOSFET#2'}, 
               {'value': 'MOSFET#3', 'label': 'MOSFET#3'},
               {'value': 'MOSFET#4', 'label': 'MOSFET#4'},
               {'value': 'MOSFET#5', 'label': 'MOSFET#5'},
               {'value': 'MOSFET#6', 'label': 'MOSFET#6'},
               {'value': 'MOSFET#7', 'label': 'MOSFET#7'},
               {'value': 'MOSFET#8', 'label': 'MOSFET#8'},
               {'value': 'MOSFET#9', 'label': 'MOSFET#9'},
               {'value': 'MOSFET#10', 'label': 'MOSFET#10'},
               {'value': 'MOSFET#36', 'label': 'MOSFET#36'}]
parametersList = [{'value': 'Drain_Source_Resistance_Time', 'label': 'Drain_Source_Resistance_Time'}]

list['datasetOptions'] = {
    'datasetList': datasetList
}
list['testRunOptions'] = {
    'testRunList': testRunList
}
list['parametersOptions'] = {
    'parametersList': parametersList
}

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


