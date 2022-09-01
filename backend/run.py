#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

from app import create_app
import argparse

app = create_app()


# 命令行脚本运行启动方式
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=9050)
    parser.add_argument('--debug', default=True, action="store_true")
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port, debug=args.debug)
    # app.run(host='127.0.0.1', port=args.port, debug=args.debug)