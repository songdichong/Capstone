from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
yf.pdr_override()
data = pdr.get_data_yahoo("SPY", start="2017-01-01", end="2017-04-30")
print(data)