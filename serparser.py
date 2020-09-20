#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import re
import requests.hooks
def getElementInteger(element):
    return (int(element.get_text()) if element.get_text().isnumeric() else 0) if element != None else 0 
def getElementFloat(element):
    return float(element.get_text().replace(",",".")) if element != None else 0.0 
def getElementText(element):
    return element.get_text() if element != None else "unknown"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
class CurrencyParser:
    DEBUG     = False
    SERVER    = "https://kur.doviz.com/"
    USD_PATH  = "serbest-piyasa/amerikan-dolari"
    USD_BUY   = 1
    USD_SELL  = 1
    EUR_PATH  = "serbest-piyasa/euro"
    EUR_BUY   = 1
    EUR_SELL  = 1
    JPY_PATH  = "serbest-piyasa/japon-yeni"
    JPY_BUY   = 1
    JPY_SELL  = 1
    POUND_PATH= "serbest-piyasa/sterlin"
    POUND_BUY = 1
    POUND_SELL= 1
    RUBLE_PATH= "serbest-piyasa/rus-rublesi"
    RUBLE_BUY = 1
    RUBLE_SELL= 1
    YUAN_PATH = "serbest-piyasa/cin-yuani"
    YUAN_BUY  = 1
    YUAN_SELL = 1
    CURRENCIES = {}
    USD_BANKS = {}
    def __init__(self,Debug=DEBUG):
        self.DEBUG = Debug
        self.dprint("Init started")
        self.UpdateAllCurrency()
        self.dprint("Init complete")
    def dprint(self,*text):
        if(self.DEBUG):print(",".join(text))
    def UpdateAllCurrency(self):
        self.dprint("Updating currencies")
        self.UpdateUSD()
        self.UpdateEUR()
        self.UpdateJPY()
        self.UpdatePOUND()
        self.UpdateRUBLE()
        self.UpdateYUAN()
        self.PrepareBigData()
        self.dprint("Currencies are updated")
        self.dprint("Big data prepared")
    def UpdateUSD(self):
        self.dprint("Updating USD")
        buy, sell, banks = self.GetCurrencyData("%s%s"%(self.SERVER,self.USD_PATH))
        self.USD_BUY   = buy
        self.USD_SELL  = sell
        self.USD_BANKS = banks
        self.dprint("Updated USD")
    def UpdateEUR(self):
        self.dprint("Updating EUR")
        buy, sell, banks = self.GetCurrencyData("%s%s"%(self.SERVER,self.EUR_PATH))
        self.EUR_BUY   = buy
        self.EUR_SELL  = sell
        self.EUR_BANKS = banks
        self.dprint("Updated EUR")
    def UpdateJPY(self):
        self.dprint("Updating JPY")
        buy, sell, banks = self.GetCurrencyData("%s%s"%(self.SERVER,self.JPY_PATH))
        self.JPY_BUY   = buy
        self.JPY_SELL  = sell
        self.JPY_BANKS = banks
        self.dprint("Updated JPY")
    def UpdatePOUND(self):
        self.dprint("Updating POUND")
        buy, sell, banks = self.GetCurrencyData("%s%s"%(self.SERVER,self.POUND_PATH))
        self.POUND_BUY   = buy
        self.POUND_SELL  = sell
        self.POUND_BANKS = banks
        self.dprint("Updated POUND")
    def UpdateRUBLE(self):
        self.dprint("Updating RUBLE")
        buy, sell, banks = self.GetCurrencyData("%s%s"%(self.SERVER,self.RUBLE_PATH))
        self.RUBLE_BUY   = buy
        self.RUBLE_SELL  = sell
        self.RUBLE_BANKS = banks
        self.dprint("Updated RUBLE")
    def UpdateYUAN(self):
        self.dprint("Updating YUAN")
        buy, sell, banks = self.GetCurrencyData("%s%s"%(self.SERVER,self.YUAN_PATH))
        self.YUAN_BUY   = buy
        self.YUAN_SELL  = sell
        self.YUAN_BANKS = banks
        self.dprint("Updated YUAN") 
    def PrepareBigData(self):
        self.CURRENCIES = {
            "USD":{
                "buy":self.USD_BUY,
                "sell":self.USD_SELL,
                "banks":self.USD_BANKS
            },
            "EUR":{
                "buy":self.EUR_BUY,
                "sell":self.EUR_SELL,
                "banks":self.EUR_BANKS
            },
            "JPY":{
                "buy":self.JPY_BUY,
                "sell":self.JPY_SELL,
                "banks":self.JPY_BANKS
            },
            "POUND":{
                "buy":self.POUND_BUY,
                "sell":self.POUND_SELL,
                "banks":self.POUND_BANKS
            },
            "RUBLE":{
                "buy":self.RUBLE_BUY,
                "sell":self.RUBLE_SELL,
                "banks":self.RUBLE_BANKS
            },
            "YUAN":{
                "buy":self.YUAN_BUY,
                "sell":self.YUAN_SELL,
                "banks":self.YUAN_BANKS
            },
        }
    def GetCurrencyData(self,url):
        global HEADERS
        r = requests.get(url,headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        spans = soup.select('.data .value')
        buy  = getElementFloat(spans[0])
        sell = getElementFloat(spans[1])
        tables = soup.select("table")
        bank_tables = filter(lambda table: str(table).find("Banka") > 0,tables)
        r_banks = []
        for banks_table in bank_tables:
            banks = banks_table.select("tbody tr")
            for bank in banks:
                values = bank.select("td")
                bank_name = getElementText(bank.select("a")[0])
                buy  = getElementFloat(bank.select("td")[1])
                sell = getElementFloat(bank.select("td")[2])
                r_banks.append({
                    "name":bank_name,
                    "buy":buy,
                    "sell":sell,
                })
        return buy, sell, r_banks 
    def PrintAll(self):
        for currency in self.CURRENCIES:
            data = self.CURRENCIES[currency]
            banks = data["banks"]
            print("%s : \n\tBuy : %s\n\tSell : %s"%(currency,data["buy"],data["sell"]))
            print("\tBanks:")
            for bank in banks:
                print("\t\t%s (B:S): %s:%s"%(bank["name"],bank["buy"],bank["sell"]))
from base64 import b64decode
def MustContent(arr,target):
    m=False
    target = target.lower().strip()
    for i in arr:
        m = m or (target.find(i.lower()) >= 0)
    # print("|%s|%s|%s|"%(m,target,i.lower()))
    return m
class ProxyParser:
    DEBUG = False
    SERVER = "https://hidemy.name/en/proxy-list/"
    PROTOCOLS = ["HTTP","HTTPS","SOCKS4","SOCKS5"]
    PROXY_LIST = []
    def __init__(self,Debug=False):
        self.DEBUG = Debug
        self.PROXY_LIST = []
    def Reload(self,page_count=10):
        for i in range(0,page_count):
            self.PROXY_LIST += self.GetPage(i)
    def GetPage(self,pagenumber=0):
        global HEADERS
        r = requests.get("%s"%(self.SERVER),params={
            "start":pagenumber*64
        },headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.select_one("tbody")
        dts = []
        for tr in table.select("tr"):
            tds = tr.select("td")
            ip  = getElementText(tds[0])
            port= getElementInteger(tds[1])
            protocol  = getElementText(tds[4])
            anonymity = getElementText(tds[5])
            data = {
                "ip":ip,
                "port":port,
                "protocol":protocol,
                "anonymity":anonymity
            }
            if(not MustContent(self.PROTOCOLS,protocol)):
                continue
            dts.append(data)
        return dts
    def PrintAll(self):
        print("Proxies")
        for proxy in self.PROXY_LIST:
            print("\tIP/PORT: %s:%s\n\tProtocol: %s\n\tAnonymity: %s"%(proxy["ip"],proxy["port"],proxy["protocol"],proxy["anonymity"]))
def main():
    import argparse 
    parser = argparse.ArgumentParser("SerParser DEBUG CLI")
    parser.add_argument("--currency",action="store_true")
    parser.add_argument("--proxy",action="store_true")
    args = parser.parse_args()
    if(args.currency):
        cp = CurrencyParser(True)
        cp.PrintAll()
    elif(args.proxy):
        pp = ProxyParser(True)
        pp.Reload(5)
        if(len(pp.PROXY_LIST)<50):
            pp.PrintAll()
        else:
            print("I Can't print all of them so many proxy exists. Like %s"%(len(pp.PROXY_LIST)))
if __name__ == "__main__":
    main()