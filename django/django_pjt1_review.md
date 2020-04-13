- tsettings.py

  ```python
  TEMPLATES = [
      {
          'BACKEND': 'django.template.backends.django.DjangoTemplates',
          'DIRS': [
              os.path.join(BASE_DIR,'templates')
              ],
       ...
  
  #처음에는 os.path.join(BASE_DIR,'templates')를 os.path.join(BASE_DIR,'community','templates')로 작성해 오류가 발생했다.
  #os.path.join(BASE_DIR,'templates')는 BASE_DIR부터 templates폴더까지의 경로를 작성하는 것이라는 것을 생각할 때 templates 폴더는 아무런 상위폴더도 없었으므로 둘 사이에 아무것도 적지 않는 것이 맞다. 그 밖에는 settings.py에서 어려웠던 부분은 없었다. 
  ```

  

- models.py

  ```python
  from django.db import models
  
  # Create your models here.
  class Review(models.Model):
      title = models.CharField(max_length=100)
      content = models.TextField()
      rank = models.IntegerField()
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now_add=True)
  
  #코드 자체는 거의 따라 치다시피 해서 별 어려울 것이 없었지만 created_at과 updated_at에 할당된 models.DateTimeField(auto_now_add=True)값이 어떻게 넘어가는지에 대한 이해가 잘 가지 않았다.
  #이는 뒤에 views.py에서 다시 쓸 것이다.
  ```

  

- urls.py

  ```python
  #상위urls.py
  from django.contrib import admin
  from django.urls import path, include
  
  urlpatterns = [
      path('admin/', admin.site.urls),
      path('community/', include('community.urls')),
  ]
  
  #하위urls.py
  from django.urls import path
  from . import views
  
  urlpatterns = [
      path('', views.review_list),
      path('new_review/', views.new_review),
      path('review_detail/', views.review_detail),
      path('create/',views.create),
      path('<int:pk>/',views.review_detail),
  ]
  
  #하위urls.py의 경우 아예 처음부터 작성해야하는 것이다 보니 import를 까먹고 쓰지 못해 오류가 발생했었다. 또한 상위urls.py에서도 include를 import하지 못해 오류가 발생했었다.
  
  #path('create/',views.create)의 경우 html파일을 렌더링 하지 않아도 url을 입력해 경로 처리가 가능하다는 것을 처음 알았다. 기존에는 create함수가 따로 렌더링하는 html파일이 없어 경로를 따로 설정하지 않았으나 계속 오류가 발생하여 혹시나 하는 마음으로 해봤는데 잘 작동되었다. 
  
  #path('<int:pk>/',views.review_detail)의 경우 선택옵션이었다. 시간이 없어 하지 못했는데 아마 시간이 있었어도 하지 못했을 것 같다.variable routing을 활용한 것이다.
  ```

  

- views.py

  ```python
  from django.shortcuts import render,redirect
  from .models import Review
  
  
  # Create your views here.
  def review_list(request):
      reviews=Review.objects.order_by('-id').all()
      context = {
          'reviews':reviews,
      }
      return render(request,'community/review_list.html',context)
  
  def create(request):
      title = request.GET.get('title')
      content = request.GET.get('content')
      rank = request.GET.get('rank')
      review=Review()
      review.title=title
      review.content=content
      review.rank=rank
      review.save()
      return redirect('https://3fdd8495a9bc4dd093821052501b61d9.vfs.cloud9.us-west-2.amazonaws.com/community/')
  
  
  def new_review(request):
      return render(request,'community/new_review.html')
  
  def review_detail(request, pk):
      review = Review.objects.get(id=pk)
      context = {
          'review':review,
      }
      return render(request,'community/review_detail.html',context)
  
  #from .models import Review를 쓰지 않아 오류가 발생했다.
  
  #시간이 가장 오래 걸린 파트였는데, 기존에 배운 내용에 따르면 input을 받아서 처리한 후 특정 페이지를 렌더링하였는데 이 경우에는 특정 페이지를 렌더링 하는 것이 아니라 처리한 후 review_list.html로 돌아가야 했는데 경로 설정을 어떻게 해줘야 할지 몰라서 많이 헤맸다.
  
  #처음에는 review_list.html로 돌아가야 한다니까 review_list 함수에 create함수의 내용을 합쳐서 작성했으나 오류가 발생했고 둘을 분리해서 작성했을 경우 create함수의 return을 어떻게 해줘야 할지 몰라 헤맸다. redirect를 알기 전이라 인터넷을 찾아본 후 이런 기능이 있다는 것을 알고 redirect로 처리를 해줬다.
  
  #create함수의 경우 다른 것들은 별 문제 없이 작성했으나 models.py에 있던 updated_at = models.DateTimeField(auto_now_add=True)를 어떻게 review오브젝트에 지정해줘야 할지 몰라 해맸는데 알고보니 별도의 지정 없이 models에만 정의를 해주면 바로 쓸 수 있는 것이었다.
  
  #review_detail의 경우 해도 되고 안해도 되는 선택조건이었는데 나는 하지 못했다. 이것과 관련된 수업을 전날 진행했으나 수업을 제대로 듣지 못해 작성하지 못했다. 작성한 내용은 이후 수업을 듣고 추가한 것이다.
  ```



- new_review.html

  ```html
  {% extends 'base.html' %}
  
  {% block body %}
  <h1>게시글 작성</h1>
  <form action="/community/create" method="GET">
      <div>tilte</div>
      <input type="text" name="title">
      <div>content</div>
      <div><textarea name="content"></textarea></div>
      <div>rank</div>
      <div><input type="number" name="rank"></div>
      <hr>
      <div><input type="submit" value="게시글 작성"></div>
  </form>
  {% endblock %}
  
  <!--
  form 태그에서 action값을 어떤 것을 줘야 할지 몰라서 헤맸다. 이는 views.py에서 헤맸기 때문으로 함수를 새로 작성할 때마다 계속 경로를 바꿔줘야 했고 상기했듯 렌더링하지 않는 함수가 경로가 될 수 있다는 것을 몰랐기 때문이다.
  ```

  

- review_list.html

  ```html
  {% extends 'base.html' %}
  
  {% block body %}
  <div class="ml-3 mr-3">
      {% for review in reviews %}
          <h3>{{review.title}}</h3>
          <div>content: {{review.content}}</div>
          <div>rank: {{review.rank}}</div>
          <div>작성시간:{{review.updated_at}}</div>
          <a href="/community/{{review.pk}}/">글 보러 가기</a>
          <hr>
      {% empty %}
          <h2> review가 없습니다. </h2>
      {% endfor %}
  </div>
  {% endblock %}
  
  <!--
  #다른 것은 크게 어렵지 않았으나 상기했듯 updated_at을 그냥 위와 같이 바로 써주면 된다는 것을 모르고 cteate함수에서 review 오브젝트에 지정해주려 해서 시간을 많이 버렸다.
  
  #<a href="/community/{{review.pk}}/">글 보러 가기</a>의 경우 선택조건이었던 review_detail을 구현하기 위한 것으로 전날 있었던 이와 관련된 수업을 듣고 추가한 것이다. 경로상에 {{}}가 들어갈 수 있다는 것을 처음 알게 되었다.
  ```

  

- 정리

> 정리할 것은 크게 2가지로 내가 구현하지 못했던 `review_detail`과 시간을 오래 잡아먹었던 `views.py`의 create함수와 review_list 함수이다.



- `views.py`

  ```python
  #ver1
  #처음 구현한 모습은 아래와 같이 review_list함수 안에 현재의 review_list함수와 create함수를 합쳐서 구현한 것이었다. 그러나 계속 오류가 발생해 둘로 나눠서 구현했는데 
  def review_list(request):
      title = request.GET.get('title')
      content = request.GET.get('content')
      rank = request.GET.get('rank')
      review=Review()
      review.title=title
      review.content=content
      review.rank=rank
      review.save()
      reviews=Review.objects.all()
      context = {
          'reviews':reviews,
      }
      return render(request,'community/review_list.html',context)
  
  
  
  #ver2
  #이 버전은 create함수에 리턴이 존재하지 않았다. 작동은 했으나 글을 작성해도 작성한 글이 review_list.html에 나타나지 않았다.
  def review_list(request):
      reviews=Review.objects.order_by('-id').all()
      context = {
          'reviews':reviews,
      }
      return render(request,'community/review_list.html',context)
  
  def create(request):
      title = request.GET.get('title')
      content = request.GET.get('content')
      rank = request.GET.get('rank')
      review=Review()
      review.title=title
      review.content=content
      review.rank=rank
      review.save()
     
  
  #ver3
  #이때는 리턴을 줘야할 것이라 생각해 review_list.html이 렌더링하도록 설정했지만 이 역시 작성한 내용이 표시되지 않았고 고민하던 끝에 명세에서 redirect라는 표현을 발견해 구글링하여 완성하게 되었다.
  def review_list(request):
      reviews=Review.objects.order_by('-id').all()
      context = {
          'reviews':reviews,
      }
      return render(request,'community/review_list.html',context)
  
  def create(request):
      title = request.GET.get('title')
      content = request.GET.get('content')
      rank = request.GET.get('rank')
      review=Review()
      review.title=title
      review.content=content
      review.rank=rank
      review.save()
      return render(request,'community/review_list.html',context)
  ```

  

- review_detail

  - 아예 구현을 하지  못했기에 상세히 설명하려 한다. 게시글 목록에서 게시글을 클릭하면 해당 게시글 페이지로 이동하는 기능이었는데 순차적으로 살펴보면

  - 첫 번째로 아래와 같이 경로로 이동을 시켜야 한다.  아래 코드는 반복문이 돌면서 오브젝트들을 차례로 출력하는 것이다.

    ```html
    {% extends 'base.html' %}
    
    {% block body %}
    <div class="ml-3 mr-3">
        {% for review in reviews %}
            <h3>{{review.title}}</h3>
            <div>content: {{review.content}}</div>
            <div>rank: {{review.rank}}</div>
            <div>작성시간:{{review.updated_at}}</div>
            <a href="/community/{{review.pk}}/">글 보러 가기</a>
            <hr>
        {% empty %}
            <h2> review가 없습니다. </h2>
        {% endfor %}
    </div>
    {% endblock %}
    <!--
    {{review.pk}}에서 review.pk에는 반복문이 돌때마다 순서대로 id값이 들어가게 되는데 이 아이디 값이 들어간 경로를 받아줄 urls.py를 작성해야 한다.
    ```

  - urls.py

    ```python
    from django.urls import path
    from . import views
    
    urlpatterns = [
        ...
        path('<int:pk>/',views.review_detail),
    ]
    #variable routing을 활용해 위에서 넘어온 경로를 받아 views에서 review_detail함수를 실행시키도록 한다.
    ```

  - views.py

    ```python
    def review_detail(request, pk):
        review = Review.objects.get(id=pk)
        context = {
            'review':review,
        }
        return render(request,'community/review_detail.html',context)
    
    #인자로 request뿐 아니라 pk도 받아(urls.py에서 작성한 <int:pk>에서 pk가 만일 abc라면 인자도 pk가 아닌 abc가 된다.) Review 클래스의 모든 objects 중에서 pk와 id가 동일한 object를 뽑아 그것을 review에 담고 그것을 context에 담아 넘긴다. 
    ```

  - review_detail.html

    ```html
    {% extends 'base.html' %}
    
    {% block body %}
        <h1>{{ review.pk }}</h1>
        <p>{{ review.content }}</p>
    
    {% endblock %}
    <!--
    context에 담겨 넘어온 review는 오브젝트이므로 models.py에서 정의한 대로 title, contemt, rank 등이 지정되어 있을 것이다. 따라서 review.content는 review오브젝트에 저장된 content를 출력하게 될 것이다. 
    ```

    

  

