# 사용자 인증 관리

- django에서 사용자 정보는 다른 정보와는 다르게 특별한 처리를 해줘야 한다.

- django는 사용자 정보중 비빌번호를 저장 할 때 해시함수(input 값을 문자열로 바꿔주는 것)를 통해 암호화 해서 저장한다.

  - 장고에서는 SHA(Secure Hash Algorithm)256이라는 단방향 해시 함수 알고리즘을 사용한다(라이브러리가 내장되어 있다).
    - 단방향이기에 1234라는 비밀번호를 gweggewg8754egwdg24ggwe라는 다이제스트(암호)로 변환은 할 수 있어도 암호를 다시 1234로 변환할 수는 없다. 
  - 또한 같은 비밀번호라도 다른 암호로 변환하는데 이를 솔팅이라 하고 그 값을 솔트라 한다. 솔트 값을 암호 중간중간에 넣어 암호를 더 복잡하게 만든다.
  - 반복은 혹시라도 brute force로 암호 해독을 시도하는 경우에 대비해서 최대한 반복 횟수를 늘림으로써 해독을 어렵게 하기 위함이다.

- 따라서 django에서 정의한 form이 아닌 직접 작정한 form으로 회원가입을 할 경우 위의 비밀번호 암호화 작업을 추가적으로 해주지 않으면 비밀번호가 그대로 저장되게 된다,

- form과 model을 이미 장고에서 정의해 놓았기에 import해서 쓰기만 하면 된다.

  - 그러나 migrate는 해야 한다. 
  - 새로 정의한 모델이 없기에 migrations는 할 필요 없다.

- 사용자 계정 관리(회원가입)

  ```python
  #views.py
  from django.shortcuts import render, redirect, get_object_or_404
  from django.contrib.auth.forms import UserCreationForm  #form을 불러온다. 
  #UserCreationForm은 공식 문서를 보면 3개를 넘긴다(password1,password2,Meta 클래스로 User 모델의 username 필드).
  # 또한 패스워드 검증 관련 함수, 패스워드 암호화 함수가 내부에 존재한다.따라서 만일 개발자가 만든 회원가입 폼(게시글 생성 하듯이 회원 정보를 생성하는 방식으로 회원가입 폼을 만들었다면)에 패스워드 암호화 관련 처리가 되어 있지 않다면 이 폼으로 만든 비밀번호는 암호화 되지 않고 그냥 저장되게 된다.
  #즉 UserCreationForm이라는 모델 폼은 검증까지도 해준다. 또한 폼 내부에서 패스워드를 추가 설정한 후 저장을 한다. 
  
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
  ```

  ```python
  #settings.py
  #비밀번호 유효성을 검사하는 부분
  
  # Password validation
  # https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
  
  AUTH_PASSWORD_VALIDATORS = [
      {
          'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
      },
      {
          'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
      },
      {
          'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
      },
      {
          'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
      },
  ]
  
  ```

  

- User는 AbstractUser를 상속받고, AbstractUser는 AbstractBaseUser를 상속 받으며, AbstractBaseUser는 models.Model을 상속받는다.

  - 단계마다 담겨있는 속성들이 다르다, 따라서 만일 User를 불러 오는 것이 아니라 custom해서 만들고 싶다면 필요에 따라 무엇을 상속받게 하여 만들지 결정하면 된다.

    - AbstractUser: username, first_name, last_name,email, is_active, is_superuser,is_staff, data_joined
    - AbstractBaseUser: password, last_login

  - 위에서 보듯이 username, password 등의 정보들은 전부 User가 상속 받는 것들에 정의가 되어 있다. 결국 User는 이들을 활용하기 위한 껍데기라고도 볼 수 있다.

    ```python
    #예를 들어 만일 first_name, last_name,email은 필요가 없고 last_login을 담고 싶다면 아래와 같이 last_login속성을 지는 AbstractBaseUser 클래스를 상속 받으면 된다.
    class MyUser(AbstractBaseUser):
    	pass
    ```

    

- 로그인을 구현 할 때에는 사용자가 로그인한 상태라는 것을 알게 해줘야 한다.

  - 예를 들어 네이버에 로그인 하면 어떤 네이버 블로그를 가던, 카페를 가던 로그인 상태가 유지가 된다.

  - 웹의 기본 규약인 HTTP의 특징 

    - 요청과 응답(POST,GET등을 통한). 
    - stateless, connectless: 상태와 연결상황을 알지 못한다. email을 보내는 것과 전화를 하는 것의 차이와 유사하다.  전화는 통화중에는 실시간으로 계속 요청과 응답이 가능하지만 email은 요청을 보내고 답이 오면 연결이 끊어지게 된다. 또한 특정한 요청이 들어왔을 때 요청을 한 사람이 이전에 어떤 요청을 한 사람인지 알 수 없다. 따라서 연결이 끊어짐에도 로그인 상태가 유지되도록 해야 한다. 이를 가능하게 하는 것이 쿠키다.

  - 쿠키

    - 웹 사이트에서 어떤 행동을 할 때마다 웹은 사용자에게 쿠키를 제공(쿠키는 브라우저에 저장)하게 되고 이후부터는 사용자가 가진 쿠키를 웹에서 읽어서 그 상태를 기억하게 된다.
    - 만일 사용자가 쿠키를 임의로 조작하는 경우(예를 들어 일반 회원에서 admin으로 인식되도록 쿠키를 조작하는 경우) 문제가 생길 수 있다. 따라서 django에는 이를 막는 방법이 존재한다.

  - 세션

    - 사용자에게 제공한 쿠키에 대한 정보를 세션(DB/메모리)에 저장하고 사용자가 제출한 쿠키와 세션에 저장된 쿠키가 일치하지 않으면 요청이 들어와도 응답을 하지 않게 된다.

    - 세션에는 세션 키, 세선 데이터, 쿠키 만료 시간 등이 담겨 있다.

    - 그러나 세션은 서버 리소스를 사용하기 모든 사항에 대해서 쓰지 않고 일반적으로 변경되면 안되거나 중요한 사항에만 사용한다.

    - 로그인, 로그 아웃은 이 세션 테이블에 create과 delete를 하는 과정이다.

    - django에서는 db.sqlite3 내부의 django_session에서 세션을 관리한다.

    - 사용자가 로그인 할 경우 django_session 테이블에 기록된다.

      

  - 캐시는 특정 사이트에 대한 정보를 브라우저에 저장함으로써 다음에 해당 사이트에 접속했을 때 사이트가 더 빨리 로드되게 해준다. 즉 요청을 보냈을 때  매번 모든 정보를 받아오는 것이 아니라 요청한 정보에 대해서만 정보를 받아온다.
  
  - 캐시와 쿠키에 대한 정보는 웹브라우저의 개발자도구에서 application 탭에서 볼 수 있다.



- 로그인, 로그아웃

  - UserCreationForm과  AuthenticationForm
    -  회원가입에 쓰이는 UserCreationForm은 User모델을 상속받아서 모델을 통해 오브젝트를 생성(create)하는 Form이다(이전에 했던 ArticleForm도 Article을 상속받아 이를 통해 Article의 오브젝트를 create하는 Form이었다). 즉, 모델을 기반으로 만든 ModelForm이다. 정확히는 ModelForm을 상속 받는다.
    -  로그인에  쓰이는 Authentication은 ModelForm이 아닌 그냥 form이다. 즉, 특정한 모델을 기반으로 만든 form이 아니고 특정한 모델을 통해 오브젝트를 생성하지 않는다. 
  - 로그인은 쿠키, 세션과 관련된 것인데 쿠키는 사용자의 요청에 담겨서 온다. 따라서 로그인 코드에서는 request를 함께 넘겨준다.
  - 로그인 하지 않았을 때의 사용자명은 AnonymousUser이다.

  ```python
  from django.shortcuts import render, redirect
  from django.contrib.auth import get_user_model
  #from django.contrib.auth.models import User 이와 같이 import해도 되지만 get_user_model을 import해서 쓰는 것이 더 낫다.
  from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
  from django.contrib.auth import login as auth_login
  from django.contrib.auth import logout as auth_logout
  #as auth_login, as auth_logout으로 이름을 바꿔서 import하는 이유는 아래에 login, logout이라는 함수를 정의했기에 중복을 피하기 위함이다. 만일 아래 함수를 login, logout이 아닌 signin, signout으로 했다면 그냥 import하면 된다.
  
  
  # Create your views here.
  def index(request):
      return render(request,'accounts/index.html')
  
  def login(request):
      if request.method=="POST":
          #AuthenticationForm은 ModelForm이 아니기에 인자의 구성도 다르다. 
          #로그인은 쿠키, 세션에 관한 정보를 조작하는 것인데 쿠키에 대한 정보는 요청(request)에 담겨 
          #있다. 따라서 아래와 같이 (로그인 정보를 담고 있는)request를 넘겨줘야 한다.
          form = AuthenticationForm(request, request.POST)
          if form.is_valid():
              #로그인 할 때 데이터베이스에 세션에 대한 정보를 저장하고 이를 쿠키에 담아서 사용자에게
              #전달 해줘야 한다. 따라서 login()함수에도 request를 함께 넘겨 줘야 한다.
              #결국 form에 있는 유저 정보와 함께 쿠키를 넘겨주기 위해 request를 쓰는 것이다.
              auth_login(request,form.get_user())
              #.get_user()는 아이디, 비번 체크해서 일치하는 유저를 불러온다.
              #따라서 form.get_user()는 form에 있는 아이디,비번이 일치하는 유저를 불러온다.
              #AuthenticationForm 내부에 정의된 메소드다. 따라서 AuthenticationForm 내에서만 
              #사용이 가능하다.
              return redirect('accounts:index')
      else:
          form=AuthenticationForm()
      context = {
          'form':form
      }
      return render(request,'accounts/login.html',context)
  
  def logout(request):
      auth_logout(request)
      return redirect('accounts:index')
  ```

  

- User와 get_user_model의 차이

  ```python
  #User는 모델을 직접 가져오는 것이고
  from django.contrib.auth.models import User
  #get_user_model은 함수다
  from django.contrib.auth import get_user_model
  
  #User를 import 할 경우
  user = get_object_or_404(User,pk=pk)
  
  #get_user_model를 import 경우
  User = get_user_model()
  user = get_object_or_404(User,pk=pk)
  
  #User는 내부에 이미 정의되어 있는데 만일 나중에 개발자가 재정의(e.g. MyUser) 할 경우 User를 찾아서 일일이 재정의한 이름으로 바꿔줘야 하기 때문에 get_user_model()을 쓰는 것이 더 낫다.
  ```

  

- `is_authenticated`

  - 로그인 상태인지 확인하는 속성
  - `User`가 상속받는 `AbstractBaseUser`에 정의되어 있다.
  - `is_authenticated`를 별 다른 import 없이 사용하고, html파일에서도 사용할 수 있는 이유는 `settings.py`에 정의되어 있기 때문이다.

  ```python
  TEMPLATES = [
      {    #DjangoTemplates(DTL)라는 엔진을 쓰고 있다는 의미, jinja2 등으로 변경 가능
          'BACKEND': 'django.template.backends.django.DjangoTemplates',
          'DIRS': [],
          #'APP_DIRS'가 True면 Installed_APPS에 등록된 앱들의 템플릿 폴더를 관리하겠다는 의미
          'APP_DIRS': True,  
          'OPTIONS': {
              'context_processors': [  #context를 처리할 때 아래의 것들을 사용할 수 있도록
                  'django.template.context_processors.debug',
                  'django.template.context_processors.request',
                  'django.contrib.auth.context_processors.auth', #정의되어 있다.
                  'django.contrib.messages.context_processors.messages',
              ],
          },
      },
  ]
  ```

  

  - request, messages를 별 다른 import 없이 사용할 수 있는 이유도 이 때문이다.

  ```python
  #로그인 된 상태에서는 로그인 페이지나 회원가입 페이지로 갈 필요가 없기에 아래와 같이 조건문을 사용하여 들어가지 않게 해준다.
  def signup(request):
      #request 객체에 user 정보가 담겨 있기에 아래와 같이 써준다.
      if request.user.is_authenticated:  #만일 로그인 상태면
          return redirect('accounts:index') #redirect
      if request.method=="POST":
          form=UserCreationForm(request.POST)
          if form.is_valid():
              form.save()
              return redirect('accounts:index')
      else:
          form = UserCreationForm()
      context = {
          'form':form,
      }
      return render(request,'accounts/signup.html', context)
  
  def login(request):
      if request.user.is_authenticated:    #만일 로그인 상태면
          return redirect('accounts:index') #redirect
      if request.method=="POST":
          form = AuthenticationForm(request, request.POST)
          if form.is_valid():
              auth_login(request,form.get_user())
              return redirect('accounts:index')
      else:
          form=AuthenticationForm()
      context = {
          'form':form
      }
      return render(request,'accounts/login.html',context)
  ```

  

- @login_required

  > 로그인이 필요한 페이지에 로그인을 하지 않고 접근했을 경우의 처리

  - @login_required를 쓰지 않고 `is_authenticated`를 활용한 조건문으로 처리해도 된다.

  - @login_required와 단순히 조건문으로 이러한 처리를 할 때의 차이는 @login_required는 로그인 경로로 이동하게 해 주고 url에 next를 포함시킨다는 것이다.

  ```python
  #만일 로그인 하지 않은 상태에서 로그아웃을 시도할 경우
  #위에서 import했던 것들은 다시 import하지 않았음
  from django.contrib.auth.decorators import login_required #import하고
  
  
  def login(request):
      if request.user.is_authenticated:
          return redirect('articles:index')
      if request.method == 'POST':
          form = AuthenticationForm(request, request.POST)
          if form.is_valid():
              auth_login(request, form.get_user())
              '''
              @login_required만 붙인다고 끝이 아니라 login 함수에 아래 코드를 써야 한다.
              정확히는 로그인 처리를 하는 함수 아래에 써야 한다. 로그인 버튼을 눌렀을 때, 즉 POST요청
              이 넘어 왔을 때 그 요청을 처리하는 함수 아래에 적어야 원하는 창으로 보내줄 수 있다. 이
              코드의 경우 로그인 처리를 하는 함수가 login함수이므로 여기다 적는 것이다.
              
              만일 @login_required가 작성되지 않았거나 작성되었더라도 로그인한 상태로 해당 경로로 
              들어갔다면 next자체가 선언되지 않을 것이고 None이 되어 False가 되고,	
              'accounts:index'로 redirect된다.
              
            그러나 만일 @login_required가 작성되었고 로그인하지 않은 상태로 해당 경로로 들어갔다면 
            next가 원래 접근하려 했던 경로에 대한 정보가 담긴채로 선언되고 해당 경로를 redirect하
            게 된다. 또한 단축평가에 따라 앞의 문장이 참이므로 뒤의 'accounts:index'는 실행되지 X
              '''
              return redirect(request.GET.get('next') or 'accounts:index')
      else:
          form = AuthenticationForm()
      context = {
          'form':form,
      }
      return render(request, 'accounts/login.html', context)
  
  
  @login_required
  def logout(request):
      auth_logout(request)
      return redirect('accounts:index')
  
  
  #로그인 하지 않은 상태에서 로그아웃으로 접근 후 url창을 확인하면 아래와 같은 url을 확인할 수 있다.
  #/accounts/login/?next=/accounts/logout/
  
  #next에 /accounts/logout/가 담기게 된다.
  
  #만일 로그인 처리가 된다면 ?next=이후에 나오는 경로로 이동하겠다는 의미이다.
  
  #따라서 위 코드에 따르면 로그인 하지 않은 상태에서 로그아웃을 한다면 우선 로그인 창이 출력되고 로그인이 완료되면 바로 로그아웃이 될 것이다.
  
  #예를 들어 만일 로그인이 필요한 기능은 새 글 쓰기에 로그인 하지 않고 접근하려 할 경우 만일 이러한 처리를 단순히 if문으로 한다면 기존 페이제로 rediect하거나 로그인을 바란다는 페이지를 render하거나 아니면 복잡한 코드를 짜서 로그인 후 원래 접근하려던 새 글 쓰기 페이지에 접근하도록 해야 할 것이다. 그러나 만일 @login_required를 쓴다면 다른 조건문 없이도 로그인 후 바로 원래 접근하려던 페이지를 띄워준다.
  
  #login_required를 작성한 함수가 아닌 login을 하는 함수에 return redirect(request.GET.get('next') or 'accounts:index')를 적어야 한다는 것을 기억해야 한다.
  ```

  - 경로(/accounts/login/?next=/accounts/logout/)에서 next 앞 부분(/accounts/login/)은 로그인 되어 있지 않을 때 login경로로 이동하겠다는 것이다.

    - 만일 urls.py에 로그인 함수를 실행시키는 경로를 login이 아닌 다른 것으로 설정해 놓았다면 제대로 작동하지 않는다.

    - 따라서 이럴 때에는 경로 명을 수정해 주거나 settings.py에서 해당 경로를 변경해 줘야 한다.

      ```python
      #urls.py 
      from django.urls import path
      from . import views
      
      app_name = "accounts"
      
      urlpatterns = [
          path('signin/',views.signin, name="signin"),
          path('logout/',views.logout, name="logout"),
      ]
      #만일 이처럼 url 경로가 설정되어 있다면  
      #/accounts/login/?next=/accounts/logout/가 아닌
      #/accounts/signin/?next=/accounts/logout/이 되게 하거나
      
      #path('signin/',views.signin, name="signin"),가 아닌
      #path('login/',views.signin, name="signin"),이 되게 해야 한다.
      
      #후자는 단순히 이름만 바꿔주면 되지만 전자는 settings.py에 코드를 추가해 줘야 한다.
      
      #settings.py
      #본래 아래의 코드는 settings.py에 존재하지 않지만 'accounts:login'이 기본값으로 설정되어 있다. 따라서 아래 코드를 추가해 줘야 한다. 만일 앱 이름이 accounts가 아니라면 이 역시 accounts가 아닌 다른 것으로 수정해 줘야 한다.
      LOGIN_URL = '/accounts/signin/'
      ```

  - login_required의 next 요청은 GET으로 밖에 가지 않는다(request.GET.get('next')). 따라서 require_POST와 함께 쓸 경우 오류가 발생할 수 있으므로 둘 중 하나는 함수 내부에 조건문으로 구현해야 한다.

    ```python
    #@require_POST를 조건문으로 처리
    @login_required
    #@require_POST
    def detail(request, article_pk):
        if request.method=="POST": #만일 POST로 요청이 들어왔다면 아래 과정을 처리하고 return
            article = get_object_or_404(Article,pk=article_pk)
        	article.delete()
        #아니라면 그냥 return
        return redirect('articles:index')
    ```
    
    

- html 파일에서 로그인 했을 때와 하지 않았을 때 각기 다른 내용을 보여주는 방법

  ```html
  {% if request.user.is_authenticated %}  <!--만일 로그인 했다면-->
    <p>{{ user.username }}, 님 환영합니다.</p>   <!--이걸 보여주고-->
  {% else %}					 <!--안했다면-->
    <a href="{% url 'accounts:login' %}">로그인</a>   <!--이걸 보여준다.-->
    <a href="{% url 'accounts:signup' %}">회원가입</a>
  {% endif %}
  
  <!--
  user와 username의 차이
  {{ user }}와 {{user.username}}은 같은 것을 출력하는데 둘의 차이는
  user는 User클래스의 인스턴스, username은 문자열이라는 것이다. 
  즉, 둘의 출력은 같으나 타입은 완전히 다르다.
  같은 것이 출력되는 이유는 user를 출력했을 때 username이 출력되도록 코드가 짜여져 있기 때문이다.
  -->
  ```

  

- 회원탈퇴, 회원 정보 수정

  - 게시글 생성의 경우 CRUD중에서 C를 제외한 R,U,D에 모두 variable routing이 필요하지만 사용자 관리에서는 R만 variable routing을 필요로 한다.

  - 회원 탈퇴와 회원 정보 수정은 이전에 했던 게시글 수정, 삭제와 같이 pk를 url로 넘겨받아서 이루어지지 않는다. 만일 위와 같은 방식으로 수정, 탈퇴를 한다면 누군가 악의적으로 이를 이용할 수 있기 때문이다.

  - 따라서 로그인 상태에서 로그인한 유저의 정보를 받아서 수정, 삭제하는 방법을 사용한다.

  - 회원 탈퇴

    ```python
    #views.py
    #위에서 import했던 것들은 다시 import하지 않았음
    from django.views.decorators.http import require_POST
    
    @require_POST  #GET으로 접근해서 삭제할 수 없도록 require_POST를 써준다.
    @login_required  #로그인 해야만 삭제할 수 있도록 한다.
    def delete(request):
        #로그인한 유저에 대한 정보가 request에 담겨 있으므로 따로 url로 pk값을 넘길 필요가X
        request.user.delete() #요청을 보낸 유저의 정보를 삭제
        return redirect('articles:index')
    ```

    ```html
    <!--detail.html(회원 프로필을 보여주는 페이지)-->
    {% block body %}
    <h1>{{ user.pk }} : {{ user.username }}</h1>
    <!--만일 요청을 보낸 유저와 detail 함수에서 context로 받아온 유저가 동일하면-->
    {% if request.user == user %} 
    	<!--아래의 회원탈퇴 form을 띄운다.-->
        <form action="{% url 'accounts:delete' %}" method="POST">
            {% csrf_token %}
            <button class="btn btn-secondary">회원 탈퇴</button>
        </form>
    {% endif %}
    <hr>
    {% endblock %}
    ```

  - 회원 정보 수정

    - 회원의 프로필을 수정하는 것은 아래와 같은 방법으로 가능하지만 비밀번호 변경은 따로 form과 함수를 사용해야 한다.

    ```python
    #form
    PasswordChangeFrom  #내부에 정의되어 있다.
    
    #함수
    .set_passowrd('새 비밀번호')
    ```

    - `UserChangeForm`이 존재하여 `views.py`에서 아래와 같이 import해서 쓸 수도 있다.

    ```python
    from django.contrib.auth.forms import UserChangeForm
    ```

    - 그러나 직접 만들어서 쓸 수도 있다.

    ```python
    #forms.py
    from django.contrib.auth import get_user_model
    from django.contrib.auth.forms import UserChangeForm
    
    # UserChangeForm를 그대로 사용하지 않고 상속받아서 custom한다.
    class CustomUserChangeForm(UserChangeForm): #UserChangeForm상속
        class Meta:
            model = get_user_model()
            fields = ['username', 'first_name', 'last_name', 'email']
    ```

    ```python
    #views.py
    from .forms import CustomUserChangeForm #직접 만든 Form을 불러오고
    
    # Create your views here.
    
    def update(request):
        if request.method == 'POST':
            #글을 수정 할 때와 같이 instance=request.user를 통해 확인을 해주고
            form = CustomUserChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('articles:index')
        else:
            form = CustomUserChangeForm(instance=request.user)
        context = {
            'form': form
        }
        return render(request, 'accounts/update.html', context)
    ```

    ```html
    <!--update.html-->
    {% extends 'base.html' %}
    
    {% load bootstrap4 %}
    {% block body %}
        <form action="" method="POST">
            {% csrf_token %}
            {% bootstrap_form form %}
            <button class="btn btn-primary">수정</button>
        </form>
    {% endblock %}
    
    
    <!--detail.html(회원 프로필을 보여주는 페이지)-->
    {% block body %}
    <h1>{{ user.pk }} : {{ user.username }}</h1>
    <!--만일 요청을 보낸 유저와 context에 담겨 넘어온 유저가 동일하면-->
    {% if request.user == user %} 
    	<!--아래의 회원탈퇴 링크를 띄운다.-->
        <a href="{% url 'accounts:update' %}">회원 수정</a>
    {% endblock %}
    ```

    

- 일반적으로 urls.py에 경로 설정을 하면 처음 서버를 실행시키고 창을 열었을 때 `Page not found (404)`태창 뜨고 뒤에 추가적인 url을 입력해야 해당 페이지가 출력된다. 만일 이게 귀찮다면 다음과 같이 하면 된다.

  ```python
  #urls.py(프로젝트)
  from django.contrib import admin
  from django.urls import path, include
  
  urlpatterns = [
      path('admin/', admin.site.urls),
      path('', include('reviews.urls')),
      ]
  from django.urls import path
  from . import views
  
  app_name = 'reviews'
  
  
  #urls.py(앱)
  urlpatterns = [
      path('',views.index, name="index" ),
  ]
  #위와 같이 프로젝트 urls.py에서 include할 때 빈 경로로 설정하면 서버를 실행 시키고 창을 띄우자 마자
  #index함수가 실행되어 해당 함수가 렌더링하는 창이 뜨게 된다. 
  #즉 본래 https://3fdd8495a9bc4dd093821052501b61d9.vfs.cloud9.us-west-2.amazonaws.com/
  #위와 같은 url의 뒤에 app이름과 app내부의 urls.py에서 정의한 경로를 추가하여 그 페이지로 이동하는 방식이었는데 프로젝트 url과 앱 url을 둘 다 비워두면 위의 url이 곧 path('',views.index, name="index" )를 가리키게 되어 index함수가 실행된다.
  ```



- User 모델의 custom

  - django에서는 프로젝트를 시작 할 때 User를 커스텀해서 사용할 것을 강하게 권장한다. 만일 이후에 커스텀 해서 사용할 일이 생겨 뒤늦게 커스텀할 경우 과정이 복잡해지기 때문이다.
  - User 모델을 custom 할 경우 User를 상속받아서 정의하는 것이 아니라 User가 상속받는 AbstractUser를 상속 받아서 사용한다.

  ```python
  from django.db import models
  from django.contrib.auth.models import AbstractUser
  
  #꼭 모델명을 User로 할 필요는 없다.
  class User(AbstractUser):
      pass
  ```

  - 위와 같이 작성한 후 migrate를 하면 에러가 발생한다.
    - 만일 위와 같이 작성하여 migrate를 한다면 테이블명이 `앱이름_user`로 생성이 될 것이다.
    - 테이블에는 이미 장고가 정의한 auth_user라는 테이블이 존재한다.
    - 따라서 기존이 정의된 auth_user는 사용할 수 없게 된다.

  - 이를 해결하기 위해 `settings.py`에 아래의 코드를 추가해야 한다. 추가하면 migrate가 가능해진다.

  ```python
  #이제 기본 유저 모델로 `앱이름.User`를 사용하겠다는 의미
  AUTH_USER_MODEL = '앱이름.User'
  
  #디폴트값은
  AUTH_USER_MODEL = 'auth.User'
  ```

  - 유저를 정의해서 사용할 경우 추가, 수정해야 하는 것들

    - User 모델의 경우 admin에 별다른 설정 없이 사용 가능했지만 이제 User를 직접 정의했으므로 admin에도 아래의 코드를 추가해야 한다.

    ```python
    #accounts/admin.py
    
    from django.contrib import admin
    from .models import User  #직접 정의한 User 모델을 가져오고
    # Register your models here.
    
    #등록한다.
    admin.site.register(User)
    ```

    - 사용자 관리 관련 form들

    ```python
    #공식문서
    class UserCreationForm(forms.ModelForm):
        #...중략...
        class Meta:
            model = User  #UserCreationForm은 django에서 직접 정의한 User를 상속받아 만든 
            #..후략..		 form이다. 따라서 UserCreationForm도 재정의 해야 한다. 								  UserChangeForm도 마찬가지 이유로 재정의가 필요하다.
            
    
            
    #재정의
    #accounts/models.py        
    from django.contrib.auth import get_user_model
    from django.contrib.auth.forms import UserCreationForm
    
    class CustomUserCreationForm(UserCreationForm):
        class Meta:
            model = get_user_model()
            fields = ['username', 'email']
            
            
    #단, AuthenticationForm은 모델폼이 아니라 그냥 폼이기에 수정 없이 사용 가능하다.
    ```

    - get_user_model을 사용하지 않았을 경우 import, model명을 바꿔줘야 한다.

    ```python
    from django.contrib.auth.models import User
    from django.contrib.auth import get_user_model
    
    #아래와 같이 하지 않고
    User = get_user_model()
    user = get_object_or_404(User,pk=pk)
    
    #아래와 같이 했을 경우
    user = get_object_or_404(User,pk=pk)
    
    
    #아래와 같이 수정해야 한다.
    from .models import MyUser #import를 수정
    
    user = get_object_or_404(MyUser,pk=pk)
    ```

  





# 데이터 베이스

- 데이터 베이스: 여러 사람이 공유하여 사용할 목적으로 체계화해 통합, 관리하는 데이터의 집합
- DBMS: 데이터베이스(DataBase)를 관리(Manage)하는 시스템(System)

  - RDBMS: 관계형 모델을 기반으로 하는 데이터베이스 관리 시스템
    - Oracle, MySQL, SQLite 등이 있으나 수업에는 SQLite를 사용
- 관계형 데이터 베이스
  - 관계를 열과 행으로 이루어진 테이블 집합으로 구성(e.g.엑셀)
  - 각 열에 특정 종류의 데이터를 기록
  - 테이블의 행은 각 객체/엔터티와 관련된 값의 모음
- RDBMS와 NOSQL
  - RDBMS: RDBMS: 관계형 데이터 베이스, 데이터를 테이블 기반으로 처리한다. 스키마에 따라 데이터를 저장하여야 하기 때문에 명확한 데이터 구조를 보장하며 각 데이터에 맞게 테이블을 나누어 데이터 중복을 피해 데이터 공간을 절약 할 수 있다는 장점이 존재한다.
  - NOSQL: RDBMS와는 달리 데이터 간의 관계를 정의하지 않는다. 스키마가 존재하지 않는다. 따라서 자유롭게 데이터 추가가 가능하다는 장점이 존재한다.



- 기본 용어

  - 스키마: 데이터 베이스에서 자료의 구조(e.g. datatype)와 제약조건(e.g.비워 둬도 되는지)에 관한 전반적 명세
  - 테이블: 열과 행의 모델을 사용해 조직된 데이터 요소들의 집합
    - column(열): 속성, 각 열에는 고유한 데이터 형식이 있다. 고유한 데이터 형식이 지정되는 열
    - row(행, 레코드): 단일 구조 데이터 항목을 가리키는 행, 데이터가 저장되는 곳 
  - PK: 각 행의 고유값으로, 저장된 레코드를 고유하게 식별할 수 있는 값



- 데이터베이스 장단점

  - 장점
    - 데이터 중복 최소화
    - 데이터 공유
    - 일관성, 무결성, 보안성
    - 데이터의 표준화 기능
    - 용이한 데이터 접근

  - 단점
    - 전문가 필요
    - 비용 부담
    - 백업과 복구가 어려웁
    - 시스템 복잡함
    - 과부하 발생



- 데이터 무결성: 데이터의 정확성과 일관성을 유지하는 것
  - 개체 무결성(Entitiy Integrity): 모든 테이블이  고유한 기본키(PK)를 가져야 하며, 빈 값은 허용되지 않음
  - 참조 무결성(Referntial Integrity): 모든 외래키 값은 참조 관계의 기본키거나 NULL
  - 도메인 무결성(Domain Integrity): 정의된 도메인에서 모든 열(속성)이 선언되도록 규정







# SQL(Structured Query Language) 기본

- RDBMS를 조작하기 위해 사용한다.
- Query란 DB에 보내는 요청이라고 할 수 있다.
- 지금까지는 ORM을 통해서 DB에 접근했었다. 

  - 파이썬 클래스를 통해서 DB에 접근
  - 파이썬 코드를 SQL로 변경해서 실행하는 방식
  - ORM을 통해 SQL보다 편리하게 데이터베이스를 다룰 수 있었다.
  - 그럼에도 SQL을 배워야 하는 이유는 결국 ORM은 남이 짜놓은 코드이기에 한계가 있다.
- 데이터 베이스 관리를 위한 언어, RDBMS의 데이터를 관리하기 위해 사용하는 프로그래밍 언어
- 종류

  - DDL(데이터 정의 언어):데이터 정의(create,drop 등)
  - DML(데이터 조작 언어): 데이터 저장, 수정, 삭제(CRUD 관련)
  - DCL(데이터 제어 언어): 데이터베이스 사용자의 권한 등 제어
- SQL에서의 Datetype

  - INTEGER, TEXT, REAL(실수), NUMERIC(boolean), BLOB



- SQLite에서 .tables, .headers on과 같은 dot( . )로 시작하는 명령어는 SQL문이 아니다. SQL문이 아닌, SQLite에서만 사용 가능한 명령어다.



- 테이블 생성, 삭제

  - 실행

  ```bash
  $ sqlite3 db.sqlite3
  
  #종료는 ctrl+d
  ```

    - sqlite에서만 사용 가능한 명령어

  ```sql
  --내가 생성한 table들 보기
  .tables
  --내가 생성한 테이블의 스키마 보기
  .schema 테이블명
  ```

  

    - 테이블 생성

  ```sql
  CREATE TABLE 테이블명 (
    컬럼명 datetype [constraints]
  )
  
  --이미 동일한 테이블이 있으면 생성하지 안음
  CREATE TABLE IF NOT EXISTS '테이블명' (
    컬럼명 datetype [constraints]
  )
  
  
  --예시
  sqlite>CREATE TABLE classmates(
      --id는 숫자 타입이며, primary키 역할을 하고, 자동으로 1씩 증가한다.
      id INTEGER PPIMARY KEY AUTOINCREMENT, 
      name TEXT NOT NULL,  --NOT NULL은 비워 둘 수 없다는 의미이다.
      age INTEGER,
      address TEXT
  );
  -- 완료 후 반드시 ;를 입력해야 한다.

  
  
  --혹은 sql파일에 작성하고 이를 불러오고 싶으면 아래와 같이 하면 된다.
  --classmate.sql 파일
  CREATE TABLE 'classmates'(
      'id' INTEGER PRIMARY KEY AUTOINCREMENT,
      'name' TEXT NOT NULL,
      'age' INTEGER,
      'address' TEXT
  );
    
  --sql 입력창에 아래와 같이 입력
  sqlite>.read classmate.sql
  ```
  
  - 테이블 이름 변경
  
  ```sql
  ALTER TABLE 테이블명 RENAME TO 새 테이블명;
  ```
  
  - 테이블 삭제
  
  ```sql
  DROP TABLE 테이블명;
  ```



  - CRUD

    - 테이블에 데이터 추가(C)

    ```sql
    INSERT INTO 테이블명 (column) VALUES (value);
    ex. INSERT INTO 테이블명 (name,age) VALUES ('홍길동',23);
    
    --모든 column에 데이터를 넣을 때는 column을 입력할 필요가 없다. 순서대로 입력만 해주면 된다.
    ex. INSERT INTO 테이블명 VALUES ('홍길동',23, '대전');
    ```

      - 다른 곳에 작성한 sql파일을 불러와 추가하는 방법 
        - db파일과 동일한 위치에 csv파일을 만든다.
        - 터미널 창에 아래의 명령어 입력

    ```
    #파일명.csv(일반적으로 data.csv로 한다.)
    
    #아이디는 이미 저장된 것과 겹치면 안된다.
    id,flight_num,departure,waypoint,arrival,price #헤더, 굳이 안 써도 된다.
    4,RT9122,Madrid,Beijing,Incheon,200   #공백을 넣으면 안된다. 공백을 넣으면 공백도 포함됨 
    5,XZ0352,LA,Moscow,Incheon,800 
    6,SQ0972,London,Beijing,Sydney,500
    ```

    ```sql
    sqlite> .mode csv
    sqlite> .headers on  --헤더가 있다는 것을 알려주고, 없으면 안 써도 된다.
    sqlite> .separator "," --""안에 csv파일 내의 자료들이 무엇으로 구분되어 있는지 적으면 된다.
    sqlite> .import 파일명.csv 테이블명
    --만일 위 테이블명을 적는 자리에 존재하지 않는 테이블을 적으면 테이블이 새로 생성된다. 그러나 모든 데이터 타입이 TEXT로 설정되고, 값이 제대로 들어가지 않는다.
    ```
    
    - 테이블의 데이터 삭제(D)
    
    ```sql
    DELETE FROM 테이블명 WHERE 조건;
    ```
    
    - 수정(U)
    
    ```sql
    UPDATE 테이블명 SET column=value WHERE 조건;
    
    --여러 개를 수정하고자 하면 콤마로 구분하여 연속해서 입력
    UPDATE 테이블명 SET column1=value1, column2=value2 WHERE 조건;
    ```
    
    - 레코드 조회(R)
    
    ```sql
    --select문: 데이터를 읽어올 수 있으며 특정 테이블을 반환한다.
    SELECT column FROM 테이블명;   --column칸에 *을 입력하면 모든 column을 조회
    
    --distinct: 중복 없이 가져오기
    SELECT DISTINCT column FROM 테이블명;
    ```
    
    


  - 표현식

    - count: 특정 테이블에 특정 레코드의 개수

    ```sql
    SELECT COUNT(column) FROM 테이블명;
    ```

    - avg: 특정 테이블에 특정 레코드의 평균

    ```sql
    SELECT AVG(column) FROM 테이블명;
    ```

    - sum: 특정 테이블에 특정 레코드의 합

    ```sql
    SELECT SUM(column) FROM 테이블명;
    ```

    - MIN: 특정 테이블에 특정 레코드의 최소값

    ```sql
    SELECT MIN(column) FROM 테이블명;
    ```

    - MAX: 특정 테이블에 특정 레코드의 최대값

    ```sql
    SELECT MAX(column) FROM 테이블명;
    ```

    

  - where: 조건문을 활용

    - 기본형

    ```sql
    SELECT column FROM 테이블명 WHERE 조건;
    
    --아래와 같이 and나 or을 사용할 수도 있다.
    SELECT column FROM 테이블명 WHERE 조건1 and/or 조건2;
    ```

    - like 활용: 특정 패턴을 보여준다(부정은 not을 사용).

    ```sql
    SELECT column FROM 테이블명 WHERE cloumn LIKE '패턴';
    
    --e.g.like 활용
    sqlited>SELECT * FROM classmates WHERE phone LIKE '010-%'
    ```

    - like에서 사용되는 키워드(와일드카드)
  - 따옴표로 묶어줘야 한다(e.g. '2\_%\_%').
    
    | %:문자열이 있을 수도 있다.    | 2%      | %앞의 문자(이 경우 2)로 시작하는 값           |
    | ----------------------------- | ------- | --------------------------------------------- |
    |                               | %2      | %뒤의 문자로(이 경우2)로 끝나는 값            |
    |                               | %2%     | %사이의 문자(이 경우2)가 들어가는 값          |
    | _:반드시 한 개의 문자가 있다. | _2%     | 아무 값이나 들어가고 두번째가 2로 시작하는 값 |
    |                               | 1___    | 1로 시작하고 4자리인 값                       |
    |                               | 2\_%\_% | 2로 시작하고 적어도 3자리인 값                |




  - order_by: 특정 column을 기준으로 정렬

    ```sql
    SELECT column FROM 테이블명 ORDER BY column1 ASC/DESC column2 ASC/DESC;
    
    --column을 column1, column2 기준으로 오름/내림차순으로 정렬한다.
    --ASC: 오름차순(기본값)
    --DESC: 내림차순
    ```



- limit: 특정 테이블에서 원하는 개수만큼 가져오기

  ```sql
  SELECT column FROM 테이블명 LIMIT 숫자;
  ```



- offset: 특정 테이블에서 원하는 개수만큼 가져오기2

  ```sql
  --숫자2에서 1을 더한 숫자에서부터(cf.인덱스) 숫자1만큼 가져온다.
  SELECT column FROM 테이블명 LIMIT 숫자1 offset 숫자2;
  ```



- gruop by: 특정 컬럼을 기준으로 그룹화

  ```sql
  SELECT column1 FROM 테이블명 GROUP BY column2;
  
  --column2를 기준으로 column1을 그룹화
  ```





# ORM

- migrate 할 경우 테이블명은 `앱이름_모델명(소문자)`으로 생성된다. 따라서 sql로 데이터를 조작하고자 할 때는  아래와 같이 접근해야 한다.

```sql
select * from 앱이름_모델명(소문자)

--e.g.
select * from people_people
```



- orm과 sql
  - orm에서는 model을 정의하고 migrate를 해줘야 했다.
  - sql에서는 그 대신 테이블을 생성한다.
  - orm은 쿼리셋 형태로, sql은 테이블 형태로 데이터를 저장
    - 쿼리셋은 쿼리의 결과로 나오는 오브젝트이다.



- 쿼리의 메서드

  - 조회

    - get: 오직 하나의 쿼리 결과만을 반환, 하나가 아니면 모두 에러(즉, 2개 이상이거나 0개이면 에러)

      -ex. 특정 게시글로 연결해 줄 경우 하나의 게시글 번호를 요청한 것이 아니면 모두 에러를 띄운다.

      -오브젝트를 바로 반환

      ```python
      Article.objects.get(title="제목1")
      
      out
      <Article:Article object (4)>
          
      User.objects.get(last_name='최')
      # MultipleObjectsReturned: get() returned more than one User -- it returned 3!
      #1개 이상의 User(3개)를 리턴하여 에러가 발생 
      
      User.objects.get(id=1000)
      # DoesNotExist: User matching query does not exist.
      # 리턴할 것이 없어 애러
      ```

      

    - filter: 쿼리셋(비어 있더라도)을 반환(.values도 QuerySet을 반환한다.)

      ex.검색을 할 때에는 그에 해당하는 모든 게시글을 보여주고, 검색 결과가 없어도(비어도) 보여준다.

      ```python
      Article.objects.filter(title="제목1")
      
      out
      <QuerySet [<Article:Article object (4)>]>
      
      #get과 달리 object를 바로 반환하지 않으므로 object를 반환하기 위해서는 뒤에 인덱스를 붙여야 한다.
      Article.objects.filter(title="제목1")[0]
      #이렇게 하면 해당하는 오브젝트 중 첫 번째 오브젝트를 반환한다.
      
      #e.g.
      type(People.objects.filter(age=47).values('first_name')) django.db.models.query.QuerySet #QuerySet을 반환
      
      type(People.objects.filter(age=47).values('first_name')[0])                     dict #dict타입을 반환
      ```

      

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
    
    
    #아래와 같이 입력하면 sql 형식으로도 보여준다.
    $ python manage.py shell_plus --print-sql
    ```

  - 쉘 종료 명령어는 `ctrl+d` 이다.

  - 쉘 창에서 아래와 같은 명령어를 입력하면 SQL command로 어떻게 표현되는지 보여준다.

    ```python
    print(쿼리셋.query)
    #쿼리셋일 경우에만 가능하다.
    
    #e.g.
    people=People.objects.all()
    type(users)
    django.db.models.query.QuerySet  #결과가 queryset이므로
    
    print(people.query)  #사용 가능
    
    SELECT "people_people"."id", "people_people"."first_name", "people_people"."last_name", "people_people"."age", "people_people"."country", "people_people"."phone", "people_people"."balance" FROM "people_people"
    ```

    



- ORM 문법

  - `makemigrations`
  - 마이그레이션 생성
  - `migrate`
    - 마이그레이션 파일의 내용을 DB에 최종 반영
  - `showmigrations`
    - 마이그레이션 DB 반영 여부 확인

  ```bash
  $python manage.py showmigrations
  ```

  - `sqlmigrate` 
    - migration을 위한 SQL statements를 보여준다. 어떤 기능을 실행하는 명령어는 아니고, 내가 django에서 class를 통해 생성하거나 변경한 table이 SQL command로 어떻게 표현되는지 보여주는 기능

  ```bash
  $ python manage.py sqlmigrate 앱이름 migrations파일 번호
  
  #e.g.
  $ python manage.py sqlmigrate people 0001
  ```

  - 테이블 생성: sql의 테이블 생성에 대응하는 orm의 테이블 생성은 model을 정의하고 migrate하는 것

  ```python
  #models.py
  class People(models.Model):
      first_name = models.CharField(max_length=10)
      last_name = models.CharField(max_length=10)
      age = models.IntegerField()
      country = models.CharField(max_length=10)
      phone = models.CharField(max_length=15)
      balance = models.IntegerField()
  ```

  ```bash
  $ python manage.py makemigrations
  $ python manage.py migrate
  ```

  

- 모든 레코드 조회(R)

  > sql의 `select * from`

  ```shell
  모델명.objects.all()
  ```

  

- 특정 레코드 조회(R)

  > sql의 `WHERE`

  ```shell
  모델명.objects.get(id=100)  #get은 오직 하나의 쿼리 결과만을 반환
  ```

  

- 레코드 생성(C) - 기존의 C방식과 동일하게 하면 된다.

  > sql의 `INSERT INTO`

  ```shell
  #이 외의 2가지 방법을 사용해도 만들 수 있다(ref. CRUD 파트).
  모델명.objects.create(column=value)
  ```

  

- 레코드 수정(U) 

  > sql의 `SET`

  ```python
  오브젝트=모델명.objects.get(조건)
  오브젝트.column = 수정할 내용
  오브젝트.save()
  
  #e.g.
  user = User.objects.get(id=100)
  user.last_name = '성'
  user.save()
  ```

  

- 레코드 삭제(D)

  > sql의 `DELETE`

  ```
  모델명.objects.get(조건).delete()
  ```

  

- 조건에 따른 쿼리문

  - 개수 세기

    >sql의 `COUNT`

  ```python
  모델명.objects.count()  #.all은 들어가지 않아도 된다(들어가도 된다).
  
  #e.g.
  User.objects.count()
  ```

  - 조건에 따른 값

    > sql의 `WHERE`

  ```python
  모델명.objects.filter(조건).values(가져올 값)
  
  #e.g.
  User.objects.filter(age=30).values('first_name')
  
  
  #조건이 2개 이상일 경우
  
  #조건이 AND일 경우
  #방법1. 
  모델명.objects.filter(조건1, 조건2).values(가져올 값)
  #e.g.
  User.objects.filter(age=30, last_name='김').count()
  
  #방법2.메서드 체이닝
  모델명.objects.filter(조건1).filter(조건2).values(가져올 값)
  #e.g.
  User.objects.filter(age=30).filter(last_name='김').count()
  
  #방법2와 같이 filter에 다시 filter를 쓰는 것이 가능한 이유
  #filter는 queryset에 사용할 수 있다.
  #filter의 결과도 queryset이기에 다시 filter 적용이 가능하다(기린의 번식의 결과 기린이 나오고 그 기린이 자라서 다시 번식이 가능한 것과 비슷하다).
  
  
  #조건이 OR일 경우
  from django.db.models import Q  #Q를 import해야 한다.
  #Q로 묶고 |로 구분한다.
  모델명.objects.filter(Q(조건1)|Q(조건2))
  
  #e.g.
  User.objects.filter(Q(balance__gte=2000)|Q(age__lte=40)).count()
  ```



- lookup

  ```python
  모델명.objects.filter(column__lookup)
  ```

  - 대소관계

  ```python
  '''
  __gte:>=
  __gt:>
  __lte:<=
  __lt:<
  '''
  
  #e.g.
  User.objects.filter(age__gte=30)
  ```

  - 문자열 포함 관련

  ```python
  """
  i라는 prefix는 case-insensitive(대소문자 구분X)의 의미를 지닌다.
  iexact: 정확하게 일치하는가
  contains, icontains: 특정 문자열을 포함하는가
  startswith, istartswith: 특정 문자열로 시작하는가
  endswith, iendswith: 특정 문자열로 끝나는가
  """
  
  #e.g.
  User.objects.filter(phone__startswith='02-') #02로 시작하는 데이터를 조회
  ```

  

- 기타

  - 정렬

  ```python
  #내림차순
  모델명.objects.order_by('-column')
  
  #오름차순
  모델명.objects.order_by('column')
  
  #제한을 둘 경우(sql의 LIMIT)
  모델명.objects.order_by('column')[:숫자]
  
  #임의의 순서를 찾을 경우(sql의 OFFSET)
  모델명.objects.order_by('column')[숫자] #0부터 시작
  ```

  - 중복 없이 조회하고자 할 경우

  ```python
  #distinct()사용
  #e.g.
  #phone이 ‘011’로 시작하는 사람들의 나이를 중복 없이 조회
  User.objects.filter(phone__startswith='011').values('age').distinct()
  ```

  

- 표현식

  - 표현식 사용을 위해서는 `aggregate`를 알아야 한다.

  ```python
  from django.db.models import Sum,Avg,Max,Min
  
  모델명.objects.aggregate(표현식('column'))
  
  #e.g.
  User.objects.aggregate(Avg('age'))
  ```

  

- group by

  - annotate는 개별 item에 추가 필드를 구성한다.

  ```python
  모델명.objects.values('column').annotate(표시할 내용)
  ```

  



# 1:N

- 관계형 데이터베이스에서는 데이터들 사이에 관계를 맺을 수 있는데, 하나의 데이터가 여러개의 데이터와 관계를 맺을 경우, 두 데이터의 관계를 1:N의 관계라고 한다.

  

- FK(Foreign Key, 외래키)

  - 부모 테이블의 데이터를 참조하기 위한 키

  - 데이터와 데이터의 관계에서 한 쪽의 PK값은 다른 데이터로 넘어가면 FK값이 된다.

  - 일반적으로 N의 위치에 있는 데이터가 FK값을 가진다.

  - 유저 정보를 관리하는 db테이블에 각 유저가 작성한 글을 저장하는 것 보다는 게시글 정보를 관리하는 db테이블에 유저 정보를 저장하는 것이 더 낫다.
  
  - 만일 유저 정보를 관리하는 db테이블에서 각 유저가 글을 작성할 때마다 그 글에 대한 정보를 db테이블에 장한다면 유저 정보를 관리하는 테이블은 무한히 늘어나야 할 것이다.
  
    | user |          |                 |                 |                 |      | article |          |
    | ---- | -------- | --------------- | --------------- | --------------- | ---- | ------- | -------- |
    | id   | nickname | create_article1 | create_article2 | create_article3 | ...  | title   | content  |
  | 1    | name1    | title1,content1 | article         | ...             |      | title1  | content1 |
    | 2    | name2    | title2,content2 | article1        | ...             |      | title2  | content2 |
  
  - 반면에 게시글 정보를 관리하는 db테이블에 유저 정보를 저장한다면 게시글 마다 유저 정보만 추가시켜주면 된다. 
  
    | user |          |      | article |          |             |
    | ---- | -------- | ---- | ------- | -------- | ----------- |
    | id   | nickname |      | title   | content  | user_id(FK) |
  | 1    | name1    |      | title1  | content1 | 1           |
    | 2    | name2    |      | title2  | content2 | 2           |
  
  - 유저의 PK값을 게시글 테이블에 저장한다. 그리고 원래 테이블이 아닌 다른 테이블에서 사용되는 pk값을 fk값이라고 부른다(유저테이블의 pk값을 게시글 테이블에서 쓴다면 같은 값을 유저 테이블에서는 pk로, 게시글 테이블에서는 fk로 부른다).
  
  - 이 경우 한 명의 유저는 여러 개의 게시글을 작성할 수 있으므로 유저와 게시글 사이에 1:N의 관계가 성립한다고 볼 수 있다.



- 만일 1:N 관계를 가지는 두 모델을 설정할 때, N에 해당하는 모델을 설정하는 과정에서 1에 해당하는 모델에 관한 정보(id나 객체)를 포함하지 않으면 `IntergrityError`가 발생한다.



- django에서의 활용

  ```python
  # Creater 모델을 생성
  class Creater(models.Model):
      username = models.CharField(max_length=5)
  
  # POST 모델을 생성
  class Post(models.Model):
      title = models.CharField(max_length=10)
      content = models.TextField()
      creater = models.ForeignKey(Creater, on_delete=models.CASCADE)
      #ForeignKey는 첫 인자로 참고할 모델(Creater)을 설정한다.
      #두 번째 인자로 on_delete를 설정한다(필수값).
      #여기서 creater가 아닌 creater_id로 하는 것이 맞다고 생각할 수 있지만 필드가 ForeignKey 라면	   creater로 넘겨도 djnago에서 내부적인 처리를 통해 creater_id로 넘어가게 된다.
  ```

  - on_delete는 Django에서 모델을 구현할 때 데이터베이스 상에서 참조무결성을 유지하기 위해서 ForeignKeyField가 바라보는 값이 삭제될 때 해당 요소를 처리하는 방법을 지정하는 것이다. 필수값이다.
    - CASCADE : ForeignKeyField를 포함하는 모델 인스턴스(row)도 같이 삭제한다.
    - PROTECT : 해당 요소가 같이 삭제되지 않도록 ProtectedError를 발생시킨다.    
    - SET_NULL : ForeignKeyField 값을 NULL로 바꾼다. null=True일 때만 사용할 수 있다.

    - SET_DEFAULT : ForeignKeyField 값을 default 값으로 변경. default 값이 있을 때만 사용 가능   
    - SET() : ForeignKeyField 값을 SET에 설정된 함수 등에 의해 설정한다.  
    - DO_NOTHING : 아무런 행동을 취하지 않는다. 참조 무결성을 해칠 위험이 있어, 잘 사용되지는 않는다.

  ```python
  #4개의 reporter를 생성
  Creater.objects.create(username='파이리')
  Creater.objects.create(username='꼬부기')
  Creater.objects.create(username='이상해씨')
  Creater.objects.create(username='피카츄')
  
  #creater1에 파이리(1)를 넣는다.
  creater1=Creater.objects.get(pk=1)
  
  
  #post(N)를 생성한다.
  post1 = Post()
  post1.title = '제목1'
  post1.content = '내용1'
  # creater는 creater 오브젝트를 저장
  post1.creater = r1
  # creater_id는 숫자(INTEGER)를 저장
  # a1.reporter_id = 1 
  post1.save()
  
  post2 = Post.objects.create(title='제목2', content='내용2', creater=creater1)
  
  
  #1(파이리):N(posts)관계 활용
  #`post` 의 경우 `creater`로 1에 해당하는 오브젝트를 가져올 수 있다.
  #`creater`의 경우 `post_set` 으로 N개(QuerySet)를 가져올 수 있다(역참조).
  
  
  #글의 작성자
  post1 = Post.objects.get(pk=2)
  post1.reporter
  
  # 2. 글의 작성자의 username
  post1.creater.username
  
  # 3. 글의 작성자의 id
  post2.creater.id
  post2.creater_id
  
  # 4. 작성자(1)의 글
  creater1 = Creater.objects.get(pk=1)
  creater1.post_set.all()
  #전부 가져오는 것이 아닌 특정 조건을 충족하는 것들을 가져오고 싶다면
  creater1.post_set.filter() 
  
  #creater1.post_set.all()은 아래의 코드와 동일하다.
  #Post.objects.filter(creater=creater1)
  
  #creater1.post_set.all()와 Post.objects.filter(creater=creater1)의 기능은 동일하지만 느낌은 다를 수 있다.
  #creater1.post_set.all()가 보다 creater1이 작성한 포스트를 모두 가져온다는 느낌을 강하게 주며 활용에 있어서도 더 편하다.
  ```

  

- 실제 장코 코드에서의 활용

  - 게시글(1)과 댓글(N)의 1:N의 관계

  ```python
  #models.py
  from django.db import models
  
  class POST(models.Model):
      title = models.CharField(max_length=100)
      content = models.TextField()
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
  
  class Comment(models.Model):
      content=models.TextField()
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
      post = models.ForeignKey(Article, on_delete=models.CASCADE)
      #위처럼 post_id가 아닌 post로 넘기면 post_id로 등록된다.
  ```

  ```python
  #forms.py
  from django import forms
  from .models import POST, Comment
  
  class PostForm(forms.ModelForm):
      class Meta:
          model = Article
          fields = '__all__'
  
  
  class CommentForm(forms.ModelForm):
      class Meta:
          model = Comment
          # fields = '__all__'을 하면 post_id도 넘어가게 되는데 그럼 댓글을 입력할 때 				post_id도 입력하게 된다. 따라서 post는 넘기지 않는다.
          fields = ['content']
          # updated_at,created_at은 자동으로 넘어간다.
  ```

  ```python
  #views.py
  from django.shortcuts import render, redirect, get_object_or_404
  from django.views.decorators.http import require_POST
  from django.contrib.auth.decorators import login_required
  from .forms import PostForm, CommentForm
  
  #유저 정보를 넘기지 않을 때의 구조(기존의 구조)
  @require_POST
  @login_required
  def comments_create(request,post_pk):
      form = CommentForm(request.POST)
      post=get_object_or_404(Post,pk=post_pk)
      if form.is_valid():
          comment=form.save()
      return redirect('posts:detail', post.pk)
  
  
  
  #유저 정보를 넘길 때의 구조
  #아래에는 comments_create를 예로 들었지만 실제로 유저 정보를 저장해야 하는 모든 것들(게시글 작성, 게시글 수정)에도 해줘야 한다. 단, 게시글 수정의 경우 작성자가 아닌 사람이 게시글을 수정하는 경우는 없을 것이므로 하지 않아도 큰 문제는 없지만 만에 하나 오류가 발생할 수 있으므로 해준다.
  @require_POST
  @login_required
  def comments_create(request,post_pk):
      form = CommentForm(request.POST)
      post=get_object_or_404(Post,pk=post_pk)
      if form.is_valid():
          comment=form.save(commit=False)
          """
          comment=form.save()를 하는 것이 아니라 comment=form.save(commit=False)를 하는 이유		 는 만일 바로 db에 반영(save)을 하면, 아직 post_id값은 넣어준 적이 없으므로 NULL값이다. 따		  라서 오류가 발생하게 된다. 그렇다고 save()안하고 comment=form를 할 수도 없다. form은 			save()를 하기 전까지는 반환받는 값이 없으므로, save()를 해줘야 비로소 다른 값에 할당할 수 		  있다. 따라서 post를 반환은 하되 데이터베이스에 반영은 하지 않는 처리를 해줘야 하는데 그 처리		 가 바로 .save(commit=False)이다.
          """
          comment.post=post  #post_id에 post.pk를 넘겨준다.
          #굳이 comment.post_id=post.pk라고 적지 않아도 알아서 id값이 넘어가게 된다.
          comment.save()
      return redirect('post:detail', post.pk)
  
  
  #댓글을 표시하는 detail페이지(게시글과 공유한다)-잘못된 방법
  def detail(request, article_pk):
      post = get_object_or_404(Post, pk=post_pk)
      comments = Comment.objects.all()
      #기존에 하던 것 처럼 위와 같이 넘기면 어떤 게시글을 보던지 같은 댓글이 보이게 된다. 따라서 각 게	 시글에 작성된 댓글만을 넘겨야 하는데 이 방법으로는 그렇게 할 수 없다.
      comment_form=CommentForm()
      context = {
          'post': post,
          'comment_form':comment_form,
          'comments':comments,
      }
      return render(request, 'post/detail.html', context)
  
  
  #댓글을 표시하는 detail페이지(게시글과 공유한다)-옳은 방법
  def detail(request, article_pk):
      post = get_object_or_404(Post, pk=post_pk)
      comments = post.comment_set.all()  #post에 작성된 comment를 모두 comments에 할당
      # 아래와 같이 쓰는 것과 같다.
      # comments=Comments.objects.filter(article_id=article.id)
      comment_form=CommentForm() #댓글 입력 창은 게시글 내에 있어야 하므로 입력from도 넘긴다.
      context = {
          'post': post,
          'comment_form':comment_form,
          'comments':comments,
      }
      return render(request, 'post/detail.html', context)
  
  #혹은 위와 같이 comments = post.comment_set.all()로 넘기는 것이 아니라 post만 넘기고 html에서 따로 처리를 해주는 방법도 있다.
  def detail(request, article_pk):
      post = get_object_or_404(Post, pk=post_pk)
      comment_form=CommentForm()
      context = {
          'post': post,
          'comment_form':comment_form,
      }
      return render(request, 'post/detail.html', context)
  #위와 같이 post를 넘긴 후
  ```
  
  ```html
  <!--아래와 같이 post.comment_set.all으로 처리하면 된다.-->
  {% load bootstrap4 %}
  <h3>댓글</h3>
      {% for comment in post.comment_set.all %}
          <li>{{ comment.user.username }} : {{ comment.content }}</li>
      {% endfor %}
      <hr>
      <form action="{% url 'articles:comments_create' article.pk %}" method="POST">
          {% csrf_token %}
          {% bootstrap_form form %}
          <button class="btn btn-primary">작성</button>
      </form>
  
  <!--또는 detail함수에서 comments = post.comment_set까지만 넘겨받아 아래와 같이 쓸 수도 있다.-->
  
  {% load bootstrap4 %}
  <h3>댓글</h3>
      {% for comment in comments.all %}
          <li>{{ comment.user.username }} : {{ comment.content }}</li>
      {% endfor %}
      <hr>
      <form action="{% url 'articles:comments_create' article.pk %}" method="POST">
          {% csrf_token %}
          {% bootstrap_form form %}
          <button class="btn btn-primary">작성</button>
      </form>
  ```
  
  ```html
  <!--로그인 한 사용자와 글 작성자가 같은 사용자일 경우에만 특정 내용을 띄우는 방법-->
  <!--아무나 게시글을 삭제하게 해선 안되므로 아래와 같이 게시글의 유저와 요청을 보낸 유저가 같을 때에만 게시글 삭제 창을 띄우게 할 수 있다.-->
  
  <!--request.user에서 request는 생략 가능-->
  
  {% if article.user == request.user  %}
      <form action="{% url 'articles:delete' article.pk %}" method="POST">
          {% csrf_token %}
          <button class="btn btn-primary">삭제</button>
      </form>
  {% endif %}
  <!--==을 쓸 때는 반드시 좌우 한 칸씩을 띄워야 하며 띄우지 않을 경우 오류가 발생한다. 또한 == 대신 is를 사용 가능하다-->
  ```
  
  ```python
  #아래와 같이 함수 내에서 request.user, 즉 로그인한 유저의 정보를 사용하고자 한다면 @login_required를 붙여주는 것이 좋다. 로그인하지 않았을 경우 request.user에는 Anonymous 유저가 들어가게 되는데 자칫하면 에러가 발생할 수 있다. 
  
  @login_required
  def delete(request):
      request.user.delete()
      return redirect('articles:index')
  ```
  
  
  
- ERD: 데이터베이스 모델링에서 활용되는 다이어그램
  - 데이터 베이스 관계 차수(카디널리티): 데이터 사이의 논리적 관계
    - 1:1 관계(수직선): 주민등록 번호와 사람
    - 1:N 관계(까마귀 발이  있는 쪽이 N): 게시글(1)과 댓글(N), 댓글쪽에 까마귀발이 존재
  - 데이터베이스 관계선택사항/옵셔널리티
    
    - 관계를 선언하는 과정에서 필수(Mandatory)적인지, 선택(optional)적인지 표현
      - 모든 사람은 주민등록 번호를 가지고 주민등록번호가 없는 사람은 없으므로 각각 필수적
      - 게시글 입장에서 댓글은 필수가 아니나, 댓글 입장에서는 게시글이 필수다.
    
    - 필수적이면 수직선으로 표현, 선택적이면 O로 표현 선택적인 쪽에 O를 붙인다.
    
  - 만일 수직선이 2개면 그 데이터는 1:N 혹은 1:1의 관계에서 1이면서 필수적인 데이터라고 할 수 있다.



- 1:N 관계 보충

  ```python
  #models.py
  class User(models.Model):
      username = models.CharField(max_length=10)
      
  class Post(models.Model):
      title = models.CharField(max_length=100)
      content = models.TextField()
      user = models.ForeignKey(User, on_delete=models.CASCADE)
  
  class Comment(models.Model):
      content = models.TextField()
      article = models.ForeignKey(Post, on_delete=models.CASCADE)
      user = models.ForeignKey(User, on_delete=models.CASCADE)
  ```

  ```python
  from onetomany.models import User, Article, Comment
  
  # objects
  u1 = User.objects.create(username='파이리')
  u2 = User.objects.create(username='꼬북이')
  
  p1 = Post.objects.create(title='글1', user=u1)
  p2 = Post.objects.create(title='글2', user=u2)
  p3 = Post.objects.create(title='글3', user=u2)
  p4 = Post.objects.create(title='글4', user=u2)
  
  c1 = Comment.objects.create(content='글1댓1', post=p1, user=u2)
  c2 = Comment.objects.create(content='글1댓2', post=p1, user=u2)
  c3 = Comment.objects.create(content='글2댓1', post=p2, user=u1)
  c4 = Comment.objects.create(content='글4댓1', post=p4, user=u1)
  c5 = Comment.objects.create(content='글3댓1', post=p3, user=u2)
  c6 = Comment.objects.create(content='글3댓2', post=p3, user=u1)
  ```

  - 1번 유저가 작성한 글들

  ```python
  u1.article_set.all()
  ```

  - 2번 유저가 작성한 댓글의 내용을 모두 출력

  ```python
  for comment in u2.comment_set.all():
      print(comment.content)
  ```

  - 3번 글의 작성된 댓글의 내용을 모두 출력

  ```python
  for comment in p3.comment_set.all():
      print(comment.content)
  ```

  ```html
  {% for comment in article.comment_set.all %}
     {{ comment.content }}
  {% endfor %}
  ```

  - title이 글1인 게시글들

  ```python
  Post.objects.filter(title='글1')
  ```

  - 글이라는 단어가 들어간 게시글들

  ```python
  Post.objects.filter(title__contains='글')
  ```

  - 댓글들(N) 중에 제목이 글1인 게시글(1)에 작성된 댓글
    - 1:N 관계에서 1의 열에 따라서,  필터링하는 방법

  ```python
  Comment.objects.filter(article__title='글1')
  ```

  

  



# 미디어 파일 관리

- static과 차이는 static은 개발자가 사용한 이미지, css, js파일이고 media는 사용자가 사용하는 이미지 등의 파일이라는 것이다.



- 미디어 파일을 첨부하기 위해서는 우선 install을 해야 한다(c9에서는 하지 않아도 된다).

  ```bash
  $ pip install pillow
  ```



- ImageField가 존재한다(∴별도의 import를 필요로 하지 않는다)

  ```python
  class Mymodel(models.Model):
      image = models.ImageField()
  ```

  

- 만일 기존에 등록한 데이터가 있는 상태로 마이그레이션을 한다면 아래와 같은 문구가 터미널 창에 뜨게 된다,

  ```bash
  $ python manage.py makemigrations
  # default값 없이 NOT NULL Field를 지정했다는 문구로 기존에 등록한 데이터들에 filed값을 지정해 줘야 한다.
  You are trying to add a non-nullable field 'image' to article without a default; we can't do that (the database needs something to populate existing rows).
  # 2가지 옵션 제시
  Please select a fix:
   # 1) 기존에 등록한 데이터들에 디폴트 값을 터미널 창에서 지금 설정
   1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
   # 2) 종료하고 직접 models.py에 default 설정
   2) Quit, and let me add a default in models.py
  Select an option: 1
  Please enter the default value now, as valid Python
  The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
  Type 'exit' to exit this prompt
  #1 또는 2를 누르면 위의 명령을 수행한다.
  ```

  - 이 경우 데이터 파일을 전부 삭제하고 다시 migarate하거나(물론 서비스가 제공 중일 때 해선 안되고 개발중일 때 빠르고 확실한 처리를 위해 하는 방법이다.)

  - 아래와 같이 default값으로 blank를 주는 방법이 있다. 이렇게 하면 그동안 미디어 파일 없이 등록되었던 모든 데이터의 image필드가 공백으로 채워지게 된다.

    ```python
    class Mymodel(models.Model):
        image = models.ImageField(blank=True)
    ```

    

- 미디어 파일을 등록하고 보기 위해서는 아래의 두 부류의 파일을 수정해야 한다.

  - 미디어 파일을 등록하기 위해 수정해야 하는 파일

    - html(사진 입력받는 form이 있는 파일)

    ```html
    <!--게시글 등록 html-->
    <form action="" method="POST" enctype="multipart/form-data">
            {% csrf_token %}
            {% bootstrap_form form %}
            <button class="btn btn-primary">제출</button>
    </form>
    <!--위와 같이 enctype="multipart/form-data"을 추가해 줘야한다.-->
    ```

    - forms.py

    ```python
    #model을 변경했으므로 당연히 forms도 변경해야 한다.
    class ArticleForm(forms.ModelForm):
        class Meta:
            model = Article
            fields = ['title', 'content', 'image'] #image를 넘긴다.
    ```

    - views.py

    ```python
    def create(request):
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES)  #request.FILES를 추가
            if form.is_valid():
                article = form.save(commit=False)
                article.user = request.user
                article.save()
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm()
        context = {
            'form': form
        }
        return render(request, 'articles/form.html', context)
    ```

    

  - 미디어 파일을 보기 위해 수정해야 하는 파일

    - html(등록된 미디어 파일을 보여주는 파일)

    ```html
    <!--<img>태그를 활용하여 이미지를 출력-->
    <img src="{{ article.image.url }}">
    ```

    - settings.py

    ```python
    #미디어 파일을 저장하기 위한 루트 경로, media 폴더 부터 BASE_DIR까지의 경로를 입력
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    
    #저장된 미디어 파일에 접근하기 위한 경로
    MEDIA_URL = '/media/'
    ```
  ```
    
  - urls.py
    
    ```python
    # 아래 2개를 import 하고
    from django.conf import settings
    from django.conf.urls.static import static
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('articles/', include('articles.urls')),
  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)는 url이 넘어가서 html파일을 실행시킬 때 media파일도 함께 보내서(서빙) 실행시킨다는 것을 알려주는 것이다.
  ```

    

- `media`폴더는 최초로 미디어 파일을 등록하면 자동으로 생성된다.
  
  - 성공적으로 등록될 경우 루트에 미디어 파일이 자동으로 저장된다.
  - 등록될 당시에는 파일 명이 같아도 이미 루트에 동명의 파일이 있는 경우 나중에 등록된 파일의 이름을 바꿔서 저장하기에 이름이 겹칠 일은 없다.



- 이미지 조작

  - 이미지 파일의 크기를 조작할 수 있다.
  - 이미지를 업로드할 때 pillow를 install 해서 사용했으나 조작 할 때는 아래와 같이 추가적인 install이 필요

  ```bash
  $ pip install pilkit djnago-imagekit
  ```

  

  - models.py

  ```python
  from imagekit.models import ImageSpecField, ProcessedImageField
  from imagekit.processors import ResizeToFill, ResizeToFit, Thumbnail
  #ResizeToFill은 지정한 사이즈대로 정확하게 자른다(사진 일부가 잘릴 수도 있다).
  #ResizeToFit은 너비(가로)와 높이(세로) 중 더 긴 곳을 설정값으로 맞추고 더 짧은 쪽은 비율에 맞춘다. 따라서 이미지가 잘릴 일이 없다.
  #Thumbnail은 ResizeToFill과 유사하지만 더 깔끔해 보이게 자른다.
  
  
  class Article(models.Model):
      image = models.ImageField()
      #ImageField와는 달리 ImageSpecField는 DB에 저장되는 것이 아니다. 따라서 migrate를 할 필요      가없다. 다만 해당 모델의 멤버 변수로써 사용이 가능하다. 단, ImageField에서 받아온 사진을 조      작하는 것이므로 ImageField를 써줘야 한다.
      #ImageSpecField는 원본은 그대로 두고 잘라서 활용만한다.
      image_thumbnail = ImageSpecField(source='image',
                            processors=[Thumbnail(300, 300)],
                            format='JPEG',
                            options={'quality': 60})
      #source는 어떤 이미지를 자를 지를 정하는 것
      #processors는 어떤 방식으로 자를 지를 정하는 것 
      #format은 어떤 형식으로 반환할지를 정하는 것
      #options은 몇 %의 퀄리티로 표현 할지 정하는 것
      
      
      # ProcessedImageField는 원본 자체를 잘라서 저장한다.
      # ImageSpecField와 달리 migrate를 해야 한다.
      image = ProcessedImageField(
                            processors=[ResizeToFill(100, 50)],
                          format='JPEG',
                            options={'quality': 60})
  ```
  
  - html
  
  ```html
  <img src="{{ article.image_thumbnail.url }}">
  ```
  
  

  

 





# M:N

- 만일 게시글에 좋아요를 표시한다고 가정한다면 2개의 테이블이 필요하다. 좋아요를 누른 유저에 대한 정보를 저장할 User, 게시글에 대한 정보를 저장할 Article.

  - 특정 유저가 특정 게시글에 좋아요를 눌렀다는 정보를 어느 테이블에 저장해야 할 지가 문제가 될 수 있다.

  - aritcle테이블에 저장할 경우

    - 1번 방법

    | id   | title | content | user_id(fk) | 좋아요 누른 유저 |
    | ---- | ----- | ------- | ----------- | ---------------- |
    | 1    | 제목1 | 내용1   | 1           | 2,3              |
    | 2    | 제목2 | 내용2   | 2           | 1                |
    | 3    | 제목3 | 내용3   | 1           | 2,3              |
    | 4    | 제목4 | 내용4   | 3           | 2                |

    - 2번 방법

    | id   | title | content | user_id(fk) | 좋아요 누른 유저1 | 좋아요 누른 유저2 |
    | ---- | ----- | ------- | ----------- | ----------------- | ----------------- |
    | 1    | 제목1 | 내용1   | 1           | 2                 | 3                 |
    | 2    | 제목2 | 내용2   | 2           | 1                 |                   |
    | 3    | 제목3 | 내용3   | 1           | 2                 | 3                 |
    | 4    | 제목4 | 내용4   | 3           | 2                 |                   |

    - 1번 방법은 한 셀에 두 개 이상의 데이터가 들어갔으므로 불가능하고, 2번 방법은 다른 유저가 좋아요를 누를때 마다 열을 늘려야 하므로 비효율 적이다. 2번글은 좋아요를 누른 사람이 1명 뿐임에도 `좋아요 누른 유저2`라는 열까지 저장해야 한다.

  - user테이블에 저장할 경우

    - 역시 위와 마찬가지 이유로 불가능하다.

  - 따라서 좋아요에 대한 정보를 저장할 제3의 테이블을 생성해서 저장한다.

    - User와 제3의 테이블의 관계도 1:N이고 Article과 제3의 테이블의 관계도 1:N이다.
    - Article의 pk값과 User의 pk값을 가져온다.
    - 위에서 aritcle테이블에 저장 했던 좋아요 정보를 제 3의 테이블에 옮기면 다음과 같다.

    | id   | article_id(FK) | user_id(FK) |
    | ---- | -------------- | ----------- |
    | 1    | 1              | 2           |
    | 2    | 1              | 3           |
    | 3    | 2              | 1           |
    | 4    | 3              | 2           |
    | 5    | 3              | 3           |
    | 6    | 4              | 2           |

    

- django에서의 활용

  - 모델 생성

  ```python
  class Doctor(models.Model):
      name = models.CharField(max_length=10)
  
  class Patient(models.Model):
      name = models.CharField(max_length=10)
  
  #제 3의 모델
  class Reservation(models.Model):
      doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
      patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
  ```

  ```python
  #환자, 의사 생성
  d1 = Doctor.objects.create(name='dr.파이리')
  d2 = Doctor.objects.create(name='dr.꼬부기')
  
  p1 = Patient.objects.create(name='철수')
  p2 = Patient.objects.create(name='영희')
  
  #예약 생성
  Reservation.objects.create(doctor=d1, patient=p1)
  Reservation.objects.create(doctor=d1, patient=p2)
  Reservation.objects.create(doctor=d2, patient=p1)
  #위는 d1,p1 등의 객체를 넘기는 방법이고 아래와 같이 id값을 넘기는 방법도 있다.
  Reservation.objects.create(doctor_id=1, patient_id=1)
  Reservation.objects.create(docto_id=1, patient_id=2)
  Reservation.objects.create(doctor_id=2, patient_id=1)
  #또는 혼용도 가능
  Reservation.objects.create(doctor_id=2, patient=p1)
  
  #ref. 1:N 관계에서도 위와 같이 생성이 가능하다.
  #객체를 넘기는 방법
  Artice.objects.create(article.user = reques.user)
  #id값을 넘기는 방법
  Artice.objects.create(article.user_id = 1)
  ```

  - 의사1의 예약 목록

  ```python
  d1.reservation_set.all()
  ```

  - 환자1의 예약 목록

  ```python
  p1.reservation_set.all()
  ```

  - 1번 의사의 환자 출력

  ```python
  for reservation in d1.reservation_set.all():
      print(reservation.patient.name)
  ```

  

- 중개모델

  - `ManyToMany`필드를 사용, `through`옵션을 통해 중개 모델을 선언
  - `ManyToMany`필드를 추가할 경우 추가적인 migrate를 할 필요가 없다. `ManyToMany`필드는 DB에 영향을 주지 않기 때문이다.
  - `ManyToMany`필드두 모델 중 아무 쪽에나 설정하면 된다. 

  ```python
  class Doctor(models.Model):
      name = models.CharField(max_length=10)
  
  class Patient(models.Model):
      name = models.CharField(max_length=10)
      # M:N 필드, Reservation을 통해 Doctor에 접근한다는 의미
      doctors = models.ManyToManyField(Doctor, 
                                      through='Reservation')
  
  class Reservation(models.Model):
      doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
      patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
  ```

  - 의사, 환자 오브젝트 가져오기

  ```python
  p1 = Patient.objects.get(pk=1)
  d1 = Doctor.objects.get(pk=1)
  ```

  - 1번 환자의 의사 목록

  ```python
  #`ManyToManyField` 가 정의된 `Patient` 는 Doctor를 직접 참조
  p1.doctors.all()
  ```

  - 1번 의사의 환자 목록

  ```python
  #`Doctor` 는 직접 참조가 아니라 `Patient` 모델의 역참조.
  d1.patient_set.all()    
  ```

  

- `related_name` : 역참조

  - 역참조 컨벤션
    - 1:N의 역참조는 `단수형모델_set`.
    - M:N의 역참조는 `복수형 모델`을 사용한다.
    - 1:N에서도 M:N에서와 같이 `related_name`을 활용하여 역참조가 가능하지만 컨벤션에 어긋나므로 그렇게 하지 않는다.
  - 역참조의 기본값은: `모델명_set`이다. 즉, 지금까지 `_set`을 활용할 때마다 역참조를 하고 있었던 것
    - `related_name`은 다른 방법으로 역참조를 할 수 있게 해준다.
    - `related_name`은 복수형으로 쓴다(naming convention)
  - ManyToManyField를 설정하고 migration을 하면 `앱이름_소문자 모델이름_모델에 정의된 ManyToManyField이름`으로 테이블이 생성된다. 
    - 예를 들어 아래 앱 이름이` reservations`라고 하면
    - `reservations_patient_doctors`라는 테이블이 생성된다.
    - 해당 테이블의 필드는 `patient_id`, `doctor_id` 2개가 생성된다.

  ```python
  class Doctor(models.Model):
      name = models.TextField()
  
  class Patient(models.Model):
      name = models.TextField()
      #related_name옵션을 통해 역참조를 설정, 참조, 역참조는 모두 복수형으로 설정한다.
      #related_name은 필수 값은 아니지만, 꼭 필요한 상황이 존재.
      doctors = models.ManyToManyField(Doctor, 
                          through='Reservation',
                          related_name='patients')
  
  class Reservation(models.Model):
      doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
      patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
  ```

  - 1번 의사의 환자 목록

  ```python
  #related_name을 설정하기 전에는 위에서 본 것과 같이 d1.patient_set.all()로 가져와야 했으나 related_name을 설정했기에 아래와 같이 참조가 가능해졌다.
  
  d1.patients.all()    
  ```

  

  - 역참조가 반드시 필요한 상황

  ```python
  #settings.AUTH_USER_MODEL은 settings.py에 정의된 유저 모델을 참조한다.
  #그냥 User를 import 해서 써도 되지만, 만일 나중에 커스텀 유저를 만들어서 쓸 경우 User를 모두 커스텀 유저로 바꿔줘야 하는 불편함이 있다. 따라서 .AUTH_USER_MODEL을 쓴다.
  from django.conf import settings
  
  
  class Article(models.Model):
      title = models.CharField(max_length=100)
      content = models.TextField()
      user = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
      users = models.ManyToManyField(settings.AUTH_USER_MODEL)
      
  
  # user, users는 모두 settings.AUTH_USER_MODEL이라는 모델과 관계가 설정되어 있다.
  # 위 코드에 따르면 article을 기준으로 봤을 때
  # article.user에서의 user는 작성자를,
  # article.users의 users는 좋아요 누른 사람을 뜻한다.
  # 그런데 user(AUTH_USER_MODEL의 오브젝트)를 기준으로 보면
  # user.article_set을 하면 user가 작성한 글인지, 좋아요를 누른 글인지 구분이 되지 않는다.
  # 따라서 migrate를 할 경우 에러가 발생하게 된다. 따라서 아래와 같이 역참조를 설정해야 한다.
  
  class Article(models.Model):
      title = models.CharField(max_length=100)
      content = models.TextField()
      user = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
      like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                              related_name='like_articles')
  ```

  

- 실제 중개 모델을 만들지 않고 중개모델을 사용

  - 위에서는 `Reservation`이라는 실제 중개 테이블을 만들어 이를 활용했으나 실제 중개 테이블을 만들지 않고도 중개 모델 활용이 가능하다.

  - `ManyToManyField`를 설정하고 DB파일을 보면 중개 테이블이 생성된 것을 확인할 수 있다.

    - 중개 테이블 이름은 `앱명_모델명_``ManyToManyField를 설정한 필드명`이다. 

  - models.py

    ```python
    class Doctor(models.Model):
        name = models.TextField()
    
    class Patient(models.Model):
        name = models.TextField()
        doctors = models.ManyToManyField(Doctor,   #through='Reservation'삭제
                            related_name='patients')
        
    #Reservation 삭제
    ```

    

  - 기존 방식

    ```python
    # 예약 생성
    #d1,p1은 위에서 정의했다고 가정
    Reservation.objects.create(doctor=d1, patient=p1)
    ```

  - 새로운 방식

    ```python
    # 예약 생성
    #d1,p1은 위에서 정의했다고 가정
    d1.patients.add(p1) #add를 통해 추가를 하면
    
    d1.patients.all()  #의사와
    <QuerySet [<Patient:Patient object (1)>]>
    p1.doctors.all()   #환자 모두에 추가가 된다.
    <QuerySet [<Doctor:Doctor object (1)>]>
    
    
    #예약 삭제
    d1.patients.remove(p1) #remove를 통해 삭제를 하면
    
    d1.patients.all()  #의사와
    <QuerySet []>
    p1.doctors.all()   #환자 모두에서 삭제가 된다.
    <QuerySet []>
    ```

  

  - 단, 중개 모델을 꼭 만들어야 하는 경우가 존재한다.

    - 두 모델 모두에 정의되지 않은, 정의할 수 없는 필드가 필요할 경우

    ```python
    #예를 들어, 예약 날짜가 필요할 경우 예약 날짜는 Doctor,Patient 중 어느 쪽에 정의하기가 어렵다. 
    class Doctor(models.Model):
        name = models.TextField()
    
    class Patient(models.Model):
        name = models.TextField()
        doctors = models.ManyToManyField(Doctor, 
                            through='Reservation',
                            related_name='patients')
    
    #따라서 Reservation이라는 중개모델을 만들어 여기에 설정한다.
    class Reservation(models.Model):
        doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
        patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
       	date = models.DateTimeField()
    ```

    

- 좋아요 기능 구현하기

  ```python
  #models.py
  class Article(models.Model):
      title = models.CharField(max_length=100)
      content = models.TextField()
      user = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
      like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                              related_name='like_articles')
  ```

  ```python
  #urls.py
  app_name = 'articles'
  
  urlpatterns = [
      path('<int:pk>/like/', views.like, name='like'),
  ]
  ```

  ```python
  #views.py
  def like(request, pk):
      article = get_object_or_404(Article, pk=pk)
      # 좋아요를 누른적이 있다면, 즉 DB에 저장되어 있으면
      # if request.user in article.like_users.all():
      # 위 처럼 써도 되지만, 아래처럼 쓸 수도 있다.
      # .exists()는 True, False값을 반환한다.
      if article.like_users.filter(id=request.user.pk).exists():
          # 좋아요 취소
          article.like_users.remove(request.user)
      else:
          # 좋아요
          article.like_users.add(request.user)
      return redirect('articles:detail', article.pk)
  ```

  ```html
  <!--user가 article에 좋아요를 표시한 users 중에 있으면-->
  {% if request.user in article.like_users.all %}
  <a href="{% url 'articles:like' article.pk %}">좋아요 취소</a>
  {% else %}
  <a href="{% url 'articles:like' article.pk %}">좋아요</a>
  {% endif %}
  <p>{{ article.like_users.all|length }}명이 좋아합니다.</p>
  <!--혹은 아래와 같이 쓸 수도 있다.-->
  <p>{{ article.like_users.count }}명이 좋아합니다.</p>
  ```

  

- 좋아요 한 글을 모아서 보는 방법

  ```html
  <h3>좋아요한 글 목록</h3>
  {% for article in user.like_articles.all %}
      <a href="{% url 'articles:detail' article.pk %}">
          <p>{{ article.title }}</p>
      </a>
  {% endfor %}
  
  <!--만일 작성한 글을 보여주는 코드를 작성하고자 한다면 구조는 위와 같다.-->
  <h3>작성한 글 목록</h3>
  <!--단, 유저와 게시글의 관계는 1:N 관계이므로 user.article_set.all로 불러온다.-->
  {% for article in user.article_set.all %} 
      <a href="{% url 'articles:detail' article.pk %}">
          <p>{{ article.title }}</p>
      </a>
  {% endfor %}
  ```

  

- count와 len의 차이

  - django 공식 문서에서도 len()을 쓰는 것 보다 count()를 쓰는 것을 권장한다.

  ```python
  article.like_users.count()
  # 위 코드를 쿼리문으로 옮기면 다음과 같다.
  select count(*) from 쿼리셋의 개수를 센 결과값을 가져온다.
  
  len(article.like_users.all())
  # 위 코드를 쿼리문으로 옮기면 다음과 같다.
  select * from로 쿼리 셋을 결과값으로 가져온 뒤 그 길이를 센다.
  
  #즉, len은 일단 모든 오브젝트를 결과값으로 가져 온 뒤 그 길이를 쟤는 것이고 count는 모든 오브젝트를 가져오지 않고 미리 개수를 센 뒤 그 결과값을 가져오는 것이다. 따라서 count가 len에 비해 효율적이다.
  #단, 쿼리 셋을 불러올 필요가 없을 경우에는 len을 쓰는 것이 낫다.
  
  #추가로
  article.like_users.count()와
  article.like_users.all.count()는 같다.
  ```



- with

  ```html
  <!--article.like_users.all를 article_like_users라는 변수에 할당하고 with 블록 안에서 사용 가능하다. 즉 article.like_users.all가 쓰일 때 마다 전체 오브젝트가 호출이 되는데 with를 사용하면 캐시를 사용하는 것 같이 오브젝트를 변수에 저장하여 사용함으로써 매번 오브젝트가 호출되지 않아도 된다.-->
  {% with article_like_users=article.like_users.all %}
     {% if request.user in article_like_users %}
     <a href="{% url 'articles:like' article.pk %}">
        <i class="fas fa-heart fa-lg animated delay-1s" style="color: red;"></i>
     </a>
     {% else %}
     <a href="{% url 'articles:like' article.pk %}">
         <i class="far fa-heart fa-lg animated infinite bounce delay-1s" 						style="color: gray;"></i>
     </a>
     {% endif %}
  	<!--이런 with의 특성으로 인해 with를 쓸 경우 count보다 length를 쓰는 것이 더 효과적이다.-->
     <p>{{ article_like_users|length }}명이 좋아합니다.</p>
  {% endwith %}
  ```

  

- 팔로우 기능 구현하기

  - follower 필드를 만들어야 하므로 User 모델을 커스텀해서 사용해야 한다.
  - accounts/models.py

```python
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    followers = models.ManyToManyField(
            settings.AUTH_USER_MODEL,
            related_name='followings'
        )
#위 처럼 동일한 Model(위의 경우 User모델)간에 M:N 관계를 설정할 경우 테이블에는 `from_소문자 모델명_id`, `to_소문자 모델명_id`로 필드명이 설정된다.

#테이블명은 앱이름_user_follwers가 된다.
```

- accounts/urls.py 

```python
from django.urls import path
from . import views
  
app_name = 'accounts'
urlpatterns = [
    path('<int:pk>/follow/', views.follow, name='follow'),
]
```

  - views.py

  ```python
  def follow(request, pk):
      User = get_user_model()
      # 아래의 user는 팔로우 당하는 사람, 팔로우를 요청한 사람은 request.user
      user = get_object_or_404(User, pk=pk)
      if user != request.user:
          # 팔로우가 되어 있다면,
          if user.followers.filter(pk=request.user.pk).exists():
              # 삭제
              user.followers.remove(request.user)
          else:
            # 추가
              user.followers.add(request.user)
    return redirect('accounts:detail', user.pk)
  ```

  - detail.html(유저 프로필)

  ```python
  {% with user_followers=user.followers.all %}
      {% if request.user == user %}
          <a href="{% url 'accounts:update' %}">회원 수정</a>
          <form action="{% url 'accounts:delete' %}" method="POST">
              {% csrf_token %}
              <button class="btn btn-secondary">회원 탈퇴</button>
          </form>
      {% else %}
          <hr>
              {% if request.user in user_followers %}
                  <a href="{% url 'accounts:follow' user.pk %}">팔로우 취소</a>
              {% else %}
                  <a href="{% url 'accounts:follow' user.pk %}">팔로우</a>
              {% endif %}
      {% endif %}
      <p> {{ user_followers|length }}명이 팔로우</p>
      <p> {{ user.followings.count }}명을 팔로우</p>
  {% endwith %}
  ```







# Query 최적화

> https://docs.djangoproject.com/en/3.0/topics/db/optimization/ 참고

- 쿼리셋은 lazy하다.
  
  - 실제 실행되기 전까지는 작동하지 않는다.
  
  ```python
  # 아래 보면 q라는 쿼리셋을 만든 것 처럼 보이지만 실제 print되기 전까지 쿼리셋은 생성되지 않는다. 즉 sql문이 실제 실행되지 않는다.
  >>> q = Entry.objects.filter(headline__startswith="What")
  >>> q = q.filter(pub_date__lte=datetime.date.today())
  >>> q = q.exclude(body_text__icontains="food")
  
  # cf.이는 다르게 표현하면 아래와 같다(체이닝)
  q=Entry.objects.filter(headline__startswith="What").filter(pub_date__lte=datetime.date.today()).exclude(body_text__icontains="food")
  
  >>> print(q)  #이 때에야 쿼리셋이 생성된다(sql문이 실행된다.).
  ```
  
- sql문이 실제 실행되는 경우들
  
  - 반복
  - step이 있는 경우의 슬라이싱(ex.[3:8]이 아닌 [3:8:2]같은 경우)
  - print(repr)
  - len
  - boolean 연산을 할 때
  
- sql문은 한 번 실행되면, 그 이후부터는 동일한 쿼리셋을 매번 다시 불러오는 것이 아니라, 쿼리셋을 메모리에 저장하여 캐시처럼 활용한다(ref. {% with%}).



- 예시 데이터

    ```python
    # 테스트를 위한 fake data를 담은 파일
    import random
    from faker import Faker
    fake = Faker()

    for i in range(5):    #user는 5명
    User.objects.create_user(
    fake.user_name(),
    fake.email(),
    '1q2w3e4r!'
    )

    for i in range(1, 11):  #게시글 10개
    Article.objects.create(
    title=f'테스트 {i}글',
    content=fake.text(),
    user_id=random.choice(range(1, 6))
    )

    for j in range(1, 11):   #댓글은 게시글 1개당 10개(총 100개)
    Comment.objects.create(
    content=fake.sentence(),
    article_id=i,
    user_id=random.choice(range(1, 6))
    )
    ```



- 각종 최적화

   - views파일

     ```python
     #기존 함수
     def index(request):
         articles = Article.objects.order_by('-pk')
         context = {
             'articles': articles
         }
         return render(request, 'articles/index.html', context)
     
     
     #변경 함수
     #Count와 Prefetch를 import
     from django.db.models import Count, Prefetch
     
     def index(request):
         articles = Article.objects.order_by('-pk')
         
         
         # 1) 댓글 수
         # articles = Article.objects.annotate(comment_set_count=Count('comment')).order_by('-pk')
         
         '''
         annotate를 활용,
         위의 comment_set_count는 변수명이다. 아무렇게나 붙여도 된다.
         '''
         
         
         # 2) 게시글 작성자 이름 출력
         # articles = Article.objects.select_related('user').order_by('-pk')
         
         '''
         1(user):N(article)의 관계를 가지고 있는데 N입장에서 1에 대한 데이터를 같이 가지고 올 때 	select_related를 활용
         
         select_related는
         1:1, 1:N 관계에서 참조관계(N이 1을 찾을 때)일 때 사용, SQL JOIN을 통해 데이터를 가져온다.
         '''
         
         
         # 3) 댓글 목록
         # articles = Article.objects.prefetch_related('comment_set').order_by('-pk')
         
         '''
         1(article):N(comment)의 관계를 가지고 있는데 1입장에서 N에 대한 데이터를 가지고 올 때 	prefetch_related를 활용
        
         prefetch_related는
         M:N, 1:N관계에서 역참조관계(1이 N을 찾을 때)일 때 사용,  python을 통한 Join으로 데이터를 	  가져온다.
         '''
         
         
         # 4) 댓글 목록과 댓글 작성자 동시 출력
         articles = Article.objects.prefetch_related(
             	Prefetch(
             	    'comment_set',
         		    queryset=Comment.objects.select_related('user')
     		    )
         	).order_by('-pk')
         context = {
             'articles': articles
         }
         return render(request, 'articles/index.html', context)
     ```

  - html파일

    ```html
    <!--index.html-->
    
    <!--1)댓글 수 출력-->
    <!--기존함수 활용한 기존 html파일-->
    {% extends 'base.html' %}
    {% block body %}
        <h2 class="text-center">게시판 목록</h2>
        <a href="{% url 'articles:create' %}"><button class="btn btn-primary my-2">글 쓰기</button></a>
        {% for article in articles %}
            <h5>{{ article.title }}</h5>
            <p>{{ article.content }}</p>
    		<p>댓글 수 : {{ article.comment_set.count }}</p>
        {% endfor %}
    {% endblock %}
    <!--위 페이지를 출력하기 위해서 쿼리가 11번 발생하게 된다. 모든 게시글(Article 전체)을 불러오면서 1번 발생하게 되고 댓글 수를 count 하기 위한 쿼리들이 게시글 당 1번씩 생성되어 10번이 생성된다. 결국 총 11번의 쿼리가 생성된다.-->
    
    <!--N+1문제: 위와 같은 경우에 쿼리셋은 N+1번 생성되게 된다. 만일 게시글의 수(N)이 100이었다면 101번 쿼리셋이 생성되었을 것이다.-->
    
    
    
    <!--views.py에서 1)방식으로 게시글을 넘긴 후 변경한 html파일-->
    {% extends 'base.html' %}
    {% block body %}
        <h2 class="text-center">게시판 목록</h2>
        <a href="{% url 'articles:create' %}"><button class="btn btn-primary my-2">글 쓰기</button></a>
        {% for article in articles %}
            <h5>{{ article.title }}</h5>
            <p>{{ article.content }}</p>
            <p>댓글 수 : {{ article.comment_set_count }}</p>    
    		<!--views.py에서 넘어온 comment_set_count를 입력-->
        {% endfor %}
    {% endblock %}
    <!--Article 모델에 댓글의 개수라는 하나의 칼럼을 더 추가해 애초에 articles를 넘겨줄 때 댓글의 개수도 함께 가지고 와 모든 게시글을 불러오기 위한 1번의 쿼리 생성만 이루어진다.-->
    
    
    <!--2)게시글 작성자 이름 출력-->
    <!--함수를 2)로 변경한 후, html파일에선 추가적으로 수정할 것이 없다.-->
    {% extends 'base.html' %}
    {% block body %}
        <h2 class="text-center">게시판 목록</h2>
        <a href="{% url 'articles:create' %}"><button class="btn btn-primary my-2">글 쓰기</button></a>
        {% for article in articles %}
            <h5>{{ article.title }}</h5>
            <p>{{ article.content }}</p>
    		<h3>{{ article.user.username }}</h3> <!--작성자 출력-->
        {% endfor %}
    {% endblock %}
    <!--위 페이지를 출력하기 위해 쿼리는 11번 발생한다. 모든 게시글(Article 전체)을 불러오면서 1번 발생하게 되고, article 마다 하나씩 가지고 있는 user 정보를 출력하기 위해 게시글 당 1번씩 쿼리를 생성하여 총 11번 쿼리를 생성하게 된다.-->
    <!--views.py를 2)와 같이 수정하면 생성 횟수가 1번으로 줄어든다. 이는 JOIN을 활용했기 때문으로 JOIN은 두 개의 테이블을 합쳐서 하나의 테이블처럼 가지고 온다.-->
    
    
    <!--3)게시글별 댓글을 모두 출력-->
    <!--함수를 3)으로 변경한 후, html파일에선 추가적으로 수정할 것이 없다.-->
    {% extends 'base.html' %}
    {% block body %}
        <h2 class="text-center">게시판 목록</h2>
        <a href="{% url 'articles:create' %}"><button class="btn btn-primary my-2">글 쓰기</button></a>
        {% for article in articles %}
            <h5>{{ article.title }}</h5>
            <p>{{ article.content }}</p>
            {% for comment in article.comment_set.all %}
                <p>{{ comment.content }}</p>
            {% endfor %}
        </div>
        {% endfor %}
    <!--마찬가지 이유(전체 게시글을 불러오면서 1번, 10개의 댓글 불러오면서 10번)로 11번의 쿼리셋이 생성된다.-->
    <!--3)과 같이 수정 후에는 쿼리셋 생성이 2번으로 감소한다.-->
    
    
    
    <!--4) 댓글 목록과 댓글 작성자 동시 출력-->
    <!--함수를 4)로 변경한 후, html파일에선 추가적으로 수정할 것이 없다.-->
    {% extends 'base.html' %}
    {% block body %}
        <h2 class="text-center">게시판 목록</h2>
        <a href="{% url 'articles:create' %}"><button class="btn btn-primary my-2">글 쓰기</button></a>
        {% for article in articles %}
            <h5>{{ article.title }}</h5>
            <p>{{ article.content }}</p>
            {% for comment in article.comment_set.all %}
            	<p>{{ comment.user.username }} : {{ comment.content }}</p>
            {% endfor %}
        </div>
        {% endfor %}
    <!--이 경우 쿼리는 총 111번 발생한다. 모든 게시글을 불러오면서 1번, 각 게시글의 댓글을 불러오면서 10번, 댓글 마다 작성한 유저가 존재하므로 이들을 불러오는 데 또 10번이 생성되어 1+10+10*10으로 111번 발생한다.-->
    <!--개선 후에는 2개의 쿼리만 발생-->
    ```

    

- SQL JOIN 부가 설명

    - JOIN: 두 개의 테이블을 합쳐서 하나의 테이블로 가져온다.
    - 테이블, 데이터 생성

    ```sql
    -- 테이블 생성
    CREATE TABLE user(
    	id INTEGER PRIMARY KEY AUTOINCREMENT,
    	username TEXT
    );
    
    CREATE TABLE article(
    	id INTEGER PRIMARY KEY AUTOINCREMENT,
    	title TEXT,
        user_id integer NOT NULL REFERENCES user (id) DEFERRABLE INITIALLY DEFERRED
    );
    
    CREATE TABLE comment(
    	id INTEGER PRIMARY KEY AUTOINCREMENT,
    	content TEXT,
    	article_id integer NOT NULL REFERENCES article (id) DEFERRABLE INITIALLY DEFERRED
    );
    
    -- 데이터 생성
    INSERT INTO user (username) VALUES ('글쓴사람');
    INSERT INTO user (username) VALUES ('글안쓴사람');
    
    
    INSERT INTO article (title, user_id) VALUES ('1글무플', 1);
    INSERT INTO article (title, user_id) VALUES ('2글', 1);
    
    INSERT INTO comment (content, article_id) VALUES ('2글1댓', 2);
    INSERT INTO comment (content, article_id) VALUES ('2글2댓', 2);
    COMMIT;
    ```

    - LEFT OUTER JOIN(게시글 + 댓글)

    ```sql
    --artcle에 댓글 내용을 같이 가지고 오겠다
    SELECT * from article LEFT OUTER JOIN comment ON article.id=comment.article_id
    
    
    --위 명령어의 결과 테이블은 아래와 같다.
    id | title | user_id | id | content | article_id
    1  | 1글무플|    1    |    |          |
    2  | 2글   |    1    |  1  |  2글1댓  |  2
    3  | 2글   |    1    |  2  |  2글2댓  |  2
    --id | title | user_id |까지는 article의 테이블, id | content | article_id는 comment의 테이블로 두 테이블이 합쳐져 위와 같이 표시되게 된다.
    ```

    - INNER JOIN(게시글 + 사용자)

    ```sql
    SELECT * FROM article INNER JOIN user ON article.user_id = user.id;
    
    id |  title  | user_id | id | username
     1 | 1글무플  |    1    |  1  | 글쓴사람
     2 |   2글   |    1    |  1  | 글쓴사람
    ```

    

- 요약
  - 특정 모델과 관계를 갖는 추가적인 쿼리들(Comment,User)을 묶어서 가져오는 3가지 방법
    - anotate: 단순 계산 결과를 필드에 추가
    - select_related: 1:1 또는 N이 1을 찾을 때 사용
    - prefetch_related: M:N 또는 1이 N을 찾을 때







# REST API

- REST(Representational State Transfer):url 형식
  - http verb(method)에는 GET,POST,PUT/PATCH,DELETE가 있다. 
  - http verb+복수형 명사(혹은 복수형 명사+pk)로 구성되면 RESTful하다고 할 수 있다.



- API(Application Programming Interface):개발자용 접점, 일반 사용자를 위한 것이 아닌 개발자를 위한 것 
  - 프로그램 사이의 데이터 교환을 위한 접점을 뜻한다.
  - 결국 데이터 교환은 개발자의 요청에 의해 이루어지므로 개발자용 접점이라고 할 수 있다. 



- JSON(JavaScript Obeject Notation):자바스크립트 객체식 표기법, 저마다 제각각인 데이터 표기법을 표준화

  - chrome 확장프로그램 중 JSON 데이터의 가시성을 개선시켜주는` JSON Viewer`가 있다.
  - 예를 들어 청첩장을 만들기 위해 데이터를 받는다고 할 경우 사람마다 표기법이 제각각일 수 있다.

  ```python
  #1
  누가:영희가
  누구와:철수와
  언제:2020.05.15
  어디서: A호텔 예식장
      
  #2
  누가 => 영희가
  누구와 => 철수와
  언제 => 2020.05.15
  어디서 => A호텔 예식장
  
  #즉 동일한 키와 밸류를 연결하는 방식이 다 제각각이다.
  ```

  - html을 쓰지 못하는 이유: html은 태그가 정해져 있다.

  ```html
  <h1>청첩장</h1>
  
  <h2>영희</h2>
  <h2>철수</h2>
  <h2>2020.05.12</h2>
  <h2>A호텔 예식장</h2>
  
  <!--위 처럼 HTML은 태그가 정해져 있어 key를 표기할 수 없다.-->
  ```

  - 이러한 단점을 보완하기 위해서 JSON 이전에 XML(eXtended Markup Language)이 활용되었다.
    - XML은 태그에 제약이 없다.

  ```xml
  <제목>청첩장</제목>
  
  <누가>영희</누가>
  <누구와>철수</누구와>
  <언제>2020.05.12</언제>
  <어디서>A호텔 예식장</어디서>
  ```

  - JSON은 XML 보다 짧은 길이로 데이터를 받아올 수 있어 더 많이 사용되기 시작
    - 닫는 태그도 없을 뿐더러 XML은 HTML처럼 문서의 구조를 잡아줘야 해서 길이가 길어진다.
    - 데이터가 많아질 수록 길이 차이가 커진다.
    - 또한 빈번하게 데이터가 교환되는 웹의 특성상 약간의 길이 차이도 큰 차이를 불러올 수 있다.

  ```python
  #JSON은 Object가 아니라 문자열이다.
  #다만 프로그래밍 언어의 해석(파이썬은 load(), JS는 parse())에 의해 dict(파이썬의 경우), object(JS의 경우)로 해석되는 것이다.
  {
      "제목":"청첩장",
      "누가":"영희가",
      "누구와":"철수와",
      "언제":"2020.05.12",
      "어디서":"A호텔 예식장"
  }
  #JSON은 반드시 쌍따옴표를 써야 한다. 위 처럼 중괄호에 담아도 되고, 대괄호에 담아도 된다.
  ```



- 기존에는 사용자에게 요청을 받은 django가 MTV를 거쳐 사용자에게 HTML파일로 데이터를 제공했다면, 지금부터는 사용자는 Vue js에게 요청을 보내고 Vue js는 django에 사용자에게 받은 요청을 보낸다. django에서는 MV만 거치고 T는 거치지 않은 상태로 Vue js에게 JSON 형태의 데이터를 넘기게 되고 Vue js는 JSON 형태의 데이터를 사용자에게 HTML파일로 제공한다.
  - 기존: 사용자 -> django(MTV), django(MTV)->사용자
  - api: 사용자 -> Vue js -> django(MV),  django(MV) -> Vue js(T) -> 사용자

- Django에서의 활용

    ```python
    from django.views.decorators.http import require_GET
    from djnago.http.response import JsonResponse  #import하고
    

    #기존에 templates 파일을 통해 데이터를 보여주던 방식
    def article_list_html(request):
        articles = Article.objects.all()
    context = { 
            'articles': articles,
        }
        return render(request, 'board/article_list.html', context)
    
    
    # JSON 데이터를 넘기는 방식
    # 방법1:직관적인 코드
    @require_GET  #읽기만 하는 것이므로 적어주는 것이 안전하다.
def article_list_json_1(request):
        articles = Article.objects.all()
        #articles에는 쿼리셋이 들어가게 된다. 쿼리셋은 리스트(대괄호)도, 딕셔너리(중괄호)도 아니기에 바		로 JSON으로 넘길 수 없다.

        data = []  #따라서 리스트(대괄호)에 담아줘야 한다.
        for article in articles:
            data.append({
                'artcle_id':article.id,
                'title':article.title,
                'content':article.content
            })
            #위 과정을 거치면 리스트안에 articles 수 만큼의 딕셔너리가 담기게 된다.
        return JsonResponse(data,safe=False)
    	#templates 파일 사용하지 않으므로 JsonResponse를 사용하여 JSON으로 데이터를 보낸다.
        #safe=False는 data가 딕셔너리가 아닐 때 써줘야 하는 것이다. 위에서 data는 list이기 때		문이 써준 것이다. 그러나 대부분의 브라우저에서 safe=False를 쓰지 않아도 되도록 지원을 하기 때문		에 크게 신경쓸 부분은 아니지만 적지 않으면 django에서 에러를 출력하기에 써줘야 한다.
    
    #위 코드는 직관적이지만 필드가 많아질 경우 입력할 내용이 많아져 위와 같이 쓰지는 않는다.
    
    
    
    # 방법2:더 간단한 방법
    #django core serializer
    from djnago.http.response import HttpResponse
    
    @require_GET #CRUD중 GET과 과 관련있으므로 require_GET을 쓴다. 안 써도 되지만 쓰면 보다 엄밀한 코드가 된다.
    def article_list_json_2(request):
        from django.core import serializers
        articles = Article.objects.all()
    	
        data = serializers.serialize('json',articles)
        #aricles라는 데이터를 json으로 바꾸겠다는 의미, 이 과정을 거치면 data에는 JSON 데이터가 문자열		에 담기게 된다.
    
        return HttpResponse(data, content_type='application/json')
                                  #str이지만 json이라고 알려주는 것
    
    #위와 같이 하면 모두 string에 담겨 넘어가게 된다. JsonResponse는 dict나 list를 받는 것이지 str을 받는 것이 아니다. 따라서 JsonResponse가 아닌 HttpResponse를 쓴다.
    
    #보다 간략해지긴 했지만 보낼 필드를 직접 설정할 수 없다는 단점이 있다. 1번 방법의 경우 보낼 것만 선택해서 dict안에 담아주면 됐으나 2번 방법은 무조건 필드를 전부 보내야 한다.
    ```



- `serializer`: 직렬화, 데이터를 보내기 편하게 한 줄로 묶는 작업

  - 위 두 방법을 보완한 더 나은 방법
  - `djangorestframework`설치(줄여서 `drf`라고 부른다)

  ```bash
  #설치가 필요
  $ pip install djangorestframework
  ```

  - `INSTALLED_APPS`에 추가

  ```python
  #settings.py
  
  INSTALLED_APPS = [
      'rest_framework'
  ]
  ```

  - `serializers.py`생성
    - form과 구성이 유사

  ```python
  from rest_framework import serializers
  from .models import Article
  
  """
  forms.py 였다면
  
  from django import forms
  
  class ArticleForm(forms.Form):
      class Meta:
          model = Article
          fields = '__all__'
  """
  
  class ArticleSerializer(serializers.ModelSerializer):
      class Meta:
          model = Article
          fields = '__all__'
  ```

  - `views.py`에서 활용

  ```python
  #views.py
  
  from rest_framework.response import Response
  from rest_framework.decorators import api_view
  #api_view가 화면으로 보이게 해준다.
  
  # rest framework
  @api_view(['GET']) #쓰는게 좋은 것이 아니라 써야만 한다. 쓰지 않으면 에러 발생
  def article_list_json_3(request):
      articles = Article.objects.all()
      serializer = ArticleSerializer(articles, many=True)
      #many=True를 해주는 이유는 Article의 객체 하나가 아니라 모든 Article객체가 담긴 쿼리셋을 넘기	는 것이기 때문이다. 즉 복수의 객체를 넘길 때는 many=True를 써줘야 한다.
  
      # rest_framework 의 serializer 를 리턴하려면, rest_framework.response.Reponse를 써야 		한다.
      return Response(serializer.data)
  ```



- 1:N 관계일 때 `Serializer` 정의

  - `models.py`

  ```python
  class Artist(models.Model):
      name = models.CharField(max_length=100)
  
  class Music(models.Model):
      title = models.CharField(max_length=100)
      artist = models.ForeignKey(Artist,on_delete=models.CASCADE)
  ```

  - `serializers.py`

  ```python
  from rest_framework import serializers
  from .models import Artist,Music,Comment
  
  #전체 조회
  class ArtistSerializer(serializers.ModelSerializer):
      class Meta:
          model = Artist
          fields = ['id','name']
  
  #상세 조회
  class ArtistDetailSerializer(serializers.ModelSerializer):
  	#역참조
  	#한 가수에게 여러 곡이 등록될 수 있으므로 many=True를 쓴다.
      music_set = MusicSerializer(many=True)
      #혹시 다른 이름으로 하고 싶다면 아래와 같이 쓰면 된다.
      # songs =  MusicSerializer(source='music_set',many=True)
      #만일 models에 related_name을 설정했다면 source 뒤에는 설정한 related_name을 적으면 된다.
      
      music_count = serializers.IntegerField(source='music_set.count')
  
      class Meta:
          model = Artist
          fields= ['id','name','music_set','music_count']
          
          
  #상속을 받아서 쓰고 싶을 경우
  class ArtistDetailSerializer(ArtistSerializer):
      
      music_set = MusicSerializer(many=True)
      music_count = serializers.IntegerField(source='music_set.count')
      
      class Meta(ArtistSerializer.Meta): #ArtistSerializer의 Meta 클래스를 상속
        fields = ArtistSerializer.Meta.fields+['music_set','music_count']
          #model은 쓰지 않아도 되고 fileds는 상속 받은 fields에 새로 추가한 fields를 추가해서 넘기		   면 된다.
  ```
  
  











# 기타

## 투표 구현 방법

- models.py

```python
class Poll(models.Model):
    title = models.CharField(max_length=100)
    red = models.CharField(max_length=100)
    blue = models.CharField(max_length=100)
# red와 blue라는 2개의 선택지가 될 charfield를 넘겨주고

class Comment(models.Model):
    text = models.CharField(max_length=100)
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE)
    pick = models.BooleanField()
```

- forms.py

```python
from django import forms
from .models import Poll, Comment

class PollForm(forms.ModelForm):
    class Meta:
        model=Poll
        fields="__all__"

class CommentForm(forms.ModelForm):
    CHOICES = (        
        (False,'Blue'),
        (True,'Red'),
    )
    pick = forms.ChoiceField(choices=CHOICES)
	#choicefield를 설정
    class Meta:
        model=Comment
        fields=['text','pick']
```

- views.py

```python
#create 페이지와 index 페이지는 생략
def detail(request,pk):
    poll = Poll.objects.get(pk=pk)
    comments = poll.comment_set.all()
    comment_form = CommentForm()
    cnt=comments.count()
    if cnt:  #if 로 분기를 한 이유는 cnt가 0일 경우 0으로 나눠 zero divide에러가 발생하기 때문
        blue=comments.filter(pick=False).count()  #blue의 개수와
        red=cnt-blue    #red의 개수
        rred=100-int(blue/cnt*100)  #red의 비율과
        rblue=100-rred  #blue의 비율을 모두 넘겨준다.
    else:
        rred=0
        rblue=0
    context = {
        'poll':poll,
        'comments':comments,
        'comment_form':comment_form,
        'rred':rred,
        'rblue':rblue,
        'blue':blue,
        'red':red,
    }
    return render(request,"detail.html",context)

def comment_create(request,poll_pk):
    comment_form = CommentForm(request.POST)
    poll = Poll.objects.get(pk=poll_pk)
    if comment_form.is_valid():
        comment=comment_form.save(commit=False)
        comment.poll=poll
        comment.save()
    return redirect("poll:detail", poll_pk)
```

- detail.html

```html
<!DOCTYPE html>
{% load bootstrap4 %}
<!--bootstrap에서 progress-bar를 가져와 progress-bar로 표시해준다.-->
<html lang="kr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <title>Document</title>
</head>
<body>
    <h1>{{poll.title}}</h1>
    <p>{{poll.red}} VS {{poll.blue}}</p>
    <a href="{% url 'poll:index' %}">뒤로가기</a>
    <div class="progress">
      <div class="progress-bar progress-bar-striped" role="progressbar" style="width: {{rblue}}%" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"><div>{{poll.blue}}{{rblue}}%({{blue}}명)</div></div>
      <div class="progress-bar progress-bar-striped bg-danger" role="progressbar" style="width: {{rred}}%" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"><div>{{poll.red}}{{rred}}%({{red}}명)</div></div>
    </div>
    <h3>댓글</h3>
    <form action="{% url 'poll:comment_create' poll.pk %}" method=POST>
        {% csrf_token %}
        {% bootstrap_form comment_form %}
        <button>댓글쓰기</button>
    </form>

    {% for comment in comments %}
        <p>{{comment.text}}</p>
        <p>{{comment.pick}}</p>
        <hr>
    {% endfor %}
    <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
</body>
</html>
```







## Gravartar

> https://ko.gravatar.com/

- 프로필 사진 같이 사진을 넣을 수 있다.

- Gravatar 'API'는 인증이 필요하지 않으며, HTTP GET 요청 하나로 모든 것을 처리할 수 있다.

- 해시 생성

  - 이메일 주소의 공백을 제거

  ```python
  #아래와 같이 email을 선언할 때 문자열에 공백이 있어선 안된다.
  email = ' email@email.com '
  
  #strip() 함수를 사용하여 공백을 제거
  email.strip()
  ```

  - 대문자를 소문자로 변환

  ```python
  #아래와 같이 email을 선언할 때 문자열에 대문자가 있어선 안된다.
  email = 'Email@emAil.com'
  
  #lower()함수를 사용하여 모두 소문자로 변환
  email.lower()
  ```

  - 혹은 둘을 동시에 실행

  ```python
  email = ' Email@emAil.com '
  
  #strip() 함수를 사용하여 공백을 제거한 후 lower()함수를 사용하여 모두 소문자로 변환
  email.strip().lower()
  ```

  - md5 해시 알고리즘을 통해 그 해시값을 받아온다(굳이 공백을 제거하고 대문자를 소문자로 변환 한 이유가 이것이다. 공백이 하나라도 들어가거나 대문자가 하나라도 생기면 해시값이 완전히 바뀐다).

  ```python
  import hashlib
  
  email = ' email@email.com '
  email.strip().lower()
  
  hashlib.md5(email.encode('utf-8')).hexdigest()
  #위 코드의 결과로 해시값이 출력된다.
  ```

- 해시 등록(잘못된 방법)

  - Gravartar에 접속해서 My Gravatars-View rating으로 해시를 생성하고 그 주소를 아래와 같이 html파일에 붙여넣을 경우 어떤 계정으로 접속해도 동일한 이미지가 뜨게 된다.

    ```html
    <img src='https://s.gravatar.com/avatar/a22607938d8b959b522e30b5ae09d169?s=80'>
    ```

  - 따라서 아래와 같이 유저별로 다른 사진이 뜨도록 views.py에서 해시값을 넘겨줘야 한다.

  ```python
  #views.py
  import hashlib
  
  def index(request):
      articles = Article.objects.all()
      email_hash = hashlib.md5(request.user.email.encode('utf-				       	   8').strip().lower()).hexdigest()
      context = {
          'articles':articles,
          'email_hash':email_hash,
      }
  ```

  ```html
  <img src='https://s.gravatar.com/avatar/{{ email_hash }}?s=80'>
  <!--`s=`은 사이즈를 나타낸다.-->
  ```
  - 위와 같이 해시를 등록한다 하더라도 views.py에서 해시를 정의해준 페이지 이외의 페이지로 가면 넘겨준 페이지가 아닌 디폴트 페이지를 출력하게 된다.
  - 결론적으로 위와 같은 방법을 사용하지 않는다.

- 해시 등록(옳은 방법)

  - `templatetags`라는 폴더를 앱 내부에 생성
  - `templatetags`폴더 내부에 `__init__.py`파일과 `gravatar.py`라는 파일을 생성 
  -  `gravatar.py`에 아래와 같은 코드 작성
    - 이 방법은 template에서만 활용하고자 할 때 사용한다.

  ```python
  from django import template
  from django.template.defaultfilters import stringfilter
  
  register = template.Library()
  
  @register.filter
  @stringfilter
  def profile_url(email):  #profile_url은 그냥 함수명이므로 원하는 대로 정의하면 된다.
      #방법1.
      return email.hashlib.md5(request.user.email.encode('utf-				       	   8').strip().lower()).hexdigest()
  
  	#방법2. 아래와 같이 f-string 활용
  	return f"https://s.gravatar.com/avatar/{hashlib.md5(email.encode('utf-8').strip().lower()).hexdigest()}?s=80"
  ```

  - html파일에 적용

  ```html
  {% load gravatar %}
  <!--방법1을 사용한 경우-->
  <img src='https://s.gravatar.com/avatar/{{ request.user.email|profie_url }}?s=80'>
  
  <!--방법2를 사용한 경우(f-string 활용한 경우)-->
  <img src="{{ request.user.email|profile_url }}">
  ```

  - 이제 다른 페이지에서도 계속 같은 이미지가 뜨게 된다.
  - 혹은  `gravatar.py`에 작성하지 않고 아래와 같이 `models.py`의 model에서 `property`로 설정할 수 도 있다. `property`는 데이터베이스에 저장하고자 하는 속성 값이 아닌 추가적인 속성값을 저장한다.
    - 이와 같은 방법은 ,view와 template에서 모두 활용하고자 할때 사용한다. 

  ```python
  import hashlib
  from django.db import models
  from django.conf import settings
  from django.contrib.auth.models import AbstractUser
  
  # Create your models here.
  class User(AbstractUser):
      followers = models.ManyToManyField(
              settings.AUTH_USER_MODEL,
              related_name='followings'
          )
  
      @property #모델 클래스 내부에 property 선언
      def gravatar_url(self):
          return f"https://s.gravatar.com/avatar/{hashlib.md5(self.email.encode('utf-8').strip().lower()).hexdigest()}?s=80"  #f-string활용
  ```

  - html

  ```html
  {% load gravatar %}
  <img src='{{request.user.gravatar_url}}'>
  ```

- 디폴트 이미지 지정 방법

  ```html
  {% load gravatar %}
  <img src='https://s.gravatar.com/avatar/{{ request.user.email|profie_url }}?s=80&d=data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/'>
  <!--'d='뒤에 오는 이미지가 디폴트 값이 된다.-->
  ```

  



## faker

- `faker`설치

```bash
$ pip install faker
```

- `settings.py` 의 `INSTALLED_APPS`에 아래 코드를 추가

```python
'djnago_extensions'
```

- 이제 terminal 창에서 아래와 같이 사용이 가능하다.

```bash
#아래에서 예시로 든 .text(), .name()외에도 다양한 옵션이 있다.
>>>from faker import Faker
>>>f=Faker()
>>>f.text()
'Social common~~아무말~~'
>>>f.name()
'아무 이름'

#만일 Article에 새로운 데이터를 추가하고 싶다면 아래와 같이 입력해야 한다.
>>>Article.objects.create(title=f.text(), content=f.text(), ...)
#만일 100개의 fake데이터를 만들고 싶다면 100번 입력해야 한다.

#그러나 이를 더 쉽게 하는 방법이 있다.
```

- `models.py`

```python
from django.db import models
from faker import Faker  #import

f = Faker()  #Faker를 변수에 할당


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # n개의 더미 데이터를 만드는 클레스 메소드
    # cls는 클레스 메소드를 정의한 클래스가 들어가게 된다.
    @classmethod
    def dummy(cls,n): 
        for _ in range(n):
            cls.objects.create(
                title=f.name(),
                content=f.text()
            )
```

- 터미널 창에 다음과 같이 입력

```bash
>>> Article.dummy(10)

#10개의 더미 데이터가 생성된다.
```









