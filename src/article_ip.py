import argparse

import pymongo
from pymongo import MongoClient

import findip

def main():
	parser = argparse.ArgumentParser(description='Label author-used IP')
	parser.add_argument('-b', metavar='BOARD_NAME', help='Board name', required=True)
	args = parser.parse_args()
	board = args.b

	client = MongoClient('localhost', 27017)
	collection = client['Ptt'][board]
	articles = collection.find()

	for article in articles:
		school_data = findip.findIP_School(article['ip'])

		try:
			collection.update({'_id':article['_id']}, {'$set':school_data})
		except pymongo.errors.CursorNotFound:
			print "No article in database"

		print article['article_title'], article['ip'], school_data['school'], school_data['place']


if __name__ == '__main__':
	main()