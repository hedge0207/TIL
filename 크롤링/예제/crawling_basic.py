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
# print(soup.find('div'))
# print(soup.find('title'))
# print(soup.find('p'))
# print(soup.find('p',align='left'))
# print(soup.find(['title','p']))


# print(soup.find_all('p'))
# print(type(soup.find_all('p')))
# print(soup.find_all(['title','p']))


# for i in soup.find_all(['title','p']):
#     print(i.text)

# for i in soup.find_all(['title','p']):
#     print(i.get_text())


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
# print(soup.select('div'))
# print(soup.select('.name1'))
# print(soup.select('div > span > p'))
# print(soup.select('div>span>p')[0])
# print(soup.select('span.name1>p.store'))
# print(soup.select('#fruits3>p.store'))
# print(soup.select('a[href="https://www.watermelon.com"]'))
print(soup.select('a[href]'))