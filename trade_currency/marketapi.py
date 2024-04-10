from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required,user_passes_test

from django.http.response import HttpResponseRedirect
from django.http import HttpResponse,Http404
from django.urls import reverse


from functools import wraps
from django.db.models import Q,F,Func,Value
from django.db.models import Count, Min,Max, Sum, Avg,DecimalField,DateTimeField,CharField

import json


from django.contrib.auth.models import User,Group

from trade_currency.models import TradeCurrency,TradePairs

import requests
import json
 



def get_crypto_comparedata(request):
    api_url = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC"
    try:
    	data = requests.get(api_url).json()
    	s = json.dumps(data)
    	t = round(float(s.strip('{"BTC":}')),8)

    except Exception as e:
        
        data = dict()
    return data



def cron_crypto_comparedata(fromprice,toprice):
    result =''
    
    try:
    	api_url = "https://min-api.cryptocompare.com/data/price?fsym="+fromprice+"&tsyms="+toprice
    	data = requests.get(api_url).json()
    	jsondata = json.dumps(data)
    	result = round(float(jsondata.strip('{"'+toprice+'":}')),8)
    	
    	
    except Exception as e:
        result = 0.00
    return result


from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

def cron_crypto_coingeckoapi(fromprice,toprice):
    result = ''
    try:
        api_url =cg.get_price(ids=fromprice, vs_currencies=toprice)
        data = api_url
        pairprice = data[fromprice]
        pairvalue=0
        pairkey=''
        paircheckvalue =0
        for pairkey, pairvalue in pairprice.items():
            paircheckvalue = pairvalue
        amount = round(pairvalue,8)
        result = amount
    except Exception as e:
        
        result = 0.00
    return result


def cron_crypto_24hours_coingeckoapi(fromprice,toprice):
    result = ''
    try:
        
        api_url =cg.get_price(ids=fromprice, vs_currencies=toprice,include_24hr_change='true')
        data = api_url
        pairprice = data[fromprice]
        pairvalue=0
        pairkey=''
        paircheckvalue =0
        for pairkey, pairvalue in pairprice.items():
            paircheckvalue = pairvalue
        amount = round(pairvalue,8)
        result = amount
    except Exception as e:
        result = 0.00
    return result

def checkcron_crypto_coingeckoapi(fromprice,toprice):
    result = ''
    try:
        
        api_url =cg.get_price(ids=fromprice, vs_currencies=toprice,include_24hr_change='true')
        data = api_url
        pairprice = data[fromprice]
        pairvalue=0
        pairkey=''
        paircheckvalue =0
        for pairkey, pairvalue in pairprice.items():
            paircheckvalue = pairvalue
        amount = round(pairvalue,8)
        result = amount
    except Exception as e:
        result = 0.00
    return result


def binanace_get_ticker(pair):
    res ={}
    lastprice = 0.00
    ticker=''
    for item in ticker:
        if item['symbol'] == pair:
            res = item
            lastprice= res['lastPrice']
            
            break
    
    return lastprice