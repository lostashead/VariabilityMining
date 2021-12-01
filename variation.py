# -*- coding: utf-8 -*-
import sys
import itertools
import re
import csv
# import pandas as pd
import copy
import collections
import csv
import os
import glob
import shutil

#----------各ディレクトリを作成------------
os.makedirs('vaexport', exist_ok=True)
os.makedirs('vamatrix', exist_ok=True)
#----------vaimport内の遷移列のファイルを番号ファイルへと変換------------
dirs = []
dirnum = 1
dirs.extend(glob.glob('vaimport/*.csv'))
#プリントして先頭から順番を表示する
for dir1 in dirs:
    print(str(dirnum)+':'+dir1)
    os.rename(dir1,f'vaimport/{dirnum}.csv')
    dirnum = dirnum+1

print('製品数numを入力:')
num = input()
tr0x = []
r = {}
for i in range(int(num)):
    #----------ここからvariation_group_OP.csvを作成するプログラム------------
    with open(f'vaimport/{i+1}.csv') as t:
        reader = csv.reader(t)
        tr = [row for row in reader]
        #print(tr)
        #print('\n\n')
        #読み込んだcsvの系列から空白と重複を削除する
        def get_unique_list(seq):
            seen = []
            return[x for x in seq if x not in seen and not seen.append(x) and x != [] ]
    #print(type(tr))
    #tr内をすべて小文字にする
    ogtr2 = []
    for ogtr in tr:
        if '' in ogtr:
            ogtr.remove('')
        ogtr = list(map(str.lower,ogtr))
        ogtr2.append(ogtr)
    ogtr2 = get_unique_list(ogtr2)
    #print(ogtr2)
    #print('\n\n')

    #状態[(stopping,0x00),(playing,0x01),(paused,0x02),(fwd_seek,0x03),(rev_seek,0x04),(error,0xFF)]
    #イベント[(play,0x44),(pause,0x46),(forward,0x4b),(backward,0x4c),(volume,0x0d)]
    stdict = {"stop":'0x00', "Stop":'0x00', "playing":'0x01', "Playing":'0x01', "paused":'0x02', "fwd_seek":'0x03', "rev_seek":'0x04', "error":'0xFF'}
    evdict = {"play":'0x44', "Play":'0x44', "pause":'0x46', "Pause":'0x46',"forward":'0x4b',"FWD":'0x4b',"fwd":'0x4b',"backward":'0x4c',"BWD":'0x4c',"bwd":'0x4c',"volume":'0x0d'}
    #重複を削除したリストからディクショナリを参照して0x00の形式に変換する
    k = 0
    for temptr in ogtr2:
        if len(temptr)<2:
            continue
        else:
            r["i"+str(i)+"k"+str(k)] = ([stdict[temptr[0]],evdict[temptr[1]]])
            #print(("i"+str(i)+"k"+str(k)))
            #print(r["i"+str(i)+"k"+str(k)])
            #print('\n\n')
            if ([stdict[temptr[0]],evdict[temptr[1]]]) not in tr0x:
                tr0x.append([stdict[temptr[0]],evdict[temptr[1]]])
            else:
                pass
            k = k+1
    #print(tr0x)
    #print('\n\n')

#以上の情報からvariation.csvを作成する
#iの値によって新たなリストを作って比較する
for i in range(int(num)):
    templist = []
    k=0
    for y in range(int(len(r))):
        if ("i"+str(i)+"k"+str(k)) in r:
            templist.append(r["i"+str(i)+"k"+str(k)])
            k=k+1
        else:
            pass
    for j in tr0x:
        if j in templist:
            r["i"+str(i)+"k"+str(tr0x.index(j))] = 1
        else:
            r["i"+str(i)+"k"+str(tr0x.index(j))] = 0


#for i in range(int(num)):
    #k=0
    #for j in tr0x:
        #if ("i"+str(i)+"k"+str(k)) in r:
            #print((["i"+str(i)+"k"+str(k)]))
            #print(j)
            #print(r["i"+str(i)+"k"+str(k)])
            #print('\n\n')
            #if j == r["i"+str(i)+"k"+str(k)]:
                #r["i"+str(i)+"k"+str(k)] = 1
                #k = k+1
            #else:
                #r["i"+str(i)+"k"+str(k)] = 0
                #k = k+1
        #else:
            #pass

# iは製品数kは可変性．rはディクショナリ
# 新しいKは最後に足されていくからkの最大値に合わせて0の代入もする
# 書き込み用のリストを作成する
writelist = []
writelist2 = []
k=0
for tempk in range(len(tr0x)):
    for tempi in range(int(num)):
        if ("i"+str(tempi)+"k"+str(tempk)) not in r:
            r["i"+str(tempi)+"k"+str(tempk)] = 0
        else:
            pass
        writelist2.append(r["i"+str(tempi)+"k"+str(tempk)])
    writelist2.insert(0,tr0x[k])
    #print(writelist2)
    #print('\n\n')
    writelist.append(writelist2)
    writelist2 = []
    k=k+1

for tempwl in writelist:
    tempwl.insert(1,100)

#print(writelist)
#print('\n\n')

with open('vamatrix/variation_group_OP.csv','w',newline="") as va:
    writer = csv.writer(va)
    for templist in writelist:
        writer.writerow(templist)
va.close()




#----------ここからvariation_group_OP.csvを読み込んで可変性情報を出力するプログラム------------


# a = [[('0x0d', '0x44'), 1.88],[('0x4c', '0x46'), 4.03]]
# a[0].append(1)
# print(a)

with open('vamatrix/variation_group_OP.csv') as f:
    reader = csv.reader(f)
    l = [row for row in reader]

#print(l)

#バリエーションの数をnに格納
n = len(l[0])-2
# by小山さんprint(l[0])

#CEがlのリストの何番目にあるのか数える変数
lc = 0
ce = []
for a in l:
    c = 0
    for b in range(n):
        b = b + 2
        # print(a[b])
        if a[b] == "1":
            c = c + 1
            # print(c)
        
        #全ての製品でイベント系列が存在する場合
        if c == n:
            print("CEは"+a[0]+"です")
            ce.append([a[0]])
            a.clear()
    lc = lc + 1
with open('vaexport/CE.csv','w',newline="") as CE_file:
    writer = csv.writer(CE_file)
    for ce2 in ce:
        writer.writerow(ce2)
CE_file.close()

# print(lc)
# for a in l:
# print(a)

l2 = []
l3 = []
moji =""

for a in l:
    for b in range(n):
        b = b + 2
        #リストが空でなければ
        if a:
            # print(a[b])
            moji = moji + a[b]
    
    # print(moji)
    #リストが空でなければ
    if a:
        l2.append([a[0],moji])
        l3.append([a[0],moji])
    
    moji =""

#print(l2)
#print('\n\n')
#print(l3)
#print('\n\n')
#print('\n\n')
#----------ここからAEを特定するプログラム------------
AE = []
ra = len(l2)
moji2 = ""

for a in l2:
    #aが空でない場合
    if a:
        for t in range(ra):
            if a[0] != l2[t][0]:
                if a[1] == l2[t][1]:
                    
                    moji2 = moji2 + l2[t][0] +","
                    l2[t].clear()
                    l2[t].append("1")
                    l2[t].append("1")
                    l2[t].append("1")
                    # print("AEは"+a[0],l2[t][0]+"です")
    
    moji2 = moji2 + str(a[0])
    AE.append(moji2)
    # print(l2)

    moji2 = ""

# AE.remove('AEは1')
#ダミーを削除
for a in AE[:]:
    print(a)
    if len(a) <= 17:
        AE.remove(a)
    elif a == '1':
        AE.remove(a)
print(AE)


AEwrite = []
for a in AE:
    #print(len(a))
    #if len(a) > 15:
    print("AEは"+a)
    AEwrite.append([a.replace("AEは",'')])

with open('vaexport/AE.csv','w',newline="") as AE_file:
    writer = csv.writer(AE_file)
    for AEwrite2 in AEwrite:
        writer.writerow(AEwrite2)
AE_file.close()


#---------ここからXEを特定するプログラム------------
l4 = []
print('\n\n')
for pair in itertools.combinations(l3, 2):
    l4.append(list(pair))


XE = []
for a in l4:
    XEnum = 0
    x1 = a[0][1]
    x2 = a[1][1]

    for valen in range(n):
        #print(valen)
        valen = valen +1
        if x1[XEnum:valen] != x2[XEnum:valen]:
            XEnum = XEnum +1
        
    if XEnum == n:
        print("XEは"+a[0][0]+"と"+a[1][0]+"のペアです")
        XE.append([a[0][0],a[1][0]])


    #if x1[0:1] != x2[0:1]:
        #if x1[1:2] != x2[1:2]:
            #if x1[2:3] != x2[2:3]:
                #if x1[3:4] != x2[3:4]:
                    #print("XEは"+a[0][0]+"と"+a[1][0]+"のペアです")
                    #XE.append([a[0][0],a[1][0]])
with open('vaexport/XE.csv','w',newline="") as XE_file:
    writer = csv.writer(XE_file)
    for XE2 in XE:
        writer.writerow(XE2)
XE_file.close()

