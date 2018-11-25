import numpy as np

changes = []
DP = []
word1_g = ''
word2_g = ''
g_flg=0

def find_op(i,j,c_list):
    flg=0
    global changes
    if i==0 and j==0:
        changes+=c_list
        return
    if i>0 and DP[i][j]==DP[i-1][j]+1:
        flg=1
        c_list.append('i-'+str(j)+'-'+word2_g[i-1])
        find_op(i-1,j,c_list)
        c_list.pop()
    if j>0 and DP[i][j]==DP[i][j-1]+1:
        flg=1
        c_list.append('d-'+str(j-1)+'-'+word1_g[j-1])
        find_op(i,j-1,c_list)
        c_list.pop()
    if i>0 and j>0:
        if DP[i][j]==DP[i-1][j-1]+1:
            c_list.append('s-'+str(j-1)+'-'+word1_g[j-1]+'-'+str(i-1)+'-'+word2_g[i-1])
            find_op(i-1,j-1,c_list)
            c_list.pop()
        elif flg==0:
            find_op(i-1,j-1,c_list)

def get_oper(word1,word2):
    global DP,word1_g,word2_g, changes 
    changes = []
    DP = np.zeros((len(word2)+1,len(word1)+1))
    word1_g = word1
    word2_g = word2
    for i in range(len(word1)+1):
        DP[0][i] = i
    for i in range(len(word2)+1):
        DP[i][0] = i

    for j in range (1,len(word1)+1):
        for i in range (1,len(word2)+1):
            if word1[j-1] != word2[i-1]:
                DP[i][j] = min(DP[i-1][j],DP[i][j-1],DP[i-1][j-1])+1
            else:
                DP[i][j] = DP[i-1][j-1]
    i = len(word2)
    j = len(word1)
    c_list = []
    find_op(i,j,c_list)
        
    return changes

# print get_oper('ser','anwser') 