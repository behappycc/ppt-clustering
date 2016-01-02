import pymongo
from pymongo import MongoClient, IndexModel, DESCENDING, ASCENDING

def main():
	parseAuthor('Gossiping')
	# createIndex('Gossiping')
	# queryUser('Gossiping', 'myhome6206')

def createIndex(board):
	print "createIndex"
	client = MongoClient('localhost', 27017)
	collection = client['Ptt'][board]


	collection.create_index(
		[("date", DESCENDING)]
	)


def parseAuthor(board):
	client = MongoClient('localhost', 27017)
	collection = client['Ptt'][board]

	articles = collection.find()

	for article in articles:
		author = article['author']
		print author, type(author)
		
		if type(author) is unicode:
			if u'(' in author:
				account, nickname = author.split(' ', 1)
				nickname = nickname.strip('()')
			else:
				account = author
				nickname = ""
			collection.update(
				{'_id': article['_id']},
				{'$set': {'author':{'account': account, 'nickname': nickname}}}
			)

def queryUser(board, username):
	client = MongoClient('localhost', 27017)
	collection = client['Ptt'][board]

	user_record = collection.find({
		'$or':[
			{'author.account': username}, # article
			{'messages':{                 # push
					'$elemMatch':{'push_userid': username}
			}}
		]
	}).sort('date', pymongo.DESCENDING)

	for record in user_record:
		print record['article_title'], record['date']

def queryUserArticle(board, username):
	client = MongoClient('localhost', 27017)
	collection = client['Ptt'][board]

	user_record = collection.find({'author.account': username})#.sort('date', pymongo.DESCENDING)

	for record in user_record:
		print record['article_title'], record['date']



if __name__ == '__main__':
	main()