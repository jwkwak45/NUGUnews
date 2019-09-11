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
    print(request_json)
    
    if request.args and 'message' in request.args:
        return request.args.get('message')

    # NUGU 에서 사용하는 리퀘스트 json의 action 과 actionName을 파악
    elif request_json and 'action' in request_json:
        
        # 딕셔너리로 추가
        newsdata = {}
        
        # 각 actionName에 따른 발화
        if request_json['action']['actionName'] == 'summarizeNews':
            
            response_json = makeJsonReturn(newsdata)
            return response_json
        
        elif request_json['action']['actionName'] == 's_n_default':
            
            for h in range(1,6):                
            	newsdata["news"+str(h)] = str(h)+"번." + downloadtext("nugunews.appspot.com","newsData"+str(h)+".txt")
            
            response_json = makeJsonReturn(newsdata)
            return response_json
                                                                     
            
        elif request_json['action']['actionName'] == 's_n_next1':
            
            for h in range(1,6):                
            	newsdata["news"+str(h)] = str(h+5)+"번." + downloadtext("nugunews.appspot.com","newsData"+str(h+5)+".txt")
                      
            response_json = makeJsonReturn(newsdata)
            return response_json

        elif request_json['action']['actionName'] == 's_n_next2':
            
            for h in range(1,6):                
            	newsdata["news"+str(h)] = str(h+10)+"번." + downloadtext("nugunews.appspot.com","newsData"+str(h+10)+".txt")
                      
            response_json = makeJsonReturn(newsdata)
            return response_json
        
        elif request_json['action']['actionName'] == 's_n_next3':
            
            for h in range(1,6):                
            	newsdata["news"+str(h)] = str(h+15)+"번." + downloadtext("nugunews.appspot.com","newsData"+str(h+15)+".txt")
                      
            response_json = makeJsonReturn(newsdata)
            return response_json
        
        
        elif request_json['action']['actionName'] == 's_n_num':
            
            newsdata["flag"] = "False"
            indexN = request_json['action']['parameters']['index']['value']
            i = int(indexN)
            
            if i < 21:
                newsdata["flag"] = "True"
            
            response_json = makeJsonReturn(newsdata)
            return response_json
        
        elif request_json['action']['actionName'] == 's_n_numSingle':
            
            newsdata["flag"] = "True"
            indexN = request_json['action']['parameters']['index']['value']
                                                                                                
            newsdata["selectNews"] = indexN+"번." + downloadtext("nugunews.appspot.com","newsData"+indexN+".txt")
            
            response_json = makeJsonReturn(newsdata)
            return response_json
        
        elif request_json['action']['actionName'] == 's_n_numFrom':
            
            newsdata["flag"] = "True"
            indexN = request_json['action']['parameters']['index']['value']
            i = int(indexN)
            
            #if i < 21:
            #    newsdata["flag"] = "True"
                
            for h in range(0,5):
                if i+h < 21:
                    newsdata["news"+str(h+1)] = str(i+h)+"번." + downloadtext("nugunews.appspot.com","newsData"+str(i+h)+".txt")
                      
            response_json = makeJsonReturn(newsdata)
            return response_json

    else:
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
#딕셔너리 형태로 정보 받아서 처리
def makeJsonReturn(newsData):
    response ={}
    response["version"]="2.0"
    response["resultCode"]="OK"
    response["output"]= newsData
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


    


