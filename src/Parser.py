# -*- coding: utf-8 -*-
import jieba
import jieba.posseg as pseg
import extraDict
import operator
from gensim import corpora, models, similarities  

jieba.load_userdict("gossipingDict.txt")

def wordFrequency(words, wordLen, wordTop):
    dictFreq = {}
    highFreqWord = []
    for word in words:
        if word in dictFreq:
            dictFreq[word] += 1
        else:
            dictFreq[word] = 1

    sorted_word = sorted(dictFreq.items(), key = operator.itemgetter(1), reverse=True)
    for ele in sorted_word:
        if len(ele[0]) >= wordLen:
            highFreqWord.append(ele)
    return highFreqWord[:wordTop]

def topicModel(listArticleTitle):
    jieba.load_userdict("gossipingDict.txt")
    listSentence = []
    sentence1 = "台中你是一個三寶三寶飯！"
    sentence2 = "馬總統蔡英文"
    sentence3 = "台灣大學電機系"
    sentence4 = "獨立音樂需要大家一起來推廣，歡迎加入我們的行列！"
    sentence5 = "我沒有心我沒有真實的自我我只有消瘦的臉孔所謂軟弱所謂的順從一向是我的座右銘"
    listSentence.append(sentence1)
    listSentence.append(sentence2)
    listSentence.append(sentence3)
    listSentence.append(sentence4)
    listSentence.append(sentence5)


    nWordAll = []
    for sentence in listSentence:
        words = pseg.cut(sentence)
        nWord = ['']
        for word, flag in words:
            #print word
            if((flag == 'n'or flag == 'v' or flag == 'a' or flag == 'nz' or flag == 'ns' or flag == 'nt' or flag == 'nz') and len(word)>1):
                    print word
                    nWord.append(word)
        nWordAll.append(nWord)

    print "nWordAll\n", nWordAll
    dictionary = corpora.Dictionary(nWordAll)
    print "dictionary\n", dictionary
    corpus = [dictionary.doc2bow(text) for text in nWordAll]
    print "corpus\n", corpus

    tfidf = models.TfidfModel(corpus)
    print "tfidf", tfidf
    corpus_tfidf = tfidf[corpus]
    print "corpus_tfidf", corpus_tfidf
    lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, alpha='auto', num_topics=10)
    print "lda", lda
    corpus_lda = lda[corpus_tfidf]
    for doc in corpus_lda:
        print doc

    query = u"台灣 大學"
    x = query.split( )
    query_bow = dictionary.doc2bow(x)
    print query_bow

    query_lda = lda[query_bow]
    print query_lda

    a = list(sorted(lda[query_bow], key = lambda x : x[1]))
    print a[0]
    print a[-1]
    #least related
    print lda.print_topic(a[0][0])
    #most related
    print lda.print_topic(a[-1][0])


    '''
    for i in range(0, 10):
        for j in lda.print_topics(i)[0]:
            print j
    '''    
def main():
    topicModel(123)
    '''
    sentence = "台中你是一個三寶三寶三寶三寶飯台中！"
    print "Input：", sentence
    words = jieba.cut(sentence, cut_all=False)
    #print "Output Full Mode："
    #for word in words:
    #    print word

    a = wordFrequency(words, 2, 2)
    print a[0][0], a[0][1]
    print a[1][0], a[1][1]

    school = findIP_School(u"203.71.88.102")
    print school['school'], school['place']
    '''
    pass

if __name__ == '__main__':
    main()