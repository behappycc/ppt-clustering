# -*- coding: utf-8 -*-

import re
import sys
import json
import requests
requests.packages.urllib3.disable_warnings()
import argparse
import time
import codecs
from bs4 import BeautifulSoup
from six import u

from pymongo import MongoClient

from datetime import datetime
format = '%a %b %d %H:%M:%S %Y'

__version__ = '1.0'

# if python 2, disable verify flag in requests.get()
VERIFY = True
if sys.version_info[0] < 3:
    VERIFY = False
    #requests.packages.urllib3.disable_warnings()

# logging setting -------------------------------------------------------------
import logging
logger = logging.getLogger('Master Server - %d')
logger.propagate = False
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s-%(levelname)s-%(message)s'
)
# console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
# -----------------------------------------------------------------------------


def main(cmdline=None):
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='''
        A crawler for the web version of PTT, the largest online community in Taiwan.
        Input: board name and page indices (or articla ID)
        Output: BOARD_NAME-START_INDEX-END_INDEX.json (or BOARD_NAME-ID.json)
    ''')
    parser.add_argument('-b', metavar='BOARD_NAME', help='Board name', required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', metavar=('START_INDEX', 'END_INDEX'), type=int, nargs=2, help="Start and end index")
    group.add_argument('-a', metavar='ARTICLE_ID', help="Article ID")
    group.add_argument('-l', action='store_true', help='check last time')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    
    if cmdline:
        args = parser.parse_args(cmdline)
    else:
       args = parser.parse_args()
    board = args.b 

    # build mongodb
    conn = MongoClient('localhost', 27017)
    db = conn['Ptt']
    collection = db[board]

    if args.l:

        # check last time
        last_time = conn['Ptt']['last_time'].find_one({'board': board})
        
        if last_time:
            last_time = last_time['last_time']
            logger.info("last_time: " + repr(last_time))
            conn['Ptt']['last_time'].update(
                {'board': board},
                {'$set':{'last_time': datetime.now()}}
            )
        else:
            last_time = datetime.fromtimestamp(0)
        # update last time
            conn['Ptt']['last_time'].insert_one({
                'board'     : board, 
                'last_time' : datetime.now()
            })
        logger.info("update lastime" + repr(datetime.now()))

        resp = requests.get(
            url='https://www.ptt.cc/bbs/' + board + '/index.html',
            cookies={'over18': '1'}, 
            verify=VERIFY
        )
        if resp.status_code != 200:
            logger.warning('invalid url: ' + resp.url)
            return
        
        # find first page index
        soup = BeautifulSoup(resp.text, 'html.parser')
        div = soup.find_all("div", "btn-group pull-right")[0]
        href = div.find_all('a')[1]['href']
        pattern = u'/(.+)/(.+)/index(\d+).html'
        last_index = re.match(pattern, href).group(3)
        last_index = int(last_index) + 1 

        # parsePage(collection, board, last_index, last_time)
        for index in range(last_index, 0, -1):
            if parsePage(collection, board, index, last_time):
                return 

    elif args.i:
        start = args.i[0]
        end = args.i[1]
        index = start

        for index in range(start, end+1):
            if parsePage(collection, board, index, datetime.fromtimestamp(0)):
                return 

    else:  # args.a
        article_id = args.a
        link = PTT_URL + '/bbs/' + board + '/' + article_id + '.html'
        insert(collection, parse(link, article_id, board))

overtime_flag = 0
max_overtime = 6
def parsePage(collection, board, index, last_time):
    global overtime_flag

    PTT_URL = 'https://www.ptt.cc'
    logger.info('Processing index: ' + str(index))
    resp = requests.get(
        url=PTT_URL + '/bbs/' + board + '/index' + str(index) + '.html',
        cookies={'over18': '1'}, verify=VERIFY
    )
    if resp.status_code != 200:
        logger.warning('invalid url: ' + resp.url)
        return 
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    divs = soup.find_all("div", "r-ent")
    divs = divs[::-1]
    
    for div in divs:
        try:
            # ex. link would be <a href="/bbs/PublicServan/M.1127742013.A.240.html">Re: [問題] 職等</a>
            href = div.find('a')['href']
            link = PTT_URL + href
            article_id = re.sub('\.html', '', href.split('/')[-1])

            data = parse(link, article_id, board)
            date = data['date']

            if date < last_time:
                overtime_flag += 1
                logger.info("date < last_time " + str(overtime_flag))

                if overtime_flag > max_overtime:
                    return True
                else:
                    continue
            
            insert(collection, data)
            
        except:
            pass
        time.sleep(0.1)
    return False

def insert(collection, data):
    if data:
        db_id = collection.insert_one(dict(data)).inserted_id
        logger.info('db id: ' + str(db_id))
    else:
        logger.warning('error')

def parse(link, article_id, board):
    logger.info('Processing article: ' + article_id)
    resp = requests.get(url=link, cookies={'over18': '1'}, verify=VERIFY)
    if resp.status_code != 200:
        logger.warning('invalid url: ' + resp.url)
        # return json.dumps({"error": "invalid url"}, indent=4, sort_keys=True, ensure_ascii=False)
        return None
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    main_content = soup.find(id="main-content")
    metas = main_content.select('div.article-metaline')
    author = ''
    title = ''
    date = ''
    if metas:
        author = metas[0].select('span.article-meta-value')[0].string if metas[0].select('span.article-meta-value')[0] else author
        account, nickname = author.split(" ", 1)
        author = {'account': account, 'nickname': nickname.strip("()")}
        title = metas[1].select('span.article-meta-value')[0].string if metas[1].select('span.article-meta-value')[0] else title
        date = metas[2].select('span.article-meta-value')[0].string if metas[2].select('span.article-meta-value')[0] else date

        # remove meta nodes
        for meta in metas:
            meta.extract()
        for meta in main_content.select('div.article-metaline-right'):
            meta.extract()

    # remove and keep push nodes
    pushes = main_content.find_all('div', class_='push')
    for push in pushes:
        push.extract()

    try:
        ip = main_content.find(text=re.compile(u'※ 發信站:'))
        ip = re.search('[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*', ip).group()
    except:
        ip = "None"

    # 移除 '※ 發信站:' (starts with u'\u203b'), '◆ From:' (starts with u'\u25c6'), 空行及多餘空白
    # 保留英數字, 中文及中文標點, 網址, 部分特殊符號
    filtered = [ v for v in main_content.stripped_strings if v[0] not in [u'※', u'◆'] and v[:2] not in [u'--'] ]
    expr = re.compile(u(r'[^\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\s\w:/-_.?~%()]'))
    for i in range(len(filtered)):
        filtered[i] = re.sub(expr, '', filtered[i])
    
    filtered = [_f for _f in filtered if _f]  # remove empty strings
    filtered = [x for x in filtered if article_id not in x]  # remove last line containing the url of the article
    content = ' '.join(filtered)
    content = re.sub(r'(\s)+', ' ', content)

    # push messages
    p, b, n = 0, 0, 0
    messages = []
    for push in pushes:
        if not push.find('span', 'push-tag'):
            continue
        push_tag = push.find('span', 'push-tag').string.strip(' \t\n\r')
        push_userid = push.find('span', 'push-userid').string.strip(' \t\n\r')
        # if find is None: find().strings -> list -> ' '.join; else the current way
        push_content = push.find('span', 'push-content').strings
        push_content = ' '.join(push_content)[1:].strip(' \t\n\r')  # remove ':'
        push_ipdatetime = push.find('span', 'push-ipdatetime').string.strip(' \t\n\r')
        messages.append( {'push_tag': push_tag, 'push_userid': push_userid, 'push_content': push_content, 'push_ipdatetime': push_ipdatetime} )
        if push_tag == u'推':
            p += 1
        elif push_tag == u'噓':
            b += 1
        else:
            n += 1

    # count: 推噓文相抵後的數量; all: 推文總數
    message_count = {'all': p+b+n, 'count': p-b, 'push': p, 'boo': b, "neutral": n}

    # json data
    data = {
        'board': board,
        'article_id': article_id,
        'article_title': title,
        'author': author,
        'date': date,
        'content': content,
        'ip': ip,
        'message_conut': message_count,
        'messages': messages
    }

    data['date'] = datetime.strptime(data['date'], format)
    return data

if __name__ == '__main__':
    main()
