# -*- coding: utf-8 -*-

import warnings
from code.config import get_default_args
from code.factory import Factory


# export PYTHONPATH=$PYTHONPATH:/data1/chenfang/Project/JDComment
# CUDA_VISIBLE_DEVICES=0 python3 train.py


def main():
    warnings.filterwarnings("ignore")

    root = "/data1/chenfang/Project/JDComment"
    args = get_default_args(root=root)
    factory = Factory(args)
    factory.train()
    return None


if __name__ == "__main__":
    main()
