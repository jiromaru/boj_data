##############################import#####################################
import os
import pickle
import sys

from get_dict import get_dict
from download import download
from mk_display import mk_display

##############################変数の定義########################################

#取得するデータの開始年と終了年
start_y="1980"
end_y="2018"

#使用するURL
boj_url1="https://www.stat-search.boj.or.jp/info/nme_Mdframe.html"
boj_url2="https://www.stat-search.boj.or.jp/ssi/cgi-bin/famecgi2?cgi=$nme_s050"
dl_path="https://www.stat-search.boj.or.jp/ssi/html"

##############################プログラムの実行##################################

if __name__ == '__main__':

    if os.path.exists("boj.dict") == False:
        with open("boj.dict","wb") as f1:
            pickle.dump(get_dict(boj_url1),f1)

    with open("boj.dict","rb") as f2:
        dict=pickle.load(f2)
    
    param_list=mk_display(dict)

    if len(param_list)==0:
        print("データ系列が選択されていません")
        sys.exit()
        
    download(param_list,boj_url2,start_y,end_y,dl_path)
