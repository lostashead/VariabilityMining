import pandas as pd
import collections
import csv

de=pd.read_csv('ma1transition.csv',header=None)
df=pd.read_csv('anktransitition.csv',header=None)
dg=pd.read_csv('jabtransitition.csv',header=None)
dh=pd.read_csv('E91transitition.csv',header=None)
#li= de.values.astype(str).tolist()

excelread = 'Statransitiontable.xlsx'
table = pd.read_excel(excelread,header=None)
sttable = table.values.astype(str).tolist()

def tran(date,csv_file,csv2_file):
    li = date.values.astype(str).tolist()
    transition = []
    transition.append("Stop")

    length1 = len(li)
    length2 = len(sttable)
    length3 = table.shape[1]



    for i in range(length1):

        for j in range(length3):

         for k in range(length2):

                if sttable[0][j] in li[i] and sttable[k][0] == transition[len(transition)-1]:
                    # print("s")
                    transition.append(sttable[0][j])
                    transition.append(sttable[k][j])


                    break



    ## print(transition)


    print(len(transition))
    n=2
    # usecase number

    transition2 = [tuple(transition[n * i:n * i + n]) for i in range(len(transition) - n +1 )]


    export_list_csv(transition2, csv_file)
    transition3 = [tuple(transition[2 * i:2 * i + n]) for i in range(len(transition)//2-n+2)]
    for i in range(len(transition) // 2 - n + 2):
        transition3.append('()')


    c = collections.Counter(transition3)


    export_list_csv(c.most_common(), csv2_file)



def export_list_csv(export_list, csv_file):
    # csvファイルの作成
    with open(csv_file, "w") as f:
        writer = csv.writer(f, lineterminator='\n')
        # writer.writerow(export_list)

        # csvファイルに書き込み
        writer.writerows(export_list)

# tran(de,"ma1eventran.csv","ma1evencol.csv")
# tran(df,"ankeventran.csv","ankevencol.csv")
# tran(dg,"jabeventran.csv","jabevencol.csv")
# tran(dh,"E91eventran.csv","E91evencol.csv")
#date,遷移列化,遷移列化の統計

tran(de,"vaimport/ma1eventran.csv","ma1evencol.csv")
tran(df,"vaimport/ankeventran.csv","ankevencol.csv")
tran(dg,"vaimport/jabeventran.csv","jabevencol.csv")
tran(dh,"vaimport/E91eventran.csv","E91evencol.csv")
#date,遷移列化,遷移列化の統計


