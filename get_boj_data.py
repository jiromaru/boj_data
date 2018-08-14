##############################importの設定######################################
import urllib.request
import time
import requests
import os
import sys
import shutil
import pickle
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
##############################変数の定義########################################

#開始年と終了年
start_y="1980"
end_y="2018"

#使用するpath
boj_url1="https://www.stat-search.boj.or.jp/info/nme_Mdframe.html"
boj_url2="https://www.stat-search.boj.or.jp/ssi/cgi-bin/famecgi2?cgi=$nme_s050"
dl_path="https://www.stat-search.boj.or.jp/ssi/html"

#リストの初期値
select_list=[]
param_list=[]

#クロームドライバのoption
options = Options()
options.add_argument('--headless') 
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

##############################日銀データIDの辞書を作成##########################

def get_dict(url):    
    html=requests.get(url)
    html.encoding = html.apparent_encoding
    text=html.text
    soup = BeautifulSoup(text, "html.parser")
    trs=soup.find_all("tr")
    output_dict={}
    for i in trs:
        output_list=[]
        tds=i.find_all("td")
        for j in tds:
            output_list.append(j.text)
        if output_list!=[]:
            output_dict["_".join(output_list[0:-1])]=output_list[-1]
    return output_dict
    
##############################データのダウンロード##############################

def get_boj(id_list,url):

    #クロームドライバの立ち上げ 
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
     
    try:
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.NAME,"txtDirect")))
    except:
        print("データコードの入力箇所がありません")
    finally:
        for id in id_list:
            key=id + "\n"
            driver.find_element_by_name("txtDirect").send_keys(key)

    try:
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.NAME,"btmSubmit")))
    except:
        print("検索ボタンがありません")
    finally:
        driver.find_element_by_name("btmSubmit").click()

    try:
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"//tr[contains(@ onclick,'searchDataCodeChecked(this, event);')]")))
    except:
        print("該当データ系列がありません")
    finally:
        chk_list=driver.find_elements_by_xpath("//tr[contains(@ onclick,'searchDataCodeChecked(this, event);')]")
        for chk in chk_list:
            chk.click()
        
    try:
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID,"columnNameSearch")))
    except:
        print("抽出条件に追加ボタンがありません")
    finally:
        driver.find_element_by_id("columnNameSearch").click()

    try:
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID,"fromYear")))
    except:
        print("対象期間入力箇所がありません")
    finally:
        driver.find_element_by_id("fromYear").send_keys(start_y)
        driver.find_element_by_id("toYear").send_keys(end_y)
        driver.find_element_by_xpath("//a[contains(@ onclick,'submit_code_main(document.nme_S050_form')]").click()

    new_window = driver.window_handles[-1]
    driver.switch_to_window(new_window)

    #ダウンロードしたいファイル分入ったリストになる
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"//a[contains(@ onclick,'document.DLform')]")))
    dw_list=driver.find_elements_by_xpath("//a[contains(@ onclick,'document.DLform')]")
    for dw_fl in dw_list:
        dw_fl.click()
        new_window = driver.window_handles[-1]
        driver.switch_to_window(new_window)
        file_nm=driver.find_element_by_xpath("//a[contains(@ href,'csv')]").text
        urllib.request.urlretrieve(dl_path + file_nm,file_nm )
        new_window = driver.window_handles[-2]
        driver.switch_to_window(new_window)

    driver.quit()

    print("完了")

##############################データ選択画面の作成##############################
def mk_display(dict):

    def show_selection():
        for i in lb.curselection():
            select_list.append(lb.get(i))
        print("選択項目 : ")
        print(select_list)
        root.destroy()

    root = Tk()
    root.title('Scrollbar')

    # Frame
    frame1 = ttk.Frame(root, padding=10)
    frame1.grid()

    # Listbox
    lb = Listbox(frame1,selectmode=EXTENDED,height=20,width=170)
    lb.grid(row=0, column=0)
    for key in dict.keys():
        lb.insert(END, key)

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame1,orient=VERTICAL,command=lb.yview)
    lb['yscrollcommand'] = scrollbar.set
    scrollbar.grid(row=0,column=1,sticky=(N,S))

    #Button
    button1 = ttk.Button(frame1, text='OK', command=show_selection)
    button1.grid(row=1, column=0, columnspan=2)

    root.mainloop()

    for selected in select_list:
        param_list.append(dict[selected])

    return param_list

##############################プログラムの実行##################################

if __name__ == '__main__':

    if os.path.exists("boj.dict") == False:
        with open("boj.dict","wb") as f:
            pickle.dump(get_dict(boj_url1),f)

    with open("boj.dict","rb") as f:
        dict=pickle.load(f)

    get_boj(mk_display(dict),boj_url2)
