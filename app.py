from flask import Flask, render_template,jsonify, Response, request, redirect, json
import numpy as np
import pickle

app = Flask(__name__)

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
        location_dict = {'x': 0.0, 'y': 3.4}
        location_dict['x'] =  3.14
        location_dict['y'] =  5.67
        response = app.response_class(
            response=json.dumps(location_dict),
            status=200,
            mimetype='application/json'
        )
        return response
    return "Page Up and Working"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
