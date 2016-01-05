import argparse

import pymongo
from pymongo import MongoClient

import jieba
import jieba.posseg as pseg
jieba.load_userdict("gossipingDict.txt")
from gensim import corpora, models, similarities  

topics = []

def main():
    parser = argparse.ArgumentParser(description='Label author-used IP')
    parser.add_argument('-b', metavar='BOARD_NAME', help='Board name', required=True)
    args = parser.parse_args()
    board = args.b

    readTopic()
    labelTopic(board)

def labelTopic(board):
    client = MongoClient('localhost', 27017)
    collection = client['Ptt'][board]

    dictionary = corpora.dictionary.Dictionary.load(board + "/" + board + "_dict.model")
    lda = models.ldamodel.LdaModel.load(board + '/' + board + '_lda.model')

    articles = collection.find()

    for article in articles:
        if 'topicid' not in article:
            print article['article_title']
            title = article['article_title']
            title_tokens = splitWord(title)
            corpus = dictionary.doc2bow(title_tokens)
            topic_guess = lda.get_document_topics(corpus)
            topic_guess = list(sorted(topic_guess, key = lambda x : x[1]))
            topicid = topic_guess[-1][0]
            topic = lda.print_topic(topic_guess[-1][0])

            collection.update(
                {'_id': article['_id']},
                {'$set': {
                    'topicid': topicid,
                    'topic_text': topic,
                    'topic_guess': topics[topicid]
                }}
            )



def splitWord(sentence):
    if u']' in sentence:
        sentence = sentence.split("]", 1)[1]

    nWord = []
    for word, flag in pseg.cut(sentence):
        if(flag in ['n', 'v', 'a', 'ns', 'nt', 'nz']) and (len(word)>1):
            nWord.append(word)
    return nWord



def readTopic():
    with open("topic.txt", "r") as datafile:
        for line in datafile:
            topics.append(line.strip('\n'))

if __name__ == '__main__':
    main()