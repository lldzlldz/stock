# not using yfinance as this is much faster
# for more financial info: https://stackoverflow.com/questions/44030983/yahoo-finance-url-not-working
# https://query2.finance.yahoo.com/v10/finance/quoteSummary/d05.si?modules=assetProfile%2CsummaryProfile%2CsummaryDetail%2CesgScores%2Cprice%2CincomeStatementHistory%2CincomeStatementHistoryQuarterly%2CbalanceSheetHistory%2CbalanceSheetHistoryQuarterly%2CcashflowStatementHistory%2CcashflowStatementHistoryQuarterly%2CdefaultKeyStatistics%2CfinancialData%2CcalendarEvents%2CsecFilings%2CrecommendationTrend%2CupgradeDowngradeHistory%2CinstitutionOwnership%2CfundOwnership%2CmajorDirectHolders%2CmajorHoldersBreakdown%2CinsiderTransactions%2CinsiderHolders%2CnetSharePurchaseActivity%2Cearnings%2CearningsHistory%2CearningsTrend%2CindustryTrend%2CindexTrend%2CsectorTrend
# gspread documentation : https://gspread.readthedocs.io/en/latest/

from dotenv import load_dotenv
from bs4 import BeautifulSoup
import gspread
import requests
import os
import webbrowser
import json


class stock:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.yahoo_finance_url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{self.ticker}?modules=assetProfile%2CsummaryProfile%2CsummaryDetail%2Cprice%2CdefaultKeyStatistics%2CfinancialData%2CcalendarEvents%2Cearnings%2CearningsHistory%2CearningsTrend"
        self.number = 0

        self.info = None

    def __repr__(self):
        return f"stock object <{self.ticker}>"

    def get_info(self):
        rsp = requests.get(self.yahoo_finance_url, timeout=3)
        if rsp.status_code == requests.codes.ok:
            info = rsp.json()["quoteSummary"]["result"][0]
        else:
            print(f"error with {self.ticker}")
            info = None
        self.info = info

    # raw returns float while fmt returns string
    def price(self):
        try:
            return self.info["price"]["regularMarketPrice"]["fmt"]
        except KeyError:
            return -1
        except TypeError:
            return -2

    def close(self):

        try:
            return self.info["price"]["regularMarketPreviousClose"]["fmt"]
        except KeyError:
            return -1
        except TypeError:
            return -2

    def currency(self):
        try:
            return self.info["price"]["currency"]
        except KeyError:
            return -1
        except TypeError:
            return -2

    def live_quote(self):
        try:
            if (
                self.info["price"]["quoteSourceName"] == "Delayed Quote"
                or self.info["price"]["regularMarketSource"] == "DELAYED"
            ):
                return False
            else:
                return True
        except KeyError:
            return -1
        except TypeError:
            return -2

    def dividend(self):
        pass

    def ex_dividend_date(self):
        try:
            return self.info["summaryDetail"]["exDividendDate"]["fmt"]
        except KeyError:
            return -1
        except TypeError:
            return -2

    def dividend_yield(self):
        try:
            return self.info["defaultKeyStatistics"]["lastDividendValue"][
                "raw"
            ]
        except KeyError:
            return -1
        except TypeError:
            return -2

    def pay_date(self):
        try:
            return self.info["calendarEvents"]["dividendDate"]["fmt"]
        except KeyError:
            return -1
        except TypeError:
            return -2

    def five_yr_div_yield(self):
        try:
            return self.info["summaryDetail"]["fiveYearAvgDividendYield"][
                "fmt"
            ]
        except KeyError:
            return -1
        except TypeError:
            return -2

    def name(self):
        try:
            return self.info["price"]["shortName"]
        except KeyError:
            return -1
        except TypeError:
            return -2

    def industry(self):
        try:
            return self.info["assetProfile"]["industry"]
        except KeyError:
            return -1
        except TypeError:
            return -2

    def sector(self):
        try:
            return self.info["assetProfile"]["sector"]
        except KeyError:
            return -1
        except TypeError:
            return -2

    def mkt_cap(self):
        try:
            return self.info["summaryDetail"]["marketCap"]["fmt"]
        except KeyError:
            return -1
        except TypeError:
            return -2

    def mkt_cap(self):

        try:
            return self.info["summaryDetail"]["marketCap"]["fmt"]
        except KeyError:
            return -1
        except TypeError:
            return -2

    def book_value(self):

        try:
            return self.info["defaultKeyStatistics"]["bookValue"]["fmt"]
        except KeyError:
            return -1
        except TypeError:
            return -2

    def PB(self):

        try:
            return self.info["defaultKeyStatistics"]["priceToBook"]["fmt"]
        except KeyError:
            return -1
        except TypeError:
            return -2

    def trailing_PE(self):
        try:
            return self.info["summaryDetail"]["trailingPE"]["fmt"]
        except KeyError:
            return -1
        except TypeError:
            return -2

    def foward_PE(self):
        try:
            return self.info["summaryDetail"]["fowardPE"]["fmt"]
        except KeyError:
            return -1
        except TypeError:
            return -2

    def ROA(self):
        try:
            return self.info["financialData"]["returnOnAssets"]["fmt"]
        except:
            return -1

    def ROE(self):
        try:
            return self.info["financialData"]["returnOnEquity"]["fmt"]
        except:
            return -1


class sg_stock(stock):
    def __init__(self, ticker):
        super().__init__(ticker)
        self.sg_url = f"https://www.dividends.sg/view/{self.ticker}"

    def dividend_info(self):
        rsp = requests.get(self.sg_url, timeout=3)
        if rsp.ok:
            print(rsp)
            soup = BeautifulSoup(rsp.text, "lxml")
            return soup
        else:
            print(f"error with {self.ticker}")

    def dividend_history(self):
        rsp = requests.get(self.sg_url, timeout=3)
        if rsp.ok:
            soup = BeautifulSoup(rsp.text, "lxml")
            table = soup.find(
                "table", class_=["table", "table-bordered", "table-striped"]
            ).find_all("tr")
            for tr in table:
                td = tr.find_all("td")
                row = [info.text.strip() for info in td]
                print(row)
        else:
            print(f"error with {self.ticker}")

    def ex_dividend_date(self):
        pass

    def pay_date(self):
        pass

    def TTM_div_amt(self):
        pass


def trial():
    a = sg_stock("d05")
    print(a.dividend_history())


def main():
    # load_dotenv()
    # webbrowser.open(os.getenv("GS_LINK"))
    # gc = gspread.oauth()

    # spreadsheet = gc.open_by_key(os.getenv("GS_KEY"))
    # stock_summary_sgd = spreadsheet.worksheet("Stock Summary SGD")
    # excel_dict = stock_summary_sgd.get_all_records()
    # tickers = [ticker["Yahoo Quote"] for ticker in excel_dict]
    # print(tickers)

    # units = [ticker["Units"] for ticker in excel_dict]
    # print(units)


    tickers = ['o39.si', 'bsl.si', 'u11.si', 'aapl']
    counter = 0
    store = {}
    for ticker in tickers:
        if ticker == "":
            continue
        s = stock(ticker)
        s.get_info()
        # if s.info == None:
        #     continue
        store[ticker] = {}
        store[ticker]["name"] = s.name()
        store[ticker]["price"] = float(s.price())
        store[ticker]["close"] = float(s.close())
        try:
            store[ticker]["day percentage change"] = str(round(
                (store[ticker]["price"] - store[ticker]["close"])
                / store[ticker]["close"]
                * 100,
                2,
            )) + '%'
        except ZeroDivisionError:
            store[ticker]["day percentage change"] = 0
        store[ticker]["currency"] = s.currency()
        store[ticker]["live quote"] = s.live_quote()
        store[ticker]["ex dividend date"] = s.ex_dividend_date()
        if float(s.five_yr_div_yield()) not in [-1,-2]:
            store[ticker]["five yr div yield"] = s.five_yr_div_yield() + '%'
        else:
            store[ticker]["five yr div yield"] = -1
        store[ticker]["pay date"] = s.pay_date()
        store[ticker]["industry"] = s.industry()
        store[ticker]["sector"] = s.sector()
        store[ticker]["mkt cap"] = s.mkt_cap()
        store[ticker]["P/B"] = s.PB()
        store[ticker]["trailing P/E"] = s.trailing_PE()
        store[ticker]["foward P/E"] = s.foward_PE()
        # store[ticker]["units"] = units[counter]
        # store[ticker]["value"] = '$' + str(round(
            # int(store[ticker]["units"]) * store[ticker]["price"]
        # )) + ' ' + str(store[ticker]["currency"])
        store[ticker]["ROA"] = s.ROA()
        store[ticker]["ROE"] = s.ROE()
        counter += 1

    print(store)

    new_file = json.dumps(store, ensure_ascii=False).encode(
        "utf8"
    )  # for the '-'
    with open("stock.json", "wb") as f:
        f.write(new_file)

    #gs formatting
    #to make sure the tickers are in the column section
    name_ls = [[store[ticker]["name"]] for ticker in tickers]
    price_ls = [[store[ticker]["price"]] for ticker in tickers]
    close_ls = [[store[ticker]["close"]] for ticker in tickers]
    currency_ls = [[store[ticker]["currency"]] for ticker in tickers]
    live_quote_ls = [[store[ticker]["live quote"]] for ticker in tickers]
    ex_dividend_date_ls = [
        [store[ticker]["ex dividend date"]] for ticker in tickers
    ]
    five_yr_div_yield_ls = [
        [store[ticker]["five yr div yield"]] for ticker in tickers
    ]
    pay_date_ls = [[store[ticker]["pay date"]] for ticker in tickers]

    print("-" * 100)
    print(price_ls)
    print("-" * 100)
    print(name_ls)

    # #updates to google sheets
    # stock_summary_sgd.batch_update(
    #     [
    #         {
    #             "range": "G2:G100",
    #             "values": price_ls,
    #         },
    #         {
    #             "range": "W2:W100",
    #             "values": ex_dividend_date_ls,
    #         },
    #         {
    #             "range": "Y2:Y100",
    #             "values": five_yr_div_yield_ls,
    #         },
    #         {
    #             "range": "Z2:Z100",
    #             "values": pay_date_ls,
    #         },
    #         {
    #             "range": "AA2:AA100",
    #             "values": close_ls,
    #         },
    #     ]
    # )


if __name__ == "__main__":
    main()



# can prob try using regex for the headers, and link it somwhere(maybe end of dict)
# class etf(stock)/ class bond(stock) - need to get the stock category form google sheets

