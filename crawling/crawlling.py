from urllib.request import urlopen
from bs4 import BeautifulSoup    # pip3 install beautifulsoup4
from selenium import webdriver

html = urlopen("http://www.pythonscraping.com/pages/page1.html")
bsObj = BeautifulSoup(html.read(), "html.parser")
print(bsObj.h1)