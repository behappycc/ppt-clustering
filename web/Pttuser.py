import pymongo
from pymongo import MongoClient
import time

def main():
	starttime = time.time()
	# parseAuthor('OtsukaAi')
	#queryUser('OtsukaAi', 'myhome6206')
	#queryUser('Gossiping', 'blza')
	queryArticle('Gossiping','asdfghjklasd')
	print "The execution time takes %s seconds." % (time.time() - starttime)

def queryUser(board, username):
	client = MongoClient('localhost', 27017)
	collection = client['Ptt'][board]

	user_record = collection.find({
		'$or':[
			{'author.account': username},
			{'messages':{
					'$elemMatch':{'push_userid': username}
			}}
		]
	}).sort('date', pymongo.DESCENDING)
	return user_record

	#for record in user_record:
	#	print record['article_title'], record['date']

def queryArticle(board, username):
	client = MongoClient('localhost', 27017)
	collection = client['Ptt'][board]

	user_record = collection.find({'author.account': username}).sort('date', pymongo.DESCENDING)
	for record in user_record:
		print record['article_title'], record['date']
	#return user_record

if __name__ == '__main__':	
	main()
	