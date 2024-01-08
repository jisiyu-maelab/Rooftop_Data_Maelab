# 気象条件計算時用計算式
import datetime
import numpy as np
import pandas as pd


def wind(x):
    wind = round(float(x)/22.5)
    if wind == 0 :
        return 16
    else:
        return wind


# temp外気温(度)rh相対湿度から、絶対湿度算出
def AH(temp, rh):
    AbHumid = 0.622*(6.1078*10**(7.5*temp/(237.3+temp))*rh/100)/(1013.25-(6.1078*10**(7.5*temp/(237.3+temp))*rh/100))
    return AbHumid


def weather_epw(df_all, df_solar):
    df_weather = pd.DataFrame(np.random.random([0, 0]), index=df_all.index, columns=[])
    df_weather["年"] = df_all.index.year
    df_weather["月"] = df_all.index.month
    df_weather["日"] = df_all.index.day
    df_weather["時"] = df_all.index.hour
    df_weather["分"] = df_all.index.minute
    df_weather["リマーク"] = 0
    df_weather["外気温度"] = df_all["外気温2"]  # 外気温1断線のため
    df_weather["相対湿度"] = df_all["屋外湿度計"]
    df_weather["大気圧"] = 101300 # 高度修正あり？なし？
    # df_weather["露点温度"] =
    df_weather["法線面直達日射量"] = df_solar["法線面直達日射量"] # solar sheet で処理後データ
    df_weather["水平面天空日射量"] = df_solar["水平面天空日射量"]
    df_weather["風向"] = df_all["風向"]
    df_weather["風速"] = df_all["風速"]

    df_weather["絶対湿度"] = 0.622 * (
            6.1078 * 10 ** (7.5 * df_weather["外気温度"] / (237.15 + df_weather["外気温度"])) * df_weather["相対湿度"] / 100) / (
                             1013.25 - (6.1078 * 10 ** (7.5 * df_weather["外気温度"] / (237.15 + df_weather["外気温度"])) * df_weather[
                         "相対湿度"] / 100))

    # 気圧の高度補正
    df_10s["Ft"] = 273.15 + df_10s["外気温度"]
    df_10s["大気圧"] = 1000 * 101.325 * (1 - 2.2558 * 0.000001 * 30) ** 5.256  # パソコンによる空気調和計算法　pp.27
    df_10s["飽和水蒸気圧"] = np.exp(-5800.2206 / df_10s["Ft"] + 1.3914993 -
                              0.048640239 * df_10s["Ft"] + 0.000041764768 * (df_10s["Ft"] ** 2) -
                              0.000000014452093 * (df_10s["Ft"] ** 3) + 6.5459673 * np.log(df_10s["Ft"])) / 1000
    df_10s["水蒸気分圧"] = df_10s["飽和水蒸気圧"] * df_10s["相対湿度"] / 100

    df_10s["露点温度"] = - 77.199 + 13.198 * np.log(1000 * df_10s["水蒸気分圧"]) - 0.63772 * np.log(
        1000 * df_10s["水蒸気分圧"]) ** 2 + 0.071098 * np.log(1000 * df_10s["水蒸気分圧"]) ** 3
    # df_10s["可降水量"] = #mm
    print(df_weather)


def w_to_epw(df_weather, df_all, df_solar):



    df_10s["通し日数"] = pd.to_datetime(df_10s.index, format="%Y-%m-%d %H:%M:%S").dayofyear.values
    df_10s["通し時刻"] = pd.to_datetime(df_10s.index, format="%Y-%m-%d %H:%M:%S").hour.values + pd.to_datetime(
        df_10s.index,
        format="%Y-%m-%d %H:%M:%S").minute.values

    df_10s["shiita0"] = (df_10s["通し日数"] - 1) / 365 * 2 * np.pi
    df_10s["太陽赤緯(rad)"] = 0.006918 - 0.399912 * np.cos(df_10s["shiita0"]) + 0.070257 * np.sin(
        df_10s["shiita0"]) - 0.006758 * np.cos(2 * df_10s["shiita0"]) + 0.000907 * np.sin(
        2 * df_10s["shiita0"]) - 0.002697 * np.cos(3 * df_10s["shiita0"]) + 0.00148 * np.sin(3 * df_10s["shiita0"])

    df_10s["均時差(rad)"] = 0.000075 + 0.001868 * np.cos(df_10s["shiita0"]) - 0.032077 * np.sin(
        df_10s["shiita0"]) - 0.014615 * np.cos(2 * df_10s["shiita0"]) - 0.040849 * np.sin(2 * df_10s["shiita0"])
    df_10s["均時差(度)"] = df_10s["均時差(rad)"] / np.pi * 180

    df_10s["時角(rad)"] = (df_10s["通し時刻"] - 12) / 12 * np.pi + (toukei - 135) / 180 * np.pi + df_10s["均時差(rad)"]
    df_10s["太陽高度(rad)"] = np.arcsin(
        np.sin(hokui_rad) * np.sin(df_10s["太陽赤緯(rad)"]) + np.cos(hokui_rad) * np.cos(df_10s["太陽赤緯(rad)"]) * np.cos(
            df_10s["時角(rad)"]))
    df_10s["太陽方位(rad)"] = np.arctan(
        (np.cos(hokui_rad) * np.cos(df_10s["太陽赤緯(rad)"]) * np.sin(df_10s["時角(rad)"])) / (
                np.sin(hokui_rad) * np.sin(df_10s["太陽高度(rad)"]) - np.sin(df_10s["太陽赤緯(rad)"])))

    # 太陽方位(°)計算
    df_10s["太陽方位"] = df_10s["太陽方位(rad)"] / np.pi * 180
    df_10s["太陽方位"].where((df_10s["時角(rad)"] < 0) & (df_10s["太陽方位(rad)"] > 0), df_10s["太陽方位"] - 180, inplace=True)
    df_10s["太陽方位"].where((df_10s["時角(rad)"] > 0) & (df_10s["太陽方位(rad)"] < 0), df_10s["太陽方位"] + 180, inplace=True)

    df_10s["太陽高度"] = df_10s["太陽高度(rad)"] / np.pi * 180

    df_10s["大気放射量"] = - df_10s["IR上向き赤外線放射計"]  # W/m2

    df_10s["全天日射量"] = df_10s["屋根上全天日射計"]  # W/m2

    # 直散分離 udagawa
    # 直散分離 udagawa
    df_10s["I0"] = 1370 * (1 + 0.033 * np.cos(2 * np.pi * df_10s["通し日数"] / 365))  # 大気圏外法線面日射量

    df_10s["太陽高度"].mask(df_10s["太陽高度"] < 3, 3, inplace=True)
    df_10s["太陽高度(rad)"] = df_10s["太陽高度"] * np.pi / 180

    # KTt=Ihol/(Io*sinh)
    df_10s["KTt"] = df_10s["全天日射量"] / (df_10s["I0"] * np.sin(df_10s["太陽高度(rad)"]))
    # KTtc=0.5163+0.333sinh+0.00803sinh^2
    df_10s["KTtc"] = 0.5163 + 0.333 * np.sin(df_10s["太陽高度(rad)"]) + 0.00803 * np.sin(df_10s["太陽高度(rad)"]) ** 2

    # KTt<KTtc Idn=(2.277-1.258*sinh+0.2396sinh^2)Ktt^3Io
    df_10s["直散分離_法線面直達日射"] = (2.277 - 1.258 * np.sin(df_10s["太陽高度(rad)"]) + 0.2396 * np.sin(
        df_10s["太陽高度(rad)"]) ** 2) * \
                             df_10s["KTt"] ** 3 * df_10s["I0"]
    # Kt >= Kc Idn=(-0.43+1.43KTt)Io
    df_10s["直散分離_法線面直達日射"].mask(df_10s["KTt"] > df_10s["KTtc"], df_10s["I0"] * (-0.43 + 1.43 * df_10s["KTt"]),
                                inplace=True)

    df_10s["直散分離_水平面天空日射"] = df_10s["全天日射量"] - df_10s["直散分離_法線面直達日射"] * np.sin(df_10s["太陽高度(rad)"])

    # DN の計算値が 4.18MJ/(m2h) を超える場合，計算値を 4.18MJ/(m2h) に置き換え，計算値と 4.18MJ/(m2h)との差を水平面の値に換算し，SH に加算。
    up_limit = 4.18 * 1000000 / 3600
    df_10s["直散分離_水平面天空日射"].mask(df_10s["直散分離_法線面直達日射"] > up_limit,
                                df_10s["全天日射量"] - np.sin(df_10s["太陽高度(rad)"]) * up_limit,
                                inplace=True)
    df_10s["直散分離_法線面直達日射"].mask(df_10s["直散分離_法線面直達日射"] > up_limit,
                                up_limit, inplace=True)

    # 日射量がマイナス時、０に直す
    df_10s["直散分離_水平面天空日射"].mask(df_10s["直散分離_水平面天空日射"] < 0, 0, inplace=True)
    df_10s["直散分離_法線面直達日射"].mask(df_10s["直散分離_法線面直達日射"] < 0, 0, inplace=True)

    df_10s["法線面直達日射量"] = df_10s["直散分離_法線面直達日射"]  # W/m2
    df_10s["水平面天空日射量"] = df_10s["直散分離_水平面天空日射"]  # W/m2

    # df_10s["グローバル照度"] =  #lx
    # df_10s["法線面直達照度"] =  #lx
    # df_10s["天空照度"] =  #lx
    # df_10s["天頂輝度"] =   #cd/m2

    # df_10s["雲量"] = #1-10
    # df_10s["積雪量"] = #cm

    # 以下拡張アメダスから計算不可
    # df_10s["不透明雲量"] =  #-
    # df_10s["視程"] =  #km
    # df_10s["雲高"] =   #m
    # df_10s["気象状況"] =  #-
    # df_10s["気象コード"] = #-
    # df_10s["大気の光学的厚さ"] = #-
    # df_10s["最後の積雪からの日数"] = #day
    # df_10s["降水時間"] =  #hr

    df_10s.to_csv("10s.csv", encoding="cp932")

    # 毎正時
    df_10s["外気温度"] = df_10s["外気温度"].rolling(window=360).mean()
    df_10s["露点温度"] = df_10s["露点温度"].rolling(window=360).mean()
    df_10s["相対湿度"] = df_10s["相対湿度"].rolling(window=360).mean()
    df_10s["大気圧"] = df_10s["大気圧"].rolling(window=360).mean()

    df_10s["大気放射量"] = df_10s["大気放射量"].rolling(window=360).mean()
    df_10s["全天日射量"] = df_10s["全天日射量"].rolling(window=360).mean()
    df_10s["法線面直達日射量"] = df_10s["法線面直達日射量"].rolling(window=360).mean()
    df_10s["水平面天空日射量"] = df_10s["水平面天空日射量"].rolling(window=360).mean()

    print(df_10s)
    df_epw = df_10s.resample("H").mean()

    df_epw.to_csv("epw.csv", encoding="cp932")
# def w_to_hasp(df_weather):
# 屋上データEPW化
import pandas as pd
import datetime
from pathlib import Path
import itertools

import re
import numpy as np
import sympy as sp
import math

# date_start = input("初日の日付<yyyy-mm-dd>:")
# date_end = input("末尾日の日付<yyyy-mm-dd>:")
# start = datetime.datetime.strptime(date_start, "%Y-%m-%d")
# end = datetime.datetime.strptime(date_end, "%Y-%m-%d")
#
# # 指定日付のファイルパスをリストアップ
# main = Path(r"C:\\Users\\Maelab\\Desktop\\cadacepw")
# file_list = []
# start -= datetime.timedelta(hours=2)
# end += 24 * datetime.timedelta(hours=1)
# while start <= end:
#     file = list(main.glob(start.strftime("%Y-%m-%d_%H-%M-%S") + "*.csv"))
#     file.sort()
#     file_list.append(file)
#     start += datetime.timedelta(hours=1)
# file_list = list(itertools.chain.from_iterable(file_list))
# print(file_list)
#
# hokui = float(35.712678)
# toukei = float(139.761989)
# hokui_rad = hokui / 180 * np.pi
# toukei_rad = toukei / 180 * np.pi
#
# df_lst = []
#
# for file in file_list:
#     df = pd.read_csv(file, skiprows=13, encoding="cp932", index_col=[3]).iloc[3:, 3:]
#     date_str = re.findall(r'[^\\/:*?"<>|\r\n]+$', str(file))
#     date_str = re.split("-|_", date_str[0])
#     date = date_str[0] + "-" + date_str[1] + "-" + date_str[2]
#     print(date)
#     df.rename(index=lambda s: date + " " + s, inplace=True)
#     if len(df) < 360:
#         print(str(file) + "データ欠損")
#     df_lst.append(df)
#
# print(df_lst)
# df_10s = pd.concat(df_lst)
# print(df_10s.columns)
#
# df_10s.rename(columns={"外気温1": "外気温1", "外気温2": "外気温2"}, inplace=True)
# df_10s = df_10s.loc[:,
#          ["外気温1", "外気温2", "屋外湿度計", "直達日射計", "屋根上全天日射計", "鉛直面日射計", "IR上向き日射計", "IR下向き日射計", "IR上向き赤外線放射計", "IR下向き赤外線放射計",
#           "風向", "風速"]]
#
# df_10s = df_10s.astype("float64")
# df_10s.index = pd.to_datetime(df_10s.index)
# print(df_10s.index)
# # 入力日の前日23時から,最終日の翌日1時まで
#
# # マイナス時0にする
# radiation_list = ["直達日射計", "屋根上全天日射計", "鉛直面日射計", "IR上向き日射計", "IR下向き日射計"]
# for i in radiation_list:
#     df_10s[i] = df_10s[i].mask(df_10s[i] < 0, 0)
#
# # EPW用計算
# df_10s["外気温度"] = df_10s["外気温2"]  # ℃
# df_10s["相対湿度"] = df_10s["屋外湿度計"]  # %?
# df_10s["絶対湿度"] = 0.622 * (6.1078 * 10 ** (7.5 * df_10s["外気温度"] / (237.15 + df_10s["外気温度"])) * df_10s["相対湿度"] / 100) / (
#         1013.25 - (6.1078 * 10 ** (7.5 * df_10s["外気温度"] / (237.15 + df_10s["外気温度"])) * df_10s["相対湿度"] / 100))
#
# # 気圧の高度補正
# df_10s["Ft"] = 273.15 + df_10s["外気温度"]
# df_10s["大気圧"] = 1000 * 101.325 * (1 - 2.2558 * 0.000001 * 30) ** 5.256  # パソコンによる空気調和計算法　pp.27
# df_10s["飽和水蒸気圧"] = np.exp(-5800.2206 / df_10s["Ft"] + 1.3914993 -
#                           0.048640239 * df_10s["Ft"] + 0.000041764768 * (df_10s["Ft"] ** 2) -
#                           0.000000014452093 * (df_10s["Ft"] ** 3) + 6.5459673 * np.log(df_10s["Ft"])) / 1000
# df_10s["水蒸気分圧"] = df_10s["飽和水蒸気圧"] * df_10s["相対湿度"] / 100
#
# df_10s["露点温度"] = - 77.199 + 13.198 * np.log(1000 * df_10s["水蒸気分圧"]) - 0.63772 * np.log(
#     1000 * df_10s["水蒸気分圧"]) ** 2 + 0.071098 * np.log(1000 * df_10s["水蒸気分圧"]) ** 3
# # df_10s["可降水量"] = #mm
#
# df_10s["通し日数"] = pd.to_datetime(df_10s.index, format="%Y-%m-%d %H:%M:%S").dayofyear.values
# df_10s["通し時刻"] = pd.to_datetime(df_10s.index, format="%Y-%m-%d %H:%M:%S").hour.values + pd.to_datetime(df_10s.index,
#                                                                                                        format="%Y-%m-%d %H:%M:%S").minute.values
#
# df_10s["shiita0"] = (df_10s["通し日数"] - 1) / 365 * 2 * np.pi
# df_10s["太陽赤緯(rad)"] = 0.006918 - 0.399912 * np.cos(df_10s["shiita0"]) + 0.070257 * np.sin(
#     df_10s["shiita0"]) - 0.006758 * np.cos(2 * df_10s["shiita0"]) + 0.000907 * np.sin(
#     2 * df_10s["shiita0"]) - 0.002697 * np.cos(3 * df_10s["shiita0"]) + 0.00148 * np.sin(3 * df_10s["shiita0"])
#
# df_10s["均時差(rad)"] = 0.000075 + 0.001868 * np.cos(df_10s["shiita0"]) - 0.032077 * np.sin(
#     df_10s["shiita0"]) - 0.014615 * np.cos(2 * df_10s["shiita0"]) - 0.040849 * np.sin(2 * df_10s["shiita0"])
# df_10s["均時差(度)"] = df_10s["均時差(rad)"] / np.pi * 180
#
# df_10s["時角(rad)"] = (df_10s["通し時刻"] - 12) / 12 * np.pi + (toukei - 135) / 180 * np.pi + df_10s["均時差(rad)"]
# df_10s["太陽高度(rad)"] = np.arcsin(
#     np.sin(hokui_rad) * np.sin(df_10s["太陽赤緯(rad)"]) + np.cos(hokui_rad) * np.cos(df_10s["太陽赤緯(rad)"]) * np.cos(
#         df_10s["時角(rad)"]))
# df_10s["太陽方位(rad)"] = np.arctan((np.cos(hokui_rad) * np.cos(df_10s["太陽赤緯(rad)"]) * np.sin(df_10s["時角(rad)"])) / (
#         np.sin(hokui_rad) * np.sin(df_10s["太陽高度(rad)"]) - np.sin(df_10s["太陽赤緯(rad)"])))
#
# # 太陽方位(°)計算
# df_10s["太陽方位"] = df_10s["太陽方位(rad)"] / np.pi * 180
# df_10s["太陽方位"].where((df_10s["時角(rad)"] < 0) & (df_10s["太陽方位(rad)"] > 0), df_10s["太陽方位"] - 180, inplace=True)
# df_10s["太陽方位"].where((df_10s["時角(rad)"] > 0) & (df_10s["太陽方位(rad)"] < 0), df_10s["太陽方位"] + 180, inplace=True)
#
# df_10s["太陽高度"] = df_10s["太陽高度(rad)"] / np.pi * 180
#
# df_10s["大気放射量"] = - df_10s["IR上向き赤外線放射計"]  # W/m2
#
# df_10s["全天日射量"] = df_10s["屋根上全天日射計"]  # W/m2
#
# # 直散分離 udagawa
# # 直散分離 udagawa
# df_10s["I0"] = 1370 * (1 + 0.033 * np.cos(2 * np.pi * df_10s["通し日数"] / 365))  # 大気圏外法線面日射量
#
# df_10s["太陽高度"].mask(df_10s["太陽高度"] < 3, 3, inplace=True)
# df_10s["太陽高度(rad)"] = df_10s["太陽高度"] * np.pi / 180
#
# # KTt=Ihol/(Io*sinh)
# df_10s["KTt"] = df_10s["全天日射量"] / (df_10s["I0"] * np.sin(df_10s["太陽高度(rad)"]))
# # KTtc=0.5163+0.333sinh+0.00803sinh^2
# df_10s["KTtc"] = 0.5163 + 0.333 * np.sin(df_10s["太陽高度(rad)"]) + 0.00803 * np.sin(df_10s["太陽高度(rad)"]) ** 2
#
# # KTt<KTtc Idn=(2.277-1.258*sinh+0.2396sinh^2)Ktt^3Io
# df_10s["直散分離_法線面直達日射"] = (2.277 - 1.258 * np.sin(df_10s["太陽高度(rad)"]) + 0.2396 * np.sin(df_10s["太陽高度(rad)"]) ** 2) * \
#                          df_10s["KTt"] ** 3 * df_10s["I0"]
# # Kt >= Kc Idn=(-0.43+1.43KTt)Io
# df_10s["直散分離_法線面直達日射"].mask(df_10s["KTt"] > df_10s["KTtc"], df_10s["I0"] * (-0.43 + 1.43 * df_10s["KTt"]), inplace=True)
#
# df_10s["直散分離_水平面天空日射"] = df_10s["全天日射量"] - df_10s["直散分離_法線面直達日射"] * np.sin(df_10s["太陽高度(rad)"])
#
# # DN の計算値が 4.18MJ/(m2h) を超える場合，計算値を 4.18MJ/(m2h) に置き換え，計算値と 4.18MJ/(m2h)との差を水平面の値に換算し，SH に加算。
# up_limit = 4.18 * 1000000 / 3600
# df_10s["直散分離_水平面天空日射"].mask(df_10s["直散分離_法線面直達日射"] > up_limit,
#                             df_10s["全天日射量"] - np.sin(df_10s["太陽高度(rad)"]) * up_limit,
#                             inplace=True)
# df_10s["直散分離_法線面直達日射"].mask(df_10s["直散分離_法線面直達日射"] > up_limit,
#                             up_limit, inplace=True)
#
# # 日射量がマイナス時、０に直す
# df_10s["直散分離_水平面天空日射"].mask(df_10s["直散分離_水平面天空日射"] < 0, 0, inplace=True)
# df_10s["直散分離_法線面直達日射"].mask(df_10s["直散分離_法線面直達日射"] < 0, 0, inplace=True)
#
# df_10s["法線面直達日射量"] = df_10s["直散分離_法線面直達日射"]  # W/m2
# df_10s["水平面天空日射量"] = df_10s["直散分離_水平面天空日射"]  # W/m2
#
# # df_10s["グローバル照度"] =  #lx
# # df_10s["法線面直達照度"] =  #lx
# # df_10s["天空照度"] =  #lx
# # df_10s["天頂輝度"] =   #cd/m2
#
# # df_10s["雲量"] = #1-10
# # df_10s["積雪量"] = #cm
#
# # 以下拡張アメダスから計算不可
# # df_10s["不透明雲量"] =  #-
# # df_10s["視程"] =  #km
# # df_10s["雲高"] =   #m
# # df_10s["気象状況"] =  #-
# # df_10s["気象コード"] = #-
# # df_10s["大気の光学的厚さ"] = #-
# # df_10s["最後の積雪からの日数"] = #day
# # df_10s["降水時間"] =  #hr
#
#
# df_10s.to_csv("10s.csv", encoding="cp932")
#
# # 毎正時
# df_10s["外気温度"] = df_10s["外気温度"].rolling(window=360).mean()
# df_10s["露点温度"] = df_10s["露点温度"].rolling(window=360).mean()
# df_10s["相対湿度"] = df_10s["相対湿度"].rolling(window=360).mean()
# df_10s["大気圧"] = df_10s["大気圧"].rolling(window=360).mean()
#
# df_10s["大気放射量"] = df_10s["大気放射量"].rolling(window=360).mean()
# df_10s["全天日射量"] = df_10s["全天日射量"].rolling(window=360).mean()
# df_10s["法線面直達日射量"] = df_10s["法線面直達日射量"].rolling(window=360).mean()
# df_10s["水平面天空日射量"] = df_10s["水平面天空日射量"].rolling(window=360).mean()
#
# print(df_10s)
# df_epw = df_10s.resample("H").mean()
#
# df_epw.to_csv("epw.csv", encoding="cp932")
#

def limit(x, type, limitation):
    if x == "bigger":
        if x <= limitation:
            return limitation
    if type == "smaller":
        if x >= limitation:
            return limitation



