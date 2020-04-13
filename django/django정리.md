

# MTV기초

- MTV: Model, Template, View로 장고의 기본 흐름이다. 다른 곳에서는 보통 MVC를 쓴다.
  - Model: 데이터 관리
  - Template: 인터페이스(화면)
  - View: 중간 관리(상호 동작)
- MVC: Modle,View,Controller 순서대로 MTV와 하나씩 대응



cf. **API**(Application Programming Interface, 응용 프로그램 프로그래밍 인터페이스): 응용 프로그램에서 사용할 수 있도록, 운영 체제나 프로그래밍 언어가 제공하는 기능을 제어할 수 있게 만든 인터페이스



- 기본적인 장고를 다루는 순서는 아래와 같다.

  - 프로잭트 생성(이때 생기는 intro폴더가 모든 프로젝트를 관리하는 폴더다)

    - \_\_init.py\_\_, settings.py, urls.py, wsgi.py등이 있다.
    - wsgi는 web server gateway interface이다.

  - 앱 생성

    - 앱 이름은 복수로 지정하는 것이 관례다. 

  - 장고에게 앱이 생성되었다는 것을 알리기

    - 즉, 등록을 해야하는데 이는 `settings.py`에서 한다.

    - `INSTALLED_APPS`에 추가해줘야 한다.
  
      ```python
      # $manage.py startapp pages를 통해 pages라는 app을 만들었을 경우 아래와 같이 추가해야 한다.
      
      
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

  - url 연결하기

    - 다음으로 `urls.py`에서 어떤 url로 들어갔을 때 무엇을 처리할지를 설정해줘야 한다.
  
      ```python
      from django.contrib import admin
      from django.urls import path
      from pages import views   #pages에서 views를 가져오고 
      #기본 구조
      #from app이름 import 함수정의된 파일 이름
      
      urlpatterns = [
          path('admin/', admin.site.urls),
          path('index/', views.index),
          # index라는 url로 들어가면 views의 index라는 함수를 처리를 하겠다.
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
      ```

    - redirect

      ```python
    #특정 html파일을 렌더링 하는 것이 아니라 처리가 모두 끝난 후 특정 url로 넘어가고자 할 때에는 redirect를 쓰면 된다. 물론 임폴트를 해야 한다.
      from django.shortcuts import render,redirect  #import 해주고
    
      def index(request):
          return redirect('가고자 하는 url')
      
      #redirect는 경로로 들어가는 것이므로 urls로 갔다가 views를 실행하고 views에 입력한 대로 html파일이 렌더링되는 경로를 거치지만 render는 위의 과정을 거치지 않고 바로 렌더링한다. 따라서 위의 경우처럼 특정 경로로 돌아가야 하는 경우에느 redirect를 써야한다.
      
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

    ```python
    #기본형
    from django.shortcuts import render
    
    def index(request):
    	return render(request,'index.html')
    ```

  - HTML파일에 넘겨줄 변수가 있는 경우

    - 항상 딕셔너리로 넘겨준다.

    ```python
    from django.shortcuts import render
    
    def index(request):
        import random
        pick = random.sample(range(1,46),6)
        context={
            'pick':pick
        }
    	return render(request,'lotto.html',context)
    ```





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

    ```html
    <!--lotto.html파일-->
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

    ```html
    <h1>{{ menu[0] }}</h1>
    
    out
    에러 발생
    
    
    <h1>{{ menu.0 }}</h1> <!--value인 menupan이 아닌 key인 menu를 가지고 인덱스 접근-->
    
    out
    치킨
    ```






- DTL(Django Template Language): 장고의 화면을 작성하기 위한 언어, 렌더링을 위한 언어

  
  - 기본 출력
  
    ```html
    {{}}
    ```
  
  - 반복문, 조건문 등의 문법
  
    ```html
    {% %}
    ```
  
  
  - 아래의 문법들은 파이썬에서의 문법과 같이 연산을 위해 사용하는 것이 아니다. 연산이 끝난 자료를 받아 그것을 출력하기 위한 문법들일 뿐이다.
  
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
  
    ```html
    <!--index.html-->
    <!--기본-->
    ```
  
    ```html
    <ul>
          {% for m in menu %}   <!--for문과-->
          <li>{{m}}</li>
          {% endfor %}          <!--endfor문 사이의 내용을 len(menu)번 반복-->
    </ul>
    
    out
    치킨
    피자
    햄버거
    ```
  
  - `forloop.counter`: 반복 횟수를 출력, 당연히 for문 안에만 쓸 수 있다.
  
    - `forloop.counter숫자`:입력한 숫자부터 시작한다.
  
    ```html
    <!--index.html-->
    <ul>
      {% for m in menu %}   <!--for문과-->
      <li>{{forloop.counter}} : {{m}}</li>
      {% endfor %}          <!--endfor문 사이의 내용을 len(menu)번 반복-->
    </ul>
        
    out
    1 : 치킨
    2 : 피자
    3 : 햄버거
    ```
  
    
  
    - `empty`: 반복할 것이 없을 경우 설정한 내용을 출력
  
      ```html
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
  
    ```html
    <!--기본형-->
    {% if user == 'admin' %}   <!--if문이 True면-->
    	<p>수정, 삭제</p>        <!--이 줄이 실행-->
  {% else %}				   <!--if문이 False면-->
    	<p>관리자 권한이 없습니다.</p> <!--이 줄이 실행-->
  {% endif %}     <!--for문과 마찬가지로 닫아줘야 한다.-->
    ```
  
  
  
- 기타
  
    - `|length`: 앞에 온 문자열 혹은 리스트의 길이를 출력
    
      ```html
      <!--예를 들어 content에 "안녕"을 넘겼다고 가정하면-->
      <p>{{content|length}}</p>
    
      out
    2
      ```






- settings.py에 있는 각종 옵션들

  ``` python
  DEBUG = True  #True로 되어 있으면 개발 모드라고 할 수 있다.
  
  ALLOWED_HOSTS = [] #프로젝트에서 생성한 사이트(경로)로 들어올 권한을 정하는 것이다.
  #'*'를 대괄호 사이에 넣으면 누구나 입장 가능한 상태가 된다.
  #프로그래밍에서 *는 일반적으로 "모두"를 뜻한다.
  
  
  TEMPLATES = [
      {    #DjangoTemplates(DTL)라는 엔진을 쓰고 있다는 의미
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
  
  
  #디버그
  DEBURG = True
  # True로 놓으면 오류 페이지가 상세하게 떠서 어떤 오류가 발생했고 어떤 코드에서 발생했는지 알 수 있다.
  #False로 해놓으면 오류 메세지만 출력된다. 따라서 만일 True로 해놓은 상태에서 오류가 발생하게 되면 다른 사람들이 내가 짠 코드를 전부 볼 수 있게 되므로 보안상의 심각한 문제가 생길 수 있다. 따라서 다른 사람들이 사용하게 할 때에는 반드시 False로 바꿔야 한다.
  
  
  
  # Internationalization관련 설정들
  LANGUAGE_CODE = 'en-us'  #언어를 설정하는 것으로 "ko-kr"로 바꾸면 한국어가 된다.
  
  TIME_ZONE="UTC"  #시간 설정으로 'Asia/Seoul'로 바꾸면 한국 시간이 된다.
  
  USE_I18N = True #Internationalization의 약자로 I와 N사이에 18자가 위치해 이렇게 명명
  
  USE_L10N = True #Localization의 약자로 L과 N사이에 10자가 위치해 이렇게 명명
  
  USE_TZ = True
  
  ```








# MTV 확장


- variable routing: url을 변수화 해서 변수로 사용하는 것

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

  - 위에서 name뒤에 숫자를 붙였는데 숫자가 같은 것 끼리는 변수명이 동일해야 한다.

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






- 템플릿 확장

  - 프로그래머는 반복적인일을 해야 할 때 반복을 컴퓨터에 맡길 방법이 없는지 생각해 봐야한다.

  - HTML작성시에도 마찬가지로 여러 HTML문서에 공통으로 들어가는 사항을 매번 입력하지 않고 한번의 작성만으로 끝낼 수 있는 방법이 존재한다.

    ```html
    <!--기본-->
    <!--이름에 넣고 싶은 것을 입력하고-->
    {% block 이름 %}
    {% endblock %}
    
    
    <!--적용-->
    <!--위에서 입력한 이름과 위 html파일의 파일명을 일치시키면 된다.-->
    {% extends base가되는 html파일명 %} <!--어떤 파일을 기준으로 확장할지 적어준다.-->
    
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
      
      
      #A어플의 views.py파일
      #A어플도 마찬가지로 바꿔준다(templates폴더의 하위에 A라는 폴더를 생성하고 그곳에 html을 넣었다고 가정).
      
      def hello(request):
          return render(request, 'A/hello.html')
      ```

      

  - 또한 템플릿 확장을 사용한 경우 base.html 파일이 모든 프로젝트에서 사용 가능하게 바꿀 수 있다.

    - 만일 A어플 내의 base.html을 A어플의 다른 템플릿들에 사용했을 경우 B어플에서도 base.html을 사용하고자 한다면 base.html을 project폴더에 `templates`폴더를 만든 후 그 안에 넣으면 된다.

    - 또한 settings.py에서 `TEMPLATES`설정을 바꿔줘야 한다.

      ```python
      TEMPLATES = [
          {
              'BACKEND': 'django.template.backends.django.DjangoTemplates',
              #본래 비어 있던 아래 []사이에 다음과 같이 입력해준다.
              #BASE_DIR은 manage.py가 존재하는 프로젝트 최상위 폴더를 의미하는데 (BASE_DIR, 		 '프로젝트명','templates')는 최상위 폴더부터 temlpates폴더까지의 경로를 ,로 구분		해서 입력한 것이다.
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



- form태그와 input태그

  - 각 태그의 특징

  ```html
  <!--form과 input태그에서 가장 중요한 것은 각기 action과 name이다. action은 input에서 입력 받은 내용을 어디로 보낼지에 관한 것이고 name은 입력 받은 내용을 어떤 변수에 담아서 보낼지에 관한 것이다. 아래의 경우 입력받은 내용을 content와 title에 담아 content와 title을 /pages/complete/라는 경로에 보내겠다는 의미다. -->
  
  
  <!--action태그를 비워 두면 해당 html파일을 호출한 함수로 데이터가 전달된다.-->
  <form action="/pages/complete/">
  	<input type="text" name="content">
      <input type="text" name="title">
  </form>
  <!--content와 title는 경로상에서 ?뒤에 표시되며 이를 쿼리문이라 한다.-->
  <!--만일 content에 1234를, titl에 5678을 입력한 경우-->
<!--~/pages/complete/?content=1234&title=5678-->
  ```

  

  - 장고에서의 활용
  
  ```python
  #views.py파일
  #위에서 받아온 입력값은 request에 담기게 된다.
  def complete(request):
     	print(request.GET) #어떤 정보가 담겨있는지
      print(request.path) #어떤 경로로 요청이 들어왔는지
      return render(request, 'complete.html')
  
  out
  QueryDict{'content':1234,'title':5678}
  /pages/complete/
  
  
  #위에서 본것과 같이 request.GET은 딕셔너리이다. 이 딕셔너리로 넘어온 정보를 활용하는 방법은 키를 입력하면 값을 돌려주는 .get()함수를 사용하는 것이다.
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
    
  
  <!--xxx를 입력받았다고 가정-->
      ```
  
      ```html
      <!--complete.html-->
      {{ qwe }}
  

<!--페이지에 xxx가 출력된다.-->
      ```

      - 정리
    
        ⓐnew/경로로 접근한다.
    
        ⓑurls.py는 접근을 감지하고 views의 new함수를 실행시킨다.
    
        ⓒnew 함수가 실행되면  new.html이 렌더링 해 화면에 출력한다.
    
        ⓓ값을 입력받는다.
    
        ⓔ입력 값은 complete/경로로 넘겨진다.
      
        ⓕurls.py는 접근을 감지하고 views의  complete함수를 실행시킨다.
    
        ⓖcomplete함수 complete.html이 렌더링 해 화면에 출력한다.







# Model

- Model은 데이터를 관리하는 작업을 한다(데이터 베이스를 모델링). 



- database를 쓰는 이유
  - 여러 사람이 접근해서 작성하는 데이터의 경우 파일로 저장하면 불편할 수 있다.



- 스키마란
  - 다양한 사람이 작성할 수 있는 데이터 베이스의 특성상 동일한 정보도 다르게 작성할 수 있다. 따라서 동일한 정보는 동일하게 저장하도록 틀을 만들어 놓아야 하는데 이를 스키마라 부른다.
  - 예를 들어 나이를 입력하라고 했을 때 동일한 20살의 나이를 누군가는 20, 누군가는 20살, 누군가는 스무살로 각기 다르게 입력할 수 있다. 따라서 IntField라는 스키마(틀)을 줘서 이에 맞게 입력하도록 하는 것



- 데이터
  - 데이터를 엑셀 파일에 비유했을 때 하나의 테이블은 하나의 sheet가 된다.
  - 열(column)은 속성을 담고 있다. 속성 혹은 레코드라고도 부른다. 스키마가 틀을 만드는 것이 바로 열이다
  - 행(row)는 각 속성의 구체적인 정보를 담고 있다. 레코드라고도 부른다.
  - PK(Primary Key): 주민등록번호, 군번, 학번과 같이 식별을 위해 지정된 고유한 값 , PK값의 column의 이름을 id라 부른다.
  - 장고에서는 객체를 저장할 때 마다 PK값을 하나씩 증가시키면서  PK값을 부여한다.



- 데이터 베이스를 조작하는 언어
  - SQL(Structured Query Language)
  - ORM(Object Relational mapper)
    - object와 database를 맵핑 시킨 것. 객체로 관계(DB)를 조작한다고 보면 된다.
    - 객체 조작은 메서드를 호출함으로써 가능하다.



- ORM

  - 기본적인 데이터베이스 조작을 CRUD(Create, Read, Update, Delete)operation 이라고 한다.

    - 게시판의 글을 생각해보면 보다 쉽게 이해할 수 있다.

  - Django shell: python interactive interpreter를 django 프로젝트에 맞게 쓸 수 있는 기능

    - 이를 사용하기 위해서는 추가적인 패키지 설치가 필요

      ```bash
      $ pip install django-extensions ipython
      ```

      - `django-extensions` 는 django 개발에 있어서 유용한 기능들을 기본적으로 제공한다.

      - `ipython` 은 인터렉티브 쉘을 조금 더 편하게 활용하기 위해서 설치.

      - 설치 후 `settings.py` 에 다음의 내용을 추가한다. (콤마 유의)

        ```python
        # django_crud/settings.py
        INSTALLED_APPS = [
            ...
            'django_extensions',
            'articles',
        ]
        ```

      - 그리고 이제부터는 아래의 명령어를 사용한다.

        ```bash
        $ python manage.py shell_plus
        ```

      - 쉘 종료 명령어는 `ctrl+d` 이다.

  - 생성 - ex. 게시글 작성

    ```python
    #방법1
    article = Article()      #Article()이라는 클래스로 article이라는 객체를 만들고
    article.title = '제목'    #article 객체의 title을 '제목'으로,
    article.content = '내용'  #article 객체의 content을 '내용'으로 설정한다.
    article.save()           #반드시 세이브를 해줘야 한다.
                             #models.DateTimeField(auto_now_add=True) 속성의 경우에는 위의 							과정을 거치지 않아도 자동으로 생성되므로 바로 쓰면 된다.
    
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
    ```
  
  - 단일 데이터 조회(고유한 값인 id를 통해 가능)

      ```python
      #방법1
      Article.objects.get(id=1)

      #방법2
      Article.objects.all()[0]  #[]안에 음수는 올 수 없다.

      #방법3
      Article.objects.all().first()
    <Article: Article object (1)>
    ```
    
  - 수정- ex. 게시글 수정

      ```python
      a1 = Article.objects.get(id=1)  #수정할 대상을 정하고
      a1.title = '제목 수정'            #수정후
      a1.save()                        #저장
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
   
   admin.site.register(Article)
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
    #auto_now=True는 최종 수정 시간을자동으로 추가해 주는 것이다.
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

  - 다른 방법은 마이그레이션 파일들과 db.sqlite3를 삭제하는 것이다(\_\_init\_\_.py는 삭제 금지). 이 경우 기존에 입력한 데이터가 날아가긴 하지만 입력된 데이터가 얼마 없을 경우 이렇게 하는 편이 깔끔하다.

  - 이후 `models.py`에서 정의한 파일을 `views.py`등 다른 곳에서 사용하고자 한다면 반드시 import를 해줘야 한다.

      ```python
      #views.py
      from 디렉토리 파일명 import 클래스명
      #동일한 디렉토리에 있을 경우 .을 입력하고 파일명은 model을 정의한 파일명을 입력하는데 보통 models.py와 views.py는 같은 폴더에 있고 model은 일반적으로 models.py에 정의하므로
      from .models import 클래스명
      #위와 같이 쓰면 된다.
      ```




- 만일 git에 push한다면 반드시 빼놓고 push해야 하는 파일들이 있으므로 꼭 `.gitignore`파일을 생성하여 빼놓을 파일을 작성해야 한다.



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




- django 공식문서에서 [ ]는 필수로 입력해야 하는 것이 아닌 옵션이다.



- POST와 GET의 차이

  - GET은 주소창에 정보를 입력하여 받아오는 것이고 POST는 주소창에 입력하지 않고 받아오는 것이다. 

  - 둘 다 정보를 받아오는 것이라는 공통점이 있지만 post는 받아온 내용을 서버에도 제출하여 서버에서 관리하고,  get은 딕셔너리에 담아 관리한다는 차이가 있다. 또한 GET은 받아온 정보가 url로 넘어가지만(따라서 크기 제한 및 보안 이슈가 있다) POST는 그렇지 않다. 일반적으로 GET은  정보를 받아서 읽는 용도로 사용하고 POST는 받아서 추가적인 처리를 더 해줄때 사용한다. GET은 a태그와 form태그 둘 다 사용가능하지만 POST는 form태그만 사용 가능하다. 요청을 보냈을 때 GET은 데이터 베이스가 변화하지 않지만 POST는 데이터 베이스가 변화한다.

  - method로 POST를 쓸 경우 보내는 곳에 아래의 코드를 추가해야 한다.  보안상의 이유로 붙이는 것이다.
  
    ```html
    {% csrf_token %}
    ```




- HTTP 상태 코드
  - 200 OK: 성공
  - 300대는 redirect
    - 301 Moved Permanently
    - 302 Found
  - 400대는 클라이언트 이슈
    - 400 Bad Request
    - 401 Unauthorized(로그인이 필요함에도 로그인 하지 않은 경우)
    - 403 forbidden(권한이 없는 경우, {csrf_token}을 안써도 이 이슈가 발생)
    - 404 Not Foubd(해당 URL이 없는 경우)
    - 405 Method Not Allowed(GET으로 처리하는데 POST로 보낸 경우)
  - 500 Internal Server Error: 서버 오류



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
  - 따옴표는 하나로 통일해라
  - 변수할당할 때는 `=` 좌우를 한 칸씩 띄우고 그렇지 않을 때는 붙여써라.
  - `views.py`에서 `import`밑에는 2줄 띄우고 각 함수 사이는 1줄 띄운다.
  - 앱 이름은 반드시 복수형으로 정한다.
  - 앱 이름 외에도 복수인 것들은 복수형으로 정한다.
  - import 작성 순서: python코어-django-직접 만든 파일 순









# 정적 파일 관리

- static: 정적 파일 관리, CSS,JS,image파일을 일반적으로 static파일이라 부른다.

  - 앱 하부폴더로 static폴더를 생성 후 static폴더 하부에 앱 이름과 동일한 폴더를 생성(templates폴더와 가은 이유로 폴더 내부에 앱 이름과 같은 이름의 폴더를 생성해준다)후 그 폴더에 필요한 파일을 작성, 만일 특정 앱이 아닌 프로젝트 전체에서 쓰고싶다면 프로젝트에 폴더를 생성하면 된다.

  - bootstrap-download-Compiled CSS ans JS 다운로드 후 위에서 생성한 폴더에 업로드

  - `settings.py`에 아래의 코드 추가

    ```python
    # serving 되는 URL 앞에 붙음.
    STATIC_URL = '/static/'
    # app 디렉토리가 아닌 static 폴더 지정
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
    ]
    ```

  - 적용하고자 하는 html파일(전부 다 적용할 것이라면 base.html파일)에 아래의 코드를 추가, 그대로 쓰는 것이 아닌 적용하고자 하는 파일을 적으면 된다.

    ```html
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Document</title>
        
        <!--추가한 코드-->
        <link rel="stylesheet" href="{% static 'bootstrap/bootstrap.min.css' %}">
        
        {% block css %}
        {% endblock %}
    </head>
    
    <body>
        
        <!--추가한 코드-->
        <script src="{% static 'bootstrap/bootstrap.min.js' %}"></script>
    
    </body>
    </html>
    ```

  - 적용 받는 HTML파일에 아래의 코드를 추가

    ```python
    {% extends 'base.html' %}  <!--extends는 항상 최상위에 와야 한다.-->
    {% load static %}
    {% block css %}
    <link rel="stylesheet" href="{% static 'stylesheets/form.css' %}">
    {% endblock %}
    ```









# form

- form.py

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
      class Meta:  #어떤 모델에서 어떤 datafield를 가져 올지를 정의하는 부분
      #M은 반드시 대문자로 쓸 것, 메타데이터를 가져오는 클래스이다. 메타데이터는 데이터에 대한 데이터로
      #사진을 찍을 때 사진이라는 데이터에는 찍은 날짜, 장소 등도 저장되는데 이 날짜, 장소등이 메타데이터	  할 수 있다. class도 마찬가지로 class라는 데이터의 메타데이터를 (아래의 경우 title, content	  등)가져오는 것이다.
      	model = Article
          fields = '__all__'
          #fields = ['title','content','created_at','updated_at'] 과 동일
          #'__all__'을 쓰고 특정한 것을 제외하고 싶다면 
          #exclude = ['title']과 같이 쓰면 된다.
          
  #위의 코드는 아래의 코드와 동일하다. 그러나 아래와 같이 쓰면 위의 models.py에 이미 쓴 내용을 다시 반복해서 써야 한다. 따라서, 위의 코드처럼 models.py에서 상속을 받아서 쓰는 방식이 주로 쓰인다.
  class ArticleForm(forms.Form):
      titlt = forms.CharField(max_length=100)
      content = forms.CharField()
      
      
      
  #혹은 아래와 같이 설정도 가능하다. 이 경우에도 Meta를 함께 넘겨줘야 한다.
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
              article = form.save()
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
  
  

- `require_POST`

  ```python
  from django.views.decorators.http import require_POST
  #이걸 쓰지 않으면 GET으로 delete 요청을 해도 delete가 된다.
  @require_POST
  def delete
  ```



- form태그 내부의 botton태그는 input태그의 submit과 동일한 역할을 수행한다. 



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

    

- HTTP메서드

  > 클라이언트가 수행하고자 하는 동작을 정의한 GET, POST 같은 동사나 OPTIONS, HEAD와 같은 명사
  >
  > GET, POST, PUT, DELETE,  HEAD, OPTIONS등이 있으나 GET, POST, PUT, DELETE 정도가 자주 쓰인다.





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
          {% bootstrap_form form %}
          <!-- input type:submit -->
          <button class="btn btn-primary">제출</button>
      </form>
  <!--아니면 그냥 위 처럼 입력하고 해당 정보가 표시되는 창에서 디버깅창(F12)에 보면 각 정보별 태그가 나와있는데, 그 태그를 보고 적용해도 된다.-->
  
  <form action="" method="POST">
  	{% csrf_token %}
  	{% bootstrap_form form %}
  	<button class="btn btn-primary">제출</button>
  </form>
  <!--아니면 그냥 위 처럼 bootstrap적용도 가능하다. 단, bootstrap을 활용하려면 settings.py도 바꿔야 하고 load도 해줘야 하기에 과정이 복잡하다.-->
  django-bootstrap4에 가면 관련 정보가 있다.
  <!--
  1.settings.py에서 installed_app에 bootstrap4를 추가
  2.쓰려는 html파일 상단에 {% load bootstrap4 %}를 입력
  3.base.html 상단에도 {% load bootstrap4 %}를 입력하고 {% bootstrap_css %}와 {% bootstrap_javascript jquery='full' %}를 각기 css,js관련 정보를 입력하던 곳에 입력
  ```

  

- message(추가 필요)
  
  - message를 별 다른 선언 없이 사용 가능한 이유는 settings에 선언이 되어 있기 때문이다.





# 사용자 인증 관리

- django에서 사용자 정보는 다른 정보와는 다르게 특별한 처리를 해줘야 한다.

- django는 사용자 정보중 비빌번호를 저장 할 때 해시함수를 통해 암호화 해서 저장한다.
  - SHA256이라는 단방향 해시 함수 알고리즘을 사용한다.
    - 단방향이기에 1234라는 비밀번호를 gweg$gewg8754egwdg24ggwe라는 암호로 변환은 할 수 있어도 암호를 다시 1234로 변환할 수는 없다. 
  - 또한 같은 비밀번호라도 다른 암호로 변환하는데 이를 솔팅이라 하고 그 값을 솔트라 한다. 솔트 값을 암호 중간중간에 넣어 암호를 더 복잡하게 만든다.
  - 반복은 혹시라도 brute force로 암호 해독을 시도하는 경우에 대비해서 최대한 반복 횟수를 늘림으로써 해독을 어렵게 하기 위함이다.

- form과 model을 이미 장고에서 정의해 놓았기에 import해서 쓰기만 하면 된다.

  ```python
  #views.py
  from django.shortcuts import render, redirect, get_object_or_404
  from django.contrib.auth import get_user_model  #모델을 불러오고
  from django.contrib.auth.forms import UserCreationForm  #form을 불러온다. 
  # from django.contrib.auth.models import User
  
  # Create your views here.
  def signup(request):
      if request.method == 'POST':
          form = UserCreationForm(request.POST)
          if form.is_valid():
              form.save()
              return redirect('articles:index')
      else:
          form = UserCreationForm()
      context = {
          'form': form
      }
      return render(request, 'accounts/signup.html', context)
  
  def detail(request, pk):
      User = get_user_model()
      user = get_object_or_404(User, pk=pk)
      context = {
          'user': user
      }
      return render(request, 'accounts/detail.html', context)
  ```

  



















