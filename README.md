# BOJ_DATA 日本銀行の統計データを取得するツール

## 概要
[日本銀行](URL "http://www.boj.or.jp/")の統計データを取得するためのツール。get_boj_data.pyを実行すると日本銀行にあるデータ系列名称の一覧が表示されるので、そこから欲しいデータを選択(複数可)→実行すると選択したデータのcsvファイルが作成される(複数ファイルを選択した場合、期種ごとにまとまってcsvファイルが作成される。ファイル名は現状ダウンロードしたままの名前)。データの置き場所に直接アクセスができないため、chromedriverとseleniumを用いてchromeの自動操作を用いてデータにアクセスする。chromedriverはheadlessモードで動かすため、実際には実行過程は見えないようになっているが、download.pyの中の「options.add_argument('--headless')」という記述を削除すれば実際に画面操作を行っている画面を見ることができる。

## 環境
OS:Windows10

言語:python3

使用モジュール(標準モジュール以外)
* BeautifulSoup
* requests
* selenium  

その他必要なもの:chromedriver.exe

### 各プログラムの説明
* get_boj_data.py  
  下記のプログラムを呼び出すメインプログラム。
* get_dict.py  
日本銀行のデータ系列名称とデータコードを紐づける辞書を作成するプログラム。非常に多くの統計データが存在し、毎回実行されると時間かかる。そのため初実行時に「boj.dict」ファイルをpickleによって作成し、二回目以降は処理がされない仕組みとなっている。  
  例:データ系列名称=基準割引率および基準貸付利率、データコード=IR01'MADR1Z@D
* mk_display.py  
  get_dict.pyで準備した辞書を使用して、取得したい統計データ名を選択するための画面を作成する(tkinterを使用)。
* download.py  
  取得したい統計データを選択後、実際に日本銀行のwebサイトから該当データを取得する(seleniumを使用)。

### 使用方法
上記プログラムとchromedriver.exeを同じディレクトリに配置し、get_boj_data.pyを実行する。

### 実行画面
![実行画面](https://github.com/jiromaru/boj_data/blob/images/boj_images.png?raw=true)
