#import CherryPy3_6_0.cherrypy
#import CherryPy3_6_0
#import CherryPy3_6_0.cherrypy
import sys
sys.path.append('./CherryPy3_6_0')
import cherrypy
import json

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "HELLO WORLD"
    index.exposed = True

    @cherrypy.expose
    def json(self, number):
        return json.dumps({"randNum":number})
cherrypy.quickstart(HelloWorld())
