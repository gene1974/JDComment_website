import json
import numpy as np
import pickle
import time
import torch

def clean_str(token):
    return token.replace('(', '').replace(')', '').replace('/', '').replace('-', '').replace('[', '').replace(']', '').replace('~', '').replace('', '')

def save_data(path, data, data_time = None):
    if data_time is None:
        data_time = time.strftime('%m%d%H%M', time.localtime())
    with open(path + '.' + data_time, 'wb') as f:
        pickle.dump(data, f)
    print('Save data: ', path + '.' + data_time)
    return data_time

def load_data(path, data_time = None):
    if data_time is not None:
        path = path + '.' + data_time
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data

