import pandas as pd
import datetime
from pathlib import Path
import itertools
import re
import numpy as np
import sympy as sp
import math
# 計算モジュールの導入
import datagrouping
import fileoperate
import errorcleaning
import cal_
import weather
import heatbalance
import cal_shading
if __name__ == "__main__":
    solar_check = 0  # 0番→直達日射計使用　1番→Perez直散分離

    date = "2023-12-03"  # <yyyy-mm-dd>の形式に入力
    # 注意：遮蔽物有無、PCM有無等の条件において、異なるテンプレを使用する必要がある！
    templatepath = r"G:\\共有ドライブ\\屋上Cadac2021\\template_test_pcm_new(床).xlsx"

    date_ymd = date.split("-")  # "-"で連接させた,年、月、日を分割し、リスト化 eg.[2020,08,01]
    date_str = date_ymd[0] + date_ymd[1] + date_ymd[2]
    df_all = fileoperate.fileoperate(date)  # ファイル集計
    print(df_all)

    print(df_all["天井表面温度F①"])
    df_error_1min = errorcleaning.errorcleaning(date, df_all)  # 極端値を書き換え
    df_all = cal_.cal_sheet(df_all)  # 追加計算や計測名の修正
    # df_weather = weather.weather(df_all)

    df_solar = cal_.cal_solar(date_ymd, df_all)  # 太陽位置計算
    # 向きの関数定義
    df_solar = cal_.cal_Perez(date_ymd, solar_check, df_all, df_solar)  # 日射計算(Perez or 計測値使用)
    df_solar = cal_shading.cal_shading(df_solar)  # 庇計算
    # epw作成の際は、★epw.pyを使用

    df_all = datagrouping.datagrouping(df_all, date_str, df_solar)  # 各シートを書き出し
    print(date + "日データ出力完了。")

    # ここからは熱収支シートのテンプレートファイルに、一日データを転写する
    heatbalance.heatbalance(templatepath, date_str)
    print("熱収支確認シートを作成した")
    # errorcleaning.red(date_str, df_error_1min)

    # heatbalance.red()
