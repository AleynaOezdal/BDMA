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

if __name__ == '__main__':
    for company in companies:
        try:
            print(f"Now company: {company}")
            pp.pprint(DAX40.tickers[str(company).upper()].sustainability.T['totalEsg'])
            print("")
        except KeyError:
            print("Error occured in fetching data from API. Continuing with next company.")
            continue
