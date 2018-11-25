import numpy as np
import sys
from word_spell_check0 import *
import copy
import string

k = 3 #k-gram

dict_word  = np.load("../data/Train/model/dictionary.npy").item() #Word Dictionary
dict_k = np.load("../data/Train/model/"+str(k)+"gram.npy").item() #K Gram Dictionary
dict_k1 = np.load("../data/Train/model/"+str(k-1)+"gram.npy").item() #K-1 Gram Dictionary
count_k = dict_k[max(dict_k, key=dict_k.get)]+ 10000
count_k1 =dict_k1[max(dict_k1, key=dict_k1.get)] + 10000

def get_prob(sentence):
    str1 = ' '.join(sentence[:-1])
    str2 = ' '.join(sentence)
    if str1 in dict_k1:
        count1 = dict_k1[str1]
    else:
        count1 = count_k1
    if str2 in dict_k:
        count2 = dict_k[str2]
    else:
        count2 = 1
    return np.log(float(count2)/count1)

def k_gram_prob():
    final_prob=0
    for i in range(k,len(sentence)+1):
        final_prob += get_prob(sentence[i-k:i])
    return final_prob

def non_word_check(i):
    global sentence
    tmp = copy.deepcopy(sentence)
    cand_list = dospellCheck(sentence[i])
    sen_prob = []
    for j in range(len(cand_list)):
        sentence[i] = cand_list[j]
        sen_prob.append(k_gram_prob());
    sen_prob = np.array(sen_prob)
    sen_order = sen_prob.argsort()
    sen_order = sen_order[::-1]
    print tmp[i]+"\t"+cand_list[sen_order[0]]+"\t"+cand_list[sen_order[1]]+"\t"+cand_list[sen_order[2]]

def word_check():
    global sentence
    sentences = []
    arg_val = []
    tmp = copy.deepcopy(sentence)
    for i in range(len(sentence)):
        sen_prob = []
        sentence = copy.deepcopy(tmp)
        cand_list = dospellCheck(sentence[i])
        if sentence[i] not in cand_list:
            cand_list.append(sentence[i])
        for j in range(len(cand_list)):
            sentence[i]  = cand_list[j]
            sen_prob.append(k_gram_prob());
        sen_prob = np.array(sen_prob)
        sen_order = sen_prob.argsort()
        sen_order = sen_order[::-1]
        sentences.append([cand_list[sen_order[0]],cand_list[sen_order[1]],cand_list[sen_order[2]]])
        arg_val.append(sen_prob[sen_order[0]])
    a_max = np.argmax(arg_val)
    sentence = copy.deepcopy(tmp)
    print sentence[a_max]+"\t"+sentences[a_max][0]+"\t"+sentences[a_max][1]+"\t"+sentences[a_max][2]

file = open(sys.argv[1],"r")
lines = file.readlines()
for sentence in lines:
    sentence = sentence.lower()
    sentence = sentence.translate(None,string.punctuation)
    #print sentence
    sentence = sentence.split()
    sentence = [s.strip(' \t\n\r') for s in sentence]
    flag = 1
    for i in range(len(sentence)):
        if sentence[i] not in dict_word:
            # print 'aa'
            non_word_check(i)
            flag = 0
        if flag == 0:
            break
    if flag==1:
        # print 'aa'
        word_check()
#Done!
