#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

api = Blueprint('api', __name__)

# from . import price
from . import test
from . import data_annotation
from . import data_analysis
from . import product_kg
from . import sentiment_analysis
