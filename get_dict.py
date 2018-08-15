##############################日銀データIDの辞書を作成##########################

import requests
from bs4 import BeautifulSoup

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