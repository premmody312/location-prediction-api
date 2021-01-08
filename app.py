from flask import Flask, render_template,jsonify, Response, request, redirect
import numpy as np
import pickle

app = Flask(__name__)

@app.route('/')
def index():
    return "API hit. Wait for model to be added"

# @app.route('/model')
# def model():
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
