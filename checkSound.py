import numpy as np
import csv
import pprint
#音素解析に必要な情報の登録
lower=['ァ','ィ','ゥ','ェ','ォ','ャ','ュ','ョ','ッ','ン']
chars=[['ア','イ','ウ','エ','オ'],
['カ','キ','ク','ケ','コ'],
['サ','','ス','セ','ソ'],
['','シ'],
['タ','チ','ツ','テ','ト'],
['ナ','ニ','ヌ','ネ','ノ'],
['ハ','ヒ','','ヘ','ホ'],
['','','フ'],
['マ','ミ','ム','メ','モ'],
['ヤ','','ユ','','ヨ'],
['ラ','リ','ル','レ','ロ'],
['ワ'],
['ガ','ギ','グ','ゲ','ゴ'],
['ザ','ジ','ズ','ゼ','ゾ'],
['ダ','ヂ','ヅ','デ','ド'],
['バ','ビ','ブ','ベ','ボ'],
['パ','ピ','プ','ペ','ポ'],
['','','ヴ'],
['ー']]
lower=[c.encode() for c in lower]
chars=[[c.encode() if c!='' else c for c in k] for k in chars]
#ここまで
data=[['blandName','A','I','U','E','O','K','S','T','N','H','M','Y','R','W','濁','半濁','長','拗','促','撥']]
dataRaw=[0]*len(data[0])
lowerIndexToData={0:[1],1:[2],2:[3],3:[4],4:[5],5:[1,18],6:[3,18],7:[5,18],8:[19],9:[20]}
charIndexToData={0:[],1:[6],2:[7],3:[7],4:[8],5:[9],6:[10],7:[10],8:[11],9:[12],10:[13],11:[14],12:[6,15],13:[7,15],14:[8,15],15:[10,15],16:[10,16],17:[14,15],18:[17]}
dataDetail=[['blandName','A','I','U','E','O','K','S','SH','T','N','H','F','M','Y','R','W','G','Z','D','B','P','V','長','拗','促','撥']]
dataDetailRaw=[0]*len(dataDetail[0])
lowerIndexToDetail={0:[1],1:[2],2:[3],3:[4],4:[5],5:[1,24],6:[3,24],7:[5,24],8:[25],9:[26]}
f=open("brandName.txt",mode='r')
blandList=[s.strip() for s in f.readlines()]
for i in range(len(blandList)):
    temp=[0]*len(data[0])#'blandName','A','I','U','E','O','K','S','T','N','H','M','Y','R','W','濁','半濁','長','拗','促','撥'
    tempDetail=[0]*len(dataDetail[0])#'blandName','A','I','U','E','O','K','S','SH','T','N','H','F','M','Y','R','W','G','Z','D','B','P','V','長','拗','促','撥'
    blandData=open(blandList[i]+".txt",mode='r',encoding='utf-8')
    gameTitles=blandData.readlines()
    temp[0]=blandList[i]
    tempDetail[0]=blandList[i]
    totalPhonemes=0
    for title in gameTitles:
        for j,c in enumerate(title):
            tempIndex=[]
            tempDetailIndex=[]
            if c.encode() in lower:
                tempIndex+=lowerIndexToData[lower.index(c.encode())]
                tempDetailIndex+=lowerIndexToDetail[lower.index(c.encode())]
                totalPhonemes+=1.0
            else:
                for k,p in enumerate(chars):
                    if c.encode() in p:
                        tempIndex+=charIndexToData[k]
                        if k!=0:
                            tempDetailIndex.append(k+5)
                        totalPhonemes+=1.0
                        work=True
                        if i<len(title)-1:
                            if title[i+1] in lower:
                                work=False
                        if work:
                            tempIndex+=[p.index(c.encode())+1]
                            tempDetailIndex+=[p.index(c.encode())+1]
                            totalPhonemes+=1.0
                        break
            for l in tempIndex:
                temp[l]+=1.0
                dataRaw[l-1]+=1.0
            for l in tempDetailIndex:
                tempDetail[l]+=1.0
                dataDetailRaw[l-1]+=1.0
    dataRaw[len(dataRaw)-1]+=totalPhonemes
    dataDetailRaw[len(dataDetailRaw)-1]+=totalPhonemes
    temp=[str(np.round((k/totalPhonemes), 4)) if j!=0 else k for j,k in enumerate(temp)]
    tempDetail=[str(np.round((k/totalPhonemes), 4)) if j!=0 else k for j,k in enumerate(tempDetail)]
    data.append(temp)
    dataDetail.append(tempDetail)
    print(temp)
    print(tempDetail)
print(data)
print(dataDetail)
dataRaw=[str(np.round((dataRaw[j-1]/dataRaw[len(dataRaw)-1]), 4)) if j!=0 else '全体' for j in range(len(dataRaw))]
dataDetailRaw=[str(np.round((dataDetailRaw[j-1]/dataDetailRaw[len(dataDetailRaw)-1]), 4)) if j!=0 else '全体' for j in range(len(dataDetailRaw))]
data.append(dataRaw)
dataDetail.append(dataDetailRaw)
result=open("data.csv",'w',encoding='utf-8')
writer=csv.writer(result)
writer.writerows(data)
resultDetail=open("dataDetail.csv",'w',encoding='utf-8')
writer=csv.writer(resultDetail)
writer.writerows(dataDetail)