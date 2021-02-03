from flask import Flask, render_template,jsonify, Response, request, redirect, json, render_template_string
import numpy as np
import pickle
import pandas as pd
import requests
import json

app = Flask(__name__)
filename_x = "finalized_model_x.sav"
filename_y = "finalized_model_y.sav"
model_x = pickle.load(open(filename_x, 'rb'))
model_y = pickle.load(open(filename_y, 'rb'))



@app.route('/')
@app.route('/index')
def index():
    return "API hit. Wait for model to be added"

# @app.route('/model')
# def model():
@app.route('/getCoordinates', methods=['GET', 'POST'])
def getCoordinates():
    if request.method == 'POST':
        if request.get_json() != None:
            #print('Hello', 'World', 2+3, file=open('file.txt', 'w'))
            coord_dict = {}
            #if request.is_json() != None:
            print(f"Value received : {coord_dict}", file=open('location_log.txt', 'a'))
            print(f"Value received : {coord_dict}")
            coord_dict = json.loads(json.dumps(request.get_json()))
            #print(f"Value received : {coord_dict}", file=open('location_log.txt', 'a'))
            temp_cord_dict = {}
            wifi_list = {"Redmi Note X":"Router1", "Redmi Note X2":"Router2", "Redmi Note X3":"Router3"}
            #for row in json.dumps(coord_dict):
            #    print("Row:",row)
            #    for attribute, value in row.items():
            #        if attribute in wifi_list.keys():
            #            temp_cord_dict[wifi_list[attribute]] = [parseFloat(value)]
            for attribute, value in coord_dict.items():
                    if attribute in wifi_list.keys():
                        print("Value:",value)
                        temp_cord_dict[wifi_list[attribute]] = [float(value)]
            if not temp_cord_dict:
                coord_dict_pd = pd.DataFrame.from_dict(temp_cord_dict)
                location_dict = {'x': 0.0, 'y': 3.4}
                location_dict['x'] =  model_x.predict(coord_dict_pd)[0]
                location_dict['y'] =  model_y.predict(coord_dict_pd)[0]
                response = app.response_class(
                    response=json.dumps(location_dict),
                    status=200,
                    mimetype='application/json'
                )
                return response
    return "Page Up and Working"

@app.route("/localRequest")
def localRequest():
    url = 'https://location-classification-api.herokuapp.com/getCoordinates'
    myobj = {"Redmi Note X":1.6381444708152757,"Redmi Note X2":1.792622696531886,"Redmi Note X3":1.938144471,"tata":2.5381444708152756,"nilam@japs":2.5381444708152756}
    x = requests.post(url, json = json.dumps(myobj))
    return render_template_string(x.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
