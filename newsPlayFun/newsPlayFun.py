from google.cloud import storage
import json
import random

#리퀘스트를 받고 해당하는 내용들을 json 형태로 반환해주어, 실제 발화로 이어지게하는 함수
#HTTP 트리거

def newsPlayFun(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    #리퀘스트 json을 받는 함수
    request_json = request.get_json()
    
    if request.args and 'message' in request.args:
        return request.args.get('message')

    # NUGU 에서 사용하는 리퀘스트 json의 action 과 actionName을 파악
    elif request_json and 'action' in request_json:

        # 각 actionName에 따른 발화
        # summarizeNews 는 기본 발화. 1~5위까지의 상위 뉴스를 알려줌
        if request_json['action']['actionName'] == 'summarizeNews':
            
            newsdata = ''
            # 한개의 파라미터로 반환하기 때문에 문자열 한개 생성
            newsdata += "1번." + downloadtext("nugunews.appspot.com","newsData0.txt")
            newsdata += "2번." + downloadtext("nugunews.appspot.com","newsData"+str(1)+".txt")
            newsdata += "3번." + downloadtext("nugunews.appspot.com","newsData"+str(2)+".txt")
            newsdata += "4번." + downloadtext("nugunews.appspot.com","newsData"+str(3)+".txt")
            newsdata += "5번." + downloadtext("nugunews.appspot.com","newsData"+str(4)+".txt")

            #json에 생성된 문자열을 넣어 반환
            response_json = makeJsonReturn(newsdata)
            return response_json
        
        # otherNews는 6위 부터의 랜덤한 뉴스를 발화
        elif request_json['action']['actionName'] == 'otherNews':
            
            #뉴스를 중복해서 발화하지 않도록 하기 위해서 숫자 셔플로 랜덤하게 발화
            rnd = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19] 
            random.shuffle(rnd)
            
            newsdata = ''
            newsdata += "1번." + downloadtext("nugunews.appspot.com","newsData"+str(rnd[0])+".txt")
            newsdata += "2번." + downloadtext("nugunews.appspot.com","newsData"+str(rnd[1])+".txt")
            newsdata += "3번." + downloadtext("nugunews.appspot.com","newsData"+str(rnd[2])+".txt")
            newsdata += "4번." + downloadtext("nugunews.appspot.com","newsData"+str(rnd[3])+".txt")
            newsdata += "5번." + downloadtext("nugunews.appspot.com","newsData"+str(rnd[4])+".txt")
            
            response_json = makeJsonReturn(newsdata)
            return response_json

        #moreNews는 6위부터 10위까지의 뉴스를 발화
        elif request_json['action']['actionName'] == 'moreNews':  
            
            newsdata = ''
            newsdata += "6번." + downloadtext("nugunews.appspot.com","newsData"+str(5)+".txt")
            newsdata += "7번." + downloadtext("nugunews.appspot.com","newsData"+str(6)+".txt")
            newsdata += "8번." + downloadtext("nugunews.appspot.com","newsData"+str(7)+".txt")
            newsdata += "9번." + downloadtext("nugunews.appspot.com","newsData"+str(8)+".txt")
            newsdata += "10번." + downloadtext("nugunews.appspot.com","newsData"+str(9)+".txt")
            
            response_json = makeJsonReturn(newsdata)
            return response_json
        
        
    else:
        # 예외 상황 그냥 처리
        return "Hi"


#텍스트에서 문자열을 가져오는 함수
def downloadtext(bucket_name, source_blob_name):
    #클라이언트 스토리지에서 버킷과 텍스트를 가져올 소스 블롭 가져옴
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    
    #blob.download as string 함수를 통해, 문자열 가져오고, utf8 로 디코딩 및 반환
    newsData = str(blob.download_as_string(),"utf-8")
    return newsData

#Json을 만들어서 response 하는 함수
#NUGU 예시를 따라서 제작
#output에 뉴스정보를 담아서 전송
def makeJsonReturn(news):
    response ={}
    response["version"]="2.0"
    response["resultCode"]="OK"
    response["output"]={'news' : news, 'news2' : news, 'news3':news}
    response["directives"] = [{"type": "AudioPlayer.Play",
            "audioItem": {     
                "stream": {
                    "url": "",
                    "offsetInMilliseconds": "",
                    "progressReport": {
                        "progressReportDelayInMilliseconds": "",
                        "progressReportIntervalInMilliseconds": ""
                    },
                    "token": "",
                    "expectedPreviousToken": ""
                },
                "metadata": { }
            }
          }]
    #파이썬 딕셔너리를 json으로 만들어서 보냄. 문자열이 깨지지 않도록 ascii 를 False 로 바꿈
    Rjson = json.dumps(response, ensure_ascii=False)
    return Rjson
