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

def topicModel():

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
        nWord = []
        for word, flag in words:
            #print word
            if(flag in ['n', 'v', 'a', 'ns', 'nt', 'nz']) and (len(word)>1):
                    nWord.append(word)
        nWordAll.append(nWord)

    '''
    dictionary = corpora.Dictionary(nWordAll)
    corpus = [dictionary.doc2bow(text) for text in nWordAll]

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, alpha='auto', num_topics=10)
    lda.save('gossiping_topic.model')
    '''
    dictionary = corpora.dictionary.Dictionary.load('Gossiping/Gossiping_dict.model')
    lda = models.ldamodel.LdaModel.load('Gossiping/Gossiping_lda.model')
    for i in range(50):
        print lda.print_topic(i)

    sentence = "故宮南院龍馬獸首是統戰？ 2青年潑"
    sentence = sentence.split("[", 1)[0]

    nWord = []
    for word, flag in pseg.cut(sentence):
        if(flag in ['n', 'v', 'a', 'ns', 'nt', 'nz']) and (len(word)>1):
            nWord.append(word)
    sentence = nWord
    corpus = dictionary.doc2bow(sentence)
    topic_guess = lda.get_document_topics(corpus)
    topic_guess = list(sorted(topic_guess, key = lambda x : x[1]))
    topicid = topic_guess[-1][0]
    topic = lda.print_topic(topic_guess[-1][0])
    
    print topic_guess[-1][0], ",", topic
    '''
    #word2vec
    model = models.Word2Vec(nWordAll, min_count=1)
    model.save('word2vec_model.model')

    #print model[u'台灣']
    sim = model.most_similar(positive=[u'台灣大學'])
    for s in sim:  
        print "word:%s,similar:%s " %(s[0],s[1])

    for w in model.most_similar(u'台灣大學'):
        print w[0], w[1], 'hi'
    '''
      
def main():
    topicModel()
    pass

if __name__ == '__main__':
    main()