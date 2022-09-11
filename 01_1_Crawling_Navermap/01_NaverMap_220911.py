# 2022.09.11
# 네이버 지도에서 특정 장소의 이름을 검색하면 URL에서 고유ID를 가져올 수 있음.
# 이 고유ID를 네이버 플레이스의 URL에 기재하여 리뷰 크롤링이 손쉽게 가능함.
# '블로그 리뷰'가 100개 미만인 장소의 '방문자 리뷰'만을 가져오기 위한 기초 코드로, 응용하여 사용

# 1. 필요 모듈 가져오기
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# 2. 옵션- 원하는 옵션으로 변경 가능
chrome_options = Options()
chrome_options.add_experimental_option("detach",True) #웹브라우저가 켜지고 나서 계속 남아있게 함.
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service(executable_path=ChromeDriverManager().install()) #크롬드라이버 매니저를 통해서 자동으로 크롬드라이버 최신버전 가져온 다음, 서비스 객체를 만들어서 서비스 변수에 저장한다.
driver = webdriver.Chrome(service = service, options=chrome_options) #크롬 옵션이 담긴 chrome_options 추가


# 3. 웹페이지 이동
ID = '1086250019' #파스쿠찌 밀양점
driver.implicitly_wait(5) #웹페이지가 로딩될때까지 5초 대기
driver.get(f"https://pcmap.place.naver.com/restaurant/"+ ID +"/review/visitor")

res = driver.page_source
soup = BeautifulSoup(res, 'html.parser')


# 4. XPATH로 블로그 리뷰 카운트 가져온 후, 크롤링 대상인지 판별(블로그리뷰가 100개 미만일 때 크롤링)
review_counts = driver.find_elements(By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div[1]/div[2]/span[3]/a/em')
for review_count in review_counts:
    print('블로그 리뷰 수 : ', review_count.text)

if len(review_count.text) > 2 :
    print('크롤링하지 않음')
else:
    print('크롤링 대상임')
    reviews = driver.find_elements(By.CLASS_NAME, 'zPfVt')
    visiter_review=[]
    for review in reviews:
        visiter_review.append(review.text)
    print(visiter_review)

# 5. 아래쪽에 '더보기' 버튼이 존재하므로 이를 클릭하는 코드를 더해 원하는 갯수만큼의 리뷰를 가져올 수 있음.
# 6. 고유 ID를 리스트로 만들어 여러 장소를 크롤링하는 코드로 활용 가능.