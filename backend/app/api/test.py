#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import jsonify
from . import api

@api.route('/test/')
def test():
    data = [i for i in range(10)]
    return jsonify({'name':'flask-route-test', 'data':data})
