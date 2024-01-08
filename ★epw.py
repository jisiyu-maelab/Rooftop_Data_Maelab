import os
import datetime
import csv
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
from epw import epw
import sys
#  注意：まずepw作成期間中の一日データをすべて書き出してから本プログラムを使用
date_start = "2023-08-01"
date_end = "2023-08-01"


def str2float(weather_data):
    try:
        return float(weather_data)
    except:
        return 0


def scraping(url, date):  # 気象庁からアメダスデータをスクリプト
    # 気象データのページを取得
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, features="lxml")
    trs = soup.find("table", {"class": "data2_s"})

    data_list = []
    data_list_per_hour = []

    # table の中身を取得
    for tr in trs.findAll('tr')[2:]:
        tds = tr.findAll('td')
        if tds[1].string == None:
            break
        data_list.append(date)
        data_list.append(tds[0].string)
        for i in range(1, 13):
            data_list.append(str2float(tds[i].string))
        data_list_per_hour.append(data_list)
        data_list = []
    return data_list_per_hour


def create_csv():
    output_dir = r"G:\共有ドライブ\屋上Cadac2021\epw"  # CSV 出力先ディレクトリ
    # データ取得開始・終了日
    start_date_ymd = date_start.split("-")
    end_date_ymd = date_end.split("-")
    start_date = datetime.date(int(start_date_ymd[0]), int(start_date_ymd[1]), int(start_date_ymd[2]))
    end_date = datetime.date(int(end_date_ymd[0]), int(end_date_ymd[1]), int(end_date_ymd[2]))
    output_file = "weather.csv"  # 出力ファイル名

    # CSV の列
    fields = ["年月日", "時間", "気圧（現地）", "気圧（海面）", "降水量", "気温", "露点温度", "蒸気圧", "湿度",
              "風速", "風向", "日照時間", "全天日射量", "降雪", "積雪", "雲量"]  # 天気、視程は今回は対象外とする

    with open(os.path.join(output_dir, output_file), 'w') as f:
        # print("f", f)
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(fields)
        date = start_date
        while date != end_date + datetime.timedelta(1):
            url = "http://www.data.jma.go.jp/obd/stats/etrn/view/hourly_s1.php?" \
                  "prec_no=44&block_no=47662&year=%d&month=%d&day=%d&view="%(date.year, date.month, date.day)
            data_per_day = scraping(url, date)
            print(type(data_per_day))
            for dpd in data_per_day:
                writer.writerow(dpd)
            date += datetime.timedelta(1)

    df_amedas = pd.read_csv(r"G:\共有ドライブ\屋上Cadac2021\epw\weather.csv", encoding="shift_jis")
    # pd.to_datetime(df_amedas["年月日"], format="%Y-%m-%d")
    print("df_amedas.head", df_amedas.head)
    df_amedas["気圧（現地）"] = df_amedas["気圧（現地）"] * 100
    df_amedas["時間"] = df_amedas["時間"] - 1
    df_amedas["時間"] = df_amedas["時間"].astype("str")
    df_amedas["時間"] = df_amedas["時間"].str.zfill(2)
    df_amedas["time"] = df_amedas["年月日"] + " " + df_amedas["時間"] + ":00"

    df_amedas["time"] = pd.to_datetime(df_amedas["time"], format='%Y-%m-%d %H:%M')
    df_amedas.index = df_amedas["time"]
    df_amedas = df_amedas[["露点温度", "湿度", "気圧（現地）", "降水量"]] # "気温",
    return df_amedas


def measurement_epw():
    # 指定日付のファイルパスをリストアップ
    main = r"G:\\共有ドライブ\\屋上Cadac2021\\day\\"
    file_list = []
    start = datetime.datetime.strptime(date_start, "%Y-%m-%d")
    end = datetime.datetime.strptime(date_end, "%Y-%m-%d")
    date = start
    while date <= end:
        file = main + date.strftime('%Y%m%d') + ".xlsx"
        file_list.append(file)
        date += datetime.timedelta(days=1)
    print(file_list)
    # 計測気象データをdf_epw_mに集計
    df_epw_m = pd.DataFrame()
    for f in file_list:
        df_meteo = pd.read_excel(f, sheet_name="気象データ", index_col=0)
        # df_meteo.drop(["IR上向き日射計", "IR上向き赤外線放射計", "IR下向き日射計", "IR下向き赤外線放射計"], axis=1)
        df_rad = pd.read_excel(f, sheet_name="日射計算", index_col=0)
        df_ir = pd.read_excel(f, sheet_name="IR", index_col=0)
        df_epw_f = pd.merge(df_meteo, df_rad, left_index=True, right_index=True)
        df_epw_f = pd.merge(df_epw_f, df_ir, left_index=True, right_index=True)
        df_epw_m = pd.concat([df_epw_m, df_epw_f], axis=0)
        # df_epw_m = df_epw_m.loc[:, ~df_epw_m.columns.duplicated()]
    print(df_epw_m.columns)

    df_epw_m_1h = pd.DataFrame()
    # df_epw_m_1h["大気放射量"] = df_epw_m.resample("H")["IR上向き赤外線放射計_x"].sum() / 60  # Wh/m2
    # df_epw_m_1h["大気放射量温度分"] = 0.0000000567 * ((df_epw_m.resample("H")["IR収支計温度"].mean() + 273.15) ** 4)  # Wh/m2
    # df_epw_m_1h["大気放射量"] = df_epw_m_1h["大気放射量"] + df_epw_m_1h["大気放射量温度分"]
    # df_epw_m_1h = df_epw_m_1h.drop(["大気放射量温度分"], axis='columns')
    df_epw_m_1h["気温"] = df_epw_m.resample("H")["外気温2"].sum() / 60  # C
    df_epw_m_1h["全天日射量"] = df_epw_m.resample("H")["水平面全天日射量"].sum() / 60  # Wh/m2
    df_epw_m_1h["法線面直達日射量"] = df_epw_m.resample("H")["法線面直達日射量"].sum() / 60  # Wh/m2
    df_epw_m_1h["水平面天空日射量"] = df_epw_m.resample("H")["水平面天空日射量"].sum() / 60  # Wh/m2
    df_epw_m_1h["風向"] = df_epw_m["風向"].loc[::60]
    df_epw_m_1h["風速"] = df_epw_m["風速"].loc[::60]
    df_epw_m_1h.to_csv(r'G:\共有ドライブ\屋上Cadac2021\epw\weather.csv', encoding="shift_jis")

    print(df_epw_m_1h)
    return df_epw_m_1h


def combine_epw(df_epw_m_1h, df_amedas):
    df_epw = pd.merge(df_epw_m_1h, df_amedas, left_index=True, right_index=True)
    print("df_epw.columns", df_epw.columns)
    df_epw.index = df_epw.index.map(lambda t: t.replace(year=2006))
    df_epw["年"] = df_epw.index.year
    df_epw["月"] = df_epw.index.month
    df_epw["日"] = df_epw.index.day
    df_epw["時"] = df_epw.index.hour
    df_epw["分"] = df_epw.index.minute

    replace_data = {"年": "Year",
                    "月": "Month",
                    "日": "Day",
                    "時": "Hour",
                    "分": "Minute",
                    "気温": "Dry Bulb Temperature",
                    "露点温度": "Dew Point Temperature",
                    "湿度": "Relative Humidity",
                    "気圧（現地）": "Atmospheric Station Pressure",
                    # "大気放射量": "Horizontal Infrared Radiation Intensity",
                    "全天日射量": "Global Horizontal Radiation",
                    "法線面直達日射量": "Direct Normal Radiation",
                    "水平面天空日射量": "Diffuse Horizontal Radiation",
                    "風向": "Wind Direction",
                    "風速": "Wind Speed",
                    "降水量": "Liquid Precipitation Depth"}

    df_epw = df_epw.rename(columns=replace_data)
    print(df_epw.columns)
    df_epw.to_csv(r'G:\共有ドライブ\屋上Cadac2021\epw\weather.csv', encoding="shift_jis")
    return df_epw


if __name__ == '__main__':
    create_csv()
    measurement_epw()
    df_epw = combine_epw(create_csv(), measurement_epw())
    a = epw()
    a.read(r"G:\共有ドライブ\屋上Cadac2021\epw\★JPN_36303333_TOKYO_EA.epw")
    # print("a.dataframe.columns", a.dataframe.columns)
    a.dataframe["Minute"] = "00"
    a.dataframe["Hour"] = a.dataframe["Hour"] - 1
    a.dataframe.index = a.dataframe["Year"].astype(str) + "-" + a.dataframe["Month"].astype(str).str.zfill(2) + "-" + \
                            a.dataframe["Day"].astype(str).str.zfill(2) + " " + a.dataframe["Hour"].astype(str).str.zfill(2)\
                            + ":" + a.dataframe["Minute"].astype(str)
    a.dataframe.index = pd.to_datetime(a.dataframe.index, format="%Y%m%d %H:%M")
    a.dataframe.loc[df_epw.index, df_epw.columns] = df_epw
    a.dataframe["Hour"] = a.dataframe["Hour"] + 1
    a.write(r"G:\\共有ドライブ\\屋上Cadac2021\\epw\\" + date_start + date_end + ".epw")
    print("epwファイルを出力しました。")




