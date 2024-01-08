import pandas as pd
from pathlib import Path
import mojimoji
import datetime
import re


def fileoperate(date):
    main = Path(r"G:\\共有ドライブ\\屋上Cadac2021\\main")
    master = Path(r"G:\\共有ドライブ\\屋上Cadac2021\\master")  # ファイルパス指定

    # main = Path(r"F:\\CADAC\Cadac3メイン\Data")
    # master = Path(r"F:\\CADAC\Cadac3マスター\Data")  # ファイルパス指定

    # 0時から24時
    date_today = datetime.datetime.strptime(date, "%Y-%m-%d")
    date_tomorrow = date_today + datetime.timedelta(days=1)
    date_str_today = date_today.strftime('%Y-%m-%d')
    date_str_tomorrow = date_tomorrow.strftime('%Y-%m-%d')

    clock = ["_00", "_01", "_02", "_03", "_04", "_05", "_06", "_07", "_08", "_09", "_10", "_11",
             "_12", "_13", "_14", "_15", "_16", "_17", "_18", "_19", "_20", "_21", "_22", "_23"]
    # list_del_today = []  # ★当日0時から
    list_del_today = ["_00", "_01", "_02", "_03", "_04", "_05"]  # ★当日0時から６時前を排除
    list_keep_today = list(set(clock) - set(list_del_today))  # 24時間から排除分を差し引く
    delete_today = list(map(lambda s: date_str_today + s, list_keep_today))
    keep_tomorrow = list(map(lambda s: date_str_tomorrow + s, list_del_today))

    name_l_main = []
    name_l_master = []
    for t in delete_today:
        name_l_main += list(main.glob(t + "*.csv"))
        name_l_master += list(master.glob(t + "*.csv"))
    for t in keep_tomorrow:
        name_l_main += list(main.glob(t + "*.csv"))
        name_l_master += list(master.glob(t + "*.csv"))
    name_l_main.sort()
    name_l_master.sort()

    df_main = pd.DataFrame()
    df_master = pd.DataFrame()
    for file_main in name_l_main:
        df_temp = pd.read_csv(file_main, skiprows=13, encoding="cp932", index_col=[3]).iloc[3:, 3:]
        result = re.findall(r'[^\\/:*?"<>|\r\n]+$', str(file_main))
        result = re.findall(r'(.+)+_+(.*?)\.csv', result[0])
        date_temp = result[0][0]
        df_temp.rename(index=lambda s: date_temp + " " + s, inplace=True)  # datetime日付追記
        df_main = df_main.append(df_temp)
    for file_master in name_l_master:
        df_temp = pd.read_csv(file_master, skiprows=13, encoding="cp932", index_col=[3]).iloc[3:, 3:]
        result = re.findall(r'[^\\/:*?"<>|\r\n]+$', str(file_master))
        result = re.findall(r'(.+)+_+(.*?)\.csv', result[0])
        date_temp = result[0][0]
        df_temp.rename(index=lambda s: date_temp + " " + s, inplace=True)   # datetime日付追記
        df_master = df_master.append(df_temp)
    print("File checked.")

    # df_main = pd.concat(list_main)
    # df_master = pd.concat(list_master, sort=False)     # 「, sort=False」追記210816岸本

    df_main.index = pd.to_datetime(df_main.index)
    df_master.index = pd.to_datetime(df_master.index)

    df_main_rounded = df_main.copy()
    df_main_rounded.index = df_main.index.floor(freq="10S")
    print("df_main_rounded.index", df_main_rounded.index)

    df_master_rounded = df_master.copy()
    df_master_rounded.index = df_master.index.floor(freq="10S")
    print("df_master_rounded.index", df_master_rounded.index)

    # DataFrameの結合
    df_all = pd.merge(df_main_rounded, df_master_rounded, left_index=True, right_index=True, how='inner')

    # df_all = pd.concat([df_main.reset_index(drop=True), df_master.reset_index(drop=True)], axis=1)

    # df_all = df_main.join(df_master)
    print(df_all)

    df_all.rename(columns=lambda z: mojimoji.zen_to_han(z), inplace=True)
    df_all.index = pd.to_datetime(df_all.index)
    df_all = df_all.astype(float)
    df_all = df_all.rename(columns={"湿度ｾﾝｻｰｱﾅﾛｸﾞ出力": "FCU温度ｾﾝｻｰｱﾅﾛｸﾞ出力"})
    # df_all["FCU温度ｾﾝｻｰｱﾅﾛｸﾞ出力"] = df_all["FCU温度ｾﾝｻｰｱﾅﾛｸﾞ出力"] * 0.5

    if len(df_all) < 8640:
        print("データに欠損があります。")

    return df_all