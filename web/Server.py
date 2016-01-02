# coding=UTF-8
# python native module
import urllib
import threading
import thread
import argparse
import os.path
import json
import pprint
# tornado module
import tornado.httpserver
import tornado.httputil as httputil
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from  tornado.escape import json_decode
from  tornado.escape import json_encode
# mongodb module
import pymongo
from pymongo import MongoClient
#custom files
import Pttuser as ptt

#localhost:8000/index
#140.112.42.151
DB_IP = "localhost"
DB_PORT = 27017

def main():
    parser = argparse.ArgumentParser(description='ptt-clustering server')
    parser.add_argument('port', type=int, help='listening port for ptt-clustering server')
    args = parser.parse_args()
    
    print("Server starting......")

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(args.port)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/index", IndexHandler),
            (r"/chart", ChartHandler),
            (r"/user",UserHandler),
            (r"/test", TestHandler),
            (r"/testajax", AjaxHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        super(Application, self).__init__(handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        pass
        #return self.settings['db']

class IndexHandler(BaseHandler):
    def get(self):
        abc = ["Item 1", "Item 2", "Item 3"]
        self.render("index.html", abc = abc)

class ChartHandler(BaseHandler):
    def get(self):
        self.render("chart.html")

class UserHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        self.username = ''
        self.records = {}
        super(UserHandler, self).__init__(application, request, **kwargs)

    def get(self):
        self.render("user.html", username = self.username, records = self.records)

    def post(self):
        username = self.get_argument("username")
        print username
        records = ptt.queryUser('OtsukaAi', username)  
        #records = ptt.queryUser('Gossiping', username)
        self.render("user.html", username = username, records = records)
        
'''
class AndroidHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        self.deviceInfo = {}
        self.deviceInfo['temperature'] = '17C'
        self.deviceInfo['humidity'] = '80%'
        self.userInfo = []
        super(AndroidHandler, self).__init__(application, request, **kwargs)

    def get(self):
        self.write(json.dumps(self.deviceInfo)) 
        #self.write(self.deviceInfo)

    def post(self):
        self.write(json.dumps(self.deviceInfo)) 
'''

class TestHandler(BaseHandler):
    def get(self):
        abc = ["Item 1", "Item 2", "Item 3"]
        self.render("test.html",title="My title", abc = abc)

class AjaxHandler(tornado.web.RequestHandler):
    def get(self):
        example_response = {}
        example_response['name'] = 'example'
        example_response['width'] = 1020

        self.write(json.dumps(example_response))

    def post(self):
        json_obj = json_decode(self.request.body)
        print('Post data received')

        for key in list(json_obj.keys()):
            print('key: %s , value: %s' % (key, json_obj[key]))

        # new dictionary
        response_to_send = {}
        response_to_send['newkey'] = json_obj['key1']

        print('Response to return')

        pprint.pprint(response_to_send)

        self.write(json.dumps(response_to_send))

if __name__ == '__main__':
    main()
