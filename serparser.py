#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests.hooks
def getElementFloat(element):
    return float(element.get_text().replace(",",".")) if element != None else 0.0 
def getElementText(element):
    return element.get_text() if element != None else "unknown"
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
        r = requests.get(url)
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


def main():
    cp = CurrencyParser(True)
    cp.PrintAll()

if __name__ == "__main__":
    main()