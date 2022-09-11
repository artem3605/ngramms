import numpy as np
import argparse
import pickle
import os
from data.class_model.model import Model



parser = argparse.ArgumentParser()

parser.add_argument(
    '--model',
    type=str,
    default='model.pkl'
)
parser.add_argument(
    '--prefix',
    type=str,
    default=''
)
parser.add_argument(
    '--length',
    type=int,
    default=15
)

args = parser.parse_args()

with open(args.model, "rb") as fp:
    md = pickle.load(fp)

print(*md.generate(args.prefix, args.length, 3))
