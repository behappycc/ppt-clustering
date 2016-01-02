import pymongo
from pymongo import MongoClient

def main():
	# parseAuthor('OtsukaAi')
	#queryUser('OtsukaAi', 'myhome6206')
	queryUser('Gossiping', 'blza')

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

if __name__ == '__main__':
	main()