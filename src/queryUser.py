import pymongo
from pymongo import MongoClient

def main():
	# parseAuthor('OtsukaAi')
	queryUserArticle('OtsukaAi', 'myhome6206')

def parseAuthor(board):
	client = MongoClient('localhost', 27017)
	collection = client['Ptt'][board]

	articles = collection.find().sort({'date': -1})

	for article in articles:
		author = article['author']
		# print author, type(author)
		
		if type(author) is unicode:
			account, nickname = author.split(' ', 1)
			nickname = nickname.strip('()')
			collection.update(
				{'_id': article['_id']},
				{'$set': {'author':{'account': account, 'nickname': nickname}}}
			)

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

	for record in user_record:
		print record['article_title'], record['date']
'''
def queryUserPush(board, username):
	
	user_record = collection.find({
		'messages':{
			'$elemMatch':{
				'push_userid': username
			}
		}
	}).sort('date', pymongo.DESCENDING)

	for record in user_record:
		print record['article_title'], record['date']
'''
if __name__ == '__main__':
	main()