#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import main
from flask import jsonify

@main.route('/test/')
def main_test():
    return jsonify({'name': 'flask-route-test'})



