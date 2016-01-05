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
import Topic as tp

#localhost:8000/index
#140.112.42.151
DB_IP = "localhost"
DB_PORT = 27017

def main():
    parser = argparse.ArgumentParser(description='ptt-clustering server')
    parser.add_argument('-p', type=int, help='listening port for ptt-clustering server')
    parser.add_argument('-b', metavar='BOARD_NAME', help='Board name', required=True)
    args = parser.parse_args()
    global board
    port = args.p
    board = args.b
    
    print("Server starting......")

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/index", IndexHandler),
            (r"/chart", ChartHandler),
            (r"/user",UserHandler),
            (r"/test",TestHandler),
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
    def __init__(self, application, request, **kwargs):
        self.popularEvents = {}
        self.newEvents = {}
        super(IndexHandler, self).__init__(application, request, **kwargs)

    def get(self):
        #list1Topic, list7Topic = tp.statisticTopic(board)
        list7Topic = tp.statisticTopicFast(board)
        self.popularEvents = tp.topicFreqDB(list7Topic)[:10]
        #self.newEvents = tp.recommendArticle(list7Topic, 5)[:7]
        self.newEvents = tp.randomChoice(tp.recommendArticle(list7Topic, 5), 5)
        self.render("index.html", popularEvents = self.popularEvents, newEvents = self.newEvents)
        #https://www.ptt.cc/bbs/Gossiping/M.1451802547.A.C20.html

    def post(self):
        json_obj = json_decode(self.request.body)
        #print 'Post data received'
        #for key in list(json_obj.keys()):
        #   print 'key: %s , value: %s' % (key, json_obj[key])
        print json_obj['key1']

        # new dictionary
        response_to_send = {}
        #response_to_send['newkey'] = json_obj['key1']
        #response_to_send['topic'] = tp.topicFreqDB(tp.statisticSchoolTopic(board, json_obj['key1']))
        #print('Response to return')
        #pprint.pprint(response_to_send)
        response_to_send['topic'] = tp.placeTopic(board, json_obj['key1'])
        self.write(json.dumps(response_to_send))

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
        records = ptt.queryUser(board, username) 
        #records = ptt.queryUser('Gossiping', username)'OtsukaAi'
        self.render("user.html", username = username, records = records)

class TestHandler(BaseHandler):
    def get(self):
        self.render("test.html")
        
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
