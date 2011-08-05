from django.shortcuts import render_to_response
import json
from maiznet.monitoring.monitor import config
from django.template import Library, Node

register = Library()

class CheckboxNode(Node):
	def render(self, context):
		rfile = open(config.STATE_PATH,"r")
		strjson = rfile.read()
		services = json.loads(strjson)
		context['services'] = services
		print "services :"
		print services
		return ''
	
def get_checkbox(parser,token):
	return CheckboxNode()

get_checkbox = register.tag(get_checkbox)
