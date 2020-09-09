from bs4 import BeautifulSoup
from selenium import webdriver
import time

# query_txt = input('크롤링할 키워드: ')

# #1단계. 크롬 드라이버를 사용하여 웹 브라우저를 실행
# #path에는 chromedriver.exe가 위치한 경로를 입력
# path = "C:\Temp\chromedriver_win32\chromedriver.exe"
# #만일 따로 경로를 지정하지 않을 경우 현재 파일이 있는 폴더에서 chromedriver.exe 파일을 찾는다.
# driver = webdriver.Chrome(path)

# # get: 웹 페이지를 여는 함수
# # 인자로 크롤링 하려는 사이트의 주소를 입력
# driver.get("https://korean.visitkorea.or.kr/main/main.do")

# #위 사이트가 열린 후에 2초의 간격을 둔다.
# time.sleep(2)


# #2단계. 검색창의 이름을 찾아서 검색어를 입력한다.
# driver.find_element_by_id('btnSearch').click()

# element = driver.find_element_by_id('inp_search')

# element.send_keys(query_txt)



# #3단계. 검색 버튼을 눌러서 실행
# driver.find_element_by_class_name("btn_search2").click()




#실습
query_txt=input('크롤링할 키워드: ')

path = "C:\Temp\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(path)

driver.get("https://www.naver.com/")
time.sleep(2)

element = driver.find_element_by_id("query")
element.send_keys(query_txt)

driver.find_element_by_id("search_btn").click()


