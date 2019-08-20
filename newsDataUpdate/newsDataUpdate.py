import base64
import requests
import json
from bs4 import BeautifulSoup
from google.cloud import storage


#뉴스 내용 요약본 자동 업데이트 함수
#구글 클라우드 스케줄러로 30분 마다 트리거

def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    pubsub_message = base64.b64decode(event['data']).decode('utf-8')

    #리스트 형태로 뉴스 내용 불러오기
    summaryData = summary()

     #리스트의 내용을 각 뉴스 데이터 파일에 업로드. 리스트의 길이 만큼 파일에 저장
    for i in range(0,len(summaryData)):
        # UTF-8 로 엔코딩 해야 제대로 업로드 됨.
        sd = str(summaryData[i]).encode("UTF-8")
        upload_blob("nugunews.appspot.com",sd,"newsData"+str(i)+".txt")

    #로그용 출력    
    print(pubsub_message)

# blob 업데이트. 데이터를 실제로 버킷에 있는 파일에 저장하는 함수
def upload_blob(bucket_name, string, destination_blob_name):
    """Uploads a file to the bucket."""
    #클라이언트 스토리지에서 버킷과 텍스트를 저장할 목표 블롭 가져옴
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # 문자열 값을 받아서 저장. content 타입을 설정할 때 UTF-8로 지정해야 문자가 깨지지 않음.
    blob.upload_from_string(string, content_type='text/plain; charset=UTF-8')

    #로그용 출력
    print('File {} uploaded to {}.'.format(
        string,
        destination_blob_name))
    
    #요약된 뉴스들을 크롤링 하여 리스트 형태로 반환하는 함수
def summary():
    req = requests.get('https://media.daum.net/ranking/popular/')

    if req.ok:
        html = req.text
        soup = BeautifulSoup(html,'html.parser')

    ranknews = soup.find('ul',{'class':'list_news2'}).find_all('a',{'class':'link_txt'})

    #다음 실시간 랭킹 뉴스 링크만 크롤링
    i = 0
    #리스트 형태로 저장
    summarys = []
    for link in ranknews:
        req = requests.get(link.attrs['href'])
        html = req.text
        soup = BeautifulSoup(html,'html.parser')
        # 약 20개까지만 크롤링, 추후 추가 가능
        if(i>19):
            break
        if soup.find("div",{"class":"layer_util layer_summary"}): 
            summary = soup.find("div",{"class":"layer_util layer_summary"}).find_all('p')
            text=''

            #p태그 안에 있는 text만 추출
            for s in summary:
                text += s.text + " "

            summarys.append(str(text))
            i+=1
            
    return summarys

