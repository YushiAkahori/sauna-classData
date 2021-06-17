# 必要なライブラリのインポート
import requests
from bs4 import BeautifulSoup
import os
# はじめに、ベースとなる1ページ目のURLを定義します
base_url = "http://scraping.aidemy.net"

url_lists = ["https://sauna-ikitai.com/saunas/2303/posts",#各務原温泉 恵みの湯
            "https://sauna-ikitai.com/saunas/1551/posts",#馬橋湯 馬橋バスセンター
            "https://sauna-ikitai.com/saunas/1708/posts",#カプセルホテルレインボー本八幡店
            "https://sauna-ikitai.com/saunas/1523/posts",#湯乃泉 草加健康センター
            "https://sauna-ikitai.com/saunas/4044/posts"]#サウナと天然温泉 湯らっくす

for url_list in url_lists:
  response =  requests.get(url_list)
  soup = BeautifulSoup(response.text, "lxml")
  path = url_list.split("/")[-2]
  last_page  = soup.find_all("li",class_="c-pagenation_link")[-2]
  last_page = int(last_page.a.get("href").split("=")[-1])
  if not os.path.isdir(path):
        os.makedirs(path)
  for i in range(1,min(last_page,8)):#1~7ページまで
    search_url = "https://sauna-ikitai.com/saunas/{}/posts?page={}".format(path,i)

    response_page =  requests.get(search_url)
    soup_page = BeautifulSoup(response_page.text, "lxml")

    index=0
    boxes = soup_page.find_all("p",class_="p-postCard_text")
    for box in boxes:
      s = box.get_text(strip=True)
      index+=1
      if len(s)>0 and s!="チェックイン":
        with open("{}/{}_{}.txt".format(path,i,index), mode='w') as f:
          f.write(s)
      

  