import decimal
from decimal import *
from django.db.models import Q,F,Func,Value
from django.db.models import Count, Min,Max, Sum, Avg,DecimalField,DateTimeField,CharField
from django.db.models.expressions import RawSQL
from django.db.models.functions import Cast,TruncSecond,ExtractSecond

from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required,user_passes_test

from django.http.response import HttpResponseRedirect
from django.http import HttpResponse,Http404
from django.urls import reverse


from functools import wraps
from django.db.models import Q,F,Func,Value
from django.db.models import Count, Min,Max, Sum, Avg,DecimalField,DateTimeField,CharField


from django.contrib.auth.models import User,Group

from trade_currency.models import TradeCurrency,TradePairs


import requests
from trade_currency.marketapi import get_crypto_comparedata,cron_crypto_comparedata,cron_crypto_coingeckoapi
from trade_currency.marketapi import cron_crypto_24hours_coingeckoapi,checkcron_crypto_coingeckoapi
from trade_currency.marketapi import binanace_get_ticker
from datetime import date,timedelta
import datetime


def calculate_buylimit(buypercentage,buylimit,lastprice):
    if buylimit == 0:
        buy_percentage_value = round(((Decimal(lastprice) * Decimal(buypercentage)) / 100),8)
        buy_marketprice =  round((abs(Decimal(lastprice) + Decimal(buy_percentage_value))),8)
    elif buylimit == 1:
        buy_percentage_value = round(((Decimal(lastprice) * Decimal(buypercentage)) / 100),8)
        buy_marketprice =  round((abs(Decimal(lastprice) - Decimal(buy_percentage_value))),8)
    return buy_marketprice

def calculate_selllimit(sellpercentage,sellimit,lastprice):
    if sellimit == 0:
        sell_percentage_value = round(((Decimal(lastprice) * Decimal(sellpercentage)) / 100),8)
        sell_marketprice =  round((abs(Decimal(lastprice) + Decimal(sell_percentage_value))),8)
    elif sellimit == 1:
        sell_percentage_value = round(((Decimal(lastprice) * Decimal(sellpercentage)) / 100),8)
        sell_marketprice =  round((abs(Decimal(lastprice) - Decimal(sell_percentage_value))),8)
    return sell_marketprice


def cron_currency_api(request):
    
    try:
        pairqs = TradePairs.objects.all()
        if pairqs:
            firstsymbol = ''
            secondsymbol = ''
            hbdsymbol = ''
            for item in pairqs:
                hbdsymbol = item.from_symbol.symbol
                if hbdsymbol != 'HBD':
                    firstsymbol = item.from_symbol.currency_label
                    secondsymbol = item.two_symbol.currency_symbol
                    last_price =  cron_crypto_coingeckoapi(firstsymbol,secondsymbol)
                    item.last_price = last_price
                    item.save()
                   
                    update_currency = TradeCurrency.objects.get(id=item.from_symbol.id)
                    update_currency.usd_value = round(last_price,2)
                    update_currency.save()
                firstsymbolname = item.from_symbol.name
                secondsymbolname = item.two_symbol.name
                firstsymbolid = item.from_symbol.id
                secondsymbolid = item.two_symbol.id
                if firstsymbolname == 'USD':
                    get_marketprice = TradePairs.objects.get(Q(from_symbol =secondsymbolid) & Q(two_symbol = firstsymbolid))
                    usd_get_marketprice = TradePairs.objects.get(Q(from_symbol =firstsymbolid) & Q(two_symbol = secondsymbolid))
                    marketprice = get_marketprice.last_price
                    checkpairprice = (1 / marketprice)
                    usd_get_marketprice.last_price = checkpairprice
                    buyvalueusd = calculate_buylimit(usd_get_marketprice.maker_fees,usd_get_marketprice.buylimit,checkpairprice)
                    sellvalueusd = calculate_selllimit(usd_get_marketprice.taker_fees,usd_get_marketprice.selllimit,checkpairprice)
                    usd_get_marketprice.change_price = buyvalueusd
                    usd_get_marketprice.volume_price = sellvalueusd
                    usd_get_marketprice.save()

        else:
            pass
    except TradePairs.DoesNotExist:
        pass
    return HttpResponseRedirect('/')


def checkcron_currency_api(request):
    try:
        pairqs = TradePairs.objects.all()
        if pairqs:
            for item in pairqs:

                firstsymbol = item.from_symbol.currency_label
                secondsymbol = item.two_symbol.currency_symbol
                last_price =  checkcron_crypto_coingeckoapi(firstsymbol,secondsymbol)
        else:
            pass
    except TradePairs.DoesNotExist:
        pass
    return HttpResponseRedirect('/')



