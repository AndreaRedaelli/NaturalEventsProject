import cherrypy
import pandas as pd
import WSCall
import json
class WebService(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def getData(self):
        if cherrypy.request.method == "OPTIONS":
           cherrypy.response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
           cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"
           cherrypy.response.headers["Access-Control-Max-Age"] = "86400"
           cherrypy.response.headers["Access-Control-Allow-Headers"] = "X-Mobile, Authorization, Origin, X-Requested-With, Content-Type, Accept"
           return ""
        arguments = cherrypy.request.json
        df = WSCall.callWS(arguments['limit'],arguments['days'],arguments['source'],arguments['status'])
        return df.to_json()
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getLayer(self):
        if cherrypy.request.method == "OPTIONS":
           cherrypy.response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
           cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"
           cherrypy.response.headers["Access-Control-Max-Age"] = "86400"
           cherrypy.response.headers["Access-Control-Allow-Headers"] = "X-Mobile, Authorization, Origin, X-Requested-With, Content-Type, Accept"
           return ""
        response = WSCall.callWSGetCapabilities();
        return json.dumps(response)
    @cherrypy.expose
    def getImage(self, layers,format,styles,bbox,crs,width,height,transparent,time):
        if cherrypy.request.method == "OPTIONS":
           cherrypy.response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
           cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"
           cherrypy.response.headers["Access-Control-Max-Age"] = "86400"
           cherrypy.response.headers["Access-Control-Allow-Headers"] = "X-Mobile, Authorization, Origin, X-Requested-With, Content-Type, Accept"
           return "" 
        cherrypy.response.headers['Content-Type'] = "image/png"
        df = WSCall.GetImage(layers,format,styles,bbox,crs,width,height,transparent,time)
        return df
if __name__ == '__main__':
    config = {'server.socket_host': '0.0.0.0',
    'server.socket_port': 9090, 
    # required for CORS
    "tools.response_headers.on": True,
    "tools.response_headers.headers": [ ("Access-Control-Allow-Origin", "*"),],      
            }
    
    cherrypy.config.update(config)
    cherrypy.quickstart(WebService())