import pandas as pd
import numpy as np
import requests
import time
import urllib
from dateutil import relativedelta
import datetime
from bs4 import BeautifulSoup

def clean_name(x):
    """clean the name to convert to something readable
    @:param x(string): e.g.'Bunde­­srep.­­Deuts­­chlan­­d · WKN 110490 · ISIN DE0001104909'

    """

    '#1.Step: Replace the "Soft Hyphen"'
    data = x.replace('\xad', '')
    data = data.replace('\u00ad', '')
    data = data.replace('\N{SOFT HYPHEN}', '')
    '#2.Step: Replace the non-breaking'
    data = data.replace('\xa0', '')
    data = data.replace('\u00a0', '')
    data = data.replace('\N{No-Break Space}', '')

    return data


def split_colum(x):
    """
    split column into name and isin

    :param x:
    :return:
    """
    name = x.split("Anleihe")[0]
    isin = x.split("ISIN")[-1]

    return pd.Series([name, isin])


def revenue_and_last_price(row):
    """
    Get for a bond from finanze.net the revenue of the day and the last price
    :param x:
    :return:
    """
    '#1.Step: Define the isin'
    isin = row["isin"]
    '#2.Step: Define url'
    url = f"https://www.finanzen.net/anleihen/{isin}"
    'there will be a redirect'
    '#2.1.Step: Define url'

    print(f'Current row: {row.name}')
    try:
        res = urllib.request.urlopen(url)
        redirect_url = res.geturl()
        finalurl = redirect_url.replace("anleihen", "/anleihen/timesandsales")
        # print(finalurl)
        df_kurs = pd.read_html(finalurl, match='Umsatz', decimal=',', thousands='.', flavor='bs4')[0]

        revenue = sum(df_kurs["Umsatz"]*df_kurs["Kurs"]/100)
        last_price = df_kurs.loc[0, "Kurs"]
        return pd.Series([revenue, last_price])
    except:
        print("error")
        print(url)

        return pd.Series([np.nan, np.nan])


def remain_time(x):
    """
    calculate the remaining time based on today in months
    :param x:
    :return:
    """
    due_date = x
    now = datetime.datetime.now()

    delta = relativedelta.relativedelta(due_date, now)
    res_months = delta.months + (delta.years * 12)

    return pd.Series([res_months])


def add_rating(row):
    """
    Get for a bond from finanze.net the rating
    :param x:
    :return:
    """
    '#1.Step: Define the isin'
    isin = row["isin"]
    '#2.Step: Define url'
    url = f"https://www.finanzen.net/anleihen/{isin}"
    print(f'Current row: {row.name}')

    website = requests.get(url)

    results = BeautifulSoup(website.content, 'html.parser')

    rating_element = results.find(class_="tachoValue tachoMr mr2")

    if rating_element!=None:
        return rating_element.text
    else:
        print("no rating found")
        return np.nan