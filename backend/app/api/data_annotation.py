#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
from . import api
from flask import jsonify, request
from app.lib.event_manager import EVENT

# 获取一条未标注的数据
@api.route('/getNextText', methods=['POST'])
def get_next_text():
    data = request.get_json()
    return jsonify(EVENT.fetch_event(data['taskNum']))

# 查看一条标注好的历史数据
@api.route('/getOneHistory', methods=['GET'])
def get_one_history():
    return jsonify(EVENT.fetch_one_history())

# 查看标注好的历史数据信息
@api.route('/getHistoryInfo', methods=['POST'])
def get_history_info():
    data = request.get_json()
    return jsonify(EVENT.fetch_history_info(data['taskNum']))

# 分页查看标注好的历史数据
@api.route('/getPageHistoryFiltered', methods=['POST'])
def get_page_history_filtered():
    data = request.get_json()
    return jsonify(EVENT.fetch_page_history_filtered(data['product'], data['category'], data['polarity']))

# 分页查看标注好的历史数据
@api.route('/getPageHistory', methods=['POST'])
def get_page_history():
    data = request.get_json()
    return jsonify(EVENT.fetch_page_history(data['page'], data['pageSize'], data['taskNum']))

# 提交一条标注好的数据
@api.route('/postEvent', methods=['POST'])
def post_event():
    data = request.get_json()
    EVENT.post_event(data['comment_id'], data, data['taskNum'])
    return jsonify('success')

# 标注和未标注的数据量
@api.route('/annotationRecord', methods=['POST'])
def get_event_count():
    data = request.get_json()
    labeled_cnt, unlabeled_cnt = EVENT.count(data['taskNum'])
    return jsonify({'labeled_cnt': labeled_cnt, 'unlabeled_cnt':unlabeled_cnt})

