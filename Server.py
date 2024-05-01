import cherrypy
import os
import json
import ReverseImageSearch as ris


class ReverseImageSearchWebapp:

    def __init__(self) -> None:
        self.revImgSearch = ris.ReverseImageSearch('wikimedia_dino', clear=False)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def search(self, url):
        res = self.revImgSearch.querySingleImage(url)
        return res

    @cherrypy.expose
    def insert(self, url):
        self.revImgSearch.insertSingleImage(url)

if __name__ == '__main__':

    PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "web")
    cherrypy.config.update({'server.socket_port': 8081})
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.on': True,
            'tools.staticdir.dir': PATH,
            'tools.staticdir.index': 'index.html',
        },
        #'/search': {
        #    'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        #    'tools.response_headers.on': True,
        #    'tools.response_headers.headers': [('Content-Type', 'application/json')],
        #},
    }

    cherrypy.quickstart(ReverseImageSearchWebapp(), '/', conf)
