#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import ast
from . import api
from flask import jsonify, request
from app.lib.JDComment.event_model import EVENTMODEL
from app.lib.event_manager import EVENT
from collections import Counter

# 获取待分析数据的分析结果
@api.route('/getProductGraph', methods=['POST'])
def get_product_graph():
    if request.is_json:
        variety = request.get_json()['variety']
        print('Received: ', variety)
    elif hasattr(request, 'args'):
        variety = request.args.get("variety")
        print('Received: ', variety)
    else:
        print(type(request))
        return
    
    res = EVENT.get_product(variety)
    return jsonify(res)
