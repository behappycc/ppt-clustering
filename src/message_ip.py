# -*- coding=UTF-8 -*-
import ptt
import findip
import pymongo
from pymongo import MongoClient

ptt.loginPtt()
ptt.enterUserList()

client = MongoClient('localhost', 27017)
db = client['Ptt']
collect = db['Gossiping']
articles = collect.find()

for article in articles:
	for message in article['messages']:
		print(message)
		if 'push_userid' in message and 'school' not in message:
			push_userid = message['push_userid']
			user_ip = ptt.getUserIP(push_userid)
			school_data = findip.findIP_School(user_ip)

			school_data['ip'] = user_ip

			collect.update(
				{
					'_id': article['_id'],
					'messages':{
						'$elemMatch':{
							'push_userid': push_userid,
							'ip': {'$nin': [user_ip]}
						}
					}
				},
				{'$set': {
					'messages.$.ip': user_ip,
					'messages.$.school': school_data['school'],
					'messages.$.place' : school_data['place']
				}}
			)
			print('userid= ' + push_userid + " ip=" + user_ip)

ptt.logoutPtt()