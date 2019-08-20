####### 이전 코드 백업용 #######
import requests
import json
from bs4 import BeautifulSoup

def summary():
    req = requests.get('https://media.daum.net/ranking/popular/')

    if req.ok:
        html = req.text
        soup = BeautifulSoup(html,'html.parser')

    ranknews = soup.find('ul',{'class':'list_news2'}).find_all('a',{'class':'link_txt'})
    ranknews_url = []

    #다음 실시간 랭킹 뉴스 링크만 크롤링
    for link in ranknews:
        ranknews_url.append(link.attrs['href'])

    i = 0
    #뉴스 요약
    summarys = []

    #실시간 랭킹 뉴스 모두 요약하기
    for link in ranknews_url:
        req = requests.get(link)
        html = req.text
        soup = BeautifulSoup(html,'html.parser')

        if soup.find("div",{"class":"layer_util layer_summary"}): 
            summary = soup.find("div",{"class":"layer_util layer_summary"}).find_all('p')
            text=''

            #p태그 안에 있는 text만 추출
            for s in summary:
                text += s.text

            summarys.append(text)
            i+=1
    M = dict(zip(range(1, len(summary) + 1), summary))
    json.dumps(M)
    return M