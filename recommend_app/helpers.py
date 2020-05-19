# -*- coding: utf-8 -*-

import re

import numpy as np
from bs4 import BeautifulSoup
import requests
import pandas as pd
import collections

# URLからbs4オブジェクトを生成
def openURL(URL: int):
    res = requests.get(URL)
    
    if res.status_code != requests.codes.ok:
        print('Error')
        return(False) 
    
    return BeautifulSoup(res.text,'lxml')


# bs4オブジェクトから着用ブランドのリストを取得
def getBrandList(snaps):
    BrandList = []
    for snap in snaps:
        BrandList.append(list(set(map(lambda x: x.text, snap.find_all(
            'a', attrs={'href': re.compile('^/snaps/brand')})))))
    return BrandList

def getselectlist(snaps):
    selectlist=[]
    for snap in snaps:
        selectlist.append(list(map(lambda x: x.text, snap.find_all(
            'a', attrs={'href': re.compile('^/snaps/brand')}))))
    return selectlist

# 多次元配列の平坦化リスト
def flatten(l):
    for el in l:
        if isinstance(el,collections.abc.Iterable) and not isinstance(el,(str,bytes)):
            yield from flatten(el)
        else:
            yield el


# bs4オブジェクトから名前を取得
def getNameList(snaps):
    NameList = []
    for snap in snaps:
        title=snap.find('a')['title']
        NameList.append(title)
    return NameList
 

def getuniqueList(df):
    uniqueList = []

    for columns in df.columns.values:
        uniqueList.extend(df[columns])

    return collections.Counter(uniqueList)

def bays(model, A, B=None):
    pB = (model == B).sum().sum()
    pAB = (((model == A) | (model == B)).sum(axis=1) > 1).sum()
    return pAB / pB


def predict(df, brand_df, wear, k=3):
    prob = []

    for brand in brand_df.index:
        prob.append(bays(df, brand, wear))

    best_k = sorted(range(len(prob)), key=lambda i: prob[i], reverse=True)[:k]
    return list(map(lambda k: brand_df.index[k], best_k))


def bays2(model, A, B):
    pB = model == 'xxx'
    for bi in B:
        pB =  pB | (model == bi)

    pAB =  (((model == A) | pB ).sum(axis = 1) > len(B)).sum()
    return  pAB /     (pB.sum(axis = 1) > len(B) -1).sum()


def predict2(df, brand_df, wear, k = 15):
    prob = []

    for brand in brand_df.index:
        prob.append(bays2(df, brand, wear))

    best_k = sorted(range(len(prob)), key=lambda i: prob[i], reverse=True)[:k]
    return list(map(lambda k:brand_df.index[k], best_k))
