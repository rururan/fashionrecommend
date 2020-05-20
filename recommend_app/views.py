from __future__ import absolute_import
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView,CreateView,DetailView
from . import forms
import re
import numpy as np
from bs4 import BeautifulSoup
import requests
import pandas as pd
import collections
from . import helpers


class IndexView(TemplateView):
    template_name="recommend_app/index.html"

def input(request,*args,**kwargs):
    flag = True
    page = 1
    BrandList = []
    NameList = []
    selectlist=[]
    
    
    set_menslist=request.session.get("set_menslist")
    if set_menslist:
        params={"set_menslist":set_menslist}
        return render(request,"recommend_app/input.html", params)

    

    while flag:
        URL = 'https://www.fashion-press.net/snaps/sex/mens?page=' + str(page)
        soup = helpers.openURL(URL)
        snaps = soup.find_all('div',attrs={'class': 'fp_media_tile snap_media col_3'})

        if len(snaps) != 0:  # 写真がある場合はブランドを取得
            tmpBrandList = helpers.getBrandList(snaps)
            BrandList.extend(tmpBrandList)
            selectlist.extend(helpers.getselectlist(snaps))
            NameList.extend(helpers.getNameList(snaps))
            # print('get page' + str(page))
            page += 1

        else:  # 写真がない場合は終了
            flag = False
            # print('END')

    df = pd.DataFrame(data=BrandList, index=NameList)  # pandasのDataFrame型に
    df.to_csv('StreetSnapMen.csv')
    # df = pd.read_csv('StreetSnapMen.csv', index_col = 0)

    elementlist=list(helpers.flatten(selectlist))
    set_menslist=list(set(elementlist))
    set_menslist.sort()
    params={"set_menslist":set_menslist}
    request.session["set_menslist"]=set_menslist
    request.session.set_expiry(86400)

    return render(request,"recommend_app/input.html", params)

def input_women(request,*args,**kwargs):
    flag = True
    page = 1
    BrandList = []
    NameList = []
    selectlist=[]


    set_womenslist=request.session.get("set_womenslist")
    if set_womenslist:
        params={"set_womenslist":set_womenslist}
        return render(request,"recommend_app/input_women.html", params)


    while flag:
        URL = 'https://www.fashion-press.net/snaps/sex/womens?page=' + str(page)
        soup = helpers.openURL(URL)
        snaps = soup.find_all('div',attrs={'class': 'fp_media_tile snap_media col_3'})

        if len(snaps) != 0:  # 写真がある場合はブランドを取得
            tmpBrandList = helpers.getBrandList(snaps)
            BrandList.extend(tmpBrandList)
            selectlist.extend(helpers.getselectlist(snaps))
            NameList.extend(helpers.getNameList(snaps))
            # print('get page' + str(page))
            page += 1

        else:  # 写真がない場合は終了
            flag = False
            # print('END')

    df = pd.DataFrame(data=BrandList, index=NameList)  # pandasのDataFrame型に
    df.to_csv('StreetSnapWomen.csv')
    # df = pd.read_csv('StreetSnapWomen.csv', index_col = 0)

    elementlist=list(helpers.flatten(selectlist))
    set_womenslist=list(set(elementlist))
    set_womenslist.sort()
    params={"set_womenslist":set_womenslist}
    request.session["set_womenslist"]=set_womenslist
    request.session.set_expiry(86400)

    return render(request,"recommend_app/input_women.html", params) 
    
def result(request,*args,**kwargs):
    if request.method=="GET":
        selectbrand={
            "name":request.GET.get('name')
            } 
        
        df = pd.read_csv('StreetSnapMen.csv', index_col = 0) #データ読み込み
        brand = helpers.getuniqueList(df)
        brand_df = pd.DataFrame(index=list(brand.keys()),data=list(brand.values()))
        brand_df = brand_df.drop(np.nan) # NAN　を削除

        recommend=helpers.predict(df, brand_df, selectbrand["name"], k=3)

        params={"recommend":recommend}
        return render(request,"recommend_app/result.html",params)

    else:
        return render(request,"recommend_app/result.html")

def result_women(request,*args,**kwargs):
    if request.method=="GET":
        selectbrand={"name":request.GET.get('name')} 
        
        df = pd.read_csv('StreetSnapWomen.csv', index_col = 0) #データ読み込み
        brand = helpers.getuniqueList(df)
        brand_df = pd.DataFrame(index=list(brand.keys()),data=list(brand.values()))
        brand_df = brand_df.drop(np.nan) # NAN　を削除

        recommend=helpers.predict(df, brand_df, selectbrand["name"], k=3)

        params={"recommend":recommend}
        return render(request,"recommend_app/result_women.html",params)

    else:
        return render(request,"recommend_app/result_women.html")