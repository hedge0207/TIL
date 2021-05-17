# scrapy

## 기본 개념

- scrapy

  - 웹 크롤링을 위한 python 패키지
    - python으로 작성되었다.
    - spider를 작성해서 크롤링을 한다.
    - 프레임워크에 가깝다.
    - 오픈소스로 개발되었다.

  - 장점
    - 각 기능들을 spider, item, pipeline, selector 등으로 모듈화하여 유지 보수가 쉽다.
    - 비동기 요청으로 크롤링을 하기 때문에 하나의 요청에 에러가 발생하더라도 나머지 요청은 계속해서 처리 된다. 

  - beautiful soup과 비교
    - beautiful soup은 자체적으로 웹 사이트를 크롤링 할 수 없다.
    - `urlib2`와 `requests`를 사용하여 HTML 소스를 가져와야만 한다.

  |          | Beautiful Soup                          | Scrapy                               |
  | -------- | --------------------------------------- | ------------------------------------ |
  | 진입장벽 | 쉽다                                    | 비교적 어렵다                        |
  | 자료량   | 부족하다                                | 많다                                 |
  | 확장성   | 확장성이 낮다.                          | middlware를 커스터마이징 할 수 있다. |
  | 성능     | multiprocessing을 사용하면 매우 빠르다. | 빠른 편이다.                         |




- scrapy의 아키텍처

  ![](scrapy.assets/scrapy_architecture_02.png)

  - engine
    - 모든 컴포넌트의 동작은 Engine에  의해 통제된다.
    - 특정 액션이 발생했을 때 이벤트를 triggering한다.
  - Scheuler
    - engine으로부터 requests를 받고, 해당 requests를 queue에 저장한다. 
    - 이후 engine의 요청이 있을 경우 엔진에 requests를 전송한다.
  - Downloader
    - requests에 포함된 URL에서 웹 페이지를 가져와 response 객체를 만들어 engine에게 전달한다.
    - engine은 해당 response를 Spider로 전송한다.
  - Spiders
    - Scrapy 사용자가 커스텀한 클래스로, 응답을 파싱하고 해당 응답으로부터 items를 추출한다.
    - 또한 추가적인 요청을 생성하는 역할도 수행한다.
  - Item Pipeline
    - Spider에 의해 추출된 items를 처리하는 역할을 한다.
    - 일반적으로 데이터를 cleansing, 검증, 그리고 DB에 저장하는 것과 같은 역할을 수행한다.
  - Downloder middlewares
    - engine과 downloader 사이에 요청이 오갈 때 해당 요청을 처리하는 역할을 한다.
    - 아래와 같은 경우에 사용한다.
    - engine에서 downloader로 요청을 전송하기 직전에 요청을 처리해야 하는 경우.
    - engine이 downloader로 부터 받은 응답을 spider로 보내기 전에 변경하는 경우.
    - spider로 응답을 보내는 대신 새로운 요청을 전송하고자 할 경우.
    - 웹 페이지를 fetching 하지 않고 응답을 spider로 전송하는 경우. 
    - request를 drop하는 경우
  - Spider middlewares
    - spider와 engine 사이에서 spider의 input(downloader로 부터 받은 response)과 output(items와  requests)를 처리하는 역할을 수행한다.
    - 아래와 같은 경우에 사용한다.
    - spider callback의 output(items와  requests)을 후처리(change, add,remove)할 경우.
    - `start_requests`를 후처리 할 경우.
    - spider exception을 처리할 경우.
    - response 내용에 따라 일부 requests에서 callback 대신 errback을 호출할 경우.
  - 동작 과정
    - Engine은 Spider로부터 크롤링을 위한 최초의 요청을 받는다.
    - Engine은 Scheduler에서 요청을 스케줄링하며, 다음으로 크롤링할 요청에 대한 정보를 Scheduler에게 받는다.
    - Scheduler는 다음 요청에 대한 정보를 Engine에 넘겨준다.
    - Engine은 받은 요청 정보를 Downloader Middlewares를 통해Downloader에게 넘겨준다.
    - 한 페이지에 대한 다운로드가 종료되면 Downloader는 해당 페이지를 응답에 넣어서 Downloader Middlewares를 통해 Engine에 전송한다.
    - Engine은 Downloader로부터 받은 응답을 Spider Middlewares를 통해 Spider에게 전송한다.
    - Spider는 해당 응답을 처리하고 스크랩된 내용과 새로운 요청을 Spider Middlewares를 통해 Engine에 전송한다.
    - Engine은 Spider로 부터 받은 스크랩된 내용을 Item Pipelines에 전송하고, 요청은 Scheduler에 보내 다음 요청을 처리할 수 있는지 물어본다.
    - Scheduler에 더 이상 요청이 존재하지 않을 때 까지 위 과정이 반복된다.



- scrapy 프로젝트 생성하기

  -  scrapy 설치

  ```bash
  $ pip install scrapy
  ```

  - 프로젝트 생성하기
    - 프로젝트 디렉터리를 지정해 주지 않으면 프로젝트 이름에 해당하는 디렉토리를 하나 생성하고 그 내부에 spider 프로젝트를 생성한다.

  ```bash
  $ scrapy startproject <프로젝트 이름> [프로젝트 디렉터리]
  ```

  - 프로젝트 구조

  ```bash
  프로젝트명/
      scrapy.cfg            # 배포 설정 파일
  
      프로젝트명/
          __init__.py
  
          items.py          # itmes들을 정의하는 파일
  
          middlewares.py    # 커스텀 미들웨어의 기능을 정의하는 파일
  
          pipelines.py      # item pipelines(item이 다른 저장소로 저장될 때 거치는 통로)의 커스텀 모듈을 정의하는 파일
  
          settings.py       # scrapy 설정
  
          spiders/          # spider들을 정의하는 디렉터리
              __init__.py
  ```



## spider

- spider 생성하기

  - `spiders/` 디렉터리에 Python 파일을 생성한다.
    - `Spider`의 서브 클래스로 spider 클래스를 하나 생성한다.
    - 요청을 만드는 메서드와 응답을 받아서 응답에서 items들을 추출하는 메서드를 정의한다.

  ```python
  import scrapy
  
  
  class QuotesSpider(scrapy.Spider):
      name = "quotes"
  
      def start_requests(self):
          urls = [
              'http://quotes.toscrape.com/page/1/',
              'http://quotes.toscrape.com/page/2/',
          ]
          for url in urls:
              yield scrapy.Request(url=url, callback=self.parse) # 아래에서 정의한 callback 메서드(parse)를 함께 넘긴다.
          
          # 혹은
          # return [scrapy.Request(url=url, callback=self.parse) for url in urls]
  
      def parse(self, response):
          page = response.url.split("/")[-2]
          filename = f'quotes-{page}.html'
          with open(filename, 'wb') as f:
              f.write(response.body)
          self.log(f'Saved file {filename}')
  ```

  - `name`
    - Spider의 색별자로, 프로젝트 내에서 고유한 값이어야 한다.
  - `start_requests()`
    - 반드시 iterable한 `scrapy.Request`들을 반환해야한다(`yield`를 사용하여 generator 형식으로 작성해도 된다).
    - 후속 요청은 여기서 정의한 최초 요청에 의해 연속적으로 생성된다.
  - `parse()`
    - 각 reqeust에 대한 response를 처리하는 callback 메서드.
    - 인자로 받는 `response`는 page의 내용을 담고 있고, 해당 내용을 다루기 위한 메소드들을 가진`TextResponse` 클래스의 인스턴스이다.
    - page 내에서 새로운 URL들을 찾아 새로운 요청을 생성하는 역할도 수행한다.
  - `start_requests`를 더 짧게 작성하기
    - `start_requests`가  `scrapy.Request` 객체를 생성하도록하는 대신에 url들을 리스트에 담아두는 방식으로도 작성할 수 있다.
    - `parse()` 메서드는 각 request를 처리하기 위해 호출되는데, scrapy에게 명시적으로 `parse()`메서드를 호출하라고 하지 않아도 자동으로 호출된다.
    - 이는 `parse`라는 메서드명이 Scrapy에서 기본 callback 메서드명으로 사용되기 때문으로, 만일 `parse()`가 아닌 `something_else()`와 같이 메서드명을 작성한다면, 아래와 같이는 쓸 수 없다.

  ```python
  import scrapy
  
  
  class QuotesSpider(scrapy.Spider):
      name = "quotes"
      start_urls = [
          'http://quotes.toscrape.com/page/1/',
          'http://quotes.toscrape.com/page/2/',
      ]
  
      def parse(self, response):
          page = response.url.split("/")[-2]
          filename = f'quotes-{page}.html'
          with open(filename, 'wb') as f:
              f.write(response.body)
  ```

  



- Spider 실행

  - 실행하기
    - 프로젝트의 최상단 디렉터리에서 아래 명령어를 실행한다.

  ```bash
  $ scrapy crawl <Spider 식별자>
  ```

  - 위 명령어를 실행하면 무슨 일이 발생하는가?
    - scrapy는 spider의 `start_requests` 메서드의 반환 값인  `scrapy.Request`를 스케줄링한다.
    - 각 request로부터 응답을 받으면,  `Response` 객체를 인스턴스화하고, 요청과 관련된 callback 메서드(예시의 경우 `parse` 메서드)를 호출한다.
  - spider 내부에 인자를 넘기기

  ```bash
  $ scrapy crawl <spider 명> -a <key=value>
  
  # 예시
  $ scrapy crawl quotes -a tag=humor
  ```

  - 인자 사용하기
    - `getattr`을 사용한다.

  ```python
  import scrapy
  
  
  class QuotesSpider(scrapy.Spider):
      name = "quotes"
  
      def start_requests(self):
          url = 'http://quotes.toscrape.com/'
          # tag에 humor가 담긴다.
          tag = getattr(self, 'tag', None)
          if tag is not None:
              url = url + 'tag/' + tag
          yield scrapy.Request(url, self.parse)
  
      def parse(self, response):
          (...)
  ```





## 데이터 추출하기

- scrapy shell

  - scrapy에서 데이터가 어떻게 추출되는지 이해하는 가장 좋은 방법은 scrapy shell을 사용해보는 것이다.
    - python shell을 실행시킨다.
  - 명령어
    - url을 입력할 경우 항상 따옴표로 url을 묶어줘야 한다.
    - 묶어주지 않을 경우 url에 특정 문자(& 등)이 포함되어 있으면 동작하지 않는다.

  ```bash
  $ scrapy shell <'스크랩 할 url' 또는 local 파일>
  
  # 예시
  $ scrapy shell 'http://quotes.toscrape.com/page/1/'
  ```



- response 객체에서 CSS를 사용하여 elements 선택하기 

  - 아래 명령의 결과로 `SelectorList`라 불리는 배열 형태의 객체가 반환된다.
  - 반환 받은 객체를 통해 더 상세하게 조회하거나 데이터를 추출할 수 있게 된다.

  ```shell
  # 기본형
  >>> response.css('<CSS 선택자>')
  
  # 예시: CSS 선택자가 title인 elements를 선택
  >>> response.css('title')
  # 반환값
  [<Selector xpath='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]
  ```

  - 반환 받은 객체에서 data 추출하기
    - `getall()`의 경우 배열 형태로 모든 값을 추출한다.
    - `get()`은 하나의 값만을 추출한다.
    - `re()`는 보다 상세한 조회가 가능하다.

  ```shell
  # 태그도 함께 추출
  >>> response.css('title').getall()
  ['<title>Quotes to Scrape</title>']
  
  # 텍스트만 추출
  >>> response.css('title::text').getall()
  ['Quotes to Scrape']
  
  # getall() 대신 get()사용
  >>> response.css('title::text')[0].get()
  'Quotes to Scrape'
  
  # re() 사용
  >>> response.css('title::text').re(r'Quotes.*')
  ['Quotes to Scrape']
  >>> response.css('title::text').re(r'Q\w+')
  ['Quotes']
  >>> response.css('title::text').re(r'(\w+) to (\w+)')
  ['Quotes', 'Scrape']
  ```

  - CSS뿐 아니라 XPath를 활용할수도 있다.
    - 사실 CSS selector들은 Scrapy 내부적으로 XPath로 변환되어 실행되는 것이다.
    - CSS를 통한 방식보다 훨씬 강력하다.

  ```shell
  >>> response.path('//title')
  [<Selector xpath='//title' data='<title>Quotes to Scrape</title>'>]
  >>>response.xpath('//title/text()').get()
  'Quotes to Scrape'
  ```



- 응답으로 받은 페이지 열기

  - 아래 명령어를 입력하면 응답으로 받은 객체를 웹 브라우저로 띄어준다.

  ```shell
  >>> view(response)
  ```



- 실제 사용 예시

  - http://quotes.toscrape.com 사이트에서 quotes와 author 추출하기

  ```html
  <div class="quote">
      <span class="text">“The world as we have created it is a process of our
      thinking. It cannot be changed without changing our thinking.”</span>
      <span>
          by <small class="author">Albert Einstein</small>
          <a href="/author/Albert-Einstein">(about)</a>
      </span>
      <div class="tags">
          Tags:
          <a class="tag" href="/tag/change/page/1/">change</a>
          <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
          <a class="tag" href="/tag/thinking/page/1/">thinking</a>
          <a class="tag" href="/tag/world/page/1/">world</a>
      </div>
  </div>
  ```

  - scrapy shell 실행하기

  ```bash
  $ scarpy shell 'http://quotes.toscrape.com'
  ```

  - CSS 선택자로 Selector 객체 확인하기

  ```shell
  >>> response.css("div.quote")
  [<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype...'>, 
  <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype...'>, 
  ...]
  ```

  - 첫 번째 Selector 객체를 변수에 할당하기

  ```shell
  >>> quote = response.css("div.quote")[0]
  ```

  - text, author 추출하기

  ```bash
  >>> text = quote.css("span.text::text").get()
  >>> text
  '“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”'
  >>> author = quote.css("small.author::text").get()
  >>> author
  'Albert Einstein'
  ```

  - tags 추출하기

  ```shell
  >>> tags = quote.css("div.tags a.tag::text").getall()
  >>> tags
  ['change', 'deep-thoughts', 'thinking', 'world']
  ```



- spider에서 데이터 추출하기

  - spider는 페이지에서 추출한 데이터를 일반적으로 딕셔너리에 저장한다.
    - 이를 위해 `yield` 문법을 사용한다.

  ```python
  import scrapy
  
  
  class QuotesSpider(scrapy.Spider):
      name = "quotes"
      start_urls = [
          'http://quotes.toscrape.com/page/1/',
          'http://quotes.toscrape.com/page/2/',
      ]
  
      def parse(self, response):
          for quote in response.css('div.quote'):
              yield {
                  'text': quote.css('span.text::text').get(),
                  'author': quote.css('small.author::text').get(),
                  'tags': quote.css('div.tags a.tag::text').getall(),
              }
  ```

  - 실행하면 다음과 같이 출력된다.

  ```bash
  $ scrapy crwal quotes
  
  2021-05-17 11:17:19 [scrapy.core.scraper] DEBUG: Scraped from <200 http://quotes.toscrape.com/page/1/>
  {'text': '“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”', 'author': 'Albert Einstein', 'tags': ['change', 'deep-thoughts', 'thinking', 'world']}
  2021-05-17 11:17:19 [scrapy.core.scraper] DEBUG: Scraped from <200 http://quotes.toscrape.com/page/1/>
  {'text': '“It is our choices, Harry, that show what we truly are, far more than our abilities.”', 'author': 'J.K. Rowling', 'tags': ['abilities', 'choices']}
  ...
  ```

  

## 데이터 저장하기

- Feed exports 사용하기

  - `-O`는 기존에 파일이 없다면 새로운 파일을 생성하고, 이미 파일이 있다면 해당 파일을 덮어쓴다.
  - `-o`는 이미 존재하는 파일에 추가한다.
    - 단, 이 경우 기존 파일 형식과 맞지 않을 수 있다.
    - Json 파일의 경우  `-o` 옵션을 사용할 때 json 파일 형식이 아닌 JSON Lines 형식으로 추가하는 것을 추천한다.(e.g `quotes.jl`)

  ```bash
  $ scrapy crawl <spider 이름> -O <저장할 파일 이름>
  ```

  - 예시

  ```bash
  $ scrapy crawl quotes -O quotes.json
  ```

  

## Following links

- Following links

  - 만일 https://quotes.toscrape.com/page/1/, https://quotes.toscrape.com/page/2/과 같이 각 페이지를 하나씩 스크랩하는 것이 아니라 모든 페이지를 스크립 하는 방법
  - follow 하려는 link 정보를 확인한다.

  ```html
  <ul class="pager">
      <li class="next">
          <a href="/page/2/">Next <span aria-hidden="true">&rarr;</span></a>
      </li>
  </ul>
  ```

  - shell로 해당 링크를 추출해본다.

  ```shell
  >>> response.css('li.next a').get()
  '<a href="/page/2/">Next <span aria-hidden="true">→</span></a>'
  >>> response.css('li.next a::attr(href)').get()
  '/page/2/'
  # 또는
  >>> response.css('li.next a').attrib['href']
  '/page/2/'
  ```

  - spider에 적용
    - 이제 데이터를 추출 한 후 `parse()` 메서드는 다음 페이지에 대한 정보를 추출하고, `urljoin` 메서드를 활용하여 완전한 url로 만든 후 다음 페이지에 대한 Request를 만든다.

  ```python
  import scrapy
  
  
  class QuotesSpider(scrapy.Spider):
      name = "quotes"
      start_urls = [
          'http://quotes.toscrape.com/page/1/',
          'http://quotes.toscrape.com/page/2/',
      ]
  
      def parse(self, response):
          for quote in response.css('div.quote'):
              yield {
                  'text': quote.css('span.text::text').get(),
                  'author': quote.css('small.author::text').get(),
                  'tags': quote.css('div.tags a.tag::text').getall(),
              }
          next_page = response.css('li.next a::attr(href)').get()
          if next_page is not None:
              next_page = response.urljoin(next_page)
              yield scrapy.Request(next_page, callback=self.parse)
  ```



- `response.follow`

  - `follow()` 메서드를 사용하여 Request 생성을 보다 간소화 할 수 있다.
    - `urljoin()`을 호출하지 않아도 된다.

  ```python
  import scrapy
  
  
  class QuotesSpider(scrapy.Spider):
      name = "quotes"
      start_urls = [
          'http://quotes.toscrape.com/page/1/',
      ]
  
      def parse(self, response):
          for quote in response.css('div.quote'):
              yield {
                  'text': quote.css('span.text::text').get(),
                  'author': quote.css('span small::text').get(),
                  'tags': quote.css('div.tags a.tag::text').getall(),
              }
  
          next_page = response.css('li.next a::attr(href)').get()
          if next_page is not None:
              yield response.follow(next_page, callback=self.parse)
  ```

  - 문자열 대신 selector를 넘기는 것도 가능하다.

  ```python
  # 기존 코드
  next_page = response.css('li.next a::attr(href)').get()
  if next_page is not None:
      yield response.follow(next_page, callback=self.parse)	# 문자열을 넘긴다.
  
  # selector를 넘기는 코드
  for href in response.css('ul.pager a::attr(href)'):
      yield response.follow(href, callback=self.parse)
  ```

  - `<a>` 태그의 경우 더 간소화가 가능하다.

  ```python
  for a in response.css('ul.pager a'):
      yield response.follow(a, callback=self.parse)
  ```

  - `response.follow_all()`
    - iterable한 여러 개의 request를 생성할 때 사용한다.

  ```python
  anchors = response.css('ul.pager a')
  yield from response.follow_all(anchors, callback=self.parse)
  
  # 더 짧게 작성하는 것도 가능하다.
  yield from response.follow_all(css='ul.pager a', callback=self.parse)
  ```



- 다른 예시

  ```python
  import scrapy
  
  
  class AuthorSpider(scrapy.Spider):
      name = 'author'
  
      start_urls = ['http://quotes.toscrape.com/']
  
      def parse(self, response):
          # author 정보를 follow하기 위한 코드
          author_page_links = response.css('.author + a')
          yield from response.follow_all(author_page_links, self.parse_author)
  		
          # pagination link를 follow하기 위한 코드
          pagination_links = response.css('li.next a')
          yield from response.follow_all(pagination_links, self.parse)
  	
      # author 정보를 파싱하기 위한 메서드
      def parse_author(self, response):
          def extract_with_css(query):
              return response.css(query).get(default='').strip()
  
          yield {
              'name': extract_with_css('h3.author-title::text'),
              'birthdate': extract_with_css('.author-born-date::text'),
              'bio': extract_with_css('.author-description::text'),
          }
  ```

  - Scrapy는 내부적으로 이미 탐색한 url에는 다시 요청을 보내지 않도록 설정되어 있다. 
    - 따라서 위와 같이 여러 url에 요청을 보내는 경우에도 중복된 url로 요청을 보내지 않는다.
    - 설정을 통해 변경이 가능하다.



















