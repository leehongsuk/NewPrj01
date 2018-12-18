"""
pip가 최신인지 확인..
> python -m pip install --upgrade pip


"""
from urllib.request import urlopen
from bs4 import BeautifulSoup    # pip install BeatifulSoup4
# from selenium import webdriver


html = urlopen("http://www.pythonscraping.com/pages/page1.html")
bsObj = BeautifulSoup(html.read(), "html.parser")
print(bsObj.h1)
print(bsObj.div)
