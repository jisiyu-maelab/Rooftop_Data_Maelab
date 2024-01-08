import numpy as np
import pandas as pd


def datagrouping(df_all, date_str, df_solar):
    with pd.ExcelWriter("G:\共有ドライブ\屋上Cadac2021\day" + "\\" + date_str + ".xlsx") as writer:
        weather_sheet = df_all.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]]
        weather_sheet = weather_sheet.resample("1T").mean()
        weather_sheet.to_excel(writer, sheet_name="気象データ")
        print("シート気象データを書き出した。")

        df_solar = df_solar.resample("1T").mean()
        df_solar.to_excel(writer, sheet_name="日射計算")
        print("シート日射計算を書き出した。")

        labels = [[["日射計"]],  # 1
                  [["屋外側空気温度"]],  # 2
                  [["床表面温度"]],  # 3
                  [["天井表面温度"]],  # 4
                  [["壁表面温度"]],  # 5
                  [["上下温度"]],  # 6
                  [["ｸﾞﾛｰﾌﾞ温度"], ["放射温度"]],  # 7
                  [["天井", "10cm", "熱流計"], ["天井", "熱橋", "熱流計"], ["天井", "非敷設部", "熱流計"]],  # 8
                  [["床", "10cm", "熱流計"], ["床", "熱橋", "熱流計"], ["床", "非敷設部", "熱流計"]],  # 9
                  [["壁熱流計"]],  # 10
                  [["屋外窓ﾌﾚｰﾑ表面温度"]],  # 11
                  [["湿度"]],  # 12
                  [["FCU"], ["温度ｾﾝｻｰｱﾅﾛｸﾞ出力"]],  # 13
                  [["電力"]],  # 14
                  [["室内側", "ｶﾞﾗｽ"]],  # 15
                  [["室内側", "ﾌﾚｰﾑ"]],  # 16
                  [["ﾙｰﾊﾞｰ"]],  # 17
                  [["ｽｸﾘｰﾝ"]],  # 18
                  [["IR"]],
                  [["5cm", "熱電対"]],  # 20
                  [["5cm", "熱流計"]],
                  [["風速"]]
                  ]  # 23

        sheetname_l = ["日射計",  # 1
                       "屋外側空気温度",  # 2
                       "床表面温度",  # 3
                       "天井表面温度",  # 4
                       "壁表面温度",  # 5
                       "上下温度",  # 6
                       "ｸﾞﾛｰﾌﾞ放射温度",  # 7
                       "天井熱流計",  # 8
                       "床熱流計",  # 9
                       "壁熱流計",  # 10
                       "屋外窓ﾌﾚｰﾑ表面温度",  # 11
                       "湿度",  # 12
                       "FCU",  # 13
                       "電力",  # 14
                       "室内側ｶﾞﾗｽ",  # 15
                       "室内側ﾌﾚｰﾑ",  # 16
                       "ﾙｰﾊﾞｰ",  # 17
                       "ｽｸﾘｰﾝ",  # 18
                       "IR",  # 19
                       "PCM温度",
                       "PCM熱流",
                       "その他"
                       ]  # 23

        for a, sheet in enumerate(labels):
            sheetname = sheetname_l[a]
            column_in_group_ls = []  # 「ColumnはGroupのKeysを含めているか」のBoolean listのlist
            for b, group in enumerate(sheet):
                column_include_key_ls = []  # 「ColumnはKeyを含めているか」のBoolean listのlist
                for c, key in enumerate(group):  #
                    column_include_key = df_all.columns.str.contains(key)  # ColumnはKeyを含めているか
                    column_include_key_ls.append(column_include_key)
                # 「and」ロジックでcolumn_include_key_lsにあるBoolean listを統合し、
                # 「ColumnはGroupのKeysを含めているか」のBoolean listに変換
                column_in_sheet = column_include_key_ls[0]
                for cik in column_include_key_ls:
                    column_in_sheet = np.logical_and(column_in_sheet, cik)
                column_in_group_ls.append(column_in_sheet)
                # 「or」ロジックでcolumn_in_group_lsにあるBoolean listを統合して、
                # 「ColumnはこのSheetに属するか」のBoolean listに変換
            column_in_sheet = column_in_group_ls[0]
            for cins in column_in_group_ls:
                column_in_sheet = np.logical_or(column_in_sheet, cins)
            df_sheet = df_all.iloc[:, column_in_sheet]  # 抽出
            column_in_sheet = df_sheet.columns.values.tolist()
            column_in_sheet.sort()
            df_sheet = df_sheet.loc[:, column_in_sheet]
            df_sheet = df_sheet.resample("1T").mean()
            # print(df_sheet.columns)
            df_sheet.to_excel(writer, sheet_name=sheetname)
            # 計算過程を把握するため、メッセージを出力
            print("シート" + sheetname + "を書き出した")