import gspread
import json
import twitter
import csv
import pandas as pd
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 

# 取得したキーとアクセストークンを設定する
auth = twitter.OAuth(consumer_key="nJBZpcyMCXBmjRtTpN5FtM6qZ",
                     consumer_secret="Ok0lLw3UqQNiQ8ybprTaUc2scpUzWyTAUxoctJM43QGCISzDbP",
                     token="1016291971084632064-VOpvNqaicAoGV7Cz4ecK2btouJzYx5",
                     token_secret="0MkUaY6VKfbjWiD1hfUqGFPWRNuKVtdwinMQ9ui7ZhnLL")

t = twitter.Twitter(auth=auth)



#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('edasakocoke-a999cfa04c69.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '1KMtGTCGWMDAGUaTrmVX80vYC_45j4eS695DhkoOxiWo'

#共有設定したスプレッドシートのシート1を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

values = worksheet.get_all_values()

context = ""

total = 0
for i in range(len(values)):
    if values[i][5] != "1" :
        context += "コカ・コーラ（" + values[i][0] + "ml）" +"\n"
        context += "価格:" + values[i][1] + "（" + values[i][2] +"）" +"\n"
        context += "賞味期限:" + values[i][3] +"\n"
        context += "仕様:" + values[i][4] +"\n"
        for q in range(len(values)):
            total += int(values[q][0])
        context += "2020年度総量:" + str(total) + "ml"+"\n"
        t.statuses.update(status=context)
        worksheet.update_cell(i + 1, 6, '1')

    context = ""