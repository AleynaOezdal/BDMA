import yfinance as yf
import pprint as pp

# Source for DAX Symbols: https://de.wikipedia.org/wiki/DAX#Zusammensetzung
companies = ['ads', 'air', 'alv', 'bas', 'bayn', 'bmw', 'bnr',
             'con', '1cov', 'dtg', 'dher', 'dbk', 'db1', 'dpw',
             'dte', 'eoan', 'fre', 'fme', 'hnr1', 'hei', 'hfg',
             'hen3', 'ifx', 'lin', 'mbg', 'mrk', 'mtx', 'muv2',
             'pah3', 'pum', 'qia', 'rwe', 'sap', 'srt3', 'sie',
             'shl', 'sy1', 'vow3', 'vna', 'zal']
DAX40 = yf.Tickers(' '.join(companies))

for company in companies:
    print(f"Now company: {company}")
    print(DAX40.tickers[str(company).upper()].sustainability.T['totalEsg'])
    print("")