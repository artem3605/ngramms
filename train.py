import numpy as np
import argparse
import pickle
import os
from data.class_model.model import Model


parser = argparse.ArgumentParser()
parser.add_argument(
    '--input_dir',
    type=str,
    default='stdin'
)
parser.add_argument(
    '--model',
    type=str,
    default='model.pkl'
)
args = parser.parse_args()
md = Model()
md.fit(3, args.input_dir)
with open(args.model, "wb") as fp:
    pickle.dump(md, fp)
