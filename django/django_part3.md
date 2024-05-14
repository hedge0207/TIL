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

  

- 만일 기존에 등록한 데이터가 있는 상태로 마이그레이션을 한다면 아래와 같은 문구가 터미널 창에 뜨게 된다.

  - 기존에 등록한 데이터에는 NOT NULL 속성을 지닌 `ImageField`의 값이 저장되어 있지 않아 NOT NULL임에도 NULL값을 가져 발생하는 에러다.

  ```bash
  $ python manage.py makemigrations
  # default값 없이 NOT NULL Field를 지정했다는 문구로 기존에 등록한 데이터들에 filed의 값을 지정해 줘야 한다.
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

> https://www.django-rest-framework.org/
>
> https://meetup.toast.com/posts/92참고

- REST(Representational State Transfer): URL을 사람마다 중구난방으로 적는 것을 막기 위한 규칙
  - http verb(method)에는 GET,POST,PUT/PATCH,DELETE가 있다. 
  - `http verb+복수형 명사(혹은 복수형 명사+pk)`로 구성되면 RESTful하다고 할 수 있다.
  - 기존에 django에서 url을 설정할 때 new,update, create 등을 썼던 것은 지금까지 개발 한 것이 REST API가 아니었기 때문이다. REST API를 개발하고자 한다면 `http verb+복수형 명사(혹은 복수형 명사+pk)`형식을 맞춰야 한다.



- API(Application Programming Interface):개발자용 접점, 일반 사용자를 위한 것이 아닌 개발자를 위한 것 
  - 프로그램 사이의 데이터 교환을 위한 접점을 뜻한다.
  - 결국 데이터 교환은 개발자의 요청에 의해 이루어지므로 개발자용 접점이라고 할 수 있다. 
  - 구성
    - 자원: URL
    - 행위: HTTP method
    - 표현

- `REST API`를 사용하는 이유: 결국 개발자에게 진정으로 필요한 것은 data뿐이다. template은 사용자에게 보여주기 위한 것이므로 굳이 html, Js, css를 쓰면서 django로 구현할 필요는 없다. 따라서 django를 통해 JSON 형식에 맞춰 데이터만 제공하는 서버를 구현하기 위해 사용하는 것이다. 여기서 데이터를 제공 받고 Vue js를 활용하여 사용자에게 template을 보여주게 된다.
  - data만 주고 받으면 되는 것이므로 가장 효율적으로 데이터를 주고 받을 수 있는 JSON을 사용한다.
  - api서버란 개발자들이 요청을 보내고 응답을 받아오는 서버를 말한다. 개발자가 URL을 통해 api서버로 요청을 보내면 서버는 요청에 대한 응답을 JSON 형식으로 보내게 된다.
  - 기존에는 사용자에게 요청을 받은 django가 MTV를 거쳐 사용자에게 HTML파일로 데이터를 제공했다면, 지금부터는 사용자는 Vue js에게 요청을 보내고 Vue js는 django에 사용자에게 받은 요청을 보낸다. django에서는 MV만 거치고 T는 거치지 않은 상태로 Vue js에게 JSON 형태의 데이터를 넘기게 되고 Vue js는 JSON 형태의 데이터를 사용자에게 HTML파일로 제공한다.
  - 기존: 사용자 -> django(MTV), django(MTV)->사용자
  - api: 사용자 -> Vue js -> django(MV),  django(MV) -> Vue js(T) -> 사용자



- REST API 디자인 가이드

  - URI는 정보의 자원을 표현해야 한다.
  - 자원에 대한 행위는 HTTP Method(GET, POST, PUT, DELETE)로 표현한다.

  ```
  GET /members/delete/1
  ```

  - 위와 같은 URI는 REST를 제대로 적용하지 않은 URI, delete는 자원을 표현하는데 중점을 두어야 하고 delete 같은 행위에 대한 표현은 method를 사용해아 한다. 수정하면 아래와 같다.

  ```
  DELETE /members/1
  ```



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



- Django에서의 활용

  ```python
  from django.views.decorators.http import require_GET
  from djnago.http import JsonResponse  #import하고
  
  
  #기존에 사용하던 코드, django에서 template까지 제공하는 코드
  def article_list_html(request):
      articles = Article.objects.all()
  	context = { 
          'articles': articles,
      }
      return render(request, 'board/article_list.html', context)
  
  
  # JSON 데이터를 넘기는 방식
  # 방법1:직관적인 코드
  # 이 코드를 작성 후 urls.py에 작성한 경로로 가면 JSON 형식의 데이터가 출력된다.
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
      #JsonResponse는 safe라는 flag옵션이 존재한다.
      #safe=False는 data가 딕셔너리가 아닐 때 써줘야 하는 것이다. 위에서 data는 list이기 때문이 써준 것이다. 그러나 대부분의 브라우저에서 			safe=False를 쓰지 않아도 되도록 지원을 하기 때문에 크게 신경쓸 부분은 아니지만 적지 않으면 django에서 에러를 출력하기에 써줘야 한다.
  
  #위 코드는 직관적이지만 필드가 많아질 경우 입력할 내용이 많아져 위와 같이 쓰지는 않는다.
  
  
  
  # 방법2:더 간단한 방법
  #django core serializer
  from djnago.http.response import HttpResponse
  
  @require_GET #CRUD중 GET과 과 관련있으므로 require_GET을 쓴다. 안 써도 되지만 쓰면 보다 엄밀한 코드가 된다.
  def article_list_json_2(request):
      from django.core import serializers
      articles = Article.objects.all()
  	
      data = serializers.serialize('json',articles)
      #aricles라는 데이터를 json으로 바꾸겠다는 의미, 이 과정을 거치면 data에는 JSON 데이터가 문자열에 담기게 된다.
  	
      #아래와 같이 JsonResponse를 사용할 경우 에러가 발생하지는 않지만 JsonResponse는 dict나 list를 받는 것이지 str을 받는 것이 아니기 때문에 		받은 문자열로 받은 데이터를 해석하지 못하고 데이터를 문자열 형태로 그대로 보내게 된다. 따라서 설정한 url로 들어가보면 하나의 문자열로 쭉 이어진 	데이터가 나오게 된다. 따라서 JsonResponse가 아닌 HttpResponse를 쓴다.
      return JsonResponse(data, safe=False)
      return HttpResponse(data, content_type='application/json')
                                #str이지만 json이라고 알려주는 것
  
  #보다 간략해지긴 했지만 보낼 필드를 직접 설정할 수 없다는 단점이 있다. 1번 방법의 경우 보낼 것만 선택해서 dict안에 담아주면 됐으나 2번 방법은 무조건 필드를 전부 보내야 한다.
  ```



- `serializer`: 직렬화, 데이터를 보내기 편하게 한 줄로 묶는 작업

  - 위 두 방법을 보완한 더 나은 방법
  - `django rest framework`설치(줄여서 `drf`라고 부른다)

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
          fields = '__all__'  #위에서 본 방법2와 달리 보내고자 하는 filed를 여기서 설정 가능하다.
   
  #아래와 같이 동일한 모델을 가지고도 서로 다른 필드를 넘기도록 정의하여 쿼리 낭비를 줄일 수 있다. 예를 들어 title만 필요한 경우에 위와 같이 전부 보내는 것은 비효율적이므로 아래와 같이 동일한 model에서 title 필드만 따로 넘기는 serializer를 작성하면 된다.
  class ArticleTitleSerializer(serializers.ModelSerializer):
      class Meta:
          model = Article
          fields = ['title']
  ```

  - `views.py`에서 활용(CRUD)
    - 기존에 C, U는 POST요청과 GET 요청을 동시에 받았어야 했다. GET요청을 받은 후 응답으로 form이 담긴 HTML파일을 보내고 사용자는 해당 양식에 맞게 작성하여 POST방식으로 그 데이터(요청)를 다시 서버에 보냈다. 서버는 해당 데이터를 받고 처리(유효성 검사 등)하여 save작업을 한 후 redirect로 detail페이지에 redirect요청을 보내면 해당하는 detail페이지(HTML파일)가 최종적으로 사용자에게 전송되었다.
    - 그러나 개발자가 요청을 보내는 rest_api에서는 template이 필요 없으므로  GET요청을 받은 후 응답으로 form이 담긴 HTML파일을 보내는 과정이 사라지고, 개발자들에게는 굳이 HTML파일을 보여줄 필요가 없으므로 redirect로 detail페이지에 redirect요청을 보내면 해당하는 detail페이지(HTML파일)가 최종적으로 사용자에게 전송되는 과정도 필요가 없어진다.
    - 결국 남는 것은 요청을 POST로 보내고 서버는 요청을 처리(유효성 검사 등) 후 저장하고 JSON 형식으로 응답을 돌려주거나, http상태 코드만 돌려주거나, 둘 다 돌려주는 등 사용자가 정의한 응답을 보낼 수 있다. 개발자가 아닌 일반 사용자에게 제공하는 것이 아니므로 상대적으로 응답 방식이 널널하다. 그러나 이 역시 보다 적합한 방식의 JSON 응답이 존재한다.
    - 그러나 요청을 어떻게 보낼 것이고 받아온 요청을 어떻게 꺼낼 것인지가 문제로 남는다. 기존에는 HTML파일에 data를 입력하고 해당 데이터를 전송하면 됐지만 HTML파일을 사용하지 않으므로 요청을 보낼 방법이 없다. 이를 해결해주는 것이 `Postman`으로 아래에서 살펴볼 것이다.

  ```python
  #views.py
  
  from rest_framework.response import Response
  from rest_framework.decorators import api_view
  #api_view가 화면으로 보이게 해준다.
  
  # rest framework
  
  #R:전체 조회
  @api_view(['GET']) #쓰는게 좋은 것이 아니라 써야만 한다. 쓰지 않으면 에러 발생, @require_GET과 유사한 역할
  def article_list_json_3(request):
      articles = Article.objects.all()
      serializer = ArticleSerializer(articles, many=True)
      #serializer는 기본적으로 하나의 객체가 들어 있을 것이라고 가정한다. 따라서 복수의 객체를 넘길 때는 many=True를 설정해줘야 한다.
      #Articles는 단일 객체 하나가 아니라 모든 Article객체가 담긴 쿼리셋을 넘기는 것이기 때문에 many=True를 설정해줘야 한다.
  
      # rest_framework 의 serializer 를 리턴하려면, rest_framework.response.Reponse를 써야 한다.
      return Response(serializer.data)
  
  
  #get_object_or_404는 404에러 페이지를 HTML로 출력해서 보여준다. 그러나 rest_api에서는 template을 쓰지 않으므로 이 에러도 JSON으로 보내는 방법이 있다.
  from django.shortcuts import get_object_or_404
  
  #R:단일 조회
  @api_view(['GET'])  #이 코드를 작성하면 에러도 JSON으로 보낸다.
  def post_detail(request,post_pk):
      post = get_object_or_404(Post,pk=post_pk)
      serializer = PostSerializer(post)  #post는 단일 객체이기 때문에 many=True를 해줄 필요가 없다.
      return Response(serializer.data)
  #위와 같이 작성한 후 존재하지 않는 post_pk를 url에 입력하면 아래와 같은 JSON 데이터를 확인할 수 있다.
  '''
  HTTP 404 Not Found
  Allow: OPTIONS, GET
  Content-Type: application/json 분명히 json 타입이다.
  Vary: Accept
  
  {
      "detail": "찾을 수 없습니다."
  }
  '''
  #C: 생성
  #아래 두 가지는 인증된 사용자인지를 검증하기 위한 것이다.
  from rest_framework.decorators import permission_classes
  from rest_framework.permissions import IsAuthenticated
  
  @api_view(['POST'])  #개발자용 서버에 GET은 필요 없다.
  @permisson_classes([IsAuthenticated])  #검증되지 않은 사용자일 경우 여기서 걸린다.
  def create_post(request):
      serializer = PostSerializer(data=request.data) #data에 요청으로 들어온 data를 넣는다.
      #아래와 같이 print해보면 내부에 어떤 것들이 들어가는지 알 수 있다.
      #둘 다 form-data가 들어올 경우 query dict형태로 담는다는 공통점이 있지만 차이점은 POST는 JSON 형태로 넘어온 데이터를 잡지 못하지만 data는 		JSON 형태로 넘어온 데이터를 parsing해서 딕셔너리(query dict는 아니다)에 담는다는 것이다. Postman으로 한 번은 form-data로, 한 번은 		  Json으로 요청을 보내보면 차이를 확인 가능하다.
      #따라서 data가 더 유연하다고 할 수 있다.
      print('POST: ', request.POST)  
      print('data: ', request.data)
      if serializer.is_valid(raise_exception=True): #raise_exception=True로 설정하면 유효성 검사가 실패할 때 리턴값으로 에러 내용을 준다.
          serializer.save(uesr=request.user) #uesr=request.user를 입력하면 요청을 보낸 유저 정보가 user에 들어가게 된다.
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
          #model은 쓰지 않아도 되고 fileds는 상속 받은 fields에 새로 추가한 fields를 추가해서 넘기면 된다.
  ```

  - user와 post의 1:N 관계 등록

  ```python
  #model 정의
  
  #accounts/models.py
  from django.contrib.auth.models import AbstractUser
  
  class User(AbstractUser):
      pass
  
  
  
  #articles/models.py
  from django.db import models
  from django.conf import settings
  
  class Article(models.Model):
      user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
      title = models.CharField(max_length=100)
      content = models.TextField()
  ```

  ```python
  #serializer 정의
  
  #accounts/serializers.py
  from django.contrib.auth import get_user_model
  from rest_framework import serializers
  
  User = get_user_model()
  
  class UserSerializer(serializers.ModelSerializer):
      class Meta:
          model = User
          fields = ['id','username']
  
    
  
  #articles/serializers.py
  from rest_framework import serializers
  from accounts.serializers import UserSerializer
  
  class ArticleSerializer(serializers.ModelSerializer):
      user = UserSerializer(required=False) 
      #required=False를 주면 is_valid()에서 user의 유무 검증을 패스한다. 단, create 함수에서 추가적인 처리를 해주지 않으면 NOT NULL 			CONSTRAINT FAILED 에러가 발생한다. 왜냐하면 Article모델을 정의할 때 user칼럼에 not null이 true라는 코드를 적지 않았기 때문이다.
      #즉, 장고에서 통과시켜줬다고 db에서도 통과되는 것은 아니며 또한 html에서도 추가적인 검증을 한다.
      class Meta:
          model = Article
          fields = '__all__'
  ```

  

- 여러 데이터를 넘기고자 할 경우 아래와 같이 하면 된다.

  ```python
  # 아래와 같이 dictionary 형식으로 묶어서 return 해주면 된다.
  @api_view(['GET'])
  def moviedetail(request, movie_pk):
      movie = Movie.objects.filter(docid=movie_pk)
      genres = Genre.objects.filter(movie_id=movie_pk)
      actors = Actor.objects.filter(movie_id=movie_pk)
      keywords = Keyword.objects.filter(movie_id=movie_pk)
      return Response({
          'movie':MovieSerializer(movie,many=True).data,
          'genre':GenreSerializer(genres, many=True).data,
          'actor':ActorSerializer(actors, many=True).data,
          'keyword':KeywordSerializer(keywords, many=True).data
          })
  ```

  

- Postman

  > https://www.postman.com/
  >
  > https://chrome.google.com/webstore/detail/postman-interceptor/aicmkgpgakddgnaphhhpliifpcfhicfo

  - 첫 번째 사이트로 접속하여 다운로드 후, 두 번째 사이트로 접속하여 확장 프로그램 설치, 확장 프로그램이 없으면 쿠키에 대한 정보가 없어 요청을 보낼 수 없다.
  - 프로그램 실행 후 우측 상단의 안테나 버튼을 클릭 후 `Cookies` - `Capture Cookies`를 on으로 - `Install Intercepter Briedge`클릭 - `Domain`에 https는 빼고 요청을 보내려는 url을 입력(ex.3fdd4...vfs.cloud9....amazonaws.com)후 추가 - request탭으로 가서 `Intercepter`클릭 후 `Capture Requests`를 on으로 변경
    - c9을 사용하는 것이 아닌 local에서 진행할 경우 이렇게 복잡한 과정을 거치지 않아도 된다.
  - 메인화면에서  `+` 버튼을 클릭하여 탭을 열고 요청을 보내고자 하는 url(`urls.py`에 작성한 url)을 `Enter request URL`창에 입력.
  - 데이터를 함께 넘기려면 URL 적는 input창 아래에 Body탭-`from-data` 클릭 후 key에는 변수명, Value에는 넣으려는 값을 넣으면 된다. 혹은 Body탭의 `raw` 클릭 후 타입을 JSON으로 바꿔  JSON 형식으로 보내도 된다. 
  - Body탭은 요청에 담아 보낸 data를 적는 곳이고, Headers는 요청을 보내는 사용자에 대한 정보를 적는 곳이다.

  ```python
  #실제 코드는 django-api_pract2참고
  #urls.py
  from django.contrib import admin
  from django.urls import path,include
  
  urlpatterns = [
      path('admin/', admin.site.urls),
      path('posts/',include('posts.urls')),
  ]
  
  #posts/urls.py
  from django.urls import path
  from . import views
  
  urlpatterns = [
      #url이 restful하지 않지만 편의상 아래와 같이 쓴다.
      path('post_check/',views.create_post)
  ]
  ```

  ```python
  #views.py
  
  from rest_framework.decorators import api_view
  from .models import Post
  
  # Create your views here.
  
  @api_view(['POST'])
  def post_check(request):
      print('wow')
      #만일 post 요청이 정상적으로 온다면 terminal창에 wow가 출력될 것이다.
  ```

## Django rest-auth

- templates이 django에서 분리되면 session 인증 방식의 유저 확인을 할 수 없다. 따라서 token을 활용하여 유저 확인을 해야 한다.



- 과정
  - 회원가입 시 Vue가 user 정보를 넘기면 django는 유효성 검사 후 User테이블에 유저 정보를 추가한다. 
  - 로그인 역시 마찬가지로 Vue가 user 정보를 넘기면 django는 유효성 검사 후 토큰을 발급하고 토큰값과 유저_id(pk값)를 key와 value 형태로 저장한다. 
  - django는 Vue에 token을 넘기고 Vue는 다음 요청 때부터는 request의 header에 django에서 받은 토큰을 함께 보낸다.(`Authorization`:`Token`  `토큰값` 형태로 만들어서 보낸다. Authorization이 key에 해당하고 Token이 value에 해당한다). django는 해당 토큰을 보고 유저를 인식한다.
  - 로그아웃을 하면 발급한 토큰을 삭제한다.



- 사용 방법

  >  사용하기 위해 drf를 설치해야 한다.

  ```bash
  $ pip install django-rest-framework
  ```
  
  > django-rest-auth 문서-1
  >
  > https://django-rest-auth.readthedocs.io/en/latest/index.html
  >
  
  > token기반의 authentication을 위한 문서-2
  >
  > https://www.django-rest-framework.org/api-guide/authentication/
  >
  > all-auth 문서는 django additional 파트 참고
  
  ```bash
  #로그인, 로그아웃에 필요
  $ pip install django-rest-auth
  #회원가입에 필요(혼자 회원가입을 하게 해주는 것이 아니라 위의 rest-auth를 함께 깔아야 회원가입이 가능하다.)
  $ pip install django-allauth
  ```
  
    - `settings.py`에 아래 코드를 추가(1번 문서의 내용과 2번 문서의 내용을 수정)
  
  ```python
  #1번 문서(Installaion 파트)에 있는 내용
  INSTALLED_APPS = (
      ...,
      #drf 관련 app
      'rest_framework',
      'rest_framework.authtoken', #토큰 기반의 인증에 필요한 app
      ...,
      #rest-auth 관련 app
      'rest_auth',
  )
  
  #2번 문서에 있는 내용 수정
  #토큰 기반으로 인증을 하기 위한 코드
  REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': [
          'rest_framework.authentication.TokenAuthentication',
          #원래 'rest_framework.authentication.SessionAuthentication',지만 세션 기반이 아닌 토큰 기반이므로 위와 같이 수정해준다.
      ]
  }
  ```
  
    - `프로젝트폴더/urls.py`에 아래 코드를 추가
  
  ```python
  #1번 문서에 있는 내용
  urlpatterns = [
      ...,
      path('rest-auth/', include('rest_auth.urls')),
      #위 경로로 들어갈 경우 404에러 페이지가 뜨는데 해당 페이지의 내용을 보면 rest-auth에서 할 수 있는 것들의 목록이 나온다.
  ]
  ```



- rest-auth는 app의 일종이므로 `models`를 가지고 있다. 따라서 migrate를 해줘야 한다.

  - 여기까지 완료하면 로그인이 가능해지고 login을 하면 token을 받을 수 있다.
  - token은 db.sqlite3의 `authtoken_token`테이블의 key 값에서 확인하거나 Postman으로 요청을 보내거나 rest-auth/login 경로에서 요청을 보냄으로써 확인 할 수 있다.

  - 회원 가입을 위해서는 아래 settings.py, urls.py에 아래 코드를 추가.

  ```python
  #settings.py
  
  #문서 1번의 코드
  INSTALLED_APPS = (
      ...,
      'django.contrib.sites',
      'allauth',
      'allauth.account',
      'rest_auth.registration',
  )
  
  SITE_ID = 1
  ```

  ```python
  #urls.py
  urlpatterns = [
      ...,
      path('rest-auth/', include('rest_auth.urls')),
      path('rest-auth/registration/', include('rest_auth.registration.urls')),
  ]
  #경로는 registration대신 쓰고 싶은 것(singup등)을 써도 된다(단, 당연히 include 내부는 건들면 안된다)
  ```

- allauth 역시 마찬가지로 app의 일종이므로 `models`를 가지고 있다. 따라서 migrate를 해줘야 한다.

  - 회원가입할 때 보내야 하는 데이터는 내부적으로 username, password1, password2로 지정되어 있다.



  - logout을 했을 때는발급한 token이 사라지게 해야 한다.
    - Postman에서 Body, Params 등이 있는 곳에 Headers 탭이 존재하는데 여기에 사용자 정보가 담기게 된다. 따라서 이곳의 key에 `Authorization`을 입력하고 value에 `Token 발급받은 토큰`을 입력한 후 전송을 누르면 유저 정보가 데이터와 함께 넘어가게 된다.
    - 로그아웃 요청을 보내고자 한다면 위와 같이 Headers에 로그아웃 하고자 하는 계정의 token을 함께 넘겨주면 로그아웃이 되면서 토큰이 삭제된다(토큰이 삭제되지 않아도 로그아웃이 성공적으로 처리되었다는 메세지가 출력되므로 반드시 token이 삭제되었는지 확인해 볼 것).



- rest-auth는 별도의 코드 없이도 기본 유저로 등록되어 바로 사용이 가능하다.
  - 본래 개발자가 User 모델을 커스텀 해서 사용할 경우 `settings.py`에 `AUTH_USER_MODEL = '앱이름.모델명'`코드를 추가해야 한다.
  - 그러나 `AUTH_USER_MODEL `의 기본값이 `AUTH_USER_MODEL = 'auth.User'`이다.
  - rest-auth는 앱 이름이 `auth`, 모델명이 `User`로 등록되므로 굳이 변경하지 않아도 된다.



- JWT: 단순한 무작위 문자열이 아닌 데이터가 담긴 토큰으로, 위조가 불가능한 사인도 포함된 토큰이기에  보안상으로도 안전하고 서버에 session, token 아무것도 남기지 않는다. 회원가입을 해도 id와 사인이 서버의 db에 저장되는 것이 아니라 토큰에 저장이되고  토큰에 저장된 user id와 사인을 토대로 검증을 거쳐 로그인이 이루어진다. 최근에 유행하는 인증 방식이다.



## CORS

- CORS(교차 출처 리소스 공유)

  > https://pypi.org/project/django-cors-headers/

  - 한 웹 사이트에서 다른 웹사이트로 비동기 요청을 보내는 것은 브라우저가 막고 있다. 따라서 비동기 요청을 보낼 경우 `has been blocked by CORS policy`가 포함된 에러가 발생한다.
  - 에러의 뒷 부분에 `No 'Access-Control-Allow-Origin' header is present on the requested resource.`와 같은 메세지를 확인 할 수 있는데,  `Access-Control-Allow-Origin`라는 header가 응답하는 곳에 존재해야 한다는 의미이다.
  - 응답하는 곳은 서버인 django이므로 아래코드를 추가해야 한다(위 공식문서에 코드 있음).
  
  ```bash
  $pip install django-cors-headers
  ```
  
  ```python
  #settings.py
  
  INSTAILLED_APP = [
      ...
      'corsheaders',
      ...
  ]
  
  #기본적으로 작성된'django.middleware.common.CommonMiddleware'보다 위에 작성해야 한다.
  MIDDLEWARE = [
      ...
      'corsheaders.middleware.CorsMiddleware',
      ...
  ]
  
  #CORS_ORIGIN_ALLOW_ALL=True 와 같이 작성하면 모든 사이트에서 오는 비동기 요청을 허용하는 것이다.
  
  CORS_ORIGIN_WHITELIST = [
      "https://example.com",  #허용할 주소를 입력
  ]
  ```



# django additional

### Social Login

- 다른 사이트 회원 정보로 가입하기

- 방법

  - allauth 설치

  > https://django-allauth.readthedocs.io/en/latest/installation.html

  ```bash
  $ pip install django-allauth
  ```

  - 위 사이트 참고해서 `settings.py`에 추가해야 할 것들을 추가

    ```python
    #아래 내용은 사이트 마다 조금 다르게 추가, 사이트별 내용은 공식문서의 provider 항목 참조
    
    INSTALLED_APPS = [
        'django.contrib.sites',
        'allauth',
        'allauth.account', #기존 모델로 관리하던 계정 관리
        'allauth.socialaccount', #소셜 로그인으로 가입한 계정 관리
        
        #이용하려는 소셜 서비스를 추가, 공식문서 참고, allauth.socialaccount.providers.까지는 동일하며 그 후 사용하려는 사이트를 입력하면 된다.
        'allauth.socialaccount.providers.google',
    ]
    
    SOCIALACCOUNT_PROVIDERS = {
          'google': {
            'SCOPE': [  #구글에서 가져올 정보 중에서 profile과 email을 가져오겠다.
                  'profile', 
                'email',
              ],
            'AUTH_RARAMS': {
                  'access_type':'online'
              }
          }
    }
    
    AUTHENTICATION_BACKENDS = (
          'django.contrib.auth.backends.ModelBackend',
          'allauth.account.auth_backends.AuthenticationBackend',
    )
    
    SITE_ID = 1
    ```
  
  - 이후 migrate를 실행한 후 admin 사이트로 들어가보면 우리가 추가한 적 없는 여러 테이블이 추가된 것을 볼 수 있다(admin.py를 수정하지 않아도 됨).
  
  - 전체 url을 관리하는 urls.py에 아래 코드를 작성
  
    ```python
    urlpatterns = [
        #직접 정의한 accounts url, 반드시 이 url을 먼저 적어야 한다.
        path('accounts/', include('accounts.urls')),
        #allauth에서 정의한 accounts url
        path('accounts/', include('allauth.urls'))
    ]
    #둘이 겹쳐도 상관 없는 이유는 accounts이후의 경로가 다르기 때문이다.
    #직접 작성한 url login,logout,signup등의 경로를 일반적으로 가지지만
    #allauth의 url은 google이라는 경로를 가지기에 알아서 분기가 된다.
    ```
  
  - login 양식을 제공하는 html에 아래의 코드를 입력
  
    ```html
    {% load socialaccount%}
    
    <a href="{% provider_login_url 'google' %}">로그인</a>
    ```
  
  - views.py에는 딱히 작성할 코드가 없다. 다만 로그아웃 함수는 정의를 해야 한다.



- Google API

  > https://console.developers.google.com/projectselector2/apis/dashboard?hl=ko&supportedpurview=project

  - 프로젝트 생성-사용자 인증 정보-동의 화면 구성-내부/외부 선택 후 만들기 클릭-애플리케이션 이름 설정 후 저장

  - 사용자 인증 정보로 다시 가서 `+사용자 인증 정보 만들기` 버튼 클릭-OAuth 클라이언트 ID

  - 승인된 자바스크립트 출처에는 로컬 주소를 적어도 된다(ex. https:127.0.0.1:8000).

  - 승인된 리디렉션 URL에는 아래와 같이 작성(로컬 주소 뒤의 내용은 임의로 작성하는 것이 아닌 정해진 양식대로 작성해야 한다)

    ```python
    로컬주소/accounts/google/login/callback/
    
    e.g.
    https:127.0.0.1:8000/accounts/google/login/callback/
    ```

  - 위 과정을 끝내면 클라이언트 ID와 클라이언트  보안 비밀번호를 받게 된다.

    - admin 사이트로 들어가서 소셜어플리케이션-소셜어플리케이션 추가로 이동
    - 제공자는 Google을 선택, 이름은 아무거나 넣고 키는 비워두면 된다.
    - 클라이언트 아이디와 비밀키에 각기 클라이언트 ID와 클라이언트  보안 비밀번호를 입력
    - 선택된 사이트에 사이트 추가
    - 저장



- 여기까지 완료하면 구글 로그인이 가능해진다. 그러나 로그인하면 allauth가 설정한 url인`accounts/profile`로 redirect 된다. accounts/profile이라는 경로를 설정해 준 적이 없으므로 오류가 발생하게 되고따라서 이 경로를 수정해줘야 한다.  

  - `settings.py`에 아래 코드를 입력

  ```python
  #login 했을 때 redirect 될 경로
  LOGIN_REDIRECT_URL = '원하는 경로'
  ```



- 소셜 계정으로 로그인할 경우 최초 로그인 할 때는 signup에 해당하는 작업이 일어나고 그 뒤부터는 login에 해당하는 작업이 일어난다. 
  - 처음 로그인 할 때 실제로 User모델에 추가가 된다. 



- allauth를 migrate하면 생성되는 여러 테이블 중에서 admin사이트에 보이는 테이블 중 실제로 User를 삭제할 수 있는 테이블은 존재하지 않는다. 따라서 admin사이트에서 user 정보를 삭제하고자 한다면 admin.py에 아래 코드를 입력해야 한다. 이후 admin사이트 내의 Accounts에서 삭제하면 된다.

  ```python
  from django.contrib import admin
  from django.contrib.auth import get_user_model
  
  admin.site.register(get_user_model())
  ```

  

- logout의 중요성

  - HTTP는 기본적으로 stateless하다. 따라서 로그인한 '상태'를 유지한다는 것은 불가능하다.
  - 서버에 요청을 보낼 때 마다  쿠키에 key값(sessionid)과 그에 해당하는 value(즉 sessionid)를 함께 보낸다. 이를 통해 사용자를 식별한다.
  - 따라서 sessionid를 알고 있다면 로그인 하는 것이 가능하다.
  - 예를 들어 `sessionid:xyz`이고 xyz에 저장된 사용자 id가 admin이라면 xyz를 활용하면 admin으로 로그인 된 상태가 될 수 있다.
    - 콘솔 창을 열고 Application탭-Cookies-우측 name에 `sessionid`를 입력하과  Value에 xyz를 입력하면 admin 으로 로그인 된다.
  - 악용될 여지가 있다.
  - 그러나 실제로 sessionid는 로그아웃 할 때 삭제되고 로그인 할 때마다 새롭게 갱신된다. 따라서 다른 사람이 내가 로그인 한 상태에서 sessionid를 보더라도 내가 로그아웃 후 다시 로그인 한다면 나는 새로운 sessionid를 발급받게 되고 다른 사람이 가진 나의 이전 sessionid는 아예 연결 된 id가 존재하지 않게 된다. 따라서 로그아웃만 한다면 sessionid로 인해 피해 볼 일은 없다고 보면 된다.





### 게시글 페이지 분할하기

```python
from django.core.paginator import Paginator  #import해주고

def article_list(request):
    articles = Article.objects.all()
    #뒤에 10이라는 숫자는 한 페이지당 몇 개를 보여줄 것인지 정하는 것
    paginator = Paginator(articles,10)  
    
    #몇 번 째 페이지를 볼 것인지는 쿼리스트링으로 요청이 들어온다. 따라서 request.GET.get('page') 으로 받아온다.
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number  #get_page는 Paginator의 메소드다.
    
    context = {
        'articles':aritcles,
        'page_obj':page_obj,
    }
    return render(reqeust,'articles/articles_list.html', context)
```

- HTML 파일에 출력하기

> https://pypi.org/project/django-bootstrap-pagination/
>
> https://docs.djangoproject.com/en/3.0/topics/pagination/

```html
{% for article in page_obj %} <!--articles가 아닌 page_obj를 쓴다-->
<li>{{ article.title }}</li>
{% endfor %}
```

- 여기까지 완료하면 쿼리스트링(`?`)뒤에 `page=숫자` 를 붙여 몇 번째 페이지를 볼 것인지를 정할 수 있다.
  - e.g. 127.0.0.1:8000/?page=1
- 개발자가 아닌 사용자가 사용할 수 있도록 하기 위해서는 HTML 파일을 아래와 같이 작성해줘야 한다.

```html
<!--django 공식문서 ver-->
<div class="pagination">
    <span class="step-links">
        {% if page_obj.has_previous %}
            <a href="?page=1">&laquo; first</a>
            <a href="?page={{ page_obj.previous_page_number }}">previous</a>
        {% endif %}

        <span class="current">
            Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
        </span>

        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">next</a>
            <a href="?page={{ page_obj.paginator.num_pages }}">last &raquo;</a>
        {% endif %}
    </span>
</div>
```

- bootstrap으로 더 깔끔하게 만들 수 있다.

  - 설치

  ```bash
  $ pip install django-bootstrap-pagination
  ```

  - settings.py에 추가

  ```python
  INSTALLED_APPS = [
      'bootstrap_pagination',
  ]
  ```

  - HTML 파일 작성

  ```html
  {% load bootstrap_pagination %}
  
  <!--{% bootstrap_paginate page_obj %} 까지가 기본형이다. 아래 코드는 여러 옵션이 있는 것이다.-->
  {% bootstrap_paginate page_obj range=10 show_prev_next="false" show_first_last="true" %}
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
  - `gravatar.py`에 아래와 같은 코드 작성
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

- `django_extension` 설치
  - shell plus를 쓰기 위한 것으로 쓰지 않을 것이라면 설치하지 않아도 되고 아래의 코드도 추가하지 않아도 된다.

```bash
$ pip install django_extensions
```

- `settings.py` 의 `INSTALLED_APPS`에 아래 코드를 추가(역시 shell plus를 쓰기 위한 것)

```python
'djnago_extensions'
```

- 이제 terminal 창에서 아래와 같이 사용이 가능하다.

```bash
$ python manage.py shell_plus
```

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
    # 둘 다 인자 이름이므로 아무렇게나 해도 된다.
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
#shell plus 실행 후
>>> Article.dummy(10)

#10개의 더미 데이터가 생성된다.
```

- bulk_create
  - faker를 쓰지 않고 더미데이터를 생성하는 방법, faker에 비해 속도가 느려 잘 사용하지 않는다.

```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    @classmethod
    def dummy(cls,n):
        articles = []
        for i in range(n):
            articles.append(cls(title=f'title-{i+1}', content=f'contentlorem ipsum')) #생성하고 싶은 대로 넣으면 된다.
        cls.objects.bulk_create(articles)
```

```bash
>>> Article.dummy(10)

#10개의 더미 데이터가 생성된다.
```







