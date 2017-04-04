import urllib
from bs4 import BeautifulSoup # Parsing library
import pandas as pd

source = urllib.request.urlopen('https://www.infoplease.com/world/health-and-social-statistics/life-expectancy-countries-2015')
source # It is a socket: similar to opening a file
soup = BeautifulSoup(source)

type = soup.find('div',attrs={"class":"table-info"}).findAll('span')

print (type)

print (soup)

print (soup.prettify( ))

table = soup.find("table", {"class" : "wikitable sortable"})
print (table)

for i, row in enumerate(soup.findAll("tr")):
    cells = row.findAll("td")
    print (i, len(cells))


