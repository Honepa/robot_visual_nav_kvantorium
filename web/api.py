import os, sys
from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
from flask_login import login_required, current_user
from .models import User
from flask import current_app
from werkzeug.utils import secure_filename
import requests

api = Blueprint('api', __name__)

api_config = {
    'actions': [
        {'url': 'lights', 'type': 'btn'},
        {'url': 'wash', 'type': 'form'},
        {'url': 'backlights', 'type': 'btn'},
        {'url': 'fwdlights', 'type': 'btn'},
        {'url': 'fwd', 'type': 'btn'},
        {'url': 'lft', 'type': 'btn'},
        {'url': 'rgt', 'type': 'btn'},
        {'url': 'bck', 'type': 'btn'},

    ],
}

@api.route("/lights/<state>", methods=['POST', ])
@login_required
def lights(state):
    if request.headers['X_REQUESTED_WITH'] == 'XMLHttpRequest':
        resp = requests.get(f'http://127.0.0.1:4999/lights/{state}')
        data = {
            'echo': True, 
            'action': 'lights', 
            'state': {
                'lights': state,
                'fwd': 1,
            }
        }

        return jsonify(data), 200
    else:
        return jsonify(message="Method Not Allowed"), 405


@api.route("/wash/<state>", methods=['POST', ])
@login_required
def wash(state): # 0 by default, to avoid issues 2ith 'stop' command
    if request.headers['X_REQUESTED_WITH'] == 'XMLHttpRequest':
        resp = requests.get(f'http://127.0.0.1:4998/wash/{state}')
        if state == '1':
            print('WASH')
        else:
            print('STOP') # force stop
        data = {
            'echo': True, 
            'action': 'wash', 
            'state': {
                'wash': state,
            }
        }
        return jsonify(data), 200
    else:
        resp = requests.get(f'http://127.0.0.1:4998/wash/0')
        print('STOP') # force stop
        return jsonify(message="Method Not Allowed"), 405


@api.route("/backlights", methods=['POST', ])
@login_required
def backlights():
    if request.headers['X_REQUESTED_WITH'] == 'XMLHttpRequest':
        data = {'echo': True, 'action': 'backlights', 'state': {'lights': 1, 'fwd': 1,}}

        return jsonify(data), 200
    else:
        return jsonify(message="Method Not Allowed"), 405


@api.route("/fwdlights", methods=['POST', ])
@login_required
def fwdlights():
    if request.headers['X_REQUESTED_WITH'] == 'XMLHttpRequest':
        data = {'echo': True, 'action': 'fwdlights', 'state': {'lights': 1, 'fwd': 1,}}

        return jsonify(data), 200
    else:
        return jsonify(message="Method Not Allowed"), 405


@api.route("/fwd/<state>", methods=['POST', ])
@login_required
def fwd(state): # 0 by default, to avoid issues 2ith 'stop' command
    if request.headers['X_REQUESTED_WITH'] == 'XMLHttpRequest':
        resp = requests.get(f'http://127.0.0.1:4998/fwd/{state}')
        if state == '1':
            print('FWD')
        else:
            print('STOP') # force stop
        data = {
            'echo': True, 
            'action': 'fwd', 
            'state': {
                'fwd': state,
            }
        }
        return jsonify(data), 200
    else:
        resp = requests.get(f'http://127.0.0.1:4998/fwd/0')
        print('STOP') # force stop
        return jsonify(message="Method Not Allowed"), 405


@api.route("/lft/<state>", methods=['POST', ])
@login_required
def lft(state):
    if request.headers['X_REQUESTED_WITH'] == 'XMLHttpRequest':
        resp = requests.get(f'http://127.0.0.1:4998/lft/{state}')
        if state == '1':
            print('LFT')
        else:
            print('STOP') # force stop
        
        data = {
            'echo': True, 
            'action': 'lft', 
            'state': {
                'lft': state,
            }
        }
        return jsonify(data), 200
    else:
        resp = requests.get(f'http://127.0.0.1:4998/fwd/0')
        print('STOP') # force stop
        return jsonify(message="Method Not Allowed"), 405


@api.route("/rgt/<state>", methods=['POST', ])
@login_required
def rgt(state, angle=0):
    if request.headers['X_REQUESTED_WITH'] == 'XMLHttpRequest':
        resp = requests.get(f'http://127.0.0.1:4998/rgt/{state}')
        if state == '1':
            print('RGT')
        else:
            print('STOP') # force stop

        data = {
            'echo': True, 
            'action': 'rgt', 
            'state': {
                'rgt': state,
            }
        }
        return jsonify(data), 200
    else:
        resp = requests.get(f'http://127.0.0.1:4998/fwd/0')
        print('STOP') # force stop
        return jsonify(message="Method Not Allowed"), 405


@api.route("/bck/<state>", methods=['POST', ])
@login_required
def bck(state):
    if request.headers['X_REQUESTED_WITH'] == 'XMLHttpRequest':
        # resp = requests.get(f'http://127.0.0.1:4999/bck/{state}')
        if state == '1':
            print('bck')
        else:
            print('STOP') # force stop
        data = {
            'echo': True, 
            'action': 'bck', 
            'state': {
                'bck': state,
            }
        }
        return jsonify(data), 200
    else:
        print('STOP') # force stop
        return jsonify(message="Method Not Allowed"), 405

