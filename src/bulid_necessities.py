import os
import numpy as np
import pandas as pd

def bulid_conf_matrix(train_path,file_name):
	one_edit_freq = pd.read_csv(train_path+file_name,sep=' ',header=None)
	
	Sub_of_X_for_Y   = np.zeros([26,26],dtype = int)
	Del_of_Y_after_X = np.zeros([27,26],dtype = int)
	Ins_of_Y_after_X = np.zeros([27,26],dtype = int)
	# Rev_of_XY		 = np.zeros([26,26],dtype = int)
	
	for index, row in one_edit_freq.iterrows():
		chars = row[0].split('|')
		count = int(row[1])
		oper = len(row[0]) + len(chars[0]) - 4 
		if oper == 0:
			if chars[0].lower().isalpha() and chars[1].lower().isalpha():
				Sub_of_X_for_Y[ord(chars[0].lower())-97][ord(chars[1].lower())-97] += count
		if oper == 1:
			if chars[0].lower().isalpha() and chars[1].lower().isalpha(): 
				Del_of_Y_after_X[ord(chars[0].lower())-96][ord(chars[1][1].lower())-97] += count
			elif chars[0] == '>'and chars[1][1].lower().isalpha():
				Del_of_Y_after_X[0][ord(chars[1][1].lower())-97] += count
		if oper == 2:
			if chars[0].lower().isalpha() and chars[1].lower().isalpha(): 
				Ins_of_Y_after_X[ord(chars[1].lower())-96][ord(chars[0][1].lower())-97] += count
			elif chars[1] == '>'and chars[0][1].lower().isalpha():
				Del_of_Y_after_X[0][ord(chars[0][1].lower())-97] += count
		# if oper == 3:
		# 	if chars[0].lower().isalpha() and chars[1].lower().isalpha(): 
		# 		Rev_of_XY[ord(chars[0][1].lower())-97][ord(chars[0][0].lower())-97] += count
			
	np.save(train_path+'model/Sub_of_X_for_Y.npy',Sub_of_X_for_Y)
	np.save(train_path+'model/Del_of_Y_after_X.npy',Del_of_Y_after_X)
	np.save(train_path+'model/Ins_of_Y_after_X.npy',Ins_of_Y_after_X)
	# np.save(train_path+'model/Rev_of_XY.npy',Rev_of_XY)

def word_freq_dict(train_path,file_name):
	word_freq = pd.read_csv(train_path+file_name,sep=' ',header=None)
	word_to_freq = {row[0]:row[1] for index, row in word_freq.iterrows()}
	np.save(train_path+'model/word_to_freq.npy', word_to_freq)

def bi_freq_dict(train_path,file_name):
	bi_freq = pd.read_csv(train_path+file_name,sep=' ',header=None)
	bi_to_freq = {row[0]:row[1] for index, row in bi_freq.iterrows()}
	np.save(train_path+'model/bi_to_freq.npy', bi_to_freq)

def readDictionary(train_path,folder_name):
	folder_path = train_path + folder_name
	files = os.listdir(folder_path)
	words = {}
	for file in files:
		lines = open(folder_path+'/'+file,'r').readlines() 
		W = [line.strip(' \r\n') for line in lines ]
		W = list(set(W)) 
		words.update({w:1 for w in W if w not in words})
	np.save(train_path+'model/dictionary.npy', words)

def bigram_to_words(word_dict):
	alphabets    = 'abcdefghijklmnopqrstuvwxyz'
	bigrams = [i+j for i in alphabets for j in alphabets]
	bigram_words = {bigram:[] for bigram in bigrams}
	word_to_bigrams = {word:[word[i]+word[i+1] for i in range(len(word)-1)] for word in word_dict}
	temp = {bigram_words[bigram].append(word) for bigram in bigrams for word in word_dict if bigram in word_to_bigrams[word]}
	np.save(train_path+'model/bigram_to_words.npy', bigram_words)
	np.save(train_path+'model/word_to_bigrams.npy', word_to_bigrams)

def trigram_to_words(word_dict):
	alphabets    = 'abcdefghijklmnopqrstuvwxyz'
	trigrams = [i+j+k for i in alphabets for j in alphabets for k in alphabets]
	trigram_words = {trigram:[] for trigram in trigrams}
	word_to_trigrams = {word:[word[i]+word[i+1]+word[i+2] for i in range(len(word)-2)] for word in word_dict}
	for trigram in trigrams:
		print trigram
		for word in word_dict:
			if trigram in word_to_trigrams[word]:
				trigram_words[trigram].append(word)
	
	np.save(train_path+'model/trigram_to_words.npy', trigram_words)
	np.save(train_path+'model/word_to_trigrams.npy', word_to_trigrams)

def start_frequency(train_path,file_name):
	start_freq = pd.read_csv(train_path+file_name,sep=',',header=None)
	start_to_freq = {row[0].lower():row[1] for index, row in start_freq.iterrows()}
	np.save(train_path+'model/start_frequency.npy', start_to_freq)

def letter_freq_dict(train_path,file_name):
	letter_freq = pd.read_csv(train_path+file_name,sep=',',header=None)
	letter_to_freq = {row[0].lower():row[1] for index, row in letter_freq.iterrows()}
	np.save(train_path+'model/letter_to_freq.npy', letter_to_freq)

train_path = '/home/satti/Documents/Sem8/NLP/PA1/data/Train/'
file_name = 'info/1edit_freq.csv'
bulid_conf_matrix(train_path,file_name)
file_name = 'info/word_freq.csv'
word_freq_dict(train_path,file_name)
file_name = 'info/2l_freq.csv'
bi_freq_dict(train_path,file_name)
file_name = 'info/1l_freq.csv'
letter_freq_dict(train_path,file_name)
file_name = 'info/start.csv'
start_frequency(train_path,file_name)
folder_name = 'info/Word_lists'
readDictionary(train_path,folder_name)
file_name = 'model/dictionary.npy'
word_dict = np.load(train_path+file_name).item()
bigram_to_words(word_dict)
trigram_to_words(word_dict)


'''
f = open(train_path,'r')
lines = f.readlines()
f.close()

f = open(train_path,'w')
for line in lines:
	if len(line.split(' ')) == 2:
		f.write(line)

f.close()

folder_name = 'info/Word_lists'
def readDictionary(train_path,folder_name):
	folder_path = train_path + folder_name
	files = os.listdir(folder_path)
	words = {}
	for file in files:
		lines = open(folder_path+'/'+file,'r').readlines() 
		W = [line.strip(' \r\n') for line in lines ]
		W = list(set(W)) 
		words = {w:1 for w in W if w not in words }
	np.save(train_path+'model/dictionary.npy', words)
'''