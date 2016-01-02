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
    dictionary = corpora.dictionary.Dictionary.load('Gossiping/Gossiping_dict.model')
    lda = models.ldamodel.LdaModel.load('Gossiping/Gossiping_lda.model')
    with open("topic", 'w+') as datafile:
        for i in range(50):
            datafile.write(str(i) + " " + lda.print_topic(i).encode("utf-8") + '\n')

    
    '''
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