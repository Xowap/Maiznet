import os

relpath = os.path.dirname(os.path.realpath(__file__))

DATABASE = relpath + "/monitor.db" 
TIME=120
PORT_MUNIN=4949
IP_MUNIN="192.168.0.1"
PLUGINS = ["if_re1","if_re2","if_re3"]
IMAGES_PATH = relpath+"/../../templates/monitoring/"
LISSAGE_NUM_POINTS = 10
LISSAGE_COEFF = 10

