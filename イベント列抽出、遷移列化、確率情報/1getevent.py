import pandas as pd
import csv
excelread = 'Book2.xlsx'
st1 = pd.read_excel(excelread, usecols=[0])
st1_li = st1.values.astype(str).tolist()
state1_li = []
for s_li in st1_li:
    state1_li.append(s_li[0])

de=pd.read_csv('m1fac.csv',header=None)
df=pd.read_csv('ankfac.csv',header=None)
dg=pd.read_csv('jabfac.csv',header=None)
dh=pd.read_csv('E91fac.csv',header=None)


def tran(DataFrame,csv_file):
    li= DataFrame.iloc[:,6].values.astype(str).tolist()

    transition = []
    row=len(DataFrame)
    col=len(DataFrame.columns)

    event_li = []
    for s_li in li:
        event_li.append(s_li)



    length=len(event_li)
    print(len(state1_li))
    print(event_li)
    print(state1_li)
    k = 0




    for i in range(len(event_li)):


          for j in range(len(state1_li)):

             if state1_li[j] in event_li[i]:
                 k+=1
                 if k % 4 == 0:
                  transition.append(state1_li[j])
                  break
          continue

    print(transition)
    transition = pd.Series(transition)
    transition.to_csv(csv_file, index=False)




tran(de,"ma1transition.csv")
tran(df,"anktransitition.csv")
tran(dg,"jabtransitition.csv")
tran(dh,"E91transitition.csv")



#transition=pd.Series(transition)
#transition.to_csv('maftransition.csv',index=False)