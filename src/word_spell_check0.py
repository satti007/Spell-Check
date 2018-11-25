import sys
import numpy as np
import pandas as pd
from operations import *
from metaphone import doublemetaphone

def getEdit1Words(word):
	alphabets    = 'abcdefghijklmnopqrstuvwxyz'
	dels = [word[:i] + word[i+1:] for i in range(len(word))]
	subs = [word[:i] + c+ word[i+1:]   for i in range(len(word)) for c in alphabets]
	ins  = [word[:i] + c+ word[i:]   for i in range(len(word)+1) for c in alphabets]
	
	return list(set(dels + subs + ins))

def getEDCW(word,word_dict):
	EDCW_to_ED = {}
	edit1_words = getEdit1Words(word)
	edit2_words = list(set([e2 for e1 in edit1_words for e2 in getEdit1Words(e1)]))
	edit2_words = list(set(edit2_words)-set(edit1_words))
	candidate_words1 = [W for W in edit1_words if W in word_dict]
	EDCW_to_ED.update({W:1 for W in candidate_words1})
	candidate_words2 = [W for W in edit2_words if W in word_dict]
	EDCW_to_ED.update({W:2 for W in candidate_words2})
	
	return EDCW_to_ED,EDCW_to_ED.keys()

def editDistance(word1,word2):
	m,n = len(word1),len(word2)
	ed = [[0 for i in range(n+1)] for i in range(m+1)]
	
	for i in range(m+1):
		for j in range(n+1):
			if i == 0:
				ed[i][j] = j 
			elif j == 0:
				ed[i][j] = i  
			elif word1[i-1] == word2[j-1]:
				ed[i][j] = ed[i-1][j-1]
			else:
				ed[i][j] = 1 + min(ed[i][j-1],ed[i-1][j],ed[i-1][j-1])
	
	return ed[m][n]

def getBCW(word,word_dict,bigram_to_words,threshold,EDCW):
	bigrams = list(set([word[i]+word[i+1] for i in range(len(word)-1)]))
	word_bigrams = []
	for i in range (len(bigrams)):
		for j in range(i+1,len(bigrams)):
			word_bigrams = list(set(word_bigrams).union(set(bigram_to_words[bigrams[i]]).intersection(bigram_to_words[bigrams[j]])))
	
	word_bigrams = list(set(word_bigrams)-set(EDCW))
	BCW = {}
	BCW.update({W:editDistance(word,W) for W in word_bigrams if editDistance(word,W) < 4})
	
	return BCW,BCW.keys()

def spellCheck(word,word_dict,word_to_freq,bigram_to_words,threshold):
	EDCW_to_ED,EDCW =  getEDCW(word,word_dict)
	BCW_to_ED, BCW  =  getBCW(word,word_dict,bigram_to_words,threshold,EDCW)
	CW   =  list(set(EDCW).union(BCW))
	BCW_to_ED.update(EDCW_to_ED)
	word_to_freq.update({W:1.1 for W in CW if W not in word_to_freq})
	ranking = {W:word_to_freq[W]/float(3**BCW_to_ED[W]) for W in CW}
	CW.sort(key=lambda x: ranking[x])
	CW.reverse()
	
	return CW[:50], BCW_to_ED

def noisyChannel(oper_sug,SW_to_ED,con_mats,word_to_freq,letter_to_freq,start_frequency,bi_to_freq):
	score = {}
	S,D,I = con_mats[0],con_mats[1],con_mats[2]
	for W in oper_sug:
		if ' ' in W:
			continue
		opers,loop,P = oper_sug[W],len(oper_sug[W])/SW_to_ED[W],0
		for l in range(loop):
			s,O = 1,opers[SW_to_ED[W]*l:SW_to_ED[W]*(l+1)]
			for o in O:
				c = o.split('-')
				if c[0] == 's':
					# s += np.log((S[ord(c[2])-97][ord(c[4])-97]+1.1)/float(letter_to_freq[c[2]]))
					s = s*(S[ord(c[2])-97][ord(c[4])-97]+1.1)/float(letter_to_freq[c[2]])
				if c[0] == 'd':
					if int(c[1]) == 0:
						i = 0
						C = start_frequency[W[int(c[1])-1]]
					else:
						i = ord(W[int(c[1])-1]) - 96
						C = bi_to_freq[W[int(c[1])-1:int(c[1])+1]]
					# s += np.log((D[i][ord(c[2])-97]+1.1)/float(C))
					s = s*(D[i][ord(c[2])-97]+1.1)/float(C)
				if c[0] == 'i':
					if int(c[1]) == 0:
						i = 0
						C = start_frequency[W[int(c[1])-1]]
					else:
						i = ord(W[int(c[1])-1]) - 96
						C = letter_to_freq[W[int(c[1])-1]]
					# s += np.log((I[i][ord(c[2])-97]+1)/float(C))
					s = s*(I[i][ord(c[2])-97]+1)/float(C)
			P += s
		score[W] = P*word_to_freq[W]
	
	return score

def phonetics(score,word):
	ph_score = {}
	err_mp = doublemetaphone(word)
	for W in score:
		W_mp = doublemetaphone(W)
		if err_mp[0] == W_mp[0]:
			ph_score[W] = score[W]*np.power(10,4)
		elif err_mp[0] == W_mp[1]:
			ph_score[W] = score[W]*np.power(10,2)
		elif err_mp[1] == W_mp[1]:
			ph_score[W] = score[W]*np.power(10,1)
		else:
			ph_score[W] = score[W]*np.power(10,0)
	
	return ph_score

train_path = '../data/Train/'
file_name = 'model/word_to_freq.npy'
word_to_freq = np.load(train_path+file_name).item()
file_name = 'model/dictionary.npy'
word_dict = np.load(train_path+file_name).item()
file_name = 'model/bigram_to_words.npy'
bigram_to_words = np.load(train_path+file_name).item()
threshold = 0.1
letter_to_freq   = np.load(train_path+'model/letter_to_freq.npy').item()
bi_to_freq       = np.load(train_path+'model/bi_to_freq.npy').item()
start_frequency  = np.load(train_path+'model/start_frequency.npy').item()
Sub_of_X_for_Y   = np.load(train_path+'model/Sub_of_X_for_Y.npy')
Del_of_Y_after_X = np.load(train_path+'model/Del_of_Y_after_X.npy')
Ins_of_Y_after_X = np.load(train_path+'model/Ins_of_Y_after_X.npy')
con_mats = [Sub_of_X_for_Y,Del_of_Y_after_X,Ins_of_Y_after_X]

def dospellCheck(word):
	suggestions,SW_to_ED = spellCheck(word,word_dict,word_to_freq,bigram_to_words,threshold)
	suggestions = [W for W in suggestions if '-' not in W]
	oper_sug    = {W:get_oper(W,word) for W in suggestions}
	score       = noisyChannel(oper_sug,SW_to_ED,con_mats,word_to_freq,letter_to_freq,start_frequency,bi_to_freq)
	meta_score  = phonetics(score,word) 
	keys = sorted(meta_score, key=meta_score.get)
	keys.reverse()
	
	return keys
