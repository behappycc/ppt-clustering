import pymongo
from pymongo import MongoClient

import Parser

client = MongoClient('localhost', 27017)
db = client['Ptt']
collect = db['Gossiping']
articles = collect.find()
school_times = {}
place_times = {}
for school in Parser.school_list:
	school_times[school] = 0
for place in Parser.place_list:
	place_times[place] = 0

for article in articles:
	if article['school'] != 'unknown':
		school_times[article['school'].encode('utf-8')] += 1
		place_times[article['place'].encode('utf-8')] += 1

collect = db['Gossiping_statistics']
collect.insert_one({'school_number': school_times})
collect.insert_one({'place_number': place_times})