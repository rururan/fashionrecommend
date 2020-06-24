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
    
    with open("selectmenslist.csv","r") as f:
        for line in f:
            line = line.rstrip()
            set_menslist = line.split(",")

    #csvブランドリストをlist化する
    params={"set_menslist":set_menslist}
    return render(request,"recommend_app/input.html", params)


def input_women(request,*args,**kwargs):

    with open("selectwomenslist.csv","r") as f:
        for line in f:
            line = line.rstrip()
            set_womenslist = line.split(",")

    #csvブランドリストをlist化する
    params={"set_womenslist":set_womenslist}
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