from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
yf.pdr_override()
data = pdr.get_data_yahoo("SPY", start="2019-01-30", end="2019-02-09")
print(data)



