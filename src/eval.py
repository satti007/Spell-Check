import os
import time
import numpy as np

cmd1 = 'python word_spell_check.py ../data/Test/words_inter.in      > ../data/Test/test_words_inter.out' 
cmd2 = 'python phrase_check.py     ../data/Test/phrases_inter.in    > ../data/Test/test_phrases_inter.out' 
cmd3 = 'python phrase_check.py     ../data/Test/sentences_inter.in  > ../data/Test/test_sentences_inter.out'

cmds = [cmd1,cmd2,cmd3]
for i in range(3):
	print cmds[i]
	start_time = time.time()
	os.system(cmds[i])
	print "--- %s seconds ---" % (time.time() - start_time)
	print '################\n'
	
	if i==0:
		file = 'words'
	if i==1:
		file = 'phrases'
	if i==2:
		file = 'sentences'
	
	# print file	
	actual      = open('../data/Test/{}_inter.out'.format(file),'r').readlines()
	suggestions = open('../data/Test/test_{}_inter.out'.format(file),'r').readlines()
	MRR = 0
	for A,S in zip(actual,suggestions):
		A_words  = A.strip().split()
		S_words  = S.strip().split()
		mrr = 0
		for W in A_words[1:]:
			if W in S_words[1:]:
				mrr += 1.0/(S_words[1:].index(W)+1)
		MRR += mrr/(len(A_words) - 1)
	
	print round(MRR/len(actual),3)
	print '################\n'

# suggestions = open('../data/Test/Output/2.txt','r').readlines()
# word_to_suggestions = {}
# for S in suggestions:
# 	W = S.split('\t')
# 	word_to_suggestions[W[0]] = W[1:] 

# crct_to_wrng = np.load('../data/Test/Input/crct_to_wrng_1.npy').item()

# MRR = 0
# for key, W in crct_to_wrng.iteritems():
# 	if len(word_to_suggestions[W]) > 0:
# 		if key in word_to_suggestions[W]:
# 			mrr = word_to_suggestions[W].index(key) + 1
# 			MRR = MRR + 1.0/mrr
# 		else:
# 			mrr = 0
# 		print '{}:{}, {}  '.format(W,key,mrr)
		
# 	else:
# 		print 'No suggestions for {}'.format(crct_to_wrng[W])
# 	# break

# print MRR

'''
test_path = '../data/Test/'
files = ['1.txt', '2.txt', '3.txt']

crct_to_wrng = {}
for file in files:
	lines = open(test_path+'spell_errors/'+file,'r').readlines()
	crct_to_wrng.update({line.split(': ')[0]:line.split(': ')[1].split(' ')[0].strip('\n') for line in lines if '_' not in line})

np.save(test_path+'Input/crct_to_wrng_1.npy', crct_to_wrng)
'''