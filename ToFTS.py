from csv import reader
import sys
import re
import copy
import collections
import pandas as pd
import csv

data = pd.read_excel('astah.xlsx', 'Sheet1', index_col=None)
data.to_csv('astah.csv', encoding='shift_jis', index=False)

#astah.csvの処理
with open('astah.csv', 'r') as f:
    s = f.read()
s = s.replace('STOP', '0x00').replace('PLAYING', '0x01').replace('PLAY', '0x44').replace('PAUSE', '0x46').replace('FWD', '0x4b').replace('BWD', '0x4c')
with open('astah.csv', 'w') as f:
    f.write(s)

#AE.csvの処理
with open('vaexport/AE.csv', 'r') as f:
    s = f.read()
s = s.replace('[', '(').replace(']', ')')
with open('vaexport/AE1.csv', "w") as f:
    f.write(s)

#XE.csvの処理
with open('vaexport/XE.csv', 'r') as f:
    s = f.read()
s = s.replace('[', '(').replace(']', ')')
with open('vaexport/XE1.csv', "w") as f:
    f.write(s)

#AE，XE．astahのリスト化
with open('vaexport/AE1.csv', 'r') as csv_file:
    csv_reader = reader(csv_file)
    l = list(csv_reader)

with open('astah.csv', 'r') as csv_file2:
    csv_reader2 = reader(csv_file2)
    l2 = list(csv_reader2)

with open('vaexport/XE1.csv', 'r') as csv_file3:
    csv_reader3 = reader(csv_file3)
    l3 = list(csv_reader3)

#fdict = {'stop,pause':'f1','stop,play':'f2','stop,fwd':'f3','stop,bwd':'f4','playing,pause':'f5','playing,play':'f6','playing,fwd':'f7','playing,bwd':'f8'}
#すべての遷移にフィーチャ名を割り当てる
fdict = {"('0x00', '0x46')":'f1',"('0x00', '0x44')":'f2',"('0x00', '0x4b')":'f3',"('0x00', '0x4c')":'f4',"('0x01,0x46')":'f5',"('0x01', '0x44')":'f6',"('0x01', '0x4b')":'f7',"('0x01', '0x4c')":'f8'}

#astahの出力された表を基に辞書を作成する
ll1 = []
ll2 = []
ll1 = l2[0]
for row in l2:
    ll2.append(row[0])

del ll1[0:2]
del ll2[0:2]
keys = []
values = []
for line in ll1:
    for row in ll2:
        keys.append((row,line))

for j in range(2,len(ll1)+2):
    for i in range(2,len(ll2)+2):
        values.append((l2[i][j]))
table = dict(zip(keys, values))
#print(table)

#AE.csvが空の時の処理
if not l[0]:
    print("AE.csvが空です")

elif not l:
    print("AE.csvが空です")

#fdictのvalueをAE.csvに合わせて書き換える
else:
    #print(l)
    for AEskip in l:
        if len(AEskip[0]) <=16:
            print(str(AEskip) + "は値がペアではないためスキップされ,削除されました")
            l.remove(AEskip)
    l = str(l).replace('], [', ']/,[').replace('],[', ']/,[').replace('[', '').replace(']', '').replace('"', '')
    l = l.split('/,')
    l = tuple(l)
    AEnum = 1
    for AErabel in l:
        AErabel = eval(AErabel)
        #print(AErabel)
        #if AErabel[0][0] == '0':
            #print(str(AErabel) + "は値がペアではないためスキップされ,削除されました")
            #list(l).remove('{0}'.format(AErabel))
            #continue
        for arabel in AErabel:
            fdict['{0}'.format(arabel)] = 'A' + str(AEnum)
        AEnum +=1
    #print(fdict)
#AE.csvに合わせてラベル付けをする
    #print(l)
    l = str(l).replace('"', '').replace('), (', '),/(').replace('),(', '),/(').replace('((', '(').replace('))', ')')
    #print(l)
    l = l.split(',/')
    l = tuple(l)
    for a in l:
        a = eval(a)
        #print(a)
        #print(keys)
        if a in keys:
            table[a] = (table[a] + '/' + fdict['{0}'.format(a)])
            #print(fdict['{0}'.format(a)])

#XE.csvが空の時の処理
if not l3:    
    print("XE.csvが空です")

elif not l3[0]:
    print("XE.csvが空です")

#fdictのvalueをXE.csvに合わせて書き換える
else:
    #print(l3)
    l3 = str(l3).replace('\\t", "', '","').replace('[["', '["').replace('"]]', '"]').replace('\\t,', ',').replace('"], ["', '"],/["').replace('", "', '","')
    #print(l3)
    l3 = l3.split(',/')
    #print(l3)
    l3 = tuple(l3)
    #print(l3)
    for xe2 in l3:
        xe2 = eval(xe2)
        xe2 = tuple(xe2)
        #print(xe2[1])
        #print(l[3]==xe2[1])
        #print(fdict['{0}'.format(xe2[1])][0])
        if xe2[0] in l:
            #print(fdict['{0}'.format(xe2[1])][0])
            if '￢' not in fdict['{0}'.format(xe2[1])]:
                if '￢' not in fdict['{0}'.format(xe2[0])]:
                    fdict['{0}'.format(xe2[1])] = '￢' + fdict['{0}'.format(xe2[0])]
        if xe2[1] in l:
            #print(fdict['{0}'.format(xe2[0])][0])
            if '￢' not in fdict['{0}'.format(xe2[0])]:
                if '￢' not in fdict['{0}'.format(xe2[1])]:
                    fdict['{0}'.format(xe2[0])] = '￢' + fdict['{0}'.format(xe2[1])]
    print(fdict)

    for xrabel in l3:
        xrabel = eval(xrabel)
        for xrabel2 in xrabel:
            xrabel2 = eval(xrabel2)
            #print(xrabel2)
            if xrabel2 in keys:
                if fdict['{0}'.format(xrabel2)] not in table[xrabel2]:
                #if 'A' not in table[xrabel2]:
                    table[xrabel2] = (table[xrabel2] + '/' + fdict['{0}'.format(xrabel2)])
    
    for frabel in table.keys():
        if '/' not in table[frabel]:
            table[frabel] = (table[frabel] + '/' + fdict['{0}'.format(frabel)])
    #print(fdict)    
    #print(table)

#辞書（table）を基にExcelファイルを作成する
z = []
z2 = []
i = 0
j = 0
ll1.insert(0, '<None>')
ll1.insert(0, '状態/イベント')
ll2.insert(0, '開始疑似状態0')
ll2.insert(0, '状態/イベント')
l21 = []
l22 = []
i20 = 0
xy = []
for l20 in l2:
    if i20 == 0:
        l21 = l20
    if i20 == 1:
        l22 = l20
    i20 = i20+1

for y in ll2:
    i = 0
    for x in ll1:
        if j == 0:
            z2 = l21
        if j == 1:
            z2 = l22
        if j >=2:
            if i == 0:
                z2.append(y)
            if i == 1:
                z2.append('')
            if i >= 2:
                xy.append([y,x])
                fakelist = tuple(xy[0])
                z2.append(table[fakelist])
                xy = []
        i = i+1
    z.append(z2)
    z2 = []
    j = j+1

finalz = []
semifinalz = []
for zz1 in z:
    for zz2 in zz1:
        zz2 = zz2.replace('0x00', 'STOP').replace('0x01', 'PLAYING').replace('0x44', 'PLAY').replace('0x46', 'PAUSE').replace('0x4b', 'FWD').replace('0x4c', 'BWD')
        semifinalz.append(zz2)
    finalz.append(semifinalz)
    semifinalz = []

#ラベル付けされたExcelファイルを出力する
with open('astah2.csv', 'w', newline="") as f:
    writer = csv.writer(f)
    for tempz in finalz:
        writer.writerow(tempz)