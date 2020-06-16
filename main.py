import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, preprocessing
from sklearn.model_selection import train_test_split
import pandas as pd
from matplotlib import style
import quandl
import statistics
import math
from collections import Counter

style.use("ggplot")
quandl.ApiConfig.api_key = ''
# quandl.ApiConfig.api_version = '2015-04-09'

# data = quandl.get_table('ZACKS/FC', ticker='AAPL')
# print(str(data.head()))

how_much_better = 5.4

FEATURES = [
            # 'DE Ratio',
            # 'Trailing P/E',
            # 'Price/Sales',
            # 'Price/Book',
            # 'Profit Margin',
            # 'Operating Margin',
            # 'Return on Assets',
            # 'Return on Equity',
            # 'Revenue Per Share',
            'Market Cap',
            'Enterprise Value',
            # 'Forward P/E',
            # 'PEG Ratio',
            # 'Enterprise Value/Revenue',
            # 'Enterprise Value/EBITDA',
            # 'Revenue',
            'Gross Profit',
            # 'EBITDA',
            # 'Net Income Avl to Common ',
            # 'Diluted EPS',
            # 'Earnings Growth',
            # 'Revenue Growth',
            'Total Cash',
            # 'Total Cash Per Share',
            # 'Total Debt',
            # 'Current Ratio',
            'Book Value Per Share',
            'Cash Flow',
            #'Beta',
            # 'Held by Insiders',
            # 'Held by Institutions',
            # 'Shares Short (as of',
            # 'Short Ratio',
            # 'Short % of Float',
            'Shares Short (prior ']

FEATURES = ['DE Ratio',
            'Trailing P/E',
            # 'Price/Sales',
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
            'Shares Short (prior ']


def Status_Calc(stock, sp500):
    difference = stock - sp500

    if difference > how_much_better:
        return 1
    else:
        return 0

def Build_Data_Set():
    data_df = pd.read_csv("key_stats_acc_perf_WITH_NA.csv")

    # data_df = data_df[:100]
    data_df = data_df.reindex(np.random.permutation(data_df.index))
    data_df = data_df.fillna(0)

    data_df["Status2"] = list(map(Status_Calc, data_df["stock_p_change"], data_df["sp500_p_change"]))

    X = np.array(data_df[FEATURES].values)

    y = (data_df["Status2"]
         .replace("underperform", 0)
         .replace("outperform", 1)
         .values.tolist())

    X = preprocessing.scale(X)
    Z = np.array(data_df[["stock_p_change", "sp500_p_change"]])

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    return X, y, Z


def plot_coefficients(classifier, feature_names, top_features=17):
    coef = classifier.coef_.ravel()
    top_positive_coefficients = np.argsort(coef)[-top_features:]
    top_negative_coefficients = np.argsort(coef)[:top_features]
    top_coefficients = np.hstack([top_negative_coefficients, top_positive_coefficients])
    # create plot
    plt.figure(figsize=(15, 5))
    colors = ['red' if c < 0 else 'blue' for c in coef[top_coefficients]]
    plt.bar(np.arange(2 * top_features), coef[top_coefficients], color=colors)
    feature_names = np.array(feature_names)
    plt.xticks(np.arange(0, 1 + 2 * top_features), feature_names[top_coefficients], rotation=60, ha='right')
    plt.show()

def Analysis():
    test_size = 1
    X, y, Z = Build_Data_Set()
    print(len(X))

    clf = svm.SVC(kernel="linear", C=1.0)
    clf.fit(X[:-test_size], y[:-test_size])

    # plot_coefficients(clf, FEATURES)

    # correct_count = 0
    #
    # invest_amount = 100
    # total_invests = 0
    # if_market = 0
    # if_strat = 0
    #
    # for x in range(1, test_size + 1):
    #     if clf.predict(X[[-x]])[0] == y[-x]:
    #         correct_count += 1
    #
    #     if clf.predict(X[[-x]])[0] == 1:
    #         invest_return = invest_amount + (invest_amount * (Z[-x][0] / 100))
    #         market_return = invest_amount + (invest_amount * (Z[-x][1] / 100))
    #         total_invests += 1
    #         if not math.isnan(market_return):
    #             if_market += market_return
    #         if not math.isnan(invest_return):
    #             if_strat += invest_return
    #
    #
    # print("Accuracy:", (correct_count / test_size) * 100.00)
    #
    # print("Total Trades:", total_invests)
    # print("Ending with Strategy:", if_strat)
    # print("Ending with Market:", if_market)
    #
    # compared = ((if_strat - if_market) / if_market) * 100.0
    # do_nothing = total_invests * invest_amount
    #
    # avg_market = ((if_market - do_nothing) / do_nothing) * 100.0
    # avg_strat = ((if_strat - do_nothing) / do_nothing) * 100.0
    #
    # print("Compared to market, we earn", str(compared) + "% more")
    # print("Average investment return:", str(avg_strat) + "%")
    # print("Average market return:", str(avg_market) + "%")

    data_df = pd.read_csv("forward_sample_WITH_NA.csv")
    data_df = data_df.fillna(0)

    X = np.array(data_df[FEATURES].values)

    X = preprocessing.scale(X)

    Z = data_df["Ticker"].values.tolist()

    invest_list = []

    for i in range(len(X)):
        p = clf.predict(X[[i]])[0]
        if p == 1:
            invest_list.append(Z[i])

    print(len(invest_list))
    print(invest_list)
    return invest_list


final_list = []

loops = 8

for x in range(loops):
    stock_list = Analysis()
    for e in stock_list:
        final_list.append(e)

x = Counter(final_list)

print(15 * "_")
for each in x:
    if x[each] > loops - (loops / 3):
        print(each)

