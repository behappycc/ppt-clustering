import pymongo
from pymongo import MongoClient

import findip
import argparse
import copy
from datetime import datetime, timedelta
format = '%Y%m%d'

def main():
    parser = argparse.ArgumentParser(description='Label author-used IP')
    parser.add_argument('-b', metavar='BOARD_NAME', help='Board name', required=True)
    args = parser.parse_args()
    global board
    board = args.b

    topicRanking(board)

def topicRanking(board):
    print "topic ranking......"
    client = MongoClient('localhost', 27017)
    collection = client['Ptt'][board]

    now_time = datetime.now()
    dest_time = now_time - timedelta(days=7)

    articles = collection.find({"date": {"$gt": dest_time}}).sort('date', pymongo.DESCENDING)
    
    dest_time = now_time - timedelta(days=1)
    data = []
    date = {"dest_time": dest_time, "topic": [0]*50}
    for article in articles:
        if article['date'] < dest_time:
            dest_time = dest_time - timedelta(days=1)
            data.append(copy.deepcopy(date))
            date = {"dest_time": dest_time, "topic": [0]*50}

        date['topic'][article['topicid']] += 1

    topics = []
    with open("topic.txt", "r") as datafile:
        for line in datafile:
            topics.append(line.strip('\n'))

    with open(board+'_topic_ranking.csv', 'w+') as datafile:
        datafile.write("date," + ",".join(topics) + "\n")
        for date in data:
            datafile.write(date['dest_time'].strftime(format) + "," + ",".join([str(x) for x in date['topic']]) + "\n")



def statisticIP(board):
    client = MongoClient('localhost', 27017)
    db = client['Ptt']
    collect = db[board]
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

if __name__ == "__main__":
	main()