currency_in = 'KES'
currency_out = 'USD'
# from urllib.request import urlopen
# req = urlopen('http://finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s='+currency_in+currency_out+'=X').read()
# req

# result = "USDNOK=X",5.9423,"5/3/2010","12:39pm"
import urllib.request

wp = urllib.request.urlopen('http://finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s='+currency_in+currency_out+'=X')
pw = wp.read()
print(pw)