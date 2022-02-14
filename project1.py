import pandas as pd #리스트(배열)의 있는 값을  깔끔하게 카테고리에 맞게 출력하게 하는 모듈을 가져옵니다. 
import requests #weather 서버에 요청할때 필요한 모듈을 가져옵니다.
import RPi.GPIO as GPIO #GPIO  모듈을 가져옵니다.
from time import sleep #sleep(delay) 딜레이 함수를 가져옵니다.

GPIO.setmode(GPIO.BCM) #GPIO 핀 번호로 설정

def reset() : #세그먼트 초기화 함수 정의(불이 꺼진 상태)
    #세그먼트1 초기화
    for segment in segments1 :
        GPIO.setup(segment, GPIO.OUT)
        GPIO.output(segment, 1)
    #세그먼트2 초기화
    for segment in segments2 :
        GPIO.setup(segment, GPIO.OUT)
        GPIO.output(segment, 1)
    
def converte_kelvin_to_celsius(k): #절대온도를 섭씨온도로 바꾸고 반환하는 함수 
    return (k-273.15)

def Temperature1(temp) : #섭씨 온도를 영상 / 영하 문자열로 바꾸고 반환하는 함수
    if temp >= 0 :
        return "영상 " + str(temp) + "도"
    else :
        return "영하 " + str(temp + temp * -2) + "도"
    
def Temperature2(temp) : #섭씨 온도가 0 이상, 10 미만일 경우 문자열로 바꾸고 0을 더하고 반환하는 함수
    if temp >= 0 and temp < 10 :
        return '0' + str(temp)
    else :
        return str(temp)
        
    
#첫번째 세그먼트 연결된 핀번호 : a 부터 g 까지 튜플 자료형 선언
segments1 = (17, 27, 22, 10, 9, 11, 13)

#두번째 세그먼트 연결된 핀번호 : a 부터 g 까지 튜플 자료형 선언
segments2 = (12, 16, 18, 23, 24, 25, 20)

#딕셔너리 자료형 key(문자), index(세그먼트 출력) 선언
num = { '-' : (1,1,1,1,1,1,0), '0' : (0,0,0,0,0,0,1), '1' : (1,0,0,1,1,1,1), '2' : (0,0,1,0,0,1,0), '3' : (0,0,0,0,1,1,0),
       '4' : (1,0,0,1,1,0,0), '5' : (0,1,0,0,1,0,0), '6' : (0,1,0,0,0,0,0), '7' : (0,0,0,1,1,0,1), '8' : (0,0,0,0,0,0,0), '9' : (0,0,0,0,1,0,0) }

prov_list = [ #API 서버에 요청하는 id를 가진 리스트(배열) 선언
    {'name':'서울','city_id':'1835847'},
    {'name':'부산','city_id':'1838524'},
    {'name':'대구','city_id':'1835329'},
    {'name':'인천','city_id':'1843564'},
    {'name':'광주','city_id':'1841811'},
    {'name':'대전','city_id':'1835235'},
    {'name':'울산','city_id':'1833747'},
    {'name':'세종','city_id':'1835235'},
    {'name':'경기','city_id':'1841610'},
    {'name':'강원','city_id':'1843125'},
    {'name':'충북','city_id':'1845106'},
    {'name':'충남','city_id':'1845105'},
    {'name':'전북','city_id':'1845789'},
    {'name':'전남','city_id':'1845788'},
    {'name':'경북','city_id':'1841597'},
    {'name':'경남','city_id':'1902028'},
    {'name':'제주','city_id':'1846266'},
]

weather_info_list = [] # weather 정보를 가지는 리스트(배열) 선언, 초기화
url = 'http://api.openweathermap.org/data/2.5/weather' #weather 서버 API url에 대입

try: #KeyboardInterrup exception 잡기위한 try문
    while True : #계속 실행하는 반복문
        weather_info_list.clear() 
        #리스트(배열) 초기화
        reset() 
        #세그먼트 초기화 함수 호출
        print("지역 이름을 입력하십시오.")
        inputname = input() #도시이름 입력
        for i in range(len(prov_list)): 
            #prov_list의 크기만큼 증가하는 for문
            city_id = prov_list[i]['city_id'] 
            #prov_list 리스트의 i번째 'city_id'(key) 안에 있는 값을 city_id에 대입
            city_name = prov_list[i]['name'] 
            #prov_list 리스트의 i번째 'name'(key) 안에 있는 값을 city_name에 대입
            params = dict( #도시id와 자신의 key를 딕셔너리 자료형(사전)으로 변환후 params에 대입합니다. 
                id=city_id, 
                #도시id의 정보를 id에 대입
                APPID='1cbebe0837da91d9ce1a6a16c747d8da', 
                #자신의 Key의 값을 APPID에 대입 
            )
            resp = requests.get(url=url, params=params) 
            #url과 params를 인자로 갖고 (request)요청하여 서버에 .json파일을 (get)가져옵니다. 
            data = resp.json() 
            #json()함수를 이용하여 .json파일을 읽고 구문 분석한 값의 리스트를 data에 대입합니다.
            data_main = data['main'] 
            #data 리스트의 key값이 main인 데이터를 data_main에 대입
            if inputname == prov_list[i]['name'] : 
                #입력한 도시이름이 맞는지 판별하는 if문
                info = [ #info 배열 선언 및 데이터 대입 
                    city_id,
                    city_name, 
                    converte_kelvin_to_celsius(data_main['temp_min']), \
                    #data_main 리스트의 key값이 temp_min인 데이터를 섭씨온도로 변환 
                    converte_kelvin_to_celsius(data_main['temp']), \
                    #data_main 리스트의 key값이 temp인 데이터를 섭씨온도로 변환 
                    converte_kelvin_to_celsius(data_main['temp_max']), \
                    #data_main 리스트의 key값이 max_min인 데이터를 섭씨온도로 변환 
                    data_main['pressure'], \
                    #data_main 리스트의 key값이 pressure인 데이터
                    data_main['humidity']]
                    #data_main 리스트의 key값이 humidity인 데이터
                weather_info_list.append(info) 
                #weather_info 리스트(배열)에 info를 추가(append)
            
                #입력한 도시 날씨 데이터를 따로 변수에 저장
                outputcity = city_name 
                #도시이름을 따로 outputcity 변수에 대입
                outputtempmin = round(converte_kelvin_to_celsius(data_main['temp_min'])) 
                #최저 온도 : 절대 온도 값을 섭씨 온도로 변환 후 반올림하여 outputtempmin 변수에 대입
                outputtemp = round(converte_kelvin_to_celsius(data_main['temp'])) 
                #현재 온도 : 절대 온도 값을 섭씨 온도로 변환 후 반올림하여 outputtemp 변수에 대입
                outputtempmax = round(converte_kelvin_to_celsius(data_main['temp_max'])) 
                #최고 온도 : 절대 온도 값을 섭씨 온도로 변환 후 반올림하여 outputtempmax 변수에 대입
                
                continue #밑에는 실행되지 않고 다음 반복문으로 넘어가는 continue
    
            info = [ #다른 도시 날씨 데이터를 info에 저장
                city_id, \
                city_name, \
                converte_kelvin_to_celsius(data_main['temp_min']), \
                #data_main 리스트의 key값이 temp_min인 데이터를 섭씨온도로 변환 
                converte_kelvin_to_celsius(data_main['temp']), \
                #data_main 리스트의 key값이 temp인 데이터를 섭씨온도로 변환 
                converte_kelvin_to_celsius(data_main['temp_max']), \
                #data_main 리스트의 key값이 max_min인 데이터를 섭씨온도로 변환 
                data_main['pressure'], \
                #data_main 리스트의 key값이 pressure인 데이터
                data_main['humidity']]
                #data_main 리스트의 key값이 humidity인 데이터
            weather_info_list.append(info) #weather_info 리스트(배열)에 info를 추가(append)

        #출력문
        #panda 모듈 이용하여 weather_info_list의 정렬배치 후 데이터 출력
        df = pd.DataFrame(weather_info_list, columns=['city_id', 'city_name', \
                                                     'temp_min', 'temp', 'temp_max',\
                                                     'pressure', 'humidity'])
        print(df)
        
        print(" ") #띄어쓰기
        print("현재 입력한 " + outputcity + "지역의 최저온도는 " + Temperature1(outputtempmin) + ", 현재온도는 " + Temperature1(outputtemp) + ", 최고 온도는 " + Temperature1(outputtempmax) + "입니다.\n")
        print(" ")
            
        length = len(segments1) # 한 세그먼트 당 핀 갯수 길이를 length 변수에 저장
        array = [Temperature2(outputtempmin), Temperature2(outputtemp), Temperature2(outputtempmax)] #최저, 현재, 최고온도를 Temperature2함수를 이용하여 문자열로 반환 후 배열로 선언
        while True :
            for i in range(len(array)) : 
                #최저온도, 현재온도, 최고온도를 순서대로 반복하는 반복문
                for j in range(length) : 
                    #세그먼트의 a부터 g까지 반복하는 반복문
                    GPIO.output(segments1[j], num[array[i][0]][j]) 
                    #2개의 문자를 가진 문자열을 반복하여 첫번째 세그먼트에 하나씩 출력 (0번지) 
                    GPIO.output(segments2[j], num[array[i][1]][j]) 
                    #2개의 문자를 가진 문자열을 반복하여 세그먼트에 하나씩 출력 (1번지) 
                    sleep(0.7) 
                    #딜레이 0.7초간 프로세스 중지
    
            print("계속 출력하시겠습니까? (y/n)") #y를 입력받으면 계속 출력 할 수 있습니다.
            hello1 = input()
            if hello1 != 'y':
                break
            
        print("다른 지역을 검색하시겠습니까? (y/n)") #y를 입력받으면 계속 검색 할 수 있습니다.
        hello2 = input()
        if hello2 != 'y':
            GPIO.cleanup()
            break
        
except KeyboardInterrupt: #Ctrl + C를 입력하면 프로그램 중단(exception 방지)
    print("GoodBye")
    GPIO.cleanup() #GPIO 해제

#영하 두자릿수는 출력 불가  
#웹 API 연결 참고 https://m.blog.naver.com/wideeyed/221335980042