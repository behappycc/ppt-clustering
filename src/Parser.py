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

def readIP(filename, userIP):
    listData = []
    listIP = []
    with open(filename, 'r') as datafile:
        for line in datafile:
            listData.append(line)
    for data in listData:      
        temp = data.split(' ')
        if '~' not in temp[1]:
            school = []
            school.append(temp[0])
            school.append(temp[1])
            school.append(temp[2])
            listIP.append(school)
        else:
            tempIP1 = temp[1].split('.')
            tempIP2 = tempIP1[2].split('~')
            for i in xrange(int(tempIP2[0]), int(tempIP2[1])+1):
                school = []
                school.append(temp[0])
                school.append(tempIP1[0] + '.' + tempIP1[1] + '.' + str(i))
                school.append(temp[2])
                listIP.append(school)

    listSchool = []
    for ip in listIP:     
        if userIP.startswith(ip[1]):
            listSchool.append(ip)
            #print ip[0], ip[1]
    if len(listSchool) == 1:
        #print listSchool[0][0], listSchool[0][1]
        return listSchool
    else:
        ipLength = 0
        index = 0
        for i, j in enumerate(listSchool):
            if len(j[1]) > ipLength:
                ipLength = len(j[1])
                index = i
        #print listSchool[i][0], listSchool[i][1]
        return listSchool[i]
        
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

    school = readIP('school.csv', '140.127.36.8')
    print school[0][0], school[0][1], school[0][2]

if __name__ == '__main__':
    main()