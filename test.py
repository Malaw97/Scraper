from bs4 import BeautifulSoup
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#Initiate headless chrome option
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')


#State your designated ticker
tickers=input("What ticker(s) would you like to explore (If entering more than one, separate each ticker by a comma)? ")

def parse_input(ticker_list):
    ticks=[]
    ticker_list=ticker_list.split(',')
    for i in ticker_list:
        ticks.append(i.strip())
    return ticks

def retrieve_yahoo(ticker):
    '''
    Return data associated with a given ticker
    '''
    #Locate chromedriver.exe locally
    webdrive=webdriver.Chrome(r'D:\Documents\Github\Scraper\chromedriver.exe', options=options)
    #Assign designated ticker to hyperlink
    webdrive.get('https://finance.yahoo.com/quote/'+ticker+'/financials?p='+ticker)
    html = webdrive.execute_script('return document.body.innerHTML;')
    soup = BeautifulSoup(html,'lxml')
    Price = [i.text for i in soup.find_all('span', {'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})]
    DoD_Change = [i.text for i in soup.find_all('span', {'class':'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)'})]

    features=[]
    r=(soup.find_all('div', class_='D(tbr)'))
    for i in r:
        features.append(i)

    data=[ticker.upper(), float((Price[0]).replace((','),(''))), DoD_Change[0], features]
    return data

def main():
    l=[]
    for i in parse_input(tickers):
        l.append(retrieve_yahoo(i))
    return l

print(main())
