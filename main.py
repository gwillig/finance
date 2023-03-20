import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import urllib.request
from unicodedata import normalize
from utils import clean_name, split_colum, remain_time, revenue_and_last_price
import time
import numpy as np
from dateutil import relativedelta

# Downloading contents of the web page

# 1.Step: Download the most search bonds
url = "https://www.onvista.de/top-werte/top-anleihen"
df_pandas = pd.read_html(url, attrs={'class': 'table ov-table ov-table--fixed-x-cells outer-spacing--none'}, flavor='bs4')
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

'#3.Step:nrichment'
'#3.1.Step: Add to each index the current value and the revenue of the day'
df[['umsatz', 'kurs']] = df.apply(revenue_and_last_price, axis=1)

df[['restliche_zeit_monaten']] = df["Fälligkeit"].apply(remain_time)
# Get from https://www.finanzen.net/anleihen/a0e6fu-suedzucker-international-finance-bv-anleihe
# 2. Add to each index the Rating
# Get from https://www.finanzen.net/anleihen/a0e6fu-suedzucker-international-finance-bv-anleihe
# 3. Add to each index the sales value of the last day







