from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys

#1단계. 검색 결과를 저장할 경로와 검색어를 입력 받는다.
# query_txt = input("크롤링할 키워드: ")
# f_name = input("검색 결과를 저장할 파일경로와 이름을 지정하세요: ")
query_txt = "여수"
f_name = "C:\\Users\multicampus\Desktop\참고\TIL\etc\\test.txt"



#단계2. 크롬 드라이버를 사용하여 웹 브라우저를 실행
path = "C:\Temp\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("https://korean.visitkorea.or.kr/main/main.do")
time.sleep(2)



#단계3. 검색창의 이름을 찾아서 검색어를 입력하고 검색을 실행
driver.find_element_by_id("btnSearch").click()
element = driver.find_element_by_id("inp_search")
element.send_keys(query_txt)

driver.find_element_by_link_text("검색").click()



#단계4. 현재 페이지에 있는 내용을 화면에 출력하기
time.sleep(1)

#현재 페이지의 전체 HTML 코드를 full_html 변수에 저장
full_html = driver.page_source

soup = BeautifulSoup(full_html,'html.parser')

content_list = soup.find('ul', class_='list_thumType flnon')

for i in content_list:
    print(i.text.strip())
    print("\n")



#단계5. 현재 페이지에 있는 내용을 txt 형식으로 파일에 저장하기
orig_stdout = sys.stdout
f = open(f_name, 'a', encoding='UTF-8')

#출력을 터미널 창이 아닌 파일로 하도록 설정
sys.stdout=f
time.sleep(1)

html = driver.page_source

soup = BeautifulSoup(html,'html.parser')

content_list = soup.find('ul', class_='list_thumType flnon')

# 위에서 표준 출력 내용을 터미널 창이 아닌 f_name에 하도록 지정했기 때문에 아래 내용은 터미널 창이 아닌 txt 파일에 저장되게 된다. 
for i in content_list:
    print(i.text.strip())
    print("\n")

#다시 터미널 창에 출력 되도록 설정
sys.stdout = orig_stdout
f.close()

print("요청하신 데이터 수집 작업이 정상적으로 완료되었습니다.")



