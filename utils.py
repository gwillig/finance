import pandas as pd


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