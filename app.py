from flask import Flask, render_template,jsonify, Response, request, redirect, json, render_template_string
import numpy as np
import pickle
import pandas as pd
import requests
import json
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from os import environ

#import os
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./BigBoxStore-1e750ec615bc.json"


app = Flask(__name__)
#filename_x = "finalized_model_x.sav"
#filename_y = "finalized_model_y.sav"

filename_x = "finalized_model_x_cllg2.sav"
filename_y = "finalized_model_y_cllg2.sav"

model_x = pickle.load(open(filename_x, 'rb'))
model_y = pickle.load(open(filename_y, 'rb'))

ENV_KEYS = {
    "type": "service_account",
    "private_key_id": str(environ["FIREBASE_PRIVATE_KEY_ID"]),
    "private_key": str(environ["FIREBASE_PRIVATE_KEY"]).replace("\\n", "\n"),
    "client_email": str(environ["FIREBASE_CLIENT_EMAIL"]),
    "client_id": str(environ["FIREBASE_CLIENT_ID"]),
    "token_uri": str(environ["FIREBASE_TOKEN_URI"]),
    "auth_uri": str(environ["FIREBASE_AUTH_URI"]),
    "project_id": str(environ["FIREBASE_PROJECT_ID"]),
    "auth_provider_x509_cert_url": str("https://www.googleapis.com/oauth2/v1/certs"),
    "client_x509_cert_url": str(environ["FIREBASE_CLIENT_URI"])

}
print("ENV KEYS:", ENV_KEYS)
cred = credentials.Certificate(ENV_KEYS)
firebase_admin.initialize_app(cred)
db = firestore.client()



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
            location_dict = {'x': 662.0, 'y': 256.4}
            response = app.response_class(
                response=json.dumps(location_dict),
                status=200,
                mimetype='application/json'
            )
            coord_dict = {}
            #if request.is_json() != None:
            #Use for Android
            coord_dict = json.loads(json.dumps(request.get_json()))
            #Use for localRequest
            #coord_dict = json.loads(request.get_json())
            print(f"Value received : {coord_dict}", file=open('location_log.txt', 'a'))
            print(f"Value received : {coord_dict}")
            #print(f"Value received : {coord_dict}", file=open('location_log.txt', 'a'))
            temp_cord_dict = {}
            #wifi_list = {"Redmi Note X":"Router1", "Redmi Note X2":"Router2", "Redmi Note X3":"Router3"}
            #for row in json.dumps(coord_dict):
            #    print("Row:",row)
            #    for attribute, value in row.items():
            #        if attribute in wifi_list.keys():
            #            temp_cord_dict[wifi_list[attribute]] = [parseFloat(value)]
            #cols_of_interest = ['Isha', 'Efarm test', 'Redmi Note X2', 'Param', 'Param2', 'Lol 5']
            cols_of_interest = ['Isha', 'RedmiNoteX2', 'Param', 'PARAM2', 'Lol5', 'ASUS_X00PD','EfarmTest', 'Lol2']
            #Actual Name is the key, Feature Name of model is kwy
            wifi_list = {'Isha':'Isha', 'Efarm Test':'EfarmTest', 'Redmi Note X2': 'RedmiNoteX2', 'Param':'Param', 'PARAM2':'PARAM2', 'Lol 5':'Lol5', 'Lol 2.4':'Lol2', 'ASUS_X00PD': 'ASUS_X00PD'}
            for col in cols_of_interest:
                temp_cord_dict[col] = [float(2.7)]
            for attribute, value in coord_dict.items():
                    #if attribute in wifi_list.keys():
                    if attribute in wifi_list.keys():
                        print("Value:",value)
                        temp_cord_dict[wifi_list[attribute]] = [float(value)]
            if len(temp_cord_dict) !=0 and bool(temp_cord_dict):
                print(temp_cord_dict)
                coord_dict_pd = pd.DataFrame.from_dict(temp_cord_dict)
                location_dict = {'x': 0.0, 'y': 3.4}
                location_dict['x'] =  model_x.predict(coord_dict_pd)[0]
                location_dict['y'] =  model_y.predict(coord_dict_pd)[0]
                response = app.response_class(
                    response=json.dumps(location_dict),
                    status=200,
                    mimetype='application/json'
                )

                #firestore entry made here
                doc_ref = db.collection(u'People_In_Store').document(u""+str(coord_dict["email_json"]))
                doc_ref.set({
                    u"x":float(location_dict['x']),
                    u"y":float(location_dict['y'])
                })

                return response
    return "Page Up and Working"

@app.route("/localRequest")
def localRequest():
    url = 'https://location-classification-api.herokuapp.com/getCoordinates'
    #url = 'http://localhost:5000/getCoordinates'
    #myobj = {"Redmi Note X":1.6381444708152757,"Redmi Note X2":1.792622696531886,"Redmi Note X3":1.938144471,"tata":2.5381444708152756,"nilam@japs":2.5381444708152756}
    #myobj = {"SOMAIYA-WIFI":2.365709966975696,"SOMAIYA-GUEST":2.465709966975696,"Efarm Test":2.207329496997738,"Redmi Note X2":1.6837119514047025,"PARAM2":1.834594843519919,"Lol 5":1.5606702402547667,"Param":2.136366030648211,"Isha":2.2854795341536223,"SemHAll":2.4926226965318863}
    #myobj = {"SOMAIYA-WIFI":2.465709966975696,"SOMAIYA-GUEST":2.515709966975696,"Lol 5":1.4606702402547669,"Efarm Test":2.2573294969977384,"Lol 2.4":2.0837119514047027,"LAB2":2.2426226965318863,"Param":2.336366030648211,"Isha":2.4854795341536224,"JioPrivateNet":2.3556687130162737,"Ronak":2.734594843519919}
    #myobj = {"SOMAIYA-GUEST":2.738144470815276,"SOMAIYA-WIFI":2.450724130399211,"Param":1.690825861192966,"Efarm Test":1.5073294969977382,"Redmi Note X2":2.2337119514047026,"SemHAll":2.392622696531886,"PARAM2":2.484594843519919}
    #myobj = {"SOMAIYA-GUEST":2.415709966975696,"SOMAIYA-WIFI":2.7837119514047024,"Isha":1.3854795341536223,"Redmi Note X2":1.8837119514047025,"SemHAll":2.110670240254767,"Efarm Test":2.0337119514047024,"PARAM2":2.234594843519919,"Param":2.340825861192966,"email_json":3232}
    myobj = {"Efarm Test":0.9106702402547668,"SOMAIYA-WIFI":2.6837119514047023,"SOMAIYA-GUEST":2.6837119514047023,"SemHAll":1.7106702402547669,"ASUS_X00PD":1.4881444708152756,"Isha":1.636366030648211,"Param":1.8381444708152757,"Redmi Note X2":1.8337119514047024,"Lol 2.4":2.2372543403911367,"Lol 5":2.0606702402547667,"Pranav":2.4917233495923496,"Alum Rock":2.736366030648211,"email_json":12223}
    x = requests.post(url, json = json.dumps(myobj))

    return render_template_string(x.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
