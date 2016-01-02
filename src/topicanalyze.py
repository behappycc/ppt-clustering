# -*- coding: utf-8 -*-
import os
import argparse
import time

import jieba
import jieba.posseg as pseg
import extraDict
import operator
from gensim import corpora, models, similarities  

import pymongo
from pymongo import MongoClient




jieba.load_userdict("gossipingDict.txt")



def main():
    parser = argparse.ArgumentParser(description='Label author-used IP')
    parser.add_argument('-b', metavar='BOARD_NAME', help='Board name', required=True)
    args = parser.parse_args()
    global board
    board = args.b
    
    client = MongoClient('localhost', 27017)
    collection = client['Ptt'][board]

    start_time = time.time()

    learnLDA(collection)
    # guessTopic(collection)

    total_time = time.time() - start_time

    print str(total_time) + 'sec'

key_word = []
lda = ""
dictionary = ""
word2vec = ""

def splitWord(sentence):
    sentence = sentence.split("[", 1)[0]

    nWord = []
    for word, flag in pseg.cut(sentence):
        if(flag in ['n', 'v', 'a', 'ns', 'nt', 'nz']) and (len(word)>1):
            nWord.append(word)
    return nWord


def learnLDA(collection):
    print "learning model"

    key_word = []

    articles = collection.find()
    for article in articles:
        key_word.append(splitWord(article['article_title']))

    # lda
    global dictionary
    dictionary = corpora.Dictionary(key_word)
    corpus = [dictionary.doc2bow(sentence) for sentence in key_word]

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    global lda
    lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, alpha='auto', num_topics=50)
    
    # word2vec
    global word2vec
    word2vec = models.Word2Vec(key_word, min_count=1)
    

    if not os.path.exists(board):
        os.makedirs(board)
    dictionary.save(board + '/' + board + '_dict.model')
    lda.save(board + '/' + board + '_lda.model')
    word2vec.save(board + '/' + board + '_word2vec.model')
    print "learning finish"


def pureLDA(collection):
    print "guess topic"

    articles = collection.find()
    for article in articles:
        print article['article_title']
        tokens = splitWord(article['article_title'])
        query_bow = dictionary.doc2bow(tokens)
        topic_guess = lda.get_document_topics(query_bow)
        topic_guess = list(sorted(topic_guess, key = lambda x : x[1]))
        topicid = topic_guess[-1][0]
        topic = lda.print_topic(topic_guess[-1][0])
        
        print topic_guess[-1][0], ",", topic
        
        collection.update(
            {'_id': article['_id']},
            {'$set': {'pure_lad': {'topicid': topicid, 'topic': topic}}}
        )

def addWord2vec(collection):
    print "add word2vec"

    articles = collection.find()
    for article in articles:
        print article['article_title']
        tokens = splitWord(article['article_title'])
        
        similar_token = []
        for token in tokens:
            similar = word2vec.most_similar(token)
            similar_token.append(similar[0][0])
            similar_token.append(similar[1][0])
        tokens = tokens + similar_token

        query_bow = dictionary.doc2bow(tokens)
        topic_guess = lda.get_document_topics(query_bow)
        topic_guess = list(sorted(topic_guess, key = lambda x : x[1]))
        topicid = topic_guess[-1][0]
        topic = lda.print_topic(topic_guess[-1][0])
        
        print topic_guess[-1][0], ",", topic
        
        collection.update(
            {'_id': article['_id']},
            {'$set': {'add_word2vec':{'topicid': topicid, 'topic': topic}}}
        )


if __name__ == '__main__':
	main()