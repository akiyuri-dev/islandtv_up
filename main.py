
# -*- coding: utf-8 -*-
import json, config
from requests_oauthlib import OAuth1Session
import smtplibfrom email.mime.text
import MIMETextfrom email.utils
import formatdateimport time
import sysimport urllib
from bs4 import BeautifulSoup

#動画サイト更新確認スクレイピング＆ツイートプログラム
#author: Akiyuri
#create date: 2019-03-04
 
#Twitter二段階認証情報をconfigファイルから取得
CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET

#Twitterにログイン
twitter = OAuth1Session(CK, CS, AT, ATS)

#Tweet関数
def tweet(msg):
     url = "https://api.twitter.com/1.1/statuses/update.json"
     #ツイートテキストをセット
     params = {"status" : msg}
 
　 #postリクエスト送信＝ツイート
     res = twitter.post(url, params = params) 
 
　 if res.status_code == 200: #ツイート成功ログ
          print("Success.")
     else: #ツイート失敗ログ
          print("Failed. : %d"% res.status_code)
 
#新着動画検索パート
url = "https://j-island.net/movie/play/id/"
lastId = 0
beforeLast = 0
idList = []

#1分ごとに毎日18時間と少し稼働させたい：60/1 * 18 + 10 = 490
for i in range(490): 

    #現在ID9以上の動画が存在している
    movieId = 1
 
    #抜け番も5つ程度現時点で存在する、発見のたびに加算
    movieNotFound = 0

    #20以上抜け番（動画未アップロード）を確認したらその時間の確認を終了
    while movieNotFound < 20:

       #スクレイピングURL生成
       movieUrl = url + str(movieId)
       #スクレイピング開始       
       html = urllib.urlopen(movieUrl)
       soup = BeautifulSoup(html)
       pageTitle = "ISLAND TV"

       #稀に通信エラーでページ読み込みが間に合わない事例があるが、無視する
       if soup.find("title") is None:
　　　　pass
　　else:
              #日本語標準出力はACIIと認識されてしまうのでエンコード
              #タイトル文字化け対策
              pageTitle = soup.find("title").text.encode('utf-8')
 
              #動画ページが正式に存在するID
              #動画が存在しないページのタイトルが[ISLAND TV]
              if pageTitle != "ISLAND TV": 
                  #動画のタイトル取得
                  movieTitle = soup.find("div", attrs={'class': 'movieplay-infomation__title-title'}).text.encode('utf-8')
 
            #一度めのループで生成したIDリストに存在＝ツイート済み動画
            if movieId in idList:
                   #もうこの動画はツイートした古い動画だから無視
                   print str("True because old movie id is " + str(movieId))
                   pass
 
            #初回ループ or 初回ループで生成したIDリストに存在しない
            else:
                   #新しい動画だ！ツイートだ！
                   print str("False because new movie id is " + str(movieId))
                   print str(movieId) + ":" + str(movieTitle) + ":" + movieUrl

            #初回ループではなく、初回ループで生成したIDリストに存在しない＝新着動画
            if i != 0:
                  #Tweet処理
                  tweetMsg = movieTitle + " " + movieUrl tweet(tweetMsg)
 
            #初回ループ
            else:
                  print "already tweet!"
            BODY += str(movieId)
　　　 idList.append(movieId)
            lastId = movieId

      #動画ページが存在しないID
      else:
            movieNotFound += 1
            pass
      movieId += 1
 
      #サーバ攻撃とみなされないためにスリープ
      time.sleep(1)
 
      #とりあえず最後の動画IDまでこの時間帯の確認を終えたよメッセージ 
      print u"end of check. time is " + str(i) + ". Last Id is " + str(lastId)
     #1分スリープ
     time.sleep(60)

#1日分の処理を終了した時に出力 
print u"Ploglam is over. Please run next time.