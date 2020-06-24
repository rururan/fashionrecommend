from __future__ import absolute_import
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView,CreateView,DetailView
import re
import numpy as np
from bs4 import BeautifulSoup
import requests
import pandas as pd
import collections
from helpers import openURL,getBrandList,getselectlist,flatten,getNameList,getuniqueList
import csv


if __name__ =='__main__':
    flag = True
    page = 1
    BrandList = []
    NameList = []
    selectlist=[]
    

    while flag:
        URL = 'https://www.fashion-press.net/snaps/sex/mens?page=' + str(page)
        soup = openURL(URL)
        snaps = soup.find_all('div',attrs={'class': 'fp_media_tile snap_media col_3'})

        if len(snaps) != 0:  # 写真がある場合はブランドを取得
            tmpBrandList = getBrandList(snaps)
            BrandList.extend(tmpBrandList)
            selectlist.extend(getselectlist(snaps))
            NameList.extend(getNameList(snaps))
            # print('get page' + str(page))
            page += 1

        else:  # 写真がない場合は終了
            flag = False
            # print('END')

    df = pd.DataFrame(data=BrandList, index=NameList)  # pandasのDataFrame型に
    df.to_csv('StreetSnapMen.csv')
    # df = pd.read_csv('StreetSnapMen.csv', index_col = 0)

    elementlist=list(flatten(selectlist)) 
    set_menslist=list(set(elementlist))
    set_menslist.sort()
    
    with open("selectmenslist.csv","w")as f:
        writer = csv.writer(f)
        writer.writerow(set_menslist)