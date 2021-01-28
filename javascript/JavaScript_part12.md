# REST API

- REST(Representational State Transfer)
  - HTTP/1.0과 1.1의 스펙 작성에 참여하였고, 아파치 HTTP 서버 프로젝트의 공동설립자인 로이 필딩 (Roy Fielding)의 2000년 논문에서 처음 소개되었다.
  - 발표 당시의 웹이 HTTP의 설계 상 우수성을 제대로 사용하지 못하고 있는 상황을 보고 웹의 장점을 최대한 활용할 수 있는 아키텍쳐로서 REST를 소개하였고 이는 HTTP 프로토콜을 의도에 맞게 디자인하도록 유도하고 있다.
  - REST의 기본 원칙을 성실히 지킨 서비스 디자인을 “RESTful”이라고 표현한다.



- REST API 중심 규칙

  - 가장 중요한 기본적인 규칙 두 가지는 **URI는 자원을 표현하는 데에 집중**하고 **행위에 대한 정의는 HTTP Method를 통해 해야 한다**는 것이다.

  - URI는 정보의 자원을 표현해야 한다.

    - 리소스명은 동사보다는 명사를 사용한다. 
    - URI는 자원을 표현하는데 중점을 두어야 한다. 
    - get 같은 행위에 대한 표현이 들어가서는 안된다.

    ```
    # bad
    GET /getTodos/1		// 행위 표현이 들어갔다.
    GET /todos/show/1   // 행위 표현이 들어갔다.
    
    
    # good
    GET /todos/1
    ```

  - 자원에 대한 행위는 HTTP Method로 표현한다.

    ```
    # bad
    GET /todos/delete/1
    
    # good
    DELETE /todos/1
    ```

    

- HTTP Method

  - 주로 5가지의 Method를 사용하여 CRUD를 구현한다.

  | Method | Action         | 역할                    | 페이로드(데이터) |
  | ------ | -------------- | ----------------------- | ---------------- |
  | GET    | index/retrieve | 모든/특정 리소스를 조회 | X                |
  | POST   | create         | 리소스를 생성           | O                |
  | PUT    | replace        | 리소스의 전체를 교체    | O                |
  | PATCH  | modify         | 리소스의 일부를 수정    | O                |
  | DELETE | delete         | 모든/특정 리소스를 삭제 | X                |

  

- REST API의 구성

  - 자원(Resource), 행위(Verb), 표현(Representations)의 3가지 요소로 구성된다.
  - REST는 자체 표현 구조(Self-descriptiveness)로 구성되어 REST API만으로 요청을 이해할 수 있다.

  | 구성 요소       | 내용                    | 표현 방법             |
  | --------------- | ----------------------- | --------------------- |
  | Resource        | 자원                    | HTTP URI              |
  | Verb            | 자원에 대한 행위        | HTTP Method           |
  | Representations | 자원에 대한 행위의 내용 | HTTP Message Pay Load |

  



# SPA

- SPA(Single Page Application)
  - 단일 페이지 애플리케이션(Single Page Application, SPA)는 모던 웹의 패러다임이다. 
  - SPA는 기본적으로 단일 페이지로 구성되며 기존의 서버 사이드 렌더링과 비교할 때, 배포가 간단하며 네이티브 앱과 유사한 사용자 경험을 제공할 수 있다는 장점이 있다.
  - link tag를 사용하는 전통적인 웹 방식은 새로운 페이지 요청 시마다 정적 리소스가 다운로드되고 전체 페이지를 다시 렌더링하는 방식을 사용하므로 새로고침이 발생되어 사용성이 좋지 않다. 그리고 변경이 필요없는 부분를 포함하여 전체 페이지를 갱신하므로 비효율적이다.
  - SPA는 기본적으로 웹 애플리케이션에 필요한 모든 정적 리소스를 최초에 한번 다운로드한다. 이후 새로운 페이지 요청 시, 페이지 갱신에 필요한 데이터만을 전달받아 페이지를 갱신하므로 전체적인 트래픽을 감소할 수 있고, 전체 페이지를 다시 렌더링하지 않고 변경되는 부분만을 갱신하므로 새로고침이 발생하지 않아 네이티브 앱과 유사한 사용자 경험을 제공할 수 있다.
  - 모바일의 사용이 증가하고 있는 현 시점에 트래픽의 감소와 속도, 사용성, 반응성의 향상은 매우 중요한 이슈이다. SPA의 핵심 가치는 **사용자 경험(UX) 향상**에 있으며 부가적으로 애플리케이션 속도의 향상도 기대할 수 있어서 모바일 퍼스트(Mobile First) 전략에 부합한다.
  - 모든 소프트웨어 아키텍처에는 trade-off가 존재하며 모든 애플리케이션에 적합한 은탄환(Silver bullet)은 없듯이 SPA 또한 구조적인 단점을 가지고 있다. 대표적인 단점은 아래와 같다.
    - SPA는 웹 애플리케이션에 필요한 모든 정적 리소스를 최초에 한번 다운로드하기 때문에 초기 구동 속도가 상대적으로 느리다. 하지만 SPA는 웹페이지보다는 애플리케이션에 적합한 기술이므로 트래픽의 감소와 속도, 사용성, 반응성의 향상 등의 장점을 생각한다면 결정적인 단점이라고 할 수는 없다.
    - SPA는 서버 렌더링 방식이 아닌 자바스크립트 기반 비동기 모델(클라이언트 렌더링 방식)이다. 따라서 SEO(검색엔진 최적화)는 언제나 단점으로 부각되어 왔던 이슈이다. 하지만 SPA는 정보의 제공을 위한 웹페이지보다는 애플리케이션에 적합한 기술이므로 SEO 이슈는 심각한 문제로 볼 수 없다. Angular 또는 React 등의 SPA 프레임워크는 서버 렌더링을 지원하는 SEO 대응 기술이 이미 존재하고 있어 SEO 대응이 필요한 페이지에 대해서는 선별적 SEO 대응이 가능하다.



- Routing
  - 라우팅이란 출발지에서 목적지까지의 경로를 결정하는 기능이다. 
    - 애플리케이션의 라우팅은 사용자가 태스크를 수행하기 위해 어떤 화면(view)에서 다른 화면으로 화면을 전환하는 내비게이션을 관리하기 위한 기능을 의미한다.
    - 일반적으로 사용자자 요청한 URL 또는 이벤트를 해석하고 새로운 페이지로 전환하기 위한 데이터를 취득하기 위해 서버에 필요 데이터를 요청하고 화면을 전환하는 위한 일련의 행위를 말한다.
  - 브라우저가 화면을 전환하는 경우는 아래와 같다.
    - 브라우저의 주소창에 URL을 입력하면 해당 페이지로 이동한다.
    - 웹페이지의 링크를 클릭하면 해당 페이지로 이동한다.
    - 브라우저의 뒤로가기 또는 앞으로가기 버튼을 클릭하면 사용자가 방문한 웹페이지의 기록(history)의 뒤 또는 앞으로 이동한다.
  - AJAX 요청에 의해 서버로부터 데이터를 응답받아 화면을 생성하는 경우, 브라우저의 주소창의 URL은 변경되지 않는다. 
    - 이는 사용자의 방문 history를 관리할 수 없음을 의미하며, SEO(검색엔진 최적화) 이슈의 발생 원인이기도 하다. 
    - history 관리를 위해서는 각 페이지는 브라우저의 주소창에서 구별할 수 있는 유일한 URL을 소유하여야 한다.



- 전통적 링크 방식

  -  link tag로 동작하는 기본적인 웹페이지의 동작 방식이다.
  -  link tag(`<a href="service.html">Service</a>` 등)을 클릭하면 href 어트리뷰트의 값인 리소스의 경로가 URL의 path에 추가되어 주소창에 나타나고 해당 리소스를 서버에 요청된다.
  -  이때 서버는 html로 화면을 표시하는데 부족함이 없는 완전한 리소스를 클라이언트에 응답한다. 
  -  이를 **서버 렌더링**이라 한다. 브라우저는 서버가 응답한 html을 수신하고 렌더링한다. 
  -  이때 이전 페이지에서 수신된 html로 전환하는 과정에서 전체 페이지를 다시 렌더링하게 되므로 새로고침이 발생한다.
  -  이 방식은 JavaScript가 필요없이 응답된 html만으로 렌더링이 가능하며 각 페이지마다 고유의 URL이 존재하므로 history 관리 및 SEO 대응에 아무런 문제가 없다. 
  -  하지만 중복된 리소스를 요청마다 수신해야 하며, 전체 페이지를 다시 렌더링하는 과정에서 새로고침이 발생하여 사용성이 좋지 않은 단점이 있다.

  ```html
  <!DOCTYPE html>
  <html>
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <meta http-equiv="X-UA-Compatible" content="ie=edge">
          <title>Link</title>
          <link rel="stylesheet" href="css/style.css">
      </head>
      <body>
          <nav>
              <ul>
                  <li><a href="/">Home</a></li>
                  <li><a href="service.html">Service</a></li>
                  <li><a href="about.html">About</a></li>
              </ul>
          </nav>
          <section>
              <h1>Home</h1>
              <p>This is main page</p>
          </section>
      </body>
  </html>
  ```

  

- AJAX

  > JS 코드는 https://poiemaweb.com/js-spa 참고

  - 전통적 링크 방식의 단점을 보완하기 위해 등장한 것이 AJAX(Asynchronous JavaScript and XML)이다. 
  - AJAX는 자바스크립트를 이용해서 비동기적(Asynchronous)으로 서버와 브라우저가 데이터를 교환할 수 있는 통신 방식을 의미한다.
  - 서버로부터 웹페이지가 반환되면 화면 전체를 새로 렌더링해야 하는데 페이지 일부만을 갱신하고도 동일한 효과를 볼 수 있도록 하는 것이 AJAX이다.
  - 예제를 살펴보면 link tag(`<a id="home">Home</a>` 등)에 href 어트리뷰트를 사용하지 않는다. 그리고 웹페이지의 내용이 일부 비어있는 것을 알 수 있다.
  - 내비게이션이 클릭되면 link tag의 기본 동작을 prevent하고 AJAX을 사용하여 서버에 필요한 리소스를 요청한다. 요청된 리소스가 응답되면 클라이언트에서 웹페이지에 그 내용을 갈아끼워 html을 완성한다.
  - 이를 통해 불필요한 리소스 중복 요청을 방지할 수 있다. 또한 페이지 전체를 새로 렌더링할 필요가 없고 갱신이 필요한 일부만 로드하여 갱신하면 되므로 빠른 퍼포먼스와 부드러운 화면 표시 효과를 기대할 수 있으므로 새로고침이 없는 보다 향상된 사용자 경험을 구현할 수 있다는 장점이 있다.
  - AJAX는 URL을 변경시키지 않으므로 주소창의 주소가 변경되지 않는다. 
    - 이는 브라우저의 뒤로가기, 앞으로가기 등의 **history 관리가 동작하지 않음을 의미한다.** 
    - 물론 코드 상의 history.back(), history.go(n) 등도 동작하지 않는다. 
  - 새로고침을 클릭하면 주소창의 주소가 변경되지 않기 때문에 언제나 첫페이지가 다시 로딩된다. 
  - 하나의 주소로 동작하는 AJAX 방식은 **SEO 이슈**에서도 자유로울 수 없다.

  ```html
  <!DOCTYPE html>
  <html>
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <meta http-equiv="X-UA-Compatible" content="ie=edge">
          <title>AJAX</title>
          <link rel="stylesheet" href="css/style.css">
          <script src="js/index.js" defer></script>
      </head>
      <body>
          <nav>
              <ul id="navigation">
                  <li><a id="home">Home</a></li>
                  <li><a id="service">Service</a></li>
                  <li><a id="about">About</a></li>
              </ul>
          </nav>
          <div class="app-root">Loading..</div>
      </body>
  </html>
  ```



- Hash 방식

  > JS 코드는 https://poiemaweb.com/js-spa 참고

  - AJAX 방식은 불필요한 리소스 중복 요청을 방지할 수 있고, 새로고침이 없는 사용자 경험을 구현할 수 있다는 장점이 있지만 history 관리가 되지 않는 단점이 있다. 이를 보완한 방법이 Hash 방식이다.
  - Hash 방식은 URI의 fragment identifier(#service)의 고유 기능인 앵커(anchor)를 사용한다. 
    - fragment identifier는 hash mark 또는 hash라고 부르기도 한다.
  - 위 예제를 살펴보면 link tag(`<a href="#service">Service</a>` 등)의 href 어트리뷰트에 hash를 사용하고 있다.
    - 즉, 내비게이션이 클릭되면 hash가 추가된 URI가 주소창에 표시된다. 
    - 단, URL이 동일한 상태에서 hash가 변경되면 브라우저는 서버에 어떠한 요청도 하지 않는다. 
    - 즉, hash는 변경되어도 서버에 새로운 요청을 보내지 않으며 따라서 페이지가 갱신되지 않는다.
    - hash는 요청을 위한 것이 아니라 fragment identifier(#service)의 고유 기능인 앵커(anchor)로 웹페이지 내부에서 이동을 위한 것이기 때문이다.
  - 또한 hash 방식은 서버에 새로운 요청을 보내지 않으며 따라서 페이지가 갱신되지 않지만 페이지마다 고유의 논리적 URL이 존재하므로 history 관리에 아무런 문제가 없다.
  - hash 방식은 uri의 hash가 변경하면 발생하는 이벤트인 hashchange 이벤트를 사용하여 hash의 변경을 감지하여 필요한 AJAX 요청을 수행한다.
  - hash 방식의 단점 
    - uri에 불필요한 `#`이 들어간다는 것이다. 일반적으로 hash 방식을 사용할 때 `#!`을 사용하기도 하는데 이를 해시뱅(Hash-bang)이라고 부른다.
    - hash 방식은 과도기적 기술이다.
    - SEO 이슈

  ```html
  <!DOCTYPE html>
  <html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>SPA</title>
    <link rel="stylesheet" href="css/style.css">
    <script src="js/index.js" defer></script>
  </head>
  <body>
    <nav>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="#service">Service</a></li>
        <li><a href="#about">About</a></li>
      </ul>
    </nav>
    <div class="app-root">Loading...</div>
  </body>
  </html>
  ```



- PJAX 방식

  > JS 코드는 https://poiemaweb.com/js-spa 참고

  - hash 방식의 가장 큰 단점은 SEO 이슈이다. 이를 보완한 방법이 HTML5의 Histroy API인 `pushState`와 `popstate` 이벤트를 사용한 PJAX 방식이다. 
  - pushState와 popstate은 IE 10 이상에서 동작한다.
  - 예시를 살펴보면 link tag(`<a href="/service">Service</a>` 등)의 href 어트리뷰트에 path를 사용하고 있다. 
  - 내비게이션이 클릭되면 path가 추가된 URI가 서버로 요청된다. 
  - PJAX 방식은 내비게이션 클릭 이벤트를 캐치하고 `preventDefault`를 사용하여 서버로의 요청을 방지한다. 
  - 이후, href 어트리뷰트에 path을 사용하여 AJAX 요청을 하는 방식이다.
    - 이때 AJAX 요청은 주소창의 URL을 변경시키지 않아 history 관리가 불가능하다. 
    - 이때 사용하는 것이 `pushState` 메서드이다. 
    - `pushState` 메서드는 주소창의 URL을 변경하고 URL을 history entry로 추가하지만 요청하지는 않는다.

  - PJAX 방식은 서버에 새로운 요청을 보내지 않으며 따라서 페이지가 갱신되지 않는다. 
  - 하지만 페이지마다 고유의 URL이 존재하므로 history 관리에 아무런 문제가 없다. 또한 hash를 사용하지 않으므로 SEO에도 문제가 없다.

  ```html
  <!DOCTYPE html>
  <html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>PJAX</title>
    <link rel="stylesheet" href="css/style.css">
    <script src="js/index.js" defer></script>
  </head>
  <body>
    <nav>
      <ul id="navigation">
        <li><a href="/">Home</a></li>
        <li><a href="/service">Service</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </nav>
    <div class="app-root">Loading...</div>
  </body>
  </html>
  ```

  

- 결론

  - 모든 소프트웨어 아키텍처에는 trade-off가 존재한다. 
  - SPA 또한 모든 애플리케이션에 적합한 은탄환(Silver bullet)은 아니다. 
  - 애플리케이션의 상황을 고려하여 적절한 방법을 선택할 필요가 있다.

  | 구분             | History 관리 | SEO 대응 | 사용자 경험 | 서버 렌더링 | 구현 난이도 | IE 대응 |
  | ---------------- | ------------ | -------- | ----------- | ----------- | ----------- | ------- |
  | 전통적 링크 방식 | O            | O        | X           | O           | 간단        |         |
  | AJAX 방식        | X            | X        | O           | X           | 보통        | 7 이상  |
  | Hash 방식        | O            | X        | O           | X           | 보통        | 8 이상  |
  | PJAX 방식        | O            | O        | O           | △           | 복잡        | 10 이상 |







# 클래스

- 클래스
  - 자바스크립트는 **프로토타입 기반(prototype-based)** 객체지향 언어다. 
    - 프로토타입 기반 프로그래밍은 클래스가 필요없는(class-free) 객체지향 프로그래밍 스타일로 프로토타입 체인과 클로저 등으로 객체 지향 언어의 상속, 캡슐화(정보 은닉) 등의 개념을 구현할 수 있다.
    - ES5에서는 생성자 함수와 프로토타입, 클로저를 사용하여 객체 지향 프로그래밍을 구현하였다.
    - 하지만 클래스 기반 언어에 익숙한 프로그래머들은 프로토타입 기반 프로그래밍 방식이 혼란스러울 수 있으며 자바스크립트를 어렵게 느끼게하는 하나의 장벽처럼 인식되었다.
  - ES6의 클래스
    - ES6의 클래스는 기존 프로토타입 기반 객체지향 프로그래밍보다 클래스 기반 언어에 익숙한 프로그래머가 보다 빠르게 학습할 수 있는 단순명료한 새로운 문법을 제시하고 있다. 
    - 그렇다고 ES6의 클래스가 기존의 프로토타입 기반 객체지향 모델을 폐지하고 새로운 객체지향 모델을 제공하는 것은 아니다. 
    - 사실 **클래스도 함수**이며 기존 프로토타입 기반 패턴의 문법적 설탕(Syntactic sugar)이라고 볼 수 있다. 
    - 다만, 클래스와 생성자 함수가 정확히 동일하게 동작하지는 않는다. 클래스가 보다 엄격하다. 
    - 따라서 클래스를 프로토타입 기반 패턴의 문법적 설탕이라고 인정하지 않는 견해도 일리가 있다.



- 클래스 정의

  - ES6 클래스는 `class` 키워드를 사용하여 정의한다.
  - 클래스 이름은 성성자 함수와 마찬가지로 파스칼 케이스를 사용하는 것이 일반적이다. 
    - 파스칼 케이스를 사용하지 않아도 에러가 발생하지는 않는다.

  ```javascript
  class Person {
      // 반드시 constructor라고 작성해야 한다.
      constructor(name){
          this._name = name
      }
      
      sayHi(){
          console.log(`Hi! ${this._name}!`)
      }
  }
  
  const cha = new Person('Cha')
  cha.sayHi()     // Hi! Cha!
  console.log(cha instanceof Person)  // true
  ```

  - 클래스는 선언문 이전에 참조할 수 없다.
    - 하지만 호이스팅이 발생하지 않는 것은 아니다. 
    - 클래스는 var 키워드로 선언한 변수처럼 호이스팅되지 않고 let, const 키워드로 선언한 변수처럼 호이스팅된다. 
    - 따라서 클래스 선언문 이전에 일시적 사각지대(Temporal Dead Zone; TDZ)에 빠지기 때문에 호이스팅이 발생하지 않는 것처럼 동작한다.

  ```javascript
  var Foo = ''
  
  {
    // 호이스팅이 발생하지 않는다면 ''가 출력되어야 한다.
    console.log(Foo)	// // ReferenceError: Cannot access 'Foo' before initialization
    class Foo {}
  }
  ```

  - 일반적이지는 않지만, 표현식으로도 클래스를 정의할 수 있다. 
    - 함수와 마찬가지로 클래스는 이름을 가질 수도 갖지 않을 수도 있다. 
    - 이때 클래스가 할당된 변수를 사용해 클래스를 생성하지 않고 기명 클래스의 클래스 이름을 사용해 클래스를 생성하면 에러가 발생한다. 
    - 이는 함수와 마찬가지로 클래스 표현식에서 사용한 클래스 이름은 외부 코드에서 접근 불가능하기 때문이다.

  ```javascript
  // 클래스명 MyClass는 함수 표현식과 동일하게 클래스 몸체 내부에서만 유효한 식별자이다.
  const Foo = class MyClass {}
  
  const foo = new Foo()
  console.log(foo)  // MyClass {}
  
  new MyClass() // ReferenceError: MyClass is not defined
  ```

  

- 인스턴스 생성

  - 마치 생성자 함수 같이, `new` 연산자와 함께 클래스 이름을 호출하면 클래스의 인스턴스가 생성된다.
    - 아래 코드에서 `new` 연산자와 함께 호출한 `Foo`는 클래스의 이름이 아니라 constructor(생성자)이다. 
    - 표현식이 아닌 선언식으로 정의한 클래스의 이름은 constructor와 동일하다.

  ```javascript
  class Foo {}
  
  const foo = new Foo()
  console.log(foo instanceof Foo)	// true
  ```

  - `new` 연산자를 사용하지 않고 constructor를 호출하면 타입 에러(TypeError)가 발생한다. 
    - constructor는 `new` 연산자 없이 호출할 수 없다.

  ```javascript
  class Foo {}
  
  const foo = Foo() // TypeError: Class constructor Foo cannot be invoked without 'new'
  ```

  

- constructor

  - 인스턴스를 생성하고 클래스 필드를 초기화하기 위한 특수한 메소드이다.
  - 클래스 필드
    - 클래스 내부의 캡슐화된 변수를 말한다. 
    - 데이터 멤버 또는 멤버 변수라고도 부른다. 
    - 클래스 필드는 인스턴스의 프로퍼티 또는 정적 프로퍼티가 될 수 있다. 
    - 쉽게 말해, 자바스크립트의 생성자 함수에서 `this`에 추가한 프로퍼티를 클래스 기반 객체지향 언어에서는 클래스 필드라고 부른다.

  ```javascript
  // 클래스 선언문
  class Person {
    // constructor(생성자). 이름을 바꿀 수 없다.
    constructor(name) {
      // this는 클래스가 생성할 인스턴스를 가리킨다.
      // _name은 클래스 필드이다.
      this._name = name
    }
  }
  ```

  - constructor는 클래스 내에 한 개만 존재할 수 있다. 
    - 만약 클래스가 2개 이상의 constructor를 포함하면 문법 에러(SyntaxError)가 발생한다. 
    - 인스턴스를 생성할 때 `new` 연산자와 함께 호출한 것이 바로 constructor이며 constructor의 파라미터에 전달한 값은 클래스 필드에 할당한다.
  - constructor는 생략할 수 있다. 
    - constructor를 생략하면 클래스에 `constructor() {}`를 포함한 것과 동일하게 동작한다. 
    - 즉, 빈 객체를 생성한다. 
    - 따라서 인스턴스에 프로퍼티를 추가하려면 인스턴스를 생성한 이후, 프로퍼티를 동적으로 추가해야 한다.

  ```javascript
  class Foo { }
  
  const foo = new Foo()
  console.log(foo) // Foo {}
  
  // 프로퍼티 동적 할당 및 초기화
  foo.num = 1
  console.log(foo) // Foo&nbsp;{ num: 1 }
  ```

  - constructor는 인스턴스의 생성과 동시에 클래스 필드의 생성과 초기화를 실행한다. 
    - 따라서 클래스 필드를 초기화해야 한다면 constructor를 생략해서는 안된다.

  

- 클래스 필드

  - 클래스 몸체(class body)에는 메소드만 선언할 수 있다. 
  - 클래스 바디에 클래스 필드(멤버 변수)를 선언하면 문법 에러(SyntaxError)가 발생한다.

  ```javascript
  class Foo {
    name = '' // SyntaxError
  
    constructor() {}
  }
  ```

  - 클래스 필드의 선언과 초기화는 반드시 constructor 내부에서 실시한다.

  ```javascript
  class Foo {
    constructor(name = '') {
      this.name = name // 클래스 필드의 선언과 초기화
    }
  }
  const foo = new Foo('Cha')
  console.log(foo) // Foo { name: 'Cha' }
  ```

  - constructor 내부에서 선언한 클래스 필드는 클래스가 생성할 인스턴스를 가리키는 this에 바인딩한다.
    - 이로써 클래스 필드는 클래스가 생성할 인스턴스의 프로퍼티가 되며, 클래스의 인스턴스를 통해 클래스 외부에서 언제나 참조할 수 있다. 
    - 즉, 언제나 `public`이다.
    - ES6의 클래스는 다른 객체지향 언어처럼 private, public, protected 키워드와 같은 접근 제한자(access modifier)를 지원하지 않는다.
    - 현재 접근 제한자 지원과 관련된 논의가 진행 중이다.

  ```javascript
  class Foo {
      constructor(name = '') {
          this.name = name // public 클래스 필드
      }
  }
  
  const foo = new Foo('Cha')
  // 클래스 외부에서 참조할 수 있다.
  console.log(foo.name) // Cha
  ```

  

- getter, setter

  - getter와 setter는 클래스에서 새롭게 도입된 기능이 아니다. getter와 setter는 접근자 프로퍼티(accessor property)이다.
  - getter
    - 클래스 필드에 접근할 때마다 클래스 필드의 값을 조작하는 행위가 필요할 때 사용한다.
    - 메소드 이름 앞에 `get` 키워드를 사용해 정의한다.
    - 이때 메소드 이름은 클래스 필드 이름처럼 사용된다. 
    - 다시 말해 getter는 호출하는 것이 아니라 프로퍼티처럼 참조하는 형식으로 사용하며 참조 시에 메소드가 호출된다. 

  ```javascript
  class Foo {
      constructor(arr = []) {
          this._arr = arr
      }
  
      // getter: get 키워드 뒤에 오는 메소드 이름 firstElem은 클래스 필드 이름처럼 사용된다.
      get firstElem() {
          // getter는 반드시 무언가를 반환해야 한다.
          return this._arr.length ? this._arr[0] : null
      }
  }
  
  const foo = new Foo([1, 2])
  // 필드 firstElem에 접근하면 getter가 호출된다.
  console.log(foo.firstElem) // 1
  ```

  - setter
    - setter는 클래스 필드에 값을 할당할 때마다 클래스 필드의 값을 조작하는 행위가 필요할 때 사용한다.
    - 메소드 이름 앞에 `set` 키워드를 사용해 정의한다. 
    - 이때 메소드 이름은 클래스 필드 이름처럼 사용된다. 
    - 다시 말해 setter는 호출하는 것이 아니라 프로퍼티처럼 값을 할당하는 형식으로 사용하며 할당 시에 메소드가 호출된다.

  ```javascript
  class Foo {
      constructor(arr = []) {
          this._arr = arr
      }
  
      // getter: get 키워드 뒤에 오는 메소드 이름 firstElem은 클래스 필드 이름처럼 사용된다.
      get firstElem() {
          // getter는 반드시 무언가를 반환하여야 한다.
          return this._arr.length ? this._arr[0] : null
      }
  
      // setter: set 키워드 뒤에 오는 메소드 이름 firstElem은 클래스 필드 이름처럼 사용된다.
      set firstElem(elem) {
          // ...this._arr은 this._arr를 개별 요소로 분리한다
          this._arr = [elem, ...this._arr]
      }
  }
  
  const foo = new Foo([1, 2])
  
  // 클래스 필드 lastElem에 값을 할당하면 setter가 호출된다.
  foo.firstElem = 100
  
  console.log(foo.firstElem) // 100
  ```

  

- 정적 메소드

  - 클래스의 정적(static) 메소드를 정의할 때 `static` 키워드를 사용한다. 
    - 정적 메소드는 클래스의 인스턴스가 아닌 클래스 이름으로 호출한다.
    - 따라서 클래스의 인스턴스를 생성하지 않아도 호출할 수 있다.

  ```javascript
  class Foo {
      constructor(prop) {
          this.prop = prop
      }
  
      static staticMethod() {
  
          // 정적 메소드는 this를 사용할 수 없다.
          // 정적 메소드 내부에서 this는 클래스의 인스턴스가 아닌 클래스 자신을 가리킨다.
          return 'staticMethod';
      }
  
      prototypeMethod() {
          return this.prop;
      }
  }
  
  // 정적 메소드는 클래스 이름으로 호출한다.
  console.log(Foo.staticMethod())	// staticMethod
  
  const foo = new Foo(1)
  // 정적 메소드는 인스턴스로 호출할 수 없다.
  console.log(foo.staticMethod()) // Uncaught TypeError: foo.staticMethod is not a function
  ```

  - 클래스의 정적 메소드 용도
    - 클래스의 정적 메소드는 인스턴스로 호출할 수 없다.
    - 이것은 정적 메소드는 this를 사용할 수 없다는 것을 의미한다. 
    - 일반 메소드에서 this는 클래스의 인스턴스를 가리키며, 메소드 내부에서 this를 사용한다는 것은 클래스의 인스턴스의 생성을 전제로 하는 것이다.
    - 메소드 내부에서 this를 사용할 필요가 없는 메소드는 정적 메소드로 만들 수 있다.
    - 애플리케이션 전역에서 사용할 유틸리티(utility) 함수를 생성할 때 주로 사용한다.

  - 정적 메소드를 인스턴스로 호출할 수 없는 이유

    - 사실 클래스도 함수이고 기존 prototype 기반 패턴의 Syntactic sugar일 뿐이다.
    - 함수 객체는 prototype 프로퍼티를 갖는데, 일반 객체는 prototype 프로퍼티를 가지지 않는다.
    - 함수 객체만이 가지고 있는 prototype 프로퍼티는 함수 객체가 생성자로 사용될 때, 이 함수를 통해 생성된 객체의 부모 역할을 하는 프로토타입 객체를 가리킨다. 
    - 그리고 생성자 함수의 prototype 프로퍼티가 가리키는 프로토타입 객체가 가지고 있는 constructor 프로퍼티는 생성자 함수를 가리킨다.
    - 정적 메소드는 생성자 함수의 메소드(함수는 객체이므로 메소드를 가질 수 있다.)이고, 일반 메소드는 프로토타입 객체의 메소드이다. 
    - 인스턴스는 프로토타입 객체와 프로토타입 체인이 연결되어 있지만, 생성자 함수와는 연결되어 있지 않다.
    - 따라서 정적 메소드는 인스턴스에서 호출할 수 없다.

    ```javascript
    var Foo = (function () {
        // 생성자 함수
        function Foo(prop) {
            this.prop = prop
        }
    	
        // 정적 메소드
        Foo.staticMethod = function () {
            return 'staticMethod'
        }
    	
        // 일반 메소드
        Foo.prototype.prototypeMethod = function () {
            return this.prop
        }
    
        return Foo
    }())
    
    var foo = new Foo(1)
    console.log(foo.prototypeMethod()) 	// 123
    console.log(Foo.staticMethod()) 	// staticMethod
    console.log(foo.staticMethod()) 	// Uncaught TypeError: foo.staticMethod is not a function
    ```

    

- 클래스 상속

  - `extends` 키워드
    - 부모 클래스(base class)를 상속받는 자식 클래스(sub class)를 정의할 때 사용한다. 
  - `super` 키워드
    - 부모 클래스를 참조 하거나, 부모 클래스의 constructor를 호출할 때 사용한다.
    - `super`가 메소드로 사용될 때, 그리고 객체로 사용될 때 다르게 동작한다.
    - `super` 메소드는 자식 class의 constructor 내부에서 부모 클래스의 constructor(super-constructor)를 호출한다. 
    - 즉, 부모 클래스의 인스턴스를 생성한다. 
    - 자식 클래스의 constructor에서 `super()`를 호출하지 않으면 `this`에 대한 참조 에러(ReferenceError)가 발생한다.
    - 즉, `super` 메소드를 호출하기 이전에는 `this`를 참조할 수 없음을 의미한다.
    - `super` 키워드는 부모 클래스(Base Class)에 대한 참조다. 부모 클래스의 필드 또는 메소드를 참조하기 위해 사용한다.
  - 오버라이딩과 오버로딩
    - 오버라이딩: 상위 클래스가 가지고 있는 메소드를 하위 클래스가 재정의하여 사용하는 방식.
    - 오버로딩: 매개변수의 타입 또는 갯수가 다른, 같은 이름의 메소드를 구현하고 매개변수에 의해 메소드를 구별하여 호출하는 방식. 
    - 자바스크립트는 오버로딩을 지원하지 않지만 arguments 객체를 사용하여 구현할 수는 있다.

  ```javascript
  // 부모 클래스
  class Circle {
      
      constructor(radius) {
          this.radius = radius // 반지름
      }
  
      // 원의 지름
      getDiameter() {
          return 2 * this.radius
      }
  
      // 원의 둘레
      getPerimeter() {
          return 2 * Math.PI * this.radius
      }
  
      // 원의 넓이
      getArea() {
          return Math.PI * Math.pow(this.radius, 2)
      }
  }
  
  // 자식 클래스
  class Cylinder extends Circle {
      
      constructor(radius, height) {
          // super 메소드는 부모 클래스의 constructor를 호출하면서 인수를 전달한다.
          super(radius)
          this.height = height
      }
  
      // 원통의 넓이: 부모 클래스의 getArea 메소드를 오버라이딩하였다.
      getArea() {
          // (원통의 높이 * 원의 둘레) + (2 * 원의 넓이)
          // super 키워드는 부모 클래스(Base Class)에 대한 참조에 사용된다.
          return (this.height * super.getPerimeter()) + (2 * super.getArea())
      }
  
      // 원통의 부피
      getVolume() {
          // super 키워드는 부모 클래스(Base Class)에 대한 참조에 사용된다.
          return super.getArea() * this.height
      }
  }
  
  // 반지름이 2, 높이가 10인 원통
  const cylinder = new Cylinder(2, 10)
  
  // 원의 지름
  console.log(cylinder.getDiameter())  // 4
  // 원의 둘레
  console.log(cylinder.getPerimeter()) // 12.566370614359172
  // 원통의 넓이
  console.log(cylinder.getArea())      // 150.79644737231007
  // 원통의 부피
  console.log(cylinder.getVolume())    // 125.66370614359172
  
  // cylinder는 Cylinder 클래스의 인스턴스이다.
  console.log(cylinder instanceof Cylinder) // true
  // cylinder는 Circle 클래스의 인스턴스이다.
  console.log(cylinder instanceof Circle)   // true
  
  
  console.log(cylinder.__proto__ === Cylinder.prototype) // true
  console.log(Cylinder.prototype.__proto__ === Circle.prototype) // true
  console.log(Circle.prototype.__proto__ === Object.prototype) // true
  ```

  - ` static` 메소드와 `prototype` 메소드의 상속
    - 프로토타입 체인에 의해 부모 클래스의 정적 메소드도 상속이 된다.
    - 자식 클래스의 정적 메소드 내부에서도 `super` 키워드를 사용하여 부모 클래스의 정적 메소드를 호출할 수 있다.
    - 하지만 자식 클래스의 일반 메소드(프로토타입 메소드) 내부에서는 `super` 키워드를 사용하여 부모 클래스의 정적 메소드를 호출할 수 없다.

  ```javascript
  class Parent {
      static staticMethod() {
          return 'Hello'
      }
  }
  
  class Child extends Parent {
      static staticMethod() {
          return `${super.staticMethod()} wolrd`;
      }
  
      prototypeMethod() {
          return `${super.staticMethod()} wolrd`
      }
  }
  
  console.log(Parent.staticMethod()) 			// 'Hello'
  console.log(Child.staticMethod())  			// 'Hello wolrd'
  console.log(new Child().prototypeMethod())	// TypeError: (intermediate value).staticMethod is not a function
  ```

  



# 모듈

- 모듈
  - 애플리케이션을 구성하는 개별적 요소로서 재사용 가능한 코드 조각을 말한다. 
  - 모듈은 세부 사항을 캡슐화하고 공개가 필요한 API만을 외부에 노출한다.
  - 일반적으로 모듈은 파일 단위로 분리되어 있으며 애플리케이션은 필요에 따라 명시적으로 모듈을 로드하여 재사용한다. 
    - 즉, 모듈은 애플리케이션에 분리되어 개별적으로 존재하다가 애플리케이션의 로드에 의해 비로소 애플리케이션의 일원이 된다. 
  - 모듈은 기능별로 분리되어 작성되므로 코드의 단위를 명확히 분리하여 애플리케이션을 구성할 수 있으며 재사용성이 좋아서 개발 효율성과 유지보수성을 높일 수 있다.



- JS의 모듈

  - JS에는 본래 모듈 기능이 없었다.
    - 클라이언트 사이드 자바스크립트는 script 태그를 사용하여 외부의 스크립트 파일을 가져올 수는 있지만, 파일마다 독립적인 파일 스코프를 갖지 않고 하나의 전역 객체(Global Object)를 공유한다. 
    - 즉, 자바스크립트 파일을 여러 개의 파일로 분리하여 script 태그로 로드하여도 분리된 자바스크립트 파일들이 결국 하나의 자바스크립트 파일 내에 있는 것처럼 하나의 전역 객체를 공유한다. 
    - 따라서 분리된 자바스크립트 파일들이 하나의 전역을 갖게 되어 전역 변수가 중복되는 등의 문제가 발생할 수 있다. 
    - 이것으로는 모듈화를 구현할 수 없다.
    - JS를 클라이언트 사이드에 국한하지 않고 범용적으로 사용하고자 하는 움직임이 생기면서 모듈 기능은 반드시 해결해야 하는 핵심 과제가 되었다.
    - 이런 상황에서 제안된 것이 **CommonJS**와 **AMD(Asynchronous Module Definition)**이다.
    - 결국, 자바스크립트의 모듈화는 크게 CommonJS와 AMD 진영으로 나뉘게 되었고 브라우저에서 모듈을 사용하기 위해서는 CommonJS 또는 AMD를 구현한 모듈 로더 라이브러리를 사용해야 하는 상황이 되었다.
    - 서버 사이드 자바스크립트 런타임 환경인 Node.js는 모듈 시스템의 사실상 표준(de facto standard)인 CommonJS를 채택하였고 독자적인 진화를 거쳐 현재는 CommonJS 사양과 100% 동일하지는 않지만 기본적으로 CommonJS 방식을 따르고 있다. 
    - 즉, Node.js에서는 표준은 아니지만 모듈이 지원된다. 따라서 Node.js 환경에서는 모듈 별로 독립적인 스코프, 즉 모듈 스코프를 갖는다.
  - ES6에서는 클라이언트 사이드 자바스크립트에서도 동작하는 모듈 기능을 추가하였다.
    - script 태그에 `type="module"` 어트리뷰트를 추가하면 로드된 자바스크립트 파일은 모듈로서 동작한다. 
    - ES6 모듈의 파일 확장자는 모듈임을 명확히 하기 위해 mjs를 사용하도록 권장한다.

  ```html
  <script type="module" src="lib.mjs"></script>
  <script type="module" src="app.mjs"></script>
  ```

  - 단, 아래와 같은 이유로 아직까지는 브라우저가 지원하는 ES6 모듈 기능보다는 Webpack 등의 모듈 번들러를 사용하는 것이 일반적이다.
    - IE를 포함한 구형 브라우저는 ES6 모듈을 지원하지 않는다.
    - 브라우저의 ES6 모듈 기능을 사용하더라도 트랜스파일링이나 번들링이 필요하다.
    - 아직 지원하지 않는 기능(Bare import 등)이 있다.
    - 점차 해결되고는 있지만 아직 몇가지 이슈가 있다.



- 모듈 스코프

  - ES6 모듈 기능을 사용하지 않으면 분리된 자바스크립트 파일에 독자적인 스코프를 갖지 않고 하나의 전역을 공유한다.
    - 아래 예시의 HTML에서 2개의 자바스크립트 파일을 로드하면 로드된 자바스크립트는 하나의 전역을 공유한다.
    - 로드된 2개의 자바스크립트 파일은 하나의 전역 객체를 공유하며 하나의 전역 스코프를 갖는다. 
    - 따라서 foo.js에서 선언한 변수 x와 bar.js에서 선언한 변수 x는 중복 선언되며 의도치 않게 변수 `x`의 값이 덮어 써진다.

  ```javascript
  // foo.js
  
  var x = 'foo'
  
  // 변수 x는 전역 변수이다.
  console.log(window.x) // foo
  ```

  ```javascript
  // bar.js
  // foo.js에서 선언한 전역 변수 x와 중복된 선언이다.
  var x = 'bar'
  
  // 변수 x는 전역 변수이다.
  // foo.js에서 선언한 전역 변수 x의 값이 재할당되었다.
  console.log(window.x) // bar
  ```

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <script src="foo.js"></script>
    <script src="bar.js"></script>
  </body>
  </html>
  ```

  - ES6 모듈은 파일 자체의 스코프를 제공한다. 
    - 즉, ES6 모듈은 독자적인 **모듈 스코프**를 갖는다. 
    - 따라서, 모듈 내에서 `var` 키워드로 선언한 변수는 더 이상 전역 변수가 아니며 `window` 객체의 프로퍼티도 아니다.
    - 모듈 내에서 선언한 변수는 모듈 외부에서 참조할 수 없다. 스코프가 다르기 때문이다.

  ```javascript
  // foo.mjs
  var x = 'foo'
  
  console.log(x) // foo
  // 변수 x는 전역 변수가 아니며 window 객체의 프로퍼티도 아니다.
  console.log(window.x) // undefined
  ```

  ```javascript
  // bar.mjs
  // 변수 x는 foo.mjs에서 선언한 변수 x와 스코프가 다른 변수이다.
  var x = 'bar'
  
  console.log(x) // bar
  // 변수 x는 전역 변수가 아니며 window 객체의 프로퍼티도 아니다.
  console.log(window.x) // undefined
  ```

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <script type="module" src="foo.mjs"></script>
    <script type="module" src="bar.mjs"></script>
  </body>
  </html>
  ```



- `export` 키워드

  - 모듈은 독자적인 모듈 스코프를 갖기 때문에 모듈 안에 선언한 모든 식별자는 기본적으로 해당 모듈 내부에서만 참조할 수 있다. 
  - 만약 모듈 안에 선언한 식별자를 외부에 공개하여 다른 모듈들이 참조할 수 있게 하고 싶다면 `export` 키워드를 사용한다. 
  - 선언된 변수, 함수, 클래스 모두 export할 수 있다.
  - 모듈을 공개하려면 선언문 앞에 `export` 키워드를 사용한다. 여러 개를 export할 수 있는데 이때 각각의 export는 이름으로 구별할 수 있다.

  ```javascript
  // lib.mjs
  // 변수의 공개
  export const a = 'Hello!'
  
  // 함수의 공개
  export function foo() {
    console.log("Hello!")
  }
  
  // 클래스의 공개
  export class Person {
    constructor(name) {
      this.name = name;
    }
  }
  ```

  - 선언문 앞에 매번 `export` 키워드를 붙이는 것이 싫다면 export 대상을 모아 하나의 객체로 구성하여 한번에 export할 수도 있다.

  ```javascript
  // lib.mjs
  const a = 'Hello!'
  
  function foo() {
    console.log("Hello!")
  }
  
  class Person {
    constructor(name) {
      this.name = name
    }
  }
  
  // 변수, 함수 클래스를 하나의 객체로 구성하여 공개
  export { a, foo, Person }
  ```



- `import` 키워드

  - 모듈에서 공개(export)한 대상을 로드하려면 `import` 키워드를 사용한다.
  - 모듈이 export한 식별자로 import하며 ES6 모듈의 파일 확장자를 생략할 수 없다.

  ```javascript
  // app.mjs
  // 같은 폴더 내의 lib.mjs 모듈을 로드.
  // lib.mjs 모듈이 export한 식별자로 import한다.
  // ES6 모듈의 파일 확장자를 생략할 수 없다.
  import { a, foo, Person } from './lib.mjs';
  
  console.log(a)  // Hello!
  foo()	 		// Hello!
  console.log(new Person('Cha')) // Person { name: 'Cha' }
  ```

  - 모듈이 export한 식별자를 각각 지정하지 않고 하나의 이름으로 한꺼번에 import할 수도 있다. 
    - 이때 import되는 식별자는 as 뒤에 지정한 이름의 객체에 프로퍼티로 할당된다.

  ```javascript
  // app.mjs
  import * as lib from './lib.mjs'
  
  console.log(lib.a)  // Hello!
  lib.foo()	 		// Hello!
  lib.console.log(new lib.Person('Cha')) // Person { name: 'Cha' }
  ```

  - 이름을 변경하여 import할 수도 있다.

  ```javascript
  import { a as ab, foo as f, Person as P } from './lib.mjs';
  
  console.log(ab)  // Hello!
  f()				 // Hello!
  console.log(new P('Cha')) // Person { name: 'Cha' }
  ```

  - 모듈에서 하나만을 export할 때는 `default` 키워드를 사용할 수 있다.
    - 다만, `default`를 사용하는 경우, `var`, `let`, `const`는 사용할 수 없다.

  ```javascript
  // lib.mjs
  export default function () {
    console.log("Hello!")
  }
  
  // var, let, const 사용 불가
  export default () => {}			// O
  
  export default const foo = () => {} // => SyntaxError: Unexpected token 'const'
  ```

  - `default` 키워드와 함께 export한 모듈은 `{}` 없이 임의의 이름으로 import한다.

  ```javascript
  // app.mjs
  import someFunction from './lib.mjs';
  
  someFunction // Hello!
  ```

  













