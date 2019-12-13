import json
from os import path

try:
    with open("serverconfig.json", 'r') as c:
        config = json.load(c)
except OSError:
    raise OSError("could not open serverconfig.json")

try:
    users = config['users']
    baseDir = path.normpath(config['basedir'])
    blacklist = config['blacklist']
except KeyError:
    raise KeyError("serverconfig.json invalid")
staticDir = path.join(baseDir, 'static')