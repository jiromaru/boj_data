##############################データのダウンロード##############################

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import urllib.request

#クロームドライバのoption
options = Options()
options.add_argument('--headless') 
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')


def download(id_list,url,start_y,end_y,dl_path):

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
        urllib.request.urlretrieve(dl_path + file_nm,file_nm.replace("/",""))
        new_window = driver.window_handles[-2]
        driver.switch_to_window(new_window)

    driver.quit()

    print("完了")
