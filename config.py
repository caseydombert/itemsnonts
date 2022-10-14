import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--config', type=str, default="./config.json")
args = parser.parse_args()

path = args.config

with open(path, 'r') as f:
    configDict = json.loads(f.read())