  

# Django

- Static web page와 Dynamic web page

  - static web page: 미리 만들어둔 문서(HTML, CSS, JS 등)를 항상 똑같이 제공하는 서비스
  - dynamic web page: 사용자의 요청에 맞게 그때그때 문서를 만들어서 전달하는 서비스
  - HTML, CSS, JS 만으로는 Static web(미리 저장된 html,css,js 등의 정적 파일을 제공) 밖에 만들 수 없다.



- 장고는 web framework다.

  - web framework는 웹 페이지 개발 과정의 어려움을 줄이는 것이 주 목적이다.
  - 표준 구조를 구현하는 클래스와 라이브러리의 모임이다.



- 기본적인 명령어

  - django 설치

    ```bash
    $ pip install django[==버전]
    ```

  - 프로젝트 시작

    ```bash
    $ django-admin startproject <프로젝트명>
    ```

    - 현재 위치에 중간 단계 없이 프로젝트 생성

    ```bash
    $ django-admin startproject <프로젝트명> .
    ```

  - 앱 생성

    ```bash
    $ python manage.py startapp <앱이름>
    ```

  - 서버 실행

    - 뒤의 8080은 포트 번호로, 로컬에선 쓰지 않아도 된다.

    ```bash
    $ python manage.py runserver [port]
    ```

  - 마이그레이션

    ```bash
    $ python manage.py makemigrations
    ```

  - 마이그레이트

    ```bash
    $ python manage.py migrate
    ```





# MTV기초

- 소프트웨어 디자인 패턴
  - 소프트웨어를 어떻게 설계할 것인가.
  - MVC, MTV는 모두 소프트웨어 디자인 패턴이다.
- MTV: Model, Template, View로 장고의 기본 흐름이다. 다른 곳에서는 보통 MVC를 쓴다.
  - Model: 데이터 관리, 데이터베이스 조작, 데이터 구조화(어떻게 데이터를 넣을 것인가)
  - Template: 사용자와 웹 브라우저사이의 인터페이스(화면) 구성, 단순히 html파일을 의미하는 것이 아니라 html파일을 만드는 것을 의미, 데이터를 표시하는 곳
  - View: 중간 관리(상호 동작)
- MVC: Model, View, Controller로, 순서대로 MTV와 하나씩 대응



cf. **API**(Application Programming Interface, 응용 프로그램 프로그래밍 인터페이스): 응용 프로그램에서 사용할 수 있도록, 운영 체제나 프로그래밍 언어가 제공하는 기능을 제어할 수 있게 만든 인터페이스



- 기본적인 장고를 다루는 순서는 아래와 같다.

  - 프로잭트 생성(이때 생기는 intro폴더가 모든 프로젝트를 관리하는 폴더다)

    - `__init__.py`, `settings.py`, `urls.py`, `wsgi.py`등이 있다.
    - wsgi는 web server gateway interface이다.

  - settings.py에서 아래와 같은 코드를 입력한다.

  ```python
  ALLOWED_HOST = ['*']
  # 운용 서버에서 사용할 Host이름을 등록해 주는 것으로 IP주소와 도메인 모두 사용할 수 있다.
  # 등록되지 않은 호스트 명으로 요청이 들어올 경우 400 Bad Request Error를 반환
  # *는 모든 요청을 수락한다는 것이다.
  
  # 특정하고 싶다면 아래와 같이 특정 도메인이나 ip주소를 입력하면 된다.
   ALLOWED_HOST = ['fathomless-scrubland-30645.herokuapp.com','127.0.0.1']
  ```

  - 앱 생성

    - 앱 이름은 복수로 지정하는 것이 관례다. 

  ```bash
  $ python manage.py startapp <앱이름>
  ```

  - 장고에게 앱이 생성되었다는 것을 알리기

    - 즉, 등록을 해야하는데 이는 `settings.py`에서 한다.
  
    - `INSTALLED_APPS`에 추가해줘야 한다.
  
  
  ```python
  # $ python manage.py startapp pages를 통해 pages라는 app을 만들었을 경우 아래와 같이 추가해야 한다.
  #INSTALLED_APPS는 아래에서 확인 할 수 있듯이 리스트이다.
      
  INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
      'django.contrib.messages',
        'django.contrib.staticfiles',
      'pages',  #앱 이름 등록
  ]
  ```
  
  - settings.py에 있는 각종 옵션들
  
  
  ```python
  #디버그
  DEBUG = True  #True로 되어 있으면 개발 모드다. 배포시에는 반드시 False로 바꿔야 한다.
  # True로 놓으면 오류 페이지가 상세하게 떠서 어떤 오류가 발생했고 어떤 코드에서 발생했는지 알 수 있다.
  #False로 해놓으면 오류 메세지만 출력된다. 따라서 만일 True로 해놓은 상태에서 오류가 발생하게 되면 다른 사람들이 내가 짠 코드를 전부 볼 수 있게 되므로 보안상의 심각한 문제가 생길 수 있다. 따라서 다른 사람들이 사용하게 할 때에는 반드시 False로 바꿔야 한다.
  
  ALLOWED_HOSTS = [] #프로젝트에서 생성한 사이트(경로)로 들어올 권한을 정하는 것이다.
  #'*'를 대괄호 사이에 넣으면 누구나 입장 가능한 상태가 된다.
  #프로그래밍에서 *는 일반적으로 "모두"를 뜻한다.
  
  
  TEMPLATES = [
      {    #DjangoTemplates(DTL)라는 엔진을 쓰고 있다는 의미, jinja2 등으로 변경 가능
          'BACKEND': 'django.template.backends.django.DjangoTemplates',
          'DIRS': [],
          #'APP_DIRS'가 True면 Installed_APPS에 등록된 앱들의 템플릿 폴더를 관리하겠다는 의미
          'APP_DIRS': True,  
          'OPTIONS': {
              'context_processors': [
                  'django.template.context_processors.debug',
                  'django.template.context_processors.request',
                  'django.contrib.auth.context_processors.auth',
                  'django.contrib.messages.context_processors.messages',
              ],
          },
      },
  ]
  
  # Internationalization관련 설정들
  LANGUAGE_CODE = 'en-us'  #언어를 설정하는 것으로 "ko-kr"로 바꾸면 한국어가 된다.
  
  TIME_ZONE="UTC"  #시간 설정으로 'Asia/Seoul'로 바꾸면 한국 시간이 된다.
  
  USE_I18N = True #Internationalization의 약자로 I와 N사이에 18자가 위치해 이렇게 명명
  
  USE_L10N = True #Localization의 약자로 L과 N사이에 10자가 위치해 이렇게 명명
  

USE_TZ = True
  ```

  - url 연결하기
  
    - 다음으로 `urls.py`에서 어떤 url로 들어갔을 때 무엇을 처리할지를 설정해줘야 한다.
  
  
  ``` python
  from django.contrib import admin
  from django.urls import path
  from pages import views   #pages에서 views를 가져오고 
  #기본 구조
  #from app이름 import 함수정의된 파일 이름
  # 서버를 실행시켰을 때 urlpatterns가 비어 있다고 오류가 발생하지는 않으나(물론 관련 경로로 보내고자 한다면 오류가 발생하겠으나, 서버'만' 실행시켰을 때는 오류가 발생하지 않는다.)urlpatterns라는 리스트 자체를 정의하지 않으면 오류가 발생한다. 따라서 빈 리스트라도 만들어 두어야 한다.
  urlpatterns = [
      path('admin/', admin.site.urls),
      path('index/', views.index),
  	#index라는 url로 들어가면 views의 index라는 함수를 처리를 하겠다.
  	#기본 구조
  	#path('url/', 함수가 정의된 파일 이름.함수 이름)
  ]
  
  #꼭 위처럼 url과 함수명을 맞춰야 하는 것은 아니나 편의를 위해서 위와 같이 한다.
  #예컨데 아래와 같이 하는 것도 가능하다.
  urlpatterns = [
      path('admin/', admin.site.urls),
      path('bboong/', views.index),
  ]
  ```

- 함수 정의하기
  
    - 위에서 어떤 url에서 어떤 함수가 처리될지 정의했으니 이제 처리될 함수를 정의해야 한다.
    
  ```python
  #위에서 views의 index라는 함수를 처리할 것이라고 했으므로 views.py에서 해당 함수를 정의해야 한다.
  from django.shortcuts import render
  
  
  #해당 함수를 실행시키는 url에 접속해야 실행되기에 request라는 이름을 붙인다.
  
  #request가 아닌 다른 것을 넣어도 동작은 하지만 그렇게 하지 않는다.
  
  def index(request): #항상 첫번째 인자로 request를 정의한다.
  	return render(request,'index.html') #항상 render()를 리턴한다.
  #render는 html이 응답할 수 있게 만드는 작업을 한다. import를 해줘야 사용 가능하다.
  #역시 마찬가지로 함수명과 리턴될 html파일명을 일치시켜야 하는 것은 아니나 편의를 위해 위와 같이 한다.
  #예컨데 아래와 같이 하는 것도 가능하다.
  from django.shortcuts import render
  
  def index(request): #항상 첫번째 인자로 request를 정의한다.
      return render(request,'qwert.html')
  
  #단 꼭 request로 적는 것은 아니며 아무거나 적어도 된다. 그러나, 이렇게 쓰지 않는다.
  def index(re):
      return render(re,'qwert.html')
  ```
  
  - redirect
    - 특정 html파일을 렌더링 하는 것이 아니라 처리가 모두 끝난 후 특정 url로 넘어가고자 할 때에는 redirect를 쓰면 된다.
  
  ```python
  from django.shortcuts import render,redirect
  
  def index(request):
      return redirect('가고자 하는 url')
  
  #redirect는 경로로 들어가는 것이므로 urls로 갔다가 views를 실행하고 views에 입력한 대로 html파일이 렌더링되는 경로를 거치지만 render는 위의 과정을 거치지 않고 바로 렌더링한다. 따라서 위의 경우처럼 특정 경로로 돌아가야 하는 경우에는 redirect를 써야한다.
  
  #bitly, bit.do 등의 사이트는 리다이렉트를 해주는 사이트이다.
  ```
  
- HTML문서 작성하기
  
  - 위에서 처리될 함수를 정의했으니 이제 그 함수에 들어있는 `index.html`을 작성해줘야 한다.
  
  - 함수에서 반환할 `html` 파일은 항상 `templates`폴더 안에 생성해야 한다.
  
  ```html
  <h1>Hello!</h1>
  ```
  
- 여기까지가 한 과정이며 이제 누군가 `index/`라는 주소로 접근하게 되면 장고는 `urls.py`에 작성된 대로`view`의  `index`함수를 실행시키게 된다. `index`함수는 `html`파일을 retrun하고 작성한 `html`파일 대로 `index`가 포함된 해당 주소에는  `Hello!`가 출력된다.



- 함수 정의하기

  - 기본형

  ``` python
  #기본형
  from django.shortcuts import render
  
  def index(request):
  	return render(request,'index.html')
  ```

  - HTML파일에 넘겨줄 변수가 있는 경우

    - 항상 딕셔너리로 넘겨준다.
    - 일반적으로 html파일에 넘겨줄 내용들을 context라는 딕셔너리에 담아서 넘기며 꼭 리스트만 넘길 수 있는 것은 아니고 문자열, 빈 리스트도 넘길 수 있다.

  


- HTML문서 정리

  - 함수에서 인자를 받은 경우 중괄호 2개로 해당 인자의 키를 입력하면 된다. 화면에는 key에 해당하는 value가 출력된다.

  ```python
  #views.py파일
  from django.shortcuts import render
  
  def index(request):
      import random
      pick = random.sample(range(1,46),6)
      context={
          'picka':pick
      }
  	return render(request,'index.html',context) #context를 넘겨준다.
  #context이외의 변수에도 할당 가능하지만 관례상 context에 담는다.
  #또한 굳이 딕셔너리를 변수에 담아서 넘기지 않고 딕셔너리를 바로 넘겨도 된다.
  def index(request):
      import random
      pick = random.sample(range(1,46),6)
  	return render(request,'index.html',{'picka':pick})
  #그러나 여러개의 딕셔너리를 담아서 넘길 경우 코드가 지나치게 길어지므로 변수에 담아서 넘기는 방식을 사용한다.
  ```

  - lotto.html

  ```html
  <h1>{{picka}}</h1>
  
  out
  [22,17,44,11,38,29]
  <!--상기했듯 key값을 받아 value를 표시하는 것이므로 key값이 바뀌면 HTML문서도 수정해야 함-->
  ```

  - 배열을 출력하고자 하는 경우

    - 파이썬과 달리 인덱스로 접근할 때 대괄호가 아닌 .(dot)을 쓴다. 꼭 이때뿐만 아니라. 장고에서 HTML 작성시 대괄호나 소괄호는 사용하지 못한다.


  ```python
  #views.py파일
  from django.shortcuts import render
  
  def index(request):
      menupan=['치킨','피자','햄버거']
      context={
          'menu':menupan
      }
  	return render(request,'index.html',context)
  ```

  - index.html

  ```html
  <h1>{{ menu[0] }}</h1>
  <!--
  out
  에러 발생
  -->
  
  
  <h1>{{ menu.0 }}</h1> <!--value인 menupan이 아닌 key인 menu를 가지고 인덱스 접근-->
  
  <!--
  out
  치킨
  -->
  ```



# DTL


- DTL(Django Template Language): 장고의 화면을 작성하기 위한 언어, 렌더링을 위한 언어

    - jinja 역시 템플릿 언어 중 하나이다.

    - 파이썬에서의 문법과 같이 연산을 위해 사용하는 것이 아니다. 연산이 끝난 자료를 받아 그것을 출력하기 위한 문법들일 뿐이다.





  - 기본 출력

    ```html
    {{ }}
    ```




  - 주석: DTL의 내용을 html주석(<!---->)으로 처리하면 오류가 발생한다. 따라서 DTL 주석은 반드시 아래와 같이 해줘야 한다.

    ```html
    {# #}
    ```




  - 반복문, 조건문 등의 문법

    ```html
    {% %}
    ```




  - 반복문

    ```python
    #views.py파일
    from django.shortcuts import render
    
    def index(request):
        menupan=['치킨','피자','햄버거']
        context={
            'menu':menupan
        }
        return render(request,'index.html',context)
    ```

    - index.html

    ```html
    <ul>
        {% for m in menu %}   <!--for문과-->
          <li>{{m}}</li>
          {% endfor %}          <!--endfor문 사이의 내용을 len(menu)번 반복-->
    </ul>
    
    <!--
    out
    치킨
    피자
    햄버거
    -->
    ```


    - `forloop.counter`: 반복 횟수를 출력, 당연히 for문 안에만 쓸 수 있다.
    
      - `forloop.counter숫자`:입력한 숫자부터 시작한다(지정하지 않으면 1부터 시작).  숫자와 counter 사이에 띄어쓰기 안한다.


    ```html
    <!--index.html-->
    <ul>
      {% for m in menu %}
      <li>{{forloop.counter2}} : {{m}}</li>
      {% endfor %}
    </ul>
        
    out
    2 : 치킨
    3 : 피자
    4 : 햄버거
    ```
    
    - `empty`: 반복할 것이 없을 경우 설정한 내용을 출력
    
    ```django
    <!--no_replies가 빈 배열이라고 가정하면-->
    {% for reply in no_replies%}
    	<p>{{ reply }}</p>
    	{% empty %}
    	<p>댓글이 없어요</p>
    {% endfor %}
    
    out
    댓글이 없어요
    ```




  - 조건문

    ```django
    <!--기본형-->
    {% if user == 'admin' %}   <!--if문이 True면-->
    	<p>수정, 삭제</p>        <!--이 줄이 실행-->
    {% else %}				   <!--if문이 False면-->
    	<p>관리자 권한이 없습니다.</p> <!--이 줄이 실행-->
    {% endif %}     <!--for문과 마찬가지로 닫아줘야 한다.-->
    ```

  

- 기타

    - 일반적으로 DTL에서 `|`는 필터(filter)를 나타낸다.

    - `|length`: 앞에 온 문자열 혹은 리스트의 길이를 출력

  ```html
  <!--예를 들어 content에 "안녕"을 넘겼다고 가정하면-->
  <p>{{content|length}}</p>
  
  out
  2
  ```

    - `|truncatechars:양의 정수`: 앞의 내용을 양의 정수까지만 출력하고 나머지는 말줄임표로 처리

  ```html
  <!--content에 Life is short, you need python이 담겨 있다면-->
  
  {{ content|truncatechars:10 }}
  
  out
  Life i ...
  
  <!--공백 역시 하나의 문자로 취급되며 마지막에 오는 ...도 개수에 포함된다.-->
  ```

    - `|title`:  첫 글자를 대문자로 출력

  ```html
  {{ 'my name is smith'|title }}
  
  out
  My Name Is Smith
  ```

    - `|date`: 표현식에 따라 출력
      - 자세한 표현식은 https://docs.djangoproject.com/en/dev/ref/templates/builtins/?from=olddocs의 date참고

  
  ```html
  <!--{ date자료형|date:"표현식" } 형태-->
  today에 datetime객체가 들어있다고 가정
  {{today|date:'Y년 m월 d일 (D) A h:i'}}
  
  out
  2020년 03월 06일 (Sun) PM 04:01
  
  <!--Y는 4자리로 표기한 년도, m은 숫자만 표기된 월, d는 숫자만 표기된 일, D는 요일, A는 오전, 오후, h는 시간, i는 분-->
  ```
  






# MTV 확장


- variable routing

  - url을 변수화 해서 변수로 사용하는 것



  - variable routing에서 str이 기본값이라 문자열을 쓸 경우 str을 적지 않아도 된다.

    - 아래에서 name뒤에 숫자를 붙였는데 숫자가 같은 것 끼리는 변수명이 동일해야 한다.

    ```python
    #예시1
    #urls.py
    urlpatterns = [
        path('hi/<str:name1>', views.Hi),
    ]
    ```

    ```python
    #views.py
    def Hi(request,name1):
        context = {
            'name2': name1
        }
        return render(request, 'hi.html', context)
    ```

    ```html
    <!--hi.html-->
    <h1>안녕, {{ name2 }}</h1>
    
    <!--경로에 ~/hi/John-->
    out
    안녕, John
    ```

    ```python
    #예시2
    #urls.py
    urlpatterns = [
        path('sum/<int:a>/<int:b>/', views.sum),
    ]
    ```

    ```python
    #views.py
    def Hi(request,a,b):
        result=a+b
        context = {
            's_result': result
        }
        return render(request, 'sum.html', context)
    ```

    ```html
    <!--sum.html-->
    <h1>{{ s_result }}</h1>
    
    <!--경로에 ~/sum/6/7-->
    out
    13
    ```



  - 주의사항

    - variable routing으로 str값을 설정할 경우 주의해야 한다.
    - url 경로는 기본적으로 문자열(str)이고, url 경로를  `urlpatterns`에 정의된 순서대로 탐색해 나간다. variable routing으로 str값을 `urlpatterns` 맨 앞에 설정할 경우 모든 url 경로가 그쪽으로만 빠질 수 있다.

    ```python
    #맨 첫 줄에 variable routing으로 '<str:username>/'이라는 경로가 설정되어 있으므로, url경로로 login이 들어왔을 때, 문자열인 'login'은 views.login이 아닌 views.profile을 실행시키게 된다. 이는 `logout`도 마찬가지로, 이를 해결하기 위해서는 path('<str:username>/',views.profile,name="profile"),을 맨 마지막 줄에 적거나,
    urlpatterns = [
        path('<str:username>/',views.profile,name="profile"),
        path('login/', views.login, name='login'),
        path('logout/', views.logout, name='logout'),
    ]
    
    #아래와 같이 보다 구체적으로 url을 설정해 줘야 한다.
    urlpatterns = [
        path('profile/<username>/',views.profile,name="profile"),
        path('login/', views.login, name='login'),
        path('logout/', views.logout, name='logout'), 
    ]
    ```





- 템플릿 확장

  - 프로그래머는 반복적인일을 해야 할 때 반복을 컴퓨터에 맡길 방법이 없는지 생각해 봐야한다.

  - HTML작성시에도 마찬가지로 여러 HTML문서에 공통으로 들어가는 사항을 매번 입력하지 않고 한번의 작성만으로 끝낼 수 있는 방법이 존재한다.

    ```html
    <!--base-->
    <!--이름에 넣고 싶은 것을 입력하고-->
    {% block 이름 %}
    {% endblock %}
    
    
    <!--적용-->
    <!--위에서 입력한 이름과 위 html파일의 파일명을 일치시키면 된다.-->
    {% extends 'base가되는 html파일명' %} <!--어떤 파일을 기준으로 확장할지 적어준다.-->
    
    {% block 이름 %}
    {% endblock %} 
    ```

    ```html
    <!--base.html-->
    <!--기본 구조-->
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Articles</title>
    </head>
    <body>
        {% block body %}  <!--이 문구 위를 a라 하고-->  
        {% endblock %}       <!--이 문구 아래를 b라 하면-->  
    </body>
    </html>
    ```

    ```html
    <!--aa.html-->
    {% extends 'base.html' %} <!--상단에 기본이 되는 html파일명과 함께 이처럼 입력하고-->  
    
    {% block body %} <!--이 문구 위에는 a가 작성된 것으로 간주하고-->  
    
    {% endblock %}  <!--이 문구 아래는 b가 작성된 것으로 간주한다. -->  
    ```





- 멀티플 APP

  - 여러개의 앱을 만들 경우 url을 관리하기가 힘들어지므로 두 앱의 url을 따로 관리할 필요가 있다.

  - 따라서 그동안 프로젝트 폴더에서 관리하던 urls.py 파일을 앱마다 만들어 따로 관리한다.

  - 프로젝트 폴더 내의 urls.py파일에는 각 앱에 있는 urls.py 파일로 연결해주는 코드를 작성한다.

    ```python
    #boards와 pages라는 2개의 앱을 만들어 url을 따로 관리하고자 하는 경우 프로젝트 폴더 내의 urls.py에는 다음과 같이 작성한다.
    
    from django.contrib import admin
    from django.urls import path, include  #include를 불러오고
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        #만일 pages/라는 경로로 접근하면 pages에 있는 urls에 따른다.
        path('pages/', include('pages.urls')),
        #만일 pages/라는 경로로 접근하면 boards에 있는 urls에 따른다.
        path('boards/', include('boards.urls')),
    ] 
    ```

  - 각 앱의 입장에서도 프로젝트 urls가 연결해준 요청을 받아야 하므로 다음과 같이 작성한다.

    ```python
    #pages의 urls.py
    from django.urls import path
    from 디렉토리 import views  #디렉토리가 같을 경우 .을, 아닐 경우 디렉토리명을 입력해준다.
    
    urlpatterns = [
        #기존 프로잭트 폴더 내의 urls파일에 있던 내용을 path('admin/', admin.site.urls)만 빼고     동일하게 작성하면 된다.
        path('hello/', view.hello),
        path('lotto/', views.lotto),
        #이렇게 urls를 분리해서 작성했을 경우 이 파일이 실행된다는 것은 프로젝트 폴더 내의 urls가 싱     행되었고 pages/라는 경로가 입력되었다는 것이다. 따라서 아래와 같이 빈 따옴표를 입력하면 		pages/뒤에 아무 경로 없이 pages/로 들어왔을때 출력할 화면을 지정할 수 있다.
        path('',views.index)
    ] 
    ```

    

  - 멀티플 앱을 사용하기 위해선 urls뿐만 아니라 템플릿 파일 또한 추가적인 처리가 필요하다.

    - 장고에서는 내부적으로 모든 템플릿 파일을 하나로 합쳐서 관리한다. 따라서 만약 각기 다른 앱에 동일한 이름의 html파일이 존재할 경우 장고는 `settings.py`의 Installed_APP에서 더 위에 작성된 어플의 html파일을 적용한다. 따라서 아래의 경우  B어플 내에 작성된 views에서 `hello.html` 파일을 렌더링하라고 명령을 내려도 먼저 등록된 A어플에 있는 동명의  `hello.html` 파일을 렌더링해 의도했던 Hi!가 아닌 안녕!이 출력된다.

      ```html
      <!--A어플의 templates폴더 내에 있는 hello.html파일-->
      <h1>안녕!</h1>
      ```

      ```html
      <!--B어플의 templates폴더 내에 있는 hello.html파일-->
      <h1>Hi!</h1>
      ```

      ```python
      # settings.py파일
      INSTALLED_APPS = [
          'django.contrib.admin',
          'django.contrib.auth',
          'django.contrib.contenttypes',
          'django.contrib.sessions',
          'django.contrib.messages',
          'A',  #A가 먼저 등록되었다.
          'B',  
      ]
      ```

    - 이를 막기 위한 방법은 우선 각 APP에 있는  `templates`폴더에 하위 폴더를 하나씩 생성하고(앱의 이름과 동일하게 한다), 그 폴더 내에 html파일들을 넣는 것이다. 그 후`views.py`를 아래와  같이수정한다.

      ```python
      #B어플의 views.py파일
      
      #원래 아래와 같았던 것을
          def hello(request):
              return render(request, 'hello.html')
      
      #아래와 같이 경로를 명시해준다(templates폴더의 하위에 B라는 폴더를 생성하여 그곳에 html을 넣었다고 가정).
      def hello(request):
          return render(request, 'B/hello.html')
      ```
      
      ```python
      #A어플의 views.py파일
      #A어플도 마찬가지로 바꿔준다(templates폴더의 하위에 A라는 폴더를 생성하고 그곳에 html을 넣었다고 가정).
      
      def hello(request):
          return render(request, 'A/hello.html')
      ```
  
  
  ​    

  - 또한 템플릿 확장을 사용한 경우 base.html 파일이 모든 프로젝트에서 사용 가능하게 바꿀 수 있다.

    - 만일 A어플 내의 base.html을 A어플의 다른 html파일들에 사용했을 경우 B어플에서도 base.html을 사용하고자 한다면 base.html을 project폴더에 `templates`폴더를 만든 후 그 안에 넣으면 된다.

    - 또한 settings.py에서 `TEMPLATES`설정을 바꿔줘야 한다.

    - `DIRS`에는 어떤 순서로 파일을 찾을 것인지를 입력하는 것이다. 아래에서는 root폴더(프로젝트 폴더)만 입력했으므로 당연히 root폴더 내부에 정의한 base.html파일을 가장 먼저 찾게 된다.
  
      ```python
      TEMPLATES = [
          {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
              #본래 비어 있던 아래 []사이에 다음과 같이 입력해준다.
              #BASE_DIR은 manage.py가 존재하는 프로젝트 최상위 폴더를 의미하는데 (BASE_DIR, 		 '프로젝트명','templates')는 최상위 폴더부터 temlpates폴더까지의 경로를 ,로 구분		해서 입력한 것이다.
              #app내에 있는 폴더가 아닌, 추가적으로 templates로 활용하고 싶은 경로를 입력한다.
              #아래와 같은 설정은 settings.py내에 DATABASES에서도 찾을 수 있다.
              'DIRS': [os.path.join(BASE_DIR, '상위폴더','templates')],
              'APP_DIRS': True,  
              'OPTIONS': {
                  'context_processors': [
                      'django.template.context_processors.debug',
                      'django.template.context_processors.request',
                      'django.contrib.auth.context_processors.auth',
                      'django.contrib.messages.context_processors.messages',
                  ],
              },
          },
      ]
      #만일 templates폴더가 특정 앱이나 프로젝트 관리 폴더의 하위폴더 가 아닐 경우 '상위폴더'는 지우고 'templates'만 쓰면 된다.
      ```







# form태그와 input태그

- 각 태그의 특징

```html
<!--form과 input태그에서 가장 중요한 것은 각기 action과 name이다. action은 input에서 입력 받은 내용을 어디로 보낼지에 관한 것이고 name은 입력 받은 내용을 어떤 변수에 담아서 보낼지에 관한 것이다. 아래의 경우 입력받은 내용을 content와 title에 담아 content와 title을 /pages/complete/라는 경로에 보내겠다는 의미다. -->


<!--name을 지정하지 않으면 url에 표시되지 않는다.-->

<!--action태그를 비워 두면 해당 html파일을 호출한 함수로 데이터가 전달된다.-->
<!--또한 action에 주소를 쓸 때 반드시 /를 붙여 줘야 한다. GET으로 보낼 때는 상관 없지만 POST일 경우 오류가 발생한다. 즉 "/pages/complete"와 같이 쓰면 안된다.-->
<form action="/pages/complete/">
	<input type="text" name="content">
    <input type="text" name="title">
</form>
<!--content와 title은 경로상에서 ?뒤에 표시되며 이를 쿼리문이라 한다.-->
<!--만일 content에 1234를, title에 5678을 입력한 경우-->
<!--~/pages/complete/?content=1234&title=5678-->
```

- 장고에서의 활용

```python
#views.py파일
#위에서 받아온 입력값은 request에 담기게 된다. 즉 request는 요청받은 내용과 관련된 정보들이 담긴 객체이다.
  
def complete(request):
    print(request.GET) #어떤 정보가 담겨있는지
    print(request.path) #어떤 경로로 요청이 들어왔는지
    return render(request, 'complete.html')
  
out
QueryDict{'content':1234,'title':5678}
/pages/complete/
  
  
#위에서 본것과 같이 request.GET은 QueryDict라는 이름의 딕셔너리이다. 이 딕셔너리로 넘어온 정보를 활용하는 방법은 키를 입력하면 값을 돌려주는 .get()함수를 사용하는 것이다.
  def complete(request):
  	title = request.GET.get('title')    #'title'의 value인 5678이 title에 담기고
    content=request.GET.get('content')  #'content'의 value인 1234가 content에 담긴다.
    context = {
        'title':title,
        'content':content
    }
    return render(request, 'complete.html',context)
```




  - 위와 같은 처리를 위해서는 url은 2개를 만들어야 한다.

    - form과 input을 입력하기 위한 url
    - 입력받은 정보를 처리하기 위한 url




- 하나의 url에 위의 두 기능을 하는 함수를 작성하여 사용하는 경우가 있는데 이는 좋지 않은 방법이다.

  - 따라서 반드시 2개의 url을 작성해야 한다.

  - 예시

    ```python
    #urls.py
    
    urlpatterns = [
        path('new'/, views.new),   #입력 하기 위한 url
        path('complete/',views.complete)  #입력받은 정보를 처리하기 위한 url
    ] 
    ```

    ```python
    #views.py
    
    #입력하기 위한 함수
    def new(request):
        return render(request, 'new.html')
    def complete(request):
        ABC = request.GET.get('abc')
        context={
            'qwe'=ABC
        }
      return render(request, 'complete.html', context)
    ```

    ```html
    <!--new.html-->
    <form action="/어플명/complete/">
    	<input type="text" name="abc">
    </form>
    ```

    ```html
    <!--xxx를 입력받았다고 가정-->
    <!--complete.html-->
    {{ qwe }}
    <!--페이지에 xxx가 출력된다.-->
    ```

  - 정리


  ⓐnew/경로로 접근한다.

  ⓑurls.py는 접근을 감지하고 views의 new함수를 실행시킨다.

  ⓒnew 함수가 실행되면  new.html을 렌더링 해 화면에 출력한다.

  ⓓ값을 입력받는다.

  ⓔ입력 값은 complete/경로로 넘겨진다.

  ⓕurls.py는 접근을 감지하고 views의  complete함수를 실행시킨다.

  ⓖcomplete함수 complete.html을 렌더링 해 화면에 출력한다.




- 수정을 하고자 할 때 form태그와 input 태그

  ```html
  <form action="수정하는 함수를 실행시키는 경로">
  	<input type="text" name="abc" value={{article.title}}>
  </form>
  
  <!--위와 같이 value에 받아온 정보를 DTL로 입력하면 입력창에 article.title이 담기게 된다.-->
  ```

  





# Model

- Model은 데이터를 관리하는 작업을 한다(데이터 베이스를 모델링).



- database를 쓰는 이유
  - 여러 사람이 접근해서 작성하는 데이터의 경우 파일로 저장하면 불편할 수 있다.



- 스키마란
  - 다양한 사람이 작성할 수 있는 데이터 베이스의 특성상 동일한 정보도 다르게 작성할 수 있다. 따라서 동일한 정보는 동일하게 저장하도록 틀을 만들어 놓아야 하는데 이를 스키마라 부른다.
  - 예를 들어 나이를 입력하라고 했을 때 동일한 20살의 나이를 누군가는 20, 누군가는 20살, 누군가는 스무살로 각기 다르게 입력할 수 있다. 따라서 IntField라는 스키마(틀)을 줘서 이에 맞게 입력하도록 한다.



- 데이터
  - 데이터를 엑셀 파일에 비유했을 때 하나의 테이블은 하나의 sheet가 된다.
  - 열(column)은 속성을 담고 있다. 속성이라고도 부른다. 스키마가 만든 틀이 바로 열이다. 필드(field)는 데이터베이스의 테이블에서 열(column)을 의미한다.
  - 행(row)은 각 속성의 구체적인 정보를 담고 있다. 레코드라고도 부른다.
  - PK(Primary Key): 주민등록번호, 군번, 학번과 같이 식별을 위해 지정된 고유한 값 , id값의 column의 이름을 pk라 부른다.
  - 장고에서는 객체를 저장할 때 마다 PK값을 하나씩 증가시키면서  PK값을 부여한다.



- 데이터 베이스를 조작하는 언어
  - SQL(Structured Query Language)
  - ORM(Object Relational mapper)
    - object와 database를 맵핑 시킨 것. 파이썬의 객체로 관계(DB)를 조작한다고 보면 된다.
    - DB에 저장된 값을 객체로 넘겨준다. 예를 들어 Article이라는 모델을 정의 하고, 모델 내부에 title, content 가 정의되어 있다고 할 때, Article의 각 객체에 title,contet라는 데이터 베이스에 저장된 값을 담아서 넘겨준다.
    - 객체 조작은 메서드를 호출함으로써 가능하다.



- ORM

  - 기본적인 데이터베이스 조작을 CRUD(Create, Read, Update, Delete)operation 이라고 한다.

    - 게시판의 글을 생각해보면 보다 쉽게 이해할 수 있다.

  - 생성 - ex. 게시글 작성

    ```python
    #방법1
    article = Article()      #Article()이라는 클래스로 article이라는 객체를 만들고
    article.title = '제목'    #article 객체의 title을 '제목'으로,
    article.content = '내용'  #article 객체의 content을 '내용'으로 설정한다.
    article.save()           #반드시 세이브를 해줘야 한다.
                             #models.DateTimeField(auto_now_add=True) 속성의 경우에는 위의 과정을 거치지 않아도 자동으로 생성되므로 바로 쓰면 된다.
    #방법2
    article = Article(title='제목', content='내용')
    article.save()
    
    #방법3
    Article.objects.create(title='제목',content='내용')
    ```

  

- 조회- ex. 게시글 읽기

  - 전체 데이터 조회

  ```python
  Article.objects.all()
  >> <QuerySet [<Article: Article object (1)>]>
  
  #아래의 코드는 지금까지 생성된 Article의 모든 객체를 QuerySet 형태로 article에 담는 것이다.
  article=Article.object.all()
  
  #Article.objects.order_by('-id').all()와 같이 쓰면 역순으로 조회한다.
  ```
  
  - 단일 데이터 조회(고유한 값인 id를 통해 가능)
  ```python
  #방법1
  Article.objects.get(id=1)
  
  #방법2
  Article.objects.all()[0]  #[]안에 음수는 올 수 없다.
  
  #방법3
  Article.objects.all().first()  #첫번째 데이터 조회
  <Article: Article object (1)>
  Article.objects.all().last()   #마지막 데이터 조회
  ```
  
  
  
- 수정- ex. 게시글 수정

  ```python
  a1 = Article.objects.get(id=1)  #수정할 대상을 정하고
  a1.title = '제목 수정'       #수정후
  a1.save()                  #저장
  ```

  

- 삭제- ex. 게시글 삭제

  ```python
  a1 = Article.objects.get(id=1)
  a1.delete()
  >> (1, {'articles.Article': 1})
  ```



- Admin 페이지 활용

1. 관리자 계정 생성

```bash
$ python manage.py createsuperuser
사용자 이름 (leave blank to use 'ubuntu'): admin
이메일 주소:
Password:
Password (again):
Superuser created successfully.
```

2. admin 등록

> admin 페이지를 활용하기 위해서는 app 별로 있는 admin.py에 정의 되어야 한다.

```python
# django_crud/articles/admin.py
from django.contrib import admin
#Article 자리에는 class이름을 쓰면 된다.
from .models import Article
# Register your models here.


admin.site.register(Article)
```

3. 확인

> `/admin/` url로 접속하여, 관리자 계정으로 로그인

4. admin 페이지에 display 설정을 하는 방법

   ```python
   # django_crud/articles/admin.py
   from django.contrib import admin
   from .models import Article
   
   # Register your models here.
   class ArticleAdmin(admin.ModelAdmin): 
       #넣고 싶은 데이터들을 입력
   	list_display=('title','content','created_at','updated_at')
       #이 외에도 list_display_link, list_display_filter등도 있다.
       #list_display_link=['title'] 은 title에 링크를 설정해준다.
       #list_display_filter=['title']은 title에 필터를 적용해준다.
   
   admin.site.register(Article, ArticleAdmin)
   ```



- Model의 조작

  - `models.py`파일을 통해 클래스를 정의하는데 이것이 DB를 모델링 하는 것이다. 열에 어떤 내용이 올지를 정의하는 것이라고 볼 수 있다.

    ```python
    #models.py파일
    from djangodb import models
    #models.Model는 상속을 위해 써주는 것이다(장고에 있는 models의 Model을 상속).
    class Article(models.Model):
        #title에는 140자 이내의 문자열을 지정하겠다
        title = models.CharField(max_length=140) 
        content = models.TextField() 
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
    #auto_now_add=True는 최초 생성 시간을자동으로 추가해 주는 것이다.
    #auto_now=True는 수정 시간을자동으로 추가해 주는 것이다.
    #CharField에서 max_length는 필수 옵션이다.
    #일반적으로 input에는 CharField를 쓰고 textarea에는 TextField를 쓴다.
    #title, contemt, created_at, updated_at 등은 Article이라는 클래스의 속성이다.
    ```

    

  - 위와 같이 클래스를 정의한 후 터미널에 아래와 같이 입력하면 `migration`폴더가 생성된다. 이는 내가 클래스 정의를 통해 모델링한 DB를 반영할 준비를 하는 것이다.  폴더 내의 파일은 모델의 변경 사항을 기록하며 `migration`폴더는 앱별로 하나씩 존재한다.

    ```bash
    $ python manage.py makemigrations
    ```

  - 이후 아래의 명령어를 입력하면 최종적으로 모델링한 DB가 반영된다.

    ```bash
    $python manage.py migrate
    ```

  - 만일 모델링을 할 때(클래스를 설정할 때)오타가 난줄 모르고 `makemigrations`, `migrate`를 했다면 오타를 수정한 이후 둘을 다시 해줘야하 한다. 그럼 migration폴더에 새로운 버전이 추가된다.

  - 다른 방법은 `migrations/`폴더 내의 마이그레이션 파일들과 db.sqlite3를 삭제하는 것이다(\_\_init\_\_.py는 삭제 금지). 이 경우 기존에 입력한 데이터가 날아가긴 하지만 입력된 데이터가 얼마 없을 경우 이렇게 하는 편이 깔끔하다.

    - db.sqlite3는 데이터베이스 관련 파일이다.

  - 이후 `models.py`에서 정의한 파일을 `views.py`등 다른 곳에서 사용하고자 한다면 반드시 import를 해줘야 한다.

    ```python
    #views.py
    from 디렉토리 파일명 import 클래스명
    #ex.reviews 앱에서 movies에 정의한 Movie 모델을 쓰고자 할 경우
    #from movies.models import Movie
    
    #동일한 디렉토리에 있을 경우 .을 입력하고 파일명은 model을 정의한 파일명을 입력하는데 보통 models.py와 views.py는 같은 폴더에 있고 model은 일반적으로 models.py에 정의하므로
    from .models import 클래스명
    #위와 같이 쓰면 된다.
    ```



- 게시판에서 게시글을 클릭했을 때 해당 게시글이 보이도록 연결하는 방법

  - 모든 오브젝트들은 id(pk값)를 가지므로 이를 활용하여 어떤 글을 띄울지 설정할 수 있다.

    ```python
    #정보를 받는 review_list.html
    <a href="/community/{{review.pk}}/">글 보러 가기</a>
    #review.pk는 review라는 오브젝트의 id이다. 위 링크를 클릭하면
    #community/pk/주소로 넘어가게 될텐데 urls.py에서 아래와 같이 정의를 하고
    
    
    #urls.py
    urlpatterns = [
        path('/community/<int:a>/',views.review_detail),
    ]
    #a에는 review_list.html에서 넘어온 pk가 담기게 된다. 이후 views로 넘기면
    
    
    
    #아래와 같이 a를 인자로 받아서
    #views.py
    def review_detail(request, a):
        review = Review.objects.get(id=a)  #id가 review_list.html에서 받은 pk와 같은 오브											젝트를 review에 저장하고
        context = {                 #context에 넣어 넘긴다.
            'review':review,
        }
        return render(request,'community/review_detail.html',context)
    
    
    
    #review_detail.html
    {% extends 'base.html' %}
    
    {% block body %}
    	<p>{{review.title}}</p>
        <p>{{review.content}}</p>
    {% endblock %}
    #출력하면 된다.
    ```



- POST와 GET

  - 공통점

    - 요청 메세지이다.
    - HTML/CSS에서는 GET과 POST 요청밖에 보내지 못한다.

  - GET

    - 정보를 가져오는 것(일반적으로 정보를 받아서 읽는 용도로 사용)
    - 특정 리소스의 표시
    - 받아온 정보가 url(쿼리 스트링)로 넘어감(따라서 크기 제한 및 보안 이슈가 있다)
    - GET은 a태그와 form태그 둘 다 사용 가능, 브라우저에서 주소창을 보내는 요청
    - 데이터 베이스가 변화하지 않음

  - POST

    - DB에 어떤 값을 저장하는 것(받아서 추가적인 처리를 더 해줄때 사용)
    - 특정 리소스에 제출(서버의 상태 변화)
    - form태그만 사용 가능하다. 
    - 데이터 베이스가 변화

  - method로 POST를 쓸 경우 보내는 곳에 아래의 코드를 추가해야 한다.  보안상의 이유(사이트간 요청 변조 방지)로 붙이는 것이다.

    ```html
    {% csrf_token %}
    ```

    - 특정 url에 사용자가 의도하지 않은 작동이 일어나도록 설정하여 사용자가 해당 url을 클릭 했을 때 해당 작동이 일어나게 되는 것이 사이트간 요청 변조로, 이를 막아주는 것이 csrftoken이다.
    - 붙이지 않을 경우 403  forbidden 페이지가 뜬다.



- csrftoken 값은 새로고침 할 때마다(요청을 보낼 때 마다) 바뀌며, 이 값을 검증하여 변조된 요청인지 아닌지를 판단하는 방법으로 방어가 가능하다.
  - 쿠키에도 저장되고 이를 통해서도 방어가 가능하다. 
  - 검사를 통해 보면 csrftoken의 타입은 hidden이다.
  - settings.py의 `MIDDLEWARE`에 csrf관련 처리가 되어 있다. 만일 해당 코드를 주석처리 한다면 오류는 발생하지 않지만 보안이 무너지게 되므로 절대 해서는 안된다.



- url에 이름을 지정하는 방법

  ```python
  #views.py
  
  app_name='articles' #앱 이름을 설정해주고
  
  urlpatterns = [
      path('/community/',views.review, name="aaa")
  ]
  
  #이렇게 입력을 하면 community가 아닌 aaa를 입력해야 한다.
  
  
  
  
  #html파일에서 쓸 경우
  "{% url '앱이름:url이름' %}"
  배리어블 라우팅으로 넘겨줄 값이 있는 경우 아래와 같이 쓴다.
  "{% url '앱이름:url이름' 오브젝트이름.pk %}"
  
  #py파일에서 쓸 경우
  '앱이름:url이름', 오브젝트이름.pk
  ```



- get_object_or_404(클래스, 아이디=아이디)

  ```python
  from django.shortcuts import get_object_or_404
  
  def detail(request,pk):
  	article=Article.objects.get(pk=pk)   
      #이 경우 id에 해당하는 페이지가 없으면 500 오류 발생
      #500대는 주로 개발자의 잘못으로 발생하는 오류
  	article=get_object_or_404(Article,pk=pk)
      #이렇게 하면 id에 해당하는 페이지가 없으면 404오류 발생
      #400대는 주로 사용자의 잘못으로 발생하는 오류
  ```

  

- 스타일 가이드

  - 따옴표는 하나로 통일해라.
  - 변수를 할당할 때는 `=` 좌우를 한 칸씩 띄우고 그렇지 않을 때는 붙여써라.
  - `views.py`에서 `import`밑에는 2줄 띄우고 각 함수 사이는 1줄 띄운다.
  - 앱 이름은 반드시 복수형으로 정한다.
  - 앱 이름 외에도 복수인 것들은 복수형으로 정한다.
  - import 작성 순서: python코어-django-직접 만든 파일 순





# HTTP

- HTTP
  - HTML 문서와 같은 리소스들을 가져올 수 있도록 해주는 프로토콜
  - HTTP는 웹에서 이루어지는 모든 데이터 교환의 기초이며, 클라이언트-서버 프로토콜이기도 하다.
  - 클라이언트-서버 프로토콜이란 (보통 웹브라우저인) 수신자 측에 의해 요청이 초기화되는 프로토콜을 의미
  - 보통 브라우저인 클라이언트에 의해 전송되는 메시지를 요청(requests)이라고 부르며, 그에 대해 서버에서 응답으로 전송되는 메시지를 응답(responses)이라고 부른다.



- HTTP 메시지
  - 요청 메세지의 구성
    - method: 클라이언트가 수행하고자 하는 동작을 정의한 `GET`,`POST`같은 동사나 `OPTIONS`나 `HEAD`와 같은 명사
    - path: 가져오려는 리소스의 경로를 뜻하며 프로토콜(http:// 등), 도메인(naver.com 등), 또는 TCP 포트인 요소들을 제거한 리소스의 URL(django에서 앞 부분 다 빼고 urls.py에 작성하는 부분)
    - HTTP 프로토콜의 버전
    - 서버에 대한 추가 정보를 전달하는 선택적 헤더들
  - 응답 메세지의 구성
    - HTTP 프로토콜의 버전
    - 요청 성공 여부와 그 이유를 나타내는 상태코드(아래 HTTP 상태 코드 참조)
    - 상태 코드의 짧은 설명을 나타내는 상태 메시지.
    - 요청 헤더와 비슷한 헤더들
    - 선택 사항으로, 가져온 리소스가 포함되는 본문.



- HTTP메서드

  - 클라이언트가 수행하고자 하는 동작을 정의한 GET, POST 같은 동사나 OPTIONS, HEAD와 같은 명사

  - 종류
    - GET: 특정 리소스의 표시를 요청합니다. `GET`을 사용하는 요청은 오직 데이터를 받기만 한다. 요청받은 URI의 정보를 검색하여 응답
    - HEAD:  `GET` 메서드의 요청과 동일한 응답을 요구하지만, 응답 본문을 포함하지 않는다. GET방식과 동일하지만, 응답에 BODY가 없고 응답코드와 HEAD만 응답
    - POST: 특정 리소스에 엔티티를 제출할 때 쓰입니다. 이는 종종 서버의 상태의 변화나 부작용을 일으킨다. 요청된 자원을 생성(CREATE)
    - PUT: 요청된 자원을 수정(UPDATE)
    - PATCH: 리소스의 부분만을 수정하는 데 쓰인다.  PUT의 경우 자원 전체를 갱신하는 의미지만, PATCH는 해당자원의 일부를 교체하는 의미
    - DELETE: 특정 리소스를 삭제, 요청된 자원을 삭제
    - OPTIONS: 목적 리소스의 통신을 설정, 웹서버에서 지원되는 메소드의 종류를 확인
    - GET, POST, PUT, DELETE 정도가 자주 쓰인다.



- url

  - 도메인: path가 시작되기 전까지

    ```
    www.example.com
    ```

  - port(:뒤에 표시)

    - HTTP는 80, HTTPS는 443의 값을 가지며 일반적으로는 생략한다. 만일 특정한 포트를 임의로 설정하고 싶다고 한다면 쓸 수 있다.

    ```
    www.example.com:4040
    
    4040은 포트번호다.
    ```

  - path(/뒤에 표시)

    ```
    www.example.com/articles/create/
    
    실습하면서 일반적으로 사용하는 /뒤에 오는 것들
    ```

  - parameter(?뒤에 표시)

    ```
    www.example.com/detail?name1=abc&name2=cba
    
    ?name1=abc&name2=cba부분이 parameter로 키=값의 형태를 가지며, 여러개를 동시에 쓸 때에는 &로구분한다.
    ```

  - anchor(#뒤에 표시)

    ```
    www.example.com/detail#content3
    
    #content3부분이 anchor로 한 문서 내부에서 이동할 때 사용한다.
    detail페이지의 content3으로 이동한다는 뜻이다.
    ```




- HTTP 상태 코드
  - 200 OK: 성공
  - 300대는 redirect
    - 301 Moved Permanently
    - 302 Found
  - 400대는 클라이언트 이슈
    - 400 Bad Request(잘못된 문법으로 인하여 서버가 요청을 이해할 수 없음)
    - 401 Unauthorized(로그인이 필요함에도 로그인 하지 않은 경우)
    - 403 forbidden(권한이 없는 경우, {csrf_token}을 안써도 이 이슈가 발생), 클라이언트는 콘텐츠에 접근할 권리를 가지고 있지 않음
    - 404 Not Foubd(해당 URL이 없는 경우): 요청받은 리소스를 찾을 수 없음
    - 405 Method Not Allowed(GET으로 처리하는데 POST로 보낸 경우)
  - 500 Internal Server Error: 서버 오류, 서버가 처리 방법을 모르는 상황과 마주침



# 정적 파일 관리

- static: 정적 파일, CSS, JS, image 등의 파일을을 static파일이라 부른다.

- html파일이 위치한 templates폴더에서 관리하지 않고 아래와 같은 방법으로 관리, 사용한다.

- 정적 파일 관리 방법

  - static 폴더를 생성하고 그 하위 폴더로 app이름과 동일한 폴더를 생성한 뒤 그 안에 css,js파일을 넣는다. 일반적으로 css파일과 js파일을 각기 폴더를 만들어서 관리한다. 굳이 하위폴더를 만드는 이유는 templates 폴더 아래에 앱 이름과 같은 폴더를 하나 만들고 그 안에 html파일들을 관리하는 것과 같은 이유다.

    - static폴더는 templates폴더와 같이 이름을 변경해선 안된다.
    - 주의할 점은 만일 static폴더를 만들기 전에 서버를 켜놨다면 static폴더를 만들고 적용 한 후에 서버를 껐다 켜야 static폴더를 불러와 적용이 된다.

  - static 파일을 적용할 html 파일에 DTL(장고 템플릿 랭귀지)로 아래와 같이 작성

    ```html
    <!--아래와 같이 static파일을 불러온다는 것을 알려준다. 이 코드를 써야 아래의 href안에 들어가는 내용, "{% static 'static파일이 있는 위치/static파일' %}"을 쓸 수 있다.-->
    {% load static%}
    
    <!--static폴더의 하위 폴더부터 static파일까지의 경로를 적으면 된다-->
    <link rel="stylesheet" href="{% static 'static파일이 있는 위치/static파일' %}">
    
    <!--accounts/static/accounts/css 폴더 형식이 이와 같고 파일 명이 index.css면-->
    <link rel="stylesheet" href="{% static 'accounts/css/index.css' %}">
    
    <!--주의할 점은 템플릿 확장을 할 경우 {% load static%}은 항상 extends보다 아래에 있어야 한다는 점이다-->
    ```

  - `base.html`파일처럼 static 파일을 모든 앱으로 확장시켜 사용하고 싶을 경우 프로젝트 폴더 하부 폴더로 static 폴더를 생성하고 그 하부 폴더로 적당한 이름의 폴더를 생성한 후 그 안에 static파일을 넣으면 되며, 이 경우 base.html 작성이 담긴 templates 폴더를 사용하는 것과 마찬가지로 `settings.py`에서 아래 코드를 추가해야 한다.

    ```python
    #settings.py
    
    # serving 되는 URL 앞에 붙음.
    STATIC_URL = '/static/'
    # app 디렉토리가 아닌 static 폴더 지정시 아래 코드를 추가
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
    ]
    ```

  - base.html에서 사용할 때도 ` settings.py`를 수정하는 것만 제외하면 위와 동일하게 사용하면 되며, 만일 base.html에 적용한 static파일을 다른 html파일에서도 쓰고 싶다면 아래와 같이 쓰면 된다.

    ```html
    <!--base.html-->
    {% load static %}
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Document</title>
        <link rel="stylesheet" href="{% static 'articles/stylesheets/style.css' %}">
        <link rel="stylesheet" href="{% static 'bootstrap/bootstrap.min.css' %}">
        <!--이처럼 block css를 쓴다. 만일 다른 html파일에 추가적으로 적용하고 싶은 css, js 파일이 		없다면 쓰지 않아도 된다.-->
        {% block css %}
        {% endblock %}
    </head>
    <body>
        <div class="container">
            {% block body %}
            {% endblock %}
        <a href="{% url 'articles:index' %}">게시글 목록 보기</a>
        </div>
        <script src="{% static 'bootstrap/bootstrap.min.js' %}"></script>
    </body>
    </html>
    ```

    ```html
    <!--other.html-->
        
    <!--base.html에 적용한 css파일은 {% extends 'base.html' %} 만으로도 적용 된다. 즉, 굳이 {% load static %}, {% block css %}, {% endblock %}을 쓸 필요가 없다.-->
        
    <!--그러나 other.html 파일에 base.html에 적용되지 않은 static파일을 쓰고 싶다면 아래와 같이 block사이에 작성하면 된다.-->
    {% load static %}<!--href="{% static 경로/파일' %}"을 쓰기 위해 static을 불러 오고-->
        
    {% block css %}
    <link rel="stylesheet" href="{% static 경로/파일' %}">
    {% endblock %}
    ```





# form

- form.py

  - form에서는 label이 자동으로 들어가며, name은 정의한 대로(혹은 models에서 가져왔다면 models에 정의한 대로)들어가게 된다.

  ```python
  #models.py
  class Article(models.Model):
      title = models.CharField(max_length=100)
      content = models.TextField()
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
  ```

  ```python
  from django import forms
  from .models import Article
  
  #클래스명은 아무거나 해도 무관하지만 관례상 앱이름Form으로 한다.
  class ArticleForm(forms.ModelForm):  #상속을 받고
      class Meta:  
      #어떤 모델에서 어떤 datafield를 가져 올지를 정의하는 부분
      
      #M은 반드시 대문자로 쓸 것, 메타데이터를 가져오는 클래스이다. 메타데이터는 	데이터에 대한 데이터로
      
      #사진을 찍을 때 사진이라는 데이터에는 찍은 날짜, 장소 등도 저장되는데 이 		날짜, 장소등이 메타데이터 할 수 있다. class도 마찬가지로 class라는 데이	   터의 메타데이터를(아래의 경우 title, content 등)가져오는 것이다.
      
     #fields에 자료를 넣을 때 반드시 리스트에 넣어야 하는 것은 아니며 튜플에 넣	 는 것도 가능하다.
      	model = Article
          fields = '__all__'
          #fields = ['title','content','created_at','updated_at'] 과 			동일
          #'__all__'을 쓰고 특정한 것을 제외하고 싶다면 
          #exclude = ['title']과 같이 쓰면 된다.
          
  #만일 특정한 필드를 제외하고 전부 다 포함시키고 싶다면 아래와 같이 쓰면 된다.
  class ArticleForm(forms.ModelForm):  #상속을 받고
      class Meta:
      	model = Article
          exclude = ['title']
          #이렇게 하면 fields를 정의하지 않아도 title을 제외한 모든 Article의 fields가 넘어간다.
          
  #위의 코드는 아래의 코드와 동일하다. 그러나 아래와 같이 쓰면 위의 models.py에 이미 쓴 내용을 다시 반복해서 써야 한다. 따라서, 위의 코드처럼 models.py에서 상속을 받아서 쓰는 방식이 주로 쓰인다. 
  #또한 form을 정의할 때 CharField에서는 max_length는 필수가 아니다.
  class ArticleForm(forms.Form):
      titlt = forms.CharField(max_length=100)
      content = forms.CharField()
      
      
  #만일 클래스를 지정하고 싶다면 아래와 같이 하면 된다. 또한 아래와 같이 별도로 클래스를 지정해준 것들은 fileds에 넣을 수 없다. 왜냐하면 fileds에는 기본적으로 model에 지정한 model에 있는 필드들만 넣을 수 있기 때문이다.
  from django import forms
  from .models import Review
  
  class ArticleForm(forms.ModelForm):
      title = forms.CharField(
                  max_length=100,
                  label='글 제목',
                  help_text='글 제목은 100자이내로 작성하세요.',
                  widget=forms.TextInput(
                          attrs={
                              'class': 'my-input',
                              'placeholder': '제목 입력'
                          }
                      )
              )
      content = forms.CharField(
                  label='내용',
                  help_text='자유롭게 작성해주세요.',
                  widget=forms.Textarea(
                          attrs={
                              'row': 5,
                              'col': 50,
                          }
                      )
              )
  
      class Meta:
          model=Article
          fields = '__all__'
  ```

  ```python
  #views.py
  from .forms import ArticleForm #생성한 클래스를 가져오고 
  
  def create(request):
      if request.method=="POST":   #요청이 POST로 들어오면 보낸 데이터를 저장
          #form은 ArticleForm의 객체
          form = ArticleForm(request.POST) #request.POST에는 form에서 입력받은 딕셔너리 형태		의 데이터가 저장되어 있다 ex.{'title:제목1', 'content':'내용1'}
          #아래 코드와 동일한 코드다.
              #article = Article()
              #article.title = request.POST.get('title')
              #article.content = request.POST.get('content')
          if form.is_valid():  #사용자가 보낸 요청이 올바른지 검사
              article = form.save  #form을 저장하여 article에 담겠다.
              #article.save()
              
              return redirect('articles:detail', article.id)
  
    else: #request.method=="GET"
          form = ArticleForm()  #form.py에서 생성한 클래스를 변수에 담고
  
      context = {     #context로 넘겨준다.
          'form':form
      }
      return render(request, 'articles/create.html', context)
  ```

  ```html
  create.html
  {% extends 'base.html' %}
  
  {% block body%}
  <h2>NEW</h2>
  <!--아래와 같이 action을 공백으로 두면 같은 url로 요청을 보낸다. 만일 /create/가 아닌 다른 url로 보내고자 한다면 입력을 해주어야 한다.-->
  <form action="" method="POST">
      {% csrf_token %}
      {{ form }}   <!--받아온 form을 넣어주면 된다.-->
      <input type="submit" value="submit">
  </form>
  {% endblock %}
  
  <!--{{ form }}외에도 {{ form.as_p }}, {{ form.as_table }} 등으로 쓸 수 있는데 각기 <p>태그에 넣어서 표현하겠다, <table>태그에 넣어서 표현하겠다는 뜻이 된다.-->
  ```

- 상속을 활용한 form정의

  ```python
  #models.py
  class Article(models.Model):
      title = models.CharField(max_length=20)
      content = models.TextField()
      
  
  #forms.py
  from django import forms
  from .models import Article, Comment
  
  class ArticleForm(forms.ModelForm):
      class Meta:
          model = Article
          fields = ['title','content']
  
  class ArticleSpecialForm(ArticleForm):  #위에서 정의한 ArticleForm을 상속받아서
      book = forms.CharField(max_length=20)
  
      class Meta(ArticleForm.Meta): #ArticleForm의 Meta데이터도 상속받고
          fields = ArticleForm.Meta.fields+['book']
          #ArticleForm.Meta.fields는 ArticleForm 안의 Meta 안의 fields라는 뜻이다. 위 코드에서		  는 ['title','content']가 담겨있게 된다.
          #exclude를 설정했을 경우 ArticleForm.Meta.exclude에는 exclude에 담은 리스트가 담겨있		  게 된다.
          #추가 할 필드를 list에 넣어서 +연산으로 추가해준다.
    
  #주의점
  #만일 추가할 필드가 모델에 정의되어 있지 않다면 form으로 해당 정보를 입력받더라도 데이터 테이블에는 해당 정보를 저장할 수 없다. 예를 들어 위의 경우 Article모델에는 book이라는 필드가 존재하지 않으므로 데이터 테이블에는 book이라는 필드가 저장될 공간이 없다. 따라서 form에 따라 book을 입력하더라도 저장되지 않는다.
  
  #만일 상속 할 Form에서 fields를 리스트가 아닌 '__all__'로 했다면 위와 같이 넘길 수 없다(문자열과 리스트는 +연산이 불가능하다). 사실 넘길 필요가 없다. 이미 필드를 전부 넘겼는데 추가적으로 넘길 필드가 없기 때문이다.
  ```

  

- `require_POST`

  ```python
  from django.views.decorators.http import require_POST
  #이걸 쓰지 않으면 GET으로 delete 요청을 해도 delete가 된다.
  @require_POST
  def delete(request)
  ```



- form태그 내부의 botton태그는 input태그의 submit과 동일한 역할을 수행한다. 



- CRUD구현

  ```python
  from django.shortcuts import render, redirect, get_object_or_404
  from django.views.decorators.http import require_POST
  
  from .models import Article
  from .forms import ArticleForm
  
  # Create your views here.
  def index(request):
      articles = Article.objects.order_by('-pk')
      context = {
          'articles': articles
      }
      return render(request, 'articles/index.html', context)
  
  def create(request):
      if request.method == 'POST':
          form = ArticleForm(request.POST)
          if form.is_valid():
              article = form.save()
              return redirect('articles:index')
      else:
          form = ArticleForm()
      context = {
          'form': form
      }
      return render(request, 'articles/form.html', context)
  
  #detail은 정보의 생성, 수정 등이 일어나지 않고 조회만 하기에 GET으로 받는다.
  def detail(request, pk):  #R
      article = get_object_or_404(Article, pk=pk)
      context = {
          'article': article
      }
      return render(request, 'articles/detail.html', context)
  
  @require_POST
  def delete(request, pk):  #D
      article = get_object_or_404(Article, pk=pk)
      article.delete()
      return redirect('articles:index')
  
  def update(request, pk): #U
      # 수정시에는 해당 article 인스턴스를 넘겨줘야한다. article을 객체로 만들고
      article = get_object_or_404(Article, pk=pk)
      if request.method == 'POST':
          #instance=article을 통해 무엇을 수정할지를 지정
          #ArticleForm에서 수정할 인스턴스는 article이라는 객체라는 것을 알려준다.
          #만일 instance=article를 넣지 않는다면 계속 새로운 글이 생성된다.
          form = ArticleForm(request.POST, instance=article) 
          if form.is_valid():
              article = form.save()
              return redirect('articles:detail', article.pk)
      else:
          form = ArticleForm(instance=article)
      context = {
          'form': form
      }
      return render(request, 'articles/form.html', context)
  ```

  

- resolver_match

  ```html
  <!--
  한 html파일을 2개의 경로가 사용할 경우 아래와 같이 입력하면 어떤 url로 들어왔을 때 어떤 것을 보여줄지 정할 수 있다.
  분기의 기준은 url_name이다.
  path로 하면, url이 바뀔 때마다 바꿔줘야한다.
  -->
  {% if request.resolver_match.url_name == 'create' %}
  	<h2>새 글쓰기</h2>
  {% else %}
  	<h2>수정하기</h2>
  {% endif %}
  
  <!--form이라는 한 html파일을 2개의 url이 가리킬 경우 어떤 url이 가리키는가에 따라 위처럼 다른 내용을 보여줄 수 있다.-->
  ```

  

- forms.py에서 넘긴 form을 html에서 스타일링 하는 방법

  ```html
  <!--아래 코드 전체를 본래 {{form}}이 들어가던 곳에 넣으면 된다.-->
  {% for field in form %}
      <div class="fieldWrapper">
          {{ field.errors }} <!--error메세지-->
          {{ field.label_tag }}<!--label--> {{ field }}<!--내용-->
          {% if field.help_text %}<!--help text-->
          <p class="help">{{ field.help_text|safe }}</p>
          {% endif %}
      </div>
  {% endfor %}
  
  <!--위 처럼 for문을 사용하여 꾸밀 수 있으며 각각의 내용에 태그를 설정하여 꾸밀 수 있다.-->
  
  
  <form action="" method="POST">
          {% csrf_token %}
          {% form %}
          <button class="btn btn-primary">제출</button>
  </form>
  <!--아니면 그냥 위 처럼 입력하고 해당 정보가 표시되는 창에서 디버깅창(F12)에 보면 각 정보별 태그가 나와있는데, 그 태그를 보고 적용해도 된다.-->
  
  
  {% load bootstrap4 %}
  <form action="" method="POST">
  	{% csrf_token %}
  	{% bootstrap_form form %}
  	<button class="btn btn-primary">제출</button>
  </form>
  <!--아니면 그냥 위 처럼 bootstrap적용도 가능하다. 단, bootstrap을 활용하려면 settings.py도 바꿔야 하고 load도 해줘야 하기에 과정이 복잡하다.
  https://django-bootstrap4.readthedocs.io/en/latest/index.html에 가면 관련 정보가 있다.
  
  <!--주의! {% bootstrap_form form %}은 반드시 form태그 안에 써야 한다. 밖에 쓸 경우 form양식에 맞게 제출 해도 실제 form태그 내에서는 입력된 것이 없기에 빈 것이 제출되었다고 인식한다.-->
  
  
  적용 방법
  0.$ pip install django-bootstrap4를 입력해 설치
  1.settings.py에서 installed_app에 bootstrap4를 추가
  2.쓰려는 html파일 상단에 {% load bootstrap4 %}를 입력
  3.base.html 상단에도 {% load bootstrap4 %}를 입력하고 {% bootstrap_css %}와 {% bootstrap_javascript jquery='full' %}를 각기 css,js관련 정보를 입력하던 곳에 입력-->
  ```

  

- message

  - message를 별 다른 선언 없이 사용 가능한 이유는 이미 django내부의 `settings`에 선언이 되어 있기 때문이다(`MIDDLEWARE`, `TEMPLATES` 부분에 있다, request도 역시 마찬가지 이유로 선언 없이 사용 가능).

  - 상세한 내용은 django 공식문서에서 찾아볼 수 있다.

    > https://docs.djangoproject.com/en/3.0/ref/contrib/messages/

  - 상기한 문서에 있는 코드들 중 하나를 선택해 `views.py`의 상단에 `message`를 import 한 후 원하는 곳에 입력하면 된다.

    ```python
    from django.contrib import messages
    #아래와 같이 직접 지정해서 쓸 수도 있고
    messages.add_message(request, messages.INFO, 'Hello world.')
    
    #아래와 같이 django에서 지정한 shortcut을 사용할 수도 있다. 
    messages.debug(request, '%s SQL statements were executed.' % count)
    messages.info(request, 'Three credits remain in your account.')
    messages.success(request, 'Profile details updated.')
    messages.warning(request, 'Your account expires in three days.')
    messages.error(request, 'Document deleted.')
    
    #e.g.
    @login_required
    def update(request, pk):
        # 수정시에는 해당 article 인스턴스를 넘겨줘야한다!
        article = get_object_or_404(Article, pk=pk)
        if request.user == article.user:
            pass
        else:
            messages.warning(request, '본인 글만 수정 가능합니다.')
            return redirect('articles:index')
    
    #messages.error(request, 'Document deleted.')를 예로 들면 error는 메세지의 색을, 'Document deleted.'는 띄울 문구를 뜻하며 자유롭게 수정이 가능하다. 단, 뒤에서 살펴볼 사용자 관리에서 사용자 관리 관련 form들을 불러와 사용한 경우에는 messages.error(request, '')와 같이 비워둬도 form에 미리 저장되어 있는 메세지가 출력되며, 문자열 안에 내용을 입력해도 미리 저장되어 있는 메세지가 출력된다.
    ```

  - html 파일에 띄우려면 아래와 같이 입력하면 된다.

    - 주로 base.html파일에 작성하게 되는데 그 이유는 메세지가 어디서 사용될지 모르기에 base.html에 작성하여 어떤 html파일에서도 뜨게 하기 위함이다.

    ```html
    <!--아래와 같이 해도 bootstrap처럼 색이 뜨지는 않는다.-->
    {% if messages %}
    <ul class="messages">
      {% for message in messages %}
      <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>
          {% if message.level == DEFAULT_MESSAGE_LEVELS.ERROR %}Important: {% endif %}
          {{ message }}
      </li>
      {% endfor %}
    </ul>
    {% endif %}
    
    
    <!--bootstrap으로 스타일링 하는 방법-->
    <!DOCTYPE html>
    {% load bootstrap4 %} <!--bootstrap불러 오고-->
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Practice</title>
        {% bootstrap_css %}
    </head>
    <body>
    {% if messages %}
    <ul class="messages">
      {% for message in messages %}    <!--아래의 tags부분을 쪼개면 된다.-->
      <li{% if message.tags %} class="alert alert-{{ message.tags }}"{% endif %}>
          {% if message.level == DEFAULT_MESSAGE_LEVELS.ERROR %}Important: {% endif %}
          {{ message }}
      </li>
      {% endfor %}
    </ul>
    {% endif %}
    </body>
    </html>
    
    <!--위와 같이 하면 메세지가 list(li)태그에 들어 있어 .도 함께 출력이 되는데, 보기 싫다면 div태그로 바꿔주면 된다.-->
    ```

    

- HTTP 상태 코드 출력하기

  >https://docs.djangoproject.com/en/3.0/ref/request-response/#httpresponse-subclasses

  - 위 링크에 정의된 다양한 클래스중 하나를 import해서 사용한다.

  ```python
  #원하는 것을 import하고
  from django.http import HttpResponseForbidden
  
  #render, redirect 대신 아래와 같이 쓴다.
  return HttpResponseForbidden()
  
  #e.g.
  @login_required
  def update(request, pk):
      # 수정시에는 해당 article 인스턴스를 넘겨줘야한다!
      article = get_object_or_404(Article, pk=pk)
      if request.user == article.user:
          pass
      else:
          return HttpResponseForbidden()
  ```

  - 좀 더 범용성 있는 사용을 위해서는 아래와 같이 쓸 수도 있다.

  ```python
  #HttpResponse를 import하고
  from django.http import HttpResponse
  
  @login_required
  def update(request, pk):
      # 수정시에는 해당 article 인스턴스를 넘겨줘야한다!
      article = get_object_or_404(Article, pk=pk)
      if request.user == article.user:
          pass
      else:
  		return HttpResponse(status=401) #status 코드를 직접 지정 가능
  ```

  

- `include` 

  - html파일이 지나치게 길어질 경우 html파일을 분할해서 작성하는 것이 가능하다.
  - `{% include '파일명' %}`
  - extends와의 차이는 extends는 각각의 블록에 넣는 것이고, include는 코드를 불러오는 것이다.

  ```html
  <!--base.html파일에 navbar를 만들고 싶은데 코드가 너무 길어질 것 같으면 아래와 같이 {% include '_nav.html' %}를 써서 navbar를 작성한 파일을 불러온다.-->
  <!DOCTYPE html>
  <html lang="ko">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta http-equiv="X-UA-Compatible" content="ie=edge">
      <title>Django Live Session</title>
      {% bootstrap_css %}
  </head>
  <body>
      {% include '_nav.html' %}
      {% block body %}
      {% endblock %}
  </body>
  </html>
  ```

  ```html
  <!--_nav.html-->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <a class="navbar-brand" href="/articles/">HOME</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ml-auto">
          <li class="nav-item">
              <a class="nav-link" href="{% url 'accounts:logout' %}">로그아웃</a>
          </li>
          <li class="nav-item">
              <a class="nav-link" href="{% url 'accounts:login' %}">로그인</a>
          </li>
          <li class="nav-item">
              <a class="nav-link" href="{% url 'accounts:signup' %}">회원가입</a>
          </li>
      </ul>
    </div>
  </nav>
  ```

  

  