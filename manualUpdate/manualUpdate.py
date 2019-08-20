import base64
import requests
import json
from google.cloud import storage

#번안된 뉴스 내용 수동 업데이트 함수
#구글 클라우드 스케줄러로 트리거

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
    
#텍스트에서 문자열을 가져오는 함수
def downloadtext(bucket_name, source_blob_name):
    #클라이언트 스토리지에서 버킷과 텍스트를 가져올 소스 블롭 가져옴
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    
    #blob.download as string 함수를 통해, 문자열 가져오고, utf8 로 디코딩 및 반환
    newsData = str(blob.download_as_string(),"utf-8")
    return newsData

#번안된 뉴스들이 저장된 easyNews 파일에서 뉴스 정보를 가져와서, 라인을 나눠서 리스트로 반환
#자동 업데이트에 있는 함수를 이름을 바꾸지 않고 활용했음.
def summary():
    easynews = downloadtext("nugunews.appspot.com","easyNews1.txt")
    summarys = easynews.splitlines()
    return summarys

