import pymongo
import Parser

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['Ptt']
collect = db['Gossiping']
articles = collect.find()

for article in articles:
	school_data = Parser.findIP_School(article['ip'])

	try:
		collect.update({'_id':article['_id']}, {'$set':school_data})
	except pymongo.errors.CursorNotFound:
		print "No article in database"

	print article['article_title'], article['ip'], school_data['school'], school_data['place']