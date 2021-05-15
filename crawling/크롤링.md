# 목차

- [크롤링의 위법성](#크롤링의 위법성)
- [Beautiful Soup](#Beautiful Soup)
- [기초](#기초)
  - [HTML 코드 안에서 원하는 태그의 내용을 가져오기](#HTML-코드-안에서-원하는-태그의-내용을-가져오기)
  - [태그 내의 데이터 추출하기](#태그-내의-데이터-추출하기)
- [웹 크롤러 만들기](#웹 크롤러 만들기)
  - [사전 준비](#사전-준비)
  - [검색창에 검색어 입력 후 자동 검색 기능 구현](#검색창에-검색어-입력-후-자동-검색-기능-구현)
  - [검색된 결과에서 텍스트를 추출하여 저장하기](#검색된-결과에서-텍스트를-추출하여-저장하기)



# 크롤링의 위법성

- 1994년에 만들어진 로봇 배제 규약에 따라 웹 페이지마다 해당 페이지에서 수집해도 되는 데이터와 해선 안되는 데이터를 작성해 놓은 `robots.txt` 파일을 작성, 원칙적으로는 해당 파일에서 허가한 데이터만 수집해야 하지만 이는 강제 사항이 아닌 권고안이라서 얼마든지 허가 되지 않은 데이터에 접근하는 것이 가능하다.



- 그러나 무단으로 웹 페이지의 데이터를 크롤링하여 사용할 경우 법적 분쟁이 발생할 수 있으므로 주의가 필요하다.



- `robots.txt`

  - User-agent:* # 모든 로봇(클롤러, 스크래퍼)들에 적용
  - Disallow: / # 모든 페이지들의 색인(indexing)을 금함

  

  - Uuser-agent: 접근을 허용하지 않을 로봇 이름을 설정
  - Disallow: 허용하지 않을 항목에 대해 설정, 빈 값으로 설정할 경우, 모든 하위 경로에 대한 접근이 가능, robots.txt 파일에는 최소한 한 개의 "disallow" 필드가 존재해야 한다.
    - Disallow: /abc # /abc.html과 /abc/index.html 둘 다 허용 안됨
    - Disallow: /help # /help/index.html은 하용 안하나 /help.html은 허용 됨







# Beautiful Soup

> https://www.crummy.com/software/BeautifulSoup/bs4/doc.ko/

- 웹 크롤러를 보다 간단하게 만들 수 있도록 도와주는 파이썬의 라이브러리

- 설치

  ```bash
  $ pip install bs4
  ```







# 기초

## HTML 코드 안에서 원하는 태그의 내용을 가져오기

- 아래 메소드들은 모두 파싱된 HTML 코드에만 사용 가능하다.



- `.find()`
  - 태그를 인자로 받아 해당 태그를 가져온다.
  - 같은 태그가 여러 개 있을 경우 가장 상단의 태그 하나만 가져온다.
  - 태그의 속성을 통해 특정 태그를 가져올 수 있다.
  - 두 번째 인자로 클래스를 입력하여 해당 태그 중 인자로 넘긴 클래스를 가진 태그를 가져올 수 있다.
    - `.find('div',class_="클래스명")`
  
- `.find_all()`
  - 태그를 인자로 받아 일치하는 모든 태그를 가져온다.
  - 여러 태그를 동시가 가져오는 것이 가능하다.
  
  ```python
  from bs4 import BeautifulSoup
  
  ex1 = '''
  <html>
      <head>
          <title>bs4 연습</title>
      </head>
      <body>
          <p align='center'>내용1</p>
          <p align='left'>내용2</p>
      </body>
  </html>
  '''
  
  # HTML 코드를 파싱(분석)하고 파싱한 내용을 soup라는 변수에 저장
  soup = BeautifulSoup(ex1, 'html.parser')
  
  #.find()
  print(soup.find('div'))
  print(soup.find('title'))
  print(soup.find('p'))
  print(soup.find('p',align='left'))
  
  #out
  None						  # 일치하는 태그가 없을 경우 None을 반환한다.
  <title>bs4 연습</title>
  <p align='center'>내용1</p>    #가장 상단의 태그 하나만 가져온다.
  <p align="left">내용2</p>
  
  
  
  #.find_all()
  print(soup.find_all('p'))
  print(soup.find_all(['title','p']))
  
  #out
  [<p align="center">내용1</p>, <p align="left">내용2</p>]
  [<title>bs4 연습</title>, <p align="center">내용1</p>, <p align="left">내용2</p>]
  ```
  
  



- `.select()`

  ```python
  ex2 = '''
  <html>
      <head>
          <title>bs4 연습</title>
      </head>
      <body>
          <div>
              <span id='fruits1' class='name1' title='바나나'>바나나
                  <p class='store'>바나나 가게</p>
                  <p class='price'>3000</p>
                  <p class='count'>10</p>
                  <a href="https://www.banana.com">바나나 사이트</a>
              </span>
          </div>
          <div>
              <span id='fruits2' class='name2' title='사과'>사과
                  <p class='store'>사과 가게</p>
                  <p class='price'>4000</p>
                  <p class='count'>5</p>
                  <a href="https://www.apple.com">사과 사이트</a>
              </span>
          </div>
          <div>
              <span id='fruits3' class='name3' title='수박'>수박
                  <p class='store'>수박 가게</p>
                  <p class='price'>18000</p>
                  <p class='count'>1</p>
                  <a href="https://www.watermelon.com">수박 사이트</a>
              </span>
          </div>
          <div class="name1">동일 클래스</div>
      </body>
  </html>
  '''
  
  soup = BeautifulSoup(ex2, 'html.parser')
  ```

  

  - `.select('태그명')`: 태그명이 일치하는 모든 태그의 모든 내용을 추출

  ```python
  print(soup.select('div'))
  
  #out
  [<div>
  <span class="name1" id="fruits1" title="바나나">바나나
                  <p class="store">바나나 가게</p>
  <p class="price">3000</p>
  <p class="count">10</p>
  <a href="https://www.banana.com">바나나 사이트</a>
  </span>
  </div>, <div>
  <span class="name2" id="fruits2" title="사과">사과
                  <p class="store">사과 가게</p>
  <p class="price">4000</p>
  <p class="count">5</p>
  <a href="https://www.apple.com">사과 사이트</a>
  </span>
  </div>, <div>
  <span class="name3" id="fruits3" title="수박">수박
                  <p class="store">수박 가게</p>
  <p class="price">18000</p>
  <p class="count">1</p>
  <a href="https://www.watermelon.com">수박 사이트</a>
  </span>
  </div>, <div class="name1">동일 클래스</div>]
  ```

  

  - `.select('.클래스명')`: 동일한 클래스가 적용된 모든 태그의 모든 내용을 추출

  ```python
  print(soup.select('.name1'))
  
  #out
  [<span class="name1" id="fruits1" title="바나나">바나나
                  <p class="store">바나나 가게</p>
  <p class="price">3000</p>
  <p class="count">10</p>
  <a href="https://www.banana.com">바나나 사이트</a>
  </span>]
  ```

  

  - `.select('상위태그>하위태그>하위태그')`: 해당하는 모든 태그의 모든 내용을 추출

  ```python
  print(soup.select('div>span>p'))
  
  #out
  [<p class="store">바나나 가게</p>, <p class="price">3000</p>, <p class="count">10</p>, <p class="store">사과 가게</p>, <p class="price">4000</p>, <p class="count">5</p>, <p class="store">수박 가게</p>, <p class="price">18000</p>, <p class="count">1</p>]
  
  
  #인덱싱이 가능
  print(soup.select('div>span>p')[0])
  
  #out
  <p class="store">바나나 가게</p>
  ```

  

  - `.select('상위태그.클래스 이름>하위태그.클래스 이름')`

  ```python
  print(soup.select('span.name1>p.store'))
  
  #out
  [<p class="store">바나나 가게</p>]
  ```

  

  - `.select('#아이디)`: 일치하는 아이디의 값을 추출

  ```python
  print(soup.select('#fruits3'))
  
  #out
  [<span class="name3" id="fruits3" title="수박">수박
                  <p class="store">수박 가게</p>
  <p class="price">18000</p>
  <p class="count">1</p>
  <a href="https://www.watermelon.com">수박 사이트</a>
  </span>]
  ```

  

  - `.select('#아이디>태그.클래스 이름')`

  ```python
  print(soup.select('#fruits3>p.store'))
  
  #out
  [<p class="store">수박 가게</p>]
  ```

  

  - `.select('태그[속성=값]')`: 태그의 속성이 값과 일치하는 태그만 추출

  ```python
  print(soup.select('a[href="https://www.watermelon.com"]'))
  
  #out
  [<a href="https://www.watermelon.com">수박 사이트</a>]
  
  
  
  #해당 속성이 있는 모든 태그를 찾는 것도 가능
  print(soup.select('a[href]'))
  
  #out
  [<a href="https://www.banana.com">바나나 사이트</a>, <a href="https://www.apple.com">사과 사이
  트</a>, <a href="https://www.watermelon.com">수박 사이트</a>]
  ```



## 태그 내의 데이터 추출하기

- 태그 내의 텍스트 데이터 추출하기
  - `.string`
  - `.get_text()`

```python
for i in soup.find_all(['title','p']):
    print(i.text)
print()
for i in soup.find_all(['title','p']):
    print(i.get_text())


#out
bs4 연습
내용1
내용2

bs4 연습
내용1
내용2
```





# 웹 크롤러 만들기

## 사전 준비

- selenium
  - 웹 크롤러를 보다 쉽게 만들수 있게 해주는 패키지
  - 설치

  ```bash
  $ pip install selenium
  ```

  - import

  ```python
  from selenium import webdriver
  ```

  - selenium에서 특정 element에 접근하는 방법
    - find_element_by_name('')
    - find_element_by_id('')
    - find_element_by_class_name('')
    - find_element_by_tag_name('')
    - find_element_by_xpath('')
    - find_element_by_css_selector('')
    - find_element_by_link_text('')

- 크롬 드라이버 설치 필요(각 브라우저별 별도의 드라이버 설치)

  



## 검색창에 검색어 입력 후 자동 검색 기능 구현

- 개요: selenium이 웹 페이지를 연다 → 검색창을 찾는다 → 검색어를 입력한다. → 결과를 조회한다.
  - 위의 단계를 모두 사람이 하는 것이 아니라 selenium이 chrome driver를 실행시켜 한다.



- 예제 사이트: 대한민국 구석구석(https://korean.visitkorea.or.kr/main/main.do)



- 코드

```python
from bs4 import BeautifulSoup
from selenium import webdriver
import time

query_txt = input('크롤링할 키워드: ')

#1단계. 크롬 드라이버를 사용하여 웹 브라우저를 실행
#path에는 chromedriver.exe가 위치한 경로를 입력
path = "C:\Temp\chromedriver_win32\chromedriver.exe"
#만일 따로 경로를 지정하지 않을 경우 현재 파일이 있는 폴더에서 chromedriver.exe 파일을 찾는다.
driver = webdriver.Chrome(path)

# get: 웹 페이지를 여는 함수
# 인자로 크롤링 하려는 사이트의 주소를 입력
driver.get("https://korean.visitkorea.or.kr/main/main.do")

#위 사이트가 열린 후에 2초의 간격을 둔다.
time.sleep(2)


#2단계. 검색창의 이름을 찾아서 검색어를 입력한다.
driver.find_element_by_id('btnSearch').click()

element = driver.find_element_by_id('inp_search')

element.send_keys(query_txt)



#3단계. 검색 버튼을 눌러서 실행
driver.find_element_by_class_name("btn_search2").click()
```



- 실습: 네이버에서 자동 검색 수행하기

```python
query_txt=input('크롤링할 키워드: ')

path = "C:\Temp\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(path)

driver.get("https://www.naver.com/")
time.sleep(2)

element = driver.find_element_by_id("query")
element.send_keys(query_txt)

driver.find_element_by_id("search_btn").click()
```









## 검색된 결과에서 텍스트를 추출하여 저장하기

- 개요: selenium이 웹 페이지를 연다 → 검색창을 찾는다 → 검색어를 입력한다. → 결과를 조회한다→결과 중 유의미한 정보를 추출한다 → 출력 방식을 대화형 인터프리터(터미널 창)가 아닌 txt파일로 변경한다→정보를 파일에 저장한다.



- 예제 사이트: 대한민국 구석구석(https://korean.visitkorea.or.kr/main/main.do)



- 코드

```python
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
```



- 실습: 네이버에서 검색한 결과를 txt 파일로 저장하기