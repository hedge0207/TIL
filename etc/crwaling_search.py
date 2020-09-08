from bs4 import BeautifulSoup
from selenium import webdriver
import time

query_txt = input('크롤링할 키워드: ')

#1단계. 크롬 드라이버를 사용하여 웹 브라우저를 실행
#path에는 chromedriver.exe가 위치한 경로를 입력
path = "C:\Temp\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(path)

#크롤링 하려는 사이트의 주소를 입력
driver.get("https://korean.visitkorea.or.kr/main/main.do")

#위 사이트가 열리기 전에 2초의 간격을 둔다.
time.sleep(2)



#2단계. 검색창의 이름을 찾아서 검색어를 입력한다.
driver.find_element_by_id('btnSearch').click()

element = driver.find_element_by_id('inp_search')

element.send_keys(query_txt)



#3단계. 검색 버듵을 눌러서 실행
driver.find_element_by_class("btn_search2").click()
