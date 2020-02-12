import pandas as pd
import os
import time
from datetime import datetime
from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import re
import quandl as Quandl

style.use("dark_background")

path = "C:/dev_tools/workspace/Secondary/MachineLearningStocks/intraQuarter"
auth_tok = 'nQs-4ToCpNts7xonon1H'

def Key_Stats(gather=["Total Debt/Equity",
                      'Trailing P/E',
                      'Price/Sales',
                      'Price/Book',
                      'Profit Margin',
                      'Operating Margin',
                      'Return on Assets',
                      'Return on Equity',
                      'Revenue Per Share',
                      'Market Cap',
                      'Enterprise Value',
                      'Forward P/E',
                      'PEG Ratio',
                      'Enterprise Value/Revenue',
                      'Enterprise Value/EBITDA',
                      'Revenue',
                      'Gross Profit',
                      'EBITDA',
                      'Net Income Avl to Common ',
                      'Diluted EPS',
                      'Earnings Growth',
                      'Revenue Growth',
                      'Total Cash',
                      'Total Cash Per Share',
                      'Total Debt',
                      'Current Ratio',
                      'Book Value Per Share',
                      'Cash Flow',
                      'Beta',
                      'Held by Insiders',
                      'Held by Institutions',
                      'Shares Short (as of',
                      'Short Ratio',
                      'Short % of Float',
                      'Shares Short (prior '
                      ]
              ):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    df = pd.DataFrame(columns=['Date',
                               'Unix',
                               'Ticker',
                               'Price',
                               'stock_p_change',
                               'SP500',
                               'sp500_p_change',
                               'Difference',
                               ##############
                               'DE Ratio',
                               'Trailing P/E',
                               'Price/Sales',
                               'Price/Book',
                               'Profit Margin',
                               'Operating Margin',
                               'Return on Assets',
                               'Return on Equity',
                               'Revenue Per Share',
                               'Market Cap',
                               'Enterprise Value',
                               'Forward P/E',
                               'PEG Ratio',
                               'Enterprise Value/Revenue',
                               'Enterprise Value/EBITDA',
                               'Revenue',
                               'Gross Profit',
                               'EBITDA',
                               'Net Income Avl to Common ',
                               'Diluted EPS',
                               'Earnings Growth',
                               'Revenue Growth',
                               'Total Cash',
                               'Total Cash Per Share',
                               'Total Debt',
                               'Current Ratio',
                               'Book Value Per Share',
                               'Cash Flow',
                               'Beta',
                               'Held by Insiders',
                               'Held by Institutions',
                               'Shares Short (as of',
                               'Short Ratio',
                               'Short % of Float',
                               'Shares Short (prior ',
                               ##############
                               'Status'])

    sp500_df = pd.read_csv("YAHOO-INDEX_GSPC.csv")
    stock_df = pd.read_csv("stock_prices.csv", index_col="Date", parse_dates=True)

    ticker_list = []

    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        ticker = each_dir.split("\\")[1]
        ticker_list.append(ticker)

        # starting_stock_value = False
        # starting_sp500_value = False

        if len(each_file) > 0:
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                full_file_path = each_dir + '/' + file
                source = open(full_file_path, 'r').read()
                try:
                    value_list = []

                    for each_data in gather:
                        try:
                            regex = re.escape(each_data) + r'.*?(\d{1,8}\.\d{1,8}M?B?|N/A)%?</td>'
                            value = re.search(regex, source)
                            value = (value.group(1))

                            if "B" in value:
                                value = float(value.replace("B", '')) * 1000000000

                            elif "M" in value:
                                value = float(value.replace("M", '')) * 1000000

                            value_list.append(value)


                        except Exception as e:
                            value = "N/A"
                            value_list.append(value)
                            # print("Couldn't parse", each_data, "because of Exception:", str(e), ticker, file)

                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df.loc[sp500_df["Date"] == sp500_date]
                        sp500_value = float(row["Adj Close"])
                    except Exception as e:
                        sp500_date = datetime.fromtimestamp(unix_time - 259200).strftime('%Y-%m-%d')
                        row = sp500_df.loc[sp500_df["Date"] == sp500_date]
                        sp500_value = float(row["Adj Close"])

                    one_year_later = int(unix_time + 31536000)

                    try:
                        sp500_1y = datetime.fromtimestamp(one_year_later).strftime('%Y-%m-%d')
                        row = sp500_df.loc[sp500_df["Date"] == sp500_1y]
                        sp500_1y_value = float(row["Adj Close"])
                    except:
                        try:
                            sp500_1y = datetime.fromtimestamp(one_year_later - 259200).strftime('%Y-%m-%d')
                            row = sp500_df.loc[sp500_df["Date"] == sp500_1y]
                            sp500_1y_value = float(row["Adj Close"])
                        except Exception as e:
                            print("sp500 1 year later issue", str(e))

                    try:
                        stock_price_1y = datetime.fromtimestamp(one_year_later).strftime('%Y-%m-%d')
                        stock_price_1y = datetime.strptime(stock_price_1y, '%Y-%m-%d')
                        row = stock_df.loc[stock_price_1y][ticker.upper()]

                        stock_1y_value = round(float(row), 2)
                        # print(stock_1y_value)
                        # time.sleep(1555)

                    except Exception as e:
                        try:
                            stock_price_1y = datetime.fromtimestamp(one_year_later - 259200).strftime('%Y-%m-%d')
                            stock_price_1y = datetime.strptime(stock_price_1y, '%Y-%m-%d')
                            row = stock_df.loc[stock_price_1y][ticker.upper()]
                            stock_1y_value = round(float(row), 2)
                        except Exception as e:
                            print("stock price:", str(e))

                    try:
                        stock_price = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        stock_price = datetime.strptime(stock_price, '%Y-%m-%d')
                        row = stock_df.loc[stock_price][ticker.upper()]
                        stock_price = round(float(row), 2)

                    except Exception as e:
                        try:
                            stock_price = datetime.fromtimestamp(unix_time - 259200).strftime('%Y-%m-%d')
                            stock_price = datetime.strptime(stock_price, '%Y-%m-%d')
                            row = stock_df.loc[stock_price][ticker.upper()]
                            stock_price = round(float(row), 2)
                        except Exception as e:
                            print("stock price:", str(e))

                    stock_p_change = round((((stock_1y_value - stock_price) / stock_price) * 100), 2)
                    sp500_p_change = round((((sp500_1y_value - sp500_value) / sp500_value) * 100), 2)

                    difference = stock_p_change - sp500_p_change

                    if difference > 5:
                        status = 1
                    else:
                        status = 0

                    if value_list.count("N/A") > 15:
                        pass
                    else:

                        df = df.append({'Date': date_stamp,
                                        'Unix': unix_time,
                                        'Ticker': ticker,

                                        'Price': stock_price,
                                        'stock_p_change': stock_p_change,
                                        'SP500': sp500_value,
                                        'sp500_p_change': sp500_p_change,
                                        'Difference': difference,
                                        'DE Ratio': value_list[0],
                                        # 'Market Cap':value_list[1],
                                        'Trailing P/E': value_list[1],
                                        'Price/Sales': value_list[2],
                                        'Price/Book': value_list[3],
                                        'Profit Margin': value_list[4],
                                        'Operating Margin': value_list[5],
                                        'Return on Assets': value_list[6],
                                        'Return on Equity': value_list[7],
                                        'Revenue Per Share': value_list[8],
                                        'Market Cap': value_list[9],
                                        'Enterprise Value': value_list[10],
                                        'Forward P/E': value_list[11],
                                        'PEG Ratio': value_list[12],
                                        'Enterprise Value/Revenue': value_list[13],
                                        'Enterprise Value/EBITDA': value_list[14],
                                        'Revenue': value_list[15],
                                        'Gross Profit': value_list[16],
                                        'EBITDA': value_list[17],
                                        'Net Income Avl to Common ': value_list[18],
                                        'Diluted EPS': value_list[19],
                                        'Earnings Growth': value_list[20],
                                        'Revenue Growth': value_list[21],
                                        'Total Cash': value_list[22],
                                        'Total Cash Per Share': value_list[23],
                                        'Total Debt': value_list[24],
                                        'Current Ratio': value_list[25],
                                        'Book Value Per Share': value_list[26],
                                        'Cash Flow': value_list[27],
                                        'Beta': value_list[28],
                                        'Held by Insiders': value_list[29],
                                        'Held by Institutions': value_list[30],
                                        'Shares Short (as of': value_list[31],
                                        'Short Ratio': value_list[32],
                                        'Short % of Float': value_list[33],
                                        'Shares Short (prior ': value_list[34],
                                        'Status': status},
                                       ignore_index=True)
                except Exception as e:
                    # pass
                    print(str(e), ticker, file)
    # for each_ticker in ticker_list:
    #     try:
    #         plot_df = df[(df['Ticker'] == each_ticker)]
    #         plot_df = plot_df.set_index(['Date'])
    #
    #         if plot_df['Status'][-1] == "underperform":
    #             color = 'r'
    #         else:
    #             color = 'g'
    #
    #
    #         plot_df['Difference'].plot(label=each_ticker,color=color)
    #         plt.legend()
    #
    #     except Exception as e:
    #         pass
    #
    # plt.show()
    df.to_csv("key_stats_acc_perf_WITH_NA_enhanced.csv")


def Stock_Prices():
    df = pd.DataFrame()

    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]

    print(stock_list)

    for each_dir in stock_list[1:]:
        try:
            ticker = each_dir.split("\\")[1]
            print(ticker)
            name = "WIKI/" + ticker.upper()
            data = Quandl.get(name,
                              trim_start="2000-12-12",
                              trim_end="2014-12-30",
                              authtoken=auth_tok)
            data[ticker.upper()] = data["Adj. Close"]
            df = pd.concat([df, data[ticker.upper()]], axis=1)

        except Exception as e:
            print(str(e))
            time.sleep(10)

            try:
                ticker = each_dir.split("\\")[1]
                print(ticker)
                name = "WIKI/" + ticker.upper()
                data = Quandl.get(name,
                                  trim_start="2000-12-12",
                                  trim_end="2014-12-30",
                                  authtoken=auth_tok)
                data[ticker.upper()] = data["Adj. Close"]
                df = pd.concat([df, data[ticker.upper()]], axis=1)

            except Exception as e:
                print(str(e))

        df.to_csv("stock_prices.csv")


# Stock_Prices()


Key_Stats()