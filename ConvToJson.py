import json, xmljson, os
from pprint import pprint

FilesToConv = [f for f in os.listdir ('.') if f.endswith('.xml')]
pprint (FilesToConv)

