import sys
import os
from itertools import combinations
from collections import OrderedDict

def ReadFileAndReturnFrequentTuple(filepath,numberOfTuple,itemDictionary,candidatetuples):
    allbaskets = open(filepath, 'r')
    for basket in allbaskets:
        possibletupleInBasket=combinations(sorted([itemDictionary[item] for item in basket.split()]), numberOfTuple)
        for tupleSet in possibletupleInBasket :
            if tupleSet in candidatetuples:       
                counting=candidatetuples[tupleSet]
                candidatetuples[tupleSet] = counting + 1

    allbaskets.close()
    #return frequent tupple
    return dict((tupleSet, tuplecount) for tupleSet, tuplecount in candidatetuples.items() if tuplecount >= support),candidatetuples


cwd = os.getcwd()
filepath =cwd+"/browsing.txt"

index=0
support=100
itemIdDictionary={}
candidateItems={}
print("Pass 1: Read baskets and count in main memory the occurrences of each individual item")
transcations= open(filepath,'r')
for transaction in transcations:
    for item in transaction.split():
        if item in itemIdDictionary:
            intid=itemIdDictionary[item]
            countitems=candidateItems[intid][1]
            countitems=countitems+1
            candidateItems[intid]=(item,countitems)
        else:
            itemIdDictionary[item]=index
            candidateItems[index]=(item,1)
            index=index+1
transcations.close()

#prune non frequent items
frequentItems = sorted([itemid  for itemid, itemcount in candidateItems.items() if itemcount[1] >=support ])
print("Frequent Items")
print(frequentItems)

print("Pass 2 : Read baskets again and count in ")
candidatepairs=dict((item,0) for item in combinations(sorted(frequentItems),2) )
frequentpairs,candidatepairs= ReadFileAndReturnFrequentTuple(filepath,2,itemIdDictionary,candidatepairs)
print("Frequent Pairs")
print(frequentpairs)

print("Pass 3")
candidateThreeTuple = dict((tupleItem,0) for tupleItem in combinations(sorted(set([item for pair in frequentpairs for item in pair])),3) if ((tupleItem[0],tupleItem[1]) in frequentpairs and (tupleItem[1],tupleItem[2]) in frequentpairs ) )
frequentthreeTupple,candidateThreeTuple= ReadFileAndReturnFrequentTuple(filepath,3,itemIdDictionary,candidateThreeTuple)
print("Frequent Tuple")
print(frequentthreeTupple)

confidencePair={}
for pair,count in frequentpairs.items():
    supportA = candidateItems[pair[0]][1]
    supportB = candidateItems[pair[1]][1]
    supportAUnionB = count
    A=candidateItems[pair[0]][0]
    B=candidateItems[pair[1]][0]
    confidencePair[(A,B)]= supportAUnionB/ supportA
    confidencePair[(B,A)] = supportAUnionB/supportB
confidencpairindesc = OrderedDict(sorted(confidencePair.items(),
                                  key=lambda kv: kv[1], reverse=True))

print("Top 5 rules with confidence score")
print(confidencpairindesc)


confidenceTuple={}
for tupleitem,count in frequentthreeTupple.items():
    for pair in combinations(tupleitem,2):
        pairA =pair
        itemB=[item  for item in tupleitem if item not in pair]
        #print(pair)
        #print(tupleitem)
        #print(itemB)
        supportA = candidatepairs[pairA]
        supportB = candidateItems[itemB[0]][1]
        supportAUnionB = count
        A1=candidateItems[pairA[0]][0]
        A2=candidateItems[pairA[1]][0]
        B=candidateItems[itemB[0]][0]
        confidenceTuple[((A1,A2),B)]= supportAUnionB/ supportA
        confidenceTuple[(B,(A1,A2))] = supportAUnionB/supportB

confidenceTupleindesc = OrderedDict(sorted(confidenceTuple.items(),
                                   key=lambda kv: kv[1], reverse=True))

print("Top 5 rules with confidence score")                   
print(confidenceTupleindesc)



