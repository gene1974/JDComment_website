#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
from . import api
from flask import jsonify, request
from app.lib.JDComment.event_model import EVENTMODEL
from app.lib.event_manager import EVENT
from app.lib.cypher import KG

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

@api.route('/searchEntity', methods=['POST'])
def search_entity():
    if request.is_json:
        entity = request.get_json()['entity']
        print('Received: ', entity)
    elif hasattr(request, 'args'):
        entity = request.args.get("entity")
        print('Received: ', entity)
    else:
        print(type(request))
        return
    
    res = KG.find_all_relation(entity)
    return jsonify(res)
