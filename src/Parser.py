# -*- coding: utf-8 -*-
import jieba
import extraDict
import operator

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

#string = "台中"
#print type(string), type(string.decode('utf-8')), string.decode('utf-8')

def main():
    sentence = "台中你是一個三寶三寶三寶三寶飯台中！"
    print "Input：", sentence
    words = jieba.cut(sentence, cut_all=False)
    #print "Output Full Mode："
    #for word in words:
    #    print word

    a = wordFrequency(words, 2, 2)
    print a[0][0], a[0][1]
    print a[1][0], a[1][1]
    

if __name__ == '__main__':
    main()