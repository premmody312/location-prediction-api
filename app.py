from flask import Flask, render_template,jsonify, Response, request, redirect, json
import numpy as np
import pickle
import pandas as pd

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
        #print('Hello', 'World', 2+3, file=open('file.txt', 'w'))
        coord_dict = {}
        #if request.is_json() != None:
        coord_dict = request.get_json()
        print(f"Value received : {coord_dict}", file=open('location_log.txt', 'w'))
        temp_cord_dict = {}
        wifi_list = {}
        for row in coord_dict:
            for attribute, value in row.items():
                if attribute in wifi_list.keys():
                    temp_cord_dict[wifi_list[attribute]] = [value]

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
