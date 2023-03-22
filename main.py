import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import urllib.request
from unicodedata import normalize
from utils import clean_name, split_colum, remain_time, revenue_and_last_price,add_rating, add_finanzen_link
import time
import numpy as np
from dateutil import relativedelta

# Downloading contents of the web page

# 1.Step: Download the most search bonds
url_own_criteria = {
    "url":"https://www.onvista.de/anleihen/finder?isoCountry=DE&currentYieldRange=3;6&datetimeMaturityRange=;2024-01-22&isoCurrency=EUR&cols=instrument,instrument.isin,bondsIssuer.name,bondsDetails.coupon,bondsFigures.yieldToMaturity,quote.isoCurrency,bondsDetails.nameTypeCoupon,bondsBaseData.datetimeMaturity,quote.last,quote.performancePct,quote.performance1YearPct,quote.bid,quote.ask,bondsFigures.spread,bondsBaseData.datetimeEmission,bondsBaseData.volumeEmission,quote.market.nameExchange,bondsDetails.nominal",
    "table_finder":{'id':'finderResults'}
}
url = url_own_criteria["url"]
table_finder = url_own_criteria["table_finder"]

def onvista_bond_own_search(url,table_finder):
    """
    Convert a bond search result into a table
    :param url:
    :param table_finder:
    :return:
    """
    df_pandas = pd.read_html(url, attrs=table_finder, flavor='bs4')
    df = df_pandas[0]


    # 2.Step: Convert the column "Fälligkeit" from type object to datetime
    df['Fälligkeit'] = pd.to_datetime(df['Fälligkeit'], format='%d.%m.%Y')

    '#2.Step: Preprocessing'


    '#2.1.Step: Convert rendite from "+2,36 %" to => 2.36'
    df['Rendite'] = df['Rendite'].replace(regex={',': ".", "\+": "", " %": ""})
    df['Rendite'] = pd.to_numeric(df['Rendite'])
    '#2.2.Step:Change order of columns'
    # df = df.reindex(columns=['name', "isin", 'Anleihen-TypZins-Typ', 'Kupon', 'Nominal', 'Fälligkeit', 'Rendite'])

    '#2.1.Step: Convert name into normal string'

    '#3.Step:enrichment'

    '#3.2.Step: Rename ISIN to isin'
    df = df.rename(columns={"ISIN": "isin"})
    df[['umsatz', 'kurs']] = df.apply(revenue_and_last_price, axis=1)

    df[['restliche_zeit_monaten']] = df["Fälligkeit"].apply(remain_time)

    df['rating'] = df.apply(add_rating, axis=1)

    return df

url_most_search = {
    "url":"https://www.onvista.de/top-werte/top-anleihen",
    "table_finder":{'class': 'table ov-table ov-table--fixed-x-cells outer-spacing--none'}
}

url_own_criteria = {
    "url":"https://www.onvista.de/anleihen/finder?isoCountry=DE&currentYieldRange=3;6&datetimeMaturityRange=;2024-01-22&isoCurrency=EUR",
    "table_finder":{'id':'finderResults'}
}

url_most_search = {
    "url": "https://www.onvista.de/top-werte/top-anleihen",
    "table_finder": {'class': 'table ov-table ov-table--fixed-x-cells outer-spacing--none'}
}

url_own_criteria = {
    "url": "https://www.onvista.de/anleihen/finder?isoCountry=DE&currentYieldRange=3;6&datetimeMaturityRange=;2024-01-22&isoCurrency=EUR&cols=instrument,instrument.isin,bondsIssuer.name,bondsDetails.coupon,bondsFigures.yieldToMaturity,quote.isoCurrency,bondsDetails.nameTypeCoupon,bondsBaseData.datetimeMaturity,quote.last,quote.performancePct,quote.performance1YearPct,quote.bid,quote.ask,bondsFigures.spread,bondsBaseData.datetimeEmission,bondsBaseData.volumeEmission,quote.market.nameExchange,bondsDetails.nominal",
    "table_finder": {'id': 'finderResults'}
}


def get_df_from_onvista_most_search(url, table_finder):
    """
    Get from Onvista the most search bond list and convert it into df
    """
    df_pandas = pd.read_html(url, attrs=table_finder, flavor='bs4')
    df = df_pandas[0]

    df.keys()
    # 2.Step: Convert the column "Fälligkeit" from type object to datetime
    df['Fälligkeit'] = pd.to_datetime(df['Fälligkeit'], format='%d.%m.%Y')

    '#2.Step: Preprocessing'
    df["Wert"] = df["Wert"].apply(clean_name)
    df[['name', 'isin']] = df["Wert"].apply(split_colum)
    '#2.1.Step: Convert rendite from "+2,36 %" to => 2.36'
    df['Rendite'] = df['Rendite'].replace(regex={',': ".", "\+": "", " %": ""})
    df['Rendite'] = pd.to_numeric(df['Rendite'])
    '#2.2.Step:Change order of columns'
    df = df.reindex(columns=['name', "isin", 'Anleihen-TypZins-Typ', 'Kupon', 'Nominal', 'Fälligkeit', 'Rendite'])

    '#2.1.Step: Convert name into normal string'

    '#3.Step:enrichment'
    '#3.1.Step: Add to each index the current value and the revenue of the day'
    df[['umsatz', 'kurs']] = df.apply(revenue_and_last_price, axis=1)

    df[['restliche_zeit_monaten']] = df["Fälligkeit"].apply(remain_time)
    # Get from https://www.finanzen.net/anleihen/a0e6fu-suedzucker-international-finance-bv-anleihe
    # 2. Add to each index the Rating
    # Get from https://www.finanzen.net/anleihen/a0e6fu-suedzucker-international-finance-bv-anleihe
    # 3. Add to each index the sales value of the last day
    df['rating'] = df.apply(add_rating, axis=1)
    return df


def get_onvista_bond_own_search(url, table_finder):
    """
    Convert a bond search result into a table
    :param url:
    :param table_finder:
    :return:
    """
    df_pandas = pd.read_html(url, attrs=table_finder, flavor='bs4')
    df = df_pandas[0]

    # 2.Step: Convert the column "Fälligkeit" from type object to datetime
    df['Fälligkeit'] = pd.to_datetime(df['Fälligkeit'], format='%d.%m.%Y')

    '#2.Step: Preprocessing'

    '#2.1.Step: Convert rendite from "+2,36 %" to => 2.36'
    df['Rendite'] = df['Rendite'].replace(regex={',': ".", "\+": "", " %": ""})
    df['Rendite'] = pd.to_numeric(df['Rendite'])
    '#2.2.Step:Change order of columns'
    # df = df.reindex(columns=['name', "isin", 'Anleihen-TypZins-Typ', 'Kupon', 'Nominal', 'Fälligkeit', 'Rendite'])

    '#2.1.Step: Convert name into normal string'

    '#3.Step:enrichment'

    '#3.2.Step: Rename ISIN to isin'
    df = df.rename(columns={"ISIN": "isin"})
    df[['umsatz', 'kurs']] = df.apply(revenue_and_last_price, axis=1)

    df[['restliche_zeit_monaten']] = df["Fälligkeit"].apply(remain_time)

    df['rating'] = df.apply(add_rating, axis=1)

    return df


df1 = get_df_from_onvista_most_search(**url_most_search)
df2 = get_onvista_bond_own_search(**url_own_criteria)