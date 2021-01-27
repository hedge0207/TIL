# Device Orientation

- Device Orientation

  - HTML5가 제공하는 기능으로 중력과의 관계에서 디바이스의 물리적 방향의 변화를 감지할 수 있다. 
  - 이것을 이용하면 모바일 디바이스를 회전시켰을 때 이벤트를 감지하여 적절히 화면을 변화 시킬 수 있다.
  - 디바이스의 방향 정보를 다루는 자바스크립트 이벤트는 두가지가 있다.
    - `DeviceOrientationEvent` 가속도계(accelerometer)가 기기의 방향의 변화를 감지했을 때 발생한다.
    - `DeviceMotionEvent` 가속도에 변화가 일어났을 때 발생한다.
  - 현재 사파리를 제외한 대부분의 브라우저에서 사용할 수 있다.
  - 하지만 오래된 브라우저를 사용하는 사용자를 위해 브라우저의 이벤트 지원 여부를 먼저 확인할 필요가 있다.

  ```javascript
  if (window.DeviceOrientationEvent) {
    console.log(Our browser supports DeviceOrientation)
  } else {
    console.log("Sorry, your browser doesn't support Device Orientation")
  }
  ```

  

- `DeviceOrientationEvent`

  - 디바이스의 방향 변화는 3개의 각도( alpha, beta, gamma )를 사용하여 측정된다. 
  - `deviceorientation` 이벤트에 리스너를 등록하면 리스너 함수가 주기적으로 호출되어 업데이트된 방향 데이터를 제공한다. 
  - `deviceorientation` 이벤트는 다음 4가지의 값을 가진다.
    - DeviceOrientationEvent.absolute: 지구좌표계(Earth coordinate system)을 사용하는 지에 대한 boolean 값이다. 일반적인 경우 사용하지 않는다.
    - DeviceOrientationEvent.alpha: 0도부터 360도까지 범위의 z축을 중심으로 디바이스의 움직임을 나타낸다.
    - DeviceOrientationEvent.beta: -180도부터 180도(모바일 사파리: -90도~90도)까지 범위의 x축을 중심으로 디바이스의 움직임을 나타낸다. 이는 디바이스의 앞뒤 움직임을 나타낸다.
    - DeviceOrientationEvent.gamma: -90도부터 90도(모바일 사파리: -180도~180도)까지 범위의 y축을 중심으로 디바이스의 움직임을 나타낸다. 이는 디바이스의 좌우 움직임을 나타낸다.

  ```javascript
  window.addEventListener('deviceorientation', handleOrientation, false)
  
  function handleOrientation(event) {
      var absolute = event.absolute;
      var alpha    = event.alpha;
      var beta     = event.beta;
      var gamma    = event.gamma;
      // Do stuff with the new orientation data
  }
  ```

  

# 비동기식 처리 모델과 ajax

## 동기식 처리 모델과 비동기식 처리 모델

- 동기식 처리 모델(Synchronous processing model)

  - 직렬적으로 태스크(task)를 수행한다. 
  - 즉, 태스크는 순차적으로 실행되며 어떤 작업이 수행 중이면 다음 작업은 대기하게 된다.
    - 예를 들어 서버에서 데이터를 가져와서 화면에 표시하는 작업을 수행할 때, 서버에 데이터를 요청하고 데이터가 응답될 때까지 이후 태스크들은 블로킹(blocking, 작업 중단)된다.

  ```javascript
  // 동기적으로 동작하는 코드, 순차적으로 실행 된다.
  function func1() {
    console.log('func1')
    func2()
  }
  
  function func2() {
    console.log('func2')
    func3()
  }
  
  function func3() {
    console.log('func3')
  }
  
  func1()
  ```



- 비동기식 처리 모델(Asynchronous processing model 또는 Non-Blocking processing model)

  - 병렬적으로 태스크를 수행한다. 
  - 즉, 태스크가 종료되지 않은 상태라 하더라도 대기하지 않고 다음 태스크를 실행한다.
    - 예를 들어 서버에서 데이터를 가져와서 화면에 표시하는 태스크를 수행할 때, 서버에 데이터를 요청한 이후 서버로부터 데이터가 응답될 때까지 대기하지 않고(Non-Blocking) 즉시 다음 태스크를 수행한다. 
    - 이후 서버로부터 데이터가 응답되면 이벤트가 발생하고 이벤트 핸들러가 데이터를 가지고 수행할 태스크를 계속해 수행한다.
  - JS의 대부분의 DOM 이벤트 핸들러와 Timer 함수(setTimeout, setInterval), Ajax 요청은 비동기식 처리 모델로 동작한다.
    - 아래 예시에서 함수 `func1`이 호출되면 함수 func1은 Call Stack에 쌓인다.
    - 함수 `func1`은 함수 `func2`을 호출하므로 함수 `func2`가 Call Stack에 쌓이고 `setTimeout`이 호출된다.
    - `setTimeout`의 콜백함수는 즉시 실행되지 않고 지정 대기 시간만큼 기다리다가 “tick” 이벤트가 발생하면 태스크 큐로 이동한 후 Call Stack이 비어졌을 때 Call Stack으로 이동되어 실행된다.

  ```javascript
  // 비동기적으로 동작하는 코드, 순차적으로 실행되지 않는다.
  function func1() {
    console.log('func1')
    func2()
  }
  
  function func2() {
    setTimeout(function() {
      console.log('func2')
    }, 0)
    func3()
  }
  
  function func3() {
    console.log('func3')
  }
  
  func1()
  ```



## Ajax

- Ajax(Asynchronous JavaScript and XML)

  - 브라우저에서 웹페이지를 요청하거나 링크를 클릭하면 화면 갱신이 발생한다. 이것은 브라우저와 서버와의 통신에 의한 것이다.
    - 서버는 요청받은 페이지(HTML)를 반환하는데 이때 HTML에서 로드하는 CSS나 JavaScript 파일들도 같이 반환된다. 
    - 클라이언트의 요청에 따라 서버는 정적인 파일을 반환할 수도 있고 서버 사이드 프로그램이 만들어낸 파일이나 데이터를 반환할 수도 있다. 
    - 서버로부터 웹페이지가 반환되면 클라이언트(브라우저)는 이를 렌더링하여 화면에 표시한다.

  - Ajax는 자바스크립트를 이용해서 **비동기적(Asynchronous)**으로 서버와 브라우저가 데이터를 교환할 수 있는 통신 방식을 의미한다.
    - 서버로부터 웹페이지가 반환되면 화면 전체를 갱신해야 하는데 페이지 일부만을 갱신하고도 동일한 효과를 볼 수 있도록 하는 것이 Ajax이다. 
    - 페이지 전체를 로드하여 렌더링할 필요가 없고 갱신이 필요한 일부만 로드하여 갱신하면 되므로 빠른 퍼포먼스와 부드러운 화면 표시 효과를 기대할 수 있다.



## JSON

- JSON(JavaScript Object Notation)

  - 클라이언트와 서버 간에는 데이터 교환이 필요하다. JSON은 클라이언트와 서버 간 데이터 교환을 위한 규칙 즉 데이터 포맷을 말한다.
  - JSON은 일반 텍스트 포맷보다 효과적인 데이터 구조화가 가능하며 XML 포맷보다 가볍고 사용하기 간편하며 가독성도 좋다.
  - 자바스크립트의 객체 리터럴과 매우 흡사하다. 하지만 JSON은 순수한 텍스트로 구성된 규칙이 있는 데이터 구조이다.

  ```json
  // key는 반드시 큰 따옴표(작은 따옴표 사용 불가)로 둘러싸야 한다.
  {
    "name": "Cha",
    "gender": "male",
    "age": 28
  }
  ```

  

- `JSON.stringify`

  - 메소드 객체를 JSON 형식의 문자열로 변환한다.
  - 두 번째 인자로 replacer를 받는다.
    - 문자열화 동작 방식을 변경하는 함수.
    - SON 문자열에 포함될 값 객체의 속성들을 선택하기 위한 화이트리스트(whitelist)로 쓰이는 String과 Number 객체들의 배열.
  - 세 번째 인자로 JSON 문자열 출력에 삽입할 공백을 받는다. 
    - 숫자일 경우 10이 최대이며, 1 미만의 값은 적용되지 않는다. 
    - 문자열의 경우 해당 문자열이 공백에 채워진다.

  ```javascript
  var obj = { name: 'Cha', gender: 'male', age:28 }
  
  // 객체 => JSON 형식의 문자열
  const strObject = JSON.stringify(obj)
  console.log(typeof strObject, strObject)  // // string {"name":"Cha","gender":"male","age":28}
  
  // 객체 => JSON 형식의 문자열 + prettify
  const strPrettyObject = JSON.stringify(obj, null, 2)
  console.log(typeof strPrettyObject, strPrettyObject)
  /*
  string {
    "name": "Lee",
    "gender": "male",
    "age": 28
  }
  */
  
  // 값이 숫자일 때만 반환
  function isNum(k,v){
      return typeof v === 'number' ? undefined : v
  }
  const strFilteredObject = JSON.stringify(obj, isNum, 2)
  console.log(strFilteredObject)
  /*
  {
    "age": 28,
  }
  */
  ```



- `JSON.parse`

  - JSON 데이터를 가진 문자열을 객체로 변환한다.
    - 서버로부터 브라우저로 전송된 JSON 데이터는 문자열이다. 
    - 이 문자열을 객체로서 사용하려면 객체화하여야 하는데 이를 **역직렬화(Deserializing)**라 한다. 
    - 역직렬화를 위해서 내장 객체 JSON의 static 메소드인 `JSON.parse`를 사용한다.

  ```javascript
  var obj = { name: 'Cha', gender: 'male', age:28 }
  const strObject = JSON.stringify(obj)
  
  // JSON 형식의 문자열 => 객체
  const jsonToObject = JSON.parse(strObject)
  console.log(typeof jsonToObject, jsonToObject)	// object { name: 'Cha', gender: 'male', age: 28 }
  ```

  - 배열이 JSON 형식의 문자열로 변환되어 있는 경우 JSON.parse는 문자열을 배열 객체로 변환한다. 
    - 배열의 요소가 객체인 경우 배열의 요소까지 객체로 변환한다.

  ```javascript
  var todos = [
      { id: 1, content: 'HTML', completed: true },
      { id: 2, content: 'CSS', completed: true },
      { id: 3, content: 'JavaScript', completed: false }
  ]
  
  // 배열 => JSON 형식의 문자열
  var str = JSON.stringify(todos)
  
  // JSON 형식의 문자열 => 배열
  var parsed = JSON.parse(str)
  console.log(typeof parsed, parsed)
  /*
  object [
      { id: 1, content: 'HTML', completed: true },
      { id: 2, content: 'CSS', completed: true },
      { id: 3, content: 'JavaScript', completed: false }
  ]
  */
  ```





## XMLHttpRequest

- XMLHttpRequest
  - 브라우저는 XMLHttpRequest 객체를 이용하여 Ajax 요청을 생성하고 전송한다.
  - 서버가 브라우저의 요청에 대해 응답을 반환하면 같은 XMLHttpRequest 객체가 그 결과를 처리한다.



### Ajax request

- Ajax 요청 처리 예시

  ```javascript
  // XMLHttpRequest 객체의 생성
  const xml = new XMLHttpRequest()
  // 비동기 방식으로 Request를 오픈한다
  xml.open('GET', '/users')
  // Request를 전송한다
  xhr.send()
  ```



- `XMLHttpRequest.open`

  - XMLHttpRequest 객체의 인스턴스를 생성하고 `XMLHttpRequest.open` 메소드를 사용하여 서버로의 요청을 준비한다. 
  - `XMLHttpRequest.open`의 사용법은 아래와 같다.
    - method: HTTP method (“GET”, “POST”, “PUT”, “DELETE” 등)
    - url: 요청을 보낼 URL
    - async: 비동기 조작 여부. 옵션으로, default는 true이며 비동기 방식으로 동작한다.

  ```javascript
  XMLHttpRequest.open(method, url, async)
  ```



- ` XMLHttpRequest.send`

  - ` XMLHttpRequest.send` 메소드를 사용하여 준비된 요청을 서버에 전달한다.
  - 기본적으로 서버로 전송하는 데이터는 GET, POST 메소드에 따라 그 전송 방식에 차이가 있다.
    - GET 메소드의 경우, URL의 일부분인 쿼리문자열(query string)로 데이터를 서버로 전송한다.
    - POST 메소드의 경우, 데이터(페이로드)를 Request Body에 담아 전송한다.
    - `XMLHttpRequest.send` 메소드는 다양한 데이터를 request body에 담아 전송할 인수를 전달할 수 있다.
    - 만약 요청 메소드가 GET인 경우, send 메소드의 인수는 무시되고 request body은 null로 설정된다.

  ```javascript
  xhr.send('string')
  xhr.send({ form: 'data' })
  xhr.send(document)
  ```



- `XMLHttpRequest.setRequestHeader`

  - `XMLHttpRequest.setRequestHeader` 메소드는 HTTP Request Header의 값을 설정한다. 

  - `setRequestHeader` 메소드는 반드시 `XMLHttpRequest.open` 메소드 호출 이후에 호출한다.

  - 자주 사용하는 Request Header에는 Content-type, Accept 등이 있다.

    - Content-type: request body에 담아 전송할 데이터의 MIME-type의 정보를 표현(아래는 자주 사용되는 MIME-type들)

    | 타입                        | 서브타입                                           |
    | --------------------------- | -------------------------------------------------- |
    | text 타입                   | text/plain, text/html, text/css, text/javascript   |
    | Application 타입            | application/json, application/x-www-form-urlencode |
    | File을 업로드하기 위한 타입 | multipart/formed-data                              |

    - Accept: HTTP 클라이언트가 서버에 요청할 때 서버가 센드백할 데이터의 MIME-type을 Accept로 지정할 수 있다. 만약 Accept 헤더를 설정하지 않으면, send 메소드가 호출될 때 Accept 헤더가 `*/*`으로 전송된다.

  ```javascript
  // request body에 담아 서버로 전송할 데이터의 MIME-type을 지정하는 예시.
  // json으로 전송하는 경우
  xhr.open('POST', '/users')
  
  // 클라이언트가 서버로 전송할 데이터의 MIME-type 지정: json
  xhr.setRequestHeader('Content-type', 'application/json')
  
  const data = { id: 3, title: 'JavaScript', author: 'Park', price: 5000}
  
  xhr.send(JSON.stringify(data))
  
  // 서버가 센드백할 데이터의 MIME-type을 지정하는 예시.
  // json으로 전송하는 경우
  xhr.setRequestHeader('Accept', 'application/json');
  ```

  

###  Ajax response

- Ajax 응답 처리의 예시

  ```javascript
  // XMLHttpRequest 객체의 생성
  const xml = new XMLHttpRequest()
  
  // XMLHttpRequest.readyState 프로퍼티가 변경(이벤트 발생)될 때마다 onreadystatechange 이벤트 핸들러가 호출된다.
  xml.onreadystatechange = function (e) {
      // readyStates는 XMLHttpRequest의 상태(state)를 반환
      // readyState: 4 => DONE(서버 응답 완료)
      if (xml.readyState !== XMLHttpRequest.DONE) return
  
      // status는 response 상태 코드를 반환 : 200 => 정상 응답
      if(xhr.status === 200) {
          console.log(xml.responseText)
      } else {
          console.log('Error!')
      }
  };
  ```



- 구체적인 과정
  - XMLHttpRequest.send 메소드를 통해 서버에 Request를 전송하면 서버는 Response를 반환한다. 
    - 하지만 언제 Response가 클라이언트에 도달할 지는 알 수 없다. 
  - `XMLHttpRequest.onreadystatechange`는 Response가 클라이언트에 도달하여 발생된 이벤트를 감지하고 콜백 함수를 실행하여 준다. 
    - 즉, `XMLHttpRequest.readyState`의 변경을 감지하고 콜백 함수를 실행해 준다.
  - 이때 이벤트는 Request에 어떠한 변화가 발생한 경우 즉 `XMLHttpRequest.readyState` 프로퍼티가 변경된 경우 발생한다.



- `XMLHttpRequest.readyState`

  - XMLHttpRequest 객체는 response가 클라이언트에 도달했는지를 추적할 수 있는 `XMLHttpRequest.readyState` 프로퍼티를 제공한다.
  - 만일 `XMLHttpRequest.readyState`의 값이 4인 경우, 정상적으로 Response가 돌아온 경우이다.
  - `XMLHttpRequest.readyState`의 값

  | Value | State            | Description                                           |
  | ----- | ---------------- | ----------------------------------------------------- |
  | 0     | UNSENT           | XMLHttpRequest.open() 메소드 호출 이전                |
  | 1     | OPENED           | XMLHttpRequest.open() 메소드 호출 완료                |
  | 2     | HEADERS_RECEIVED | XMLHttpRequest.send() 메소드 호출 완료                |
  | 3     | LOADING          | 서버 응답 중(XMLHttpRequest.responseText 미완성 상태) |
  | 4     | DONE             | 서버 응답 완료                                        |

  - `XMLHttpRequest의.readyState`가 4인 경우, 서버 응답이 완료된 상태이므로 이후 `XMLHttpRequest.status`가 200(정상 응답)임을 확인하고 정상인 경우, `XMLHttpRequest.responseText`를 취득한다. 
    - `XMLHttpRequest.responseText`에는 서버가 전송한 데이터가 담겨 있다.

  ```javascript
  // XMLHttpRequest 객체의 생성
  var xhr = new XMLHttpRequest()
  // 비동기 방식으로 Request를 오픈한다
  xhr.open('GET', 'data/test.json')
  // Request를 전송한다
  xhr.send()
  
  // XMLHttpRequest.readyState 프로퍼티가 변경(이벤트 발생)될 때마다 콜백함수(이벤트 핸들러)를 호출한다.
  xhr.onreadystatechange = function (e) {
      // 이 함수는 Response가 클라이언트에 도달하면 호출된다.
  
      // readyStates는 XMLHttpRequest의 상태(state)를 반환
      // readyState: 4 => DONE(서버 응답 완료)
      if (xhr.readyState !== XMLHttpRequest.DONE) return
  
      // status는 response 상태 코드를 반환 : 200 => 정상 응답
      if(xhr.status === 200) {
          console.log(xhr.responseText)
      } else {
          console.log('Error!')
      }
  }
  ```

  - 만약 서버 응답 완료 상태에만 반응하도록 하려면 `readystatechange` 이벤트 대신 load 이벤트를 사용해도 된다.
    - ` load` 이벤트는 서버 응답이 완료된 경우에 발생한다.

  ```javascript
  // XMLHttpRequest 객체의 생성
  var xhr = new XMLHttpRequest()
  // 비동기 방식으로 Request를 오픈한다
  xhr.open('GET', 'data/test.json')
  // Request를 전송한다
  xhr.send()
  
  // load 이벤트는 서버 응답이 완료된 경우에 발생한다.
  xhr.onload = function (e) {
    // status는 response 상태 코드를 반환 : 200 => 정상 응답
    if(xhr.status === 200) {
      console.log(xhr.responseText)
    } else {
      console.log('Error!')
    }
  }
  ```





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
  - link tag(`<a href="service.html">Service</a>` 등)을 클릭하면 href 어트리뷰트의 값인 리소스의 경로가 URL의 path에 추가되어 주소창에 나타나고 해당 리소스를 서버에 요청된다.
  - 이때 서버는 html로 화면을 표시하는데 부족함이 없는 완전한 리소스를 클라이언트에 응답한다. 
  - 이를 **서버 렌더링**이라 한다. 브라우저는 서버가 응답한 html을 수신하고 렌더링한다. 
  - 이때 이전 페이지에서 수신된 html로 전환하는 과정에서 전체 페이지를 다시 렌더링하게 되므로 새로고침이 발생한다.
  - 이 방식은 JavaScript가 필요없이 응답된 html만으로 렌더링이 가능하며 각 페이지마다 고유의 URL이 존재하므로 history 관리 및 SEO 대응에 아무런 문제가 없다. 
  - 하지만 중복된 리소스를 요청마다 수신해야 하며, 전체 페이지를 다시 렌더링하는 과정에서 새로고침이 발생하여 사용성이 좋지 않은 단점이 있다.

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
    -  hash는 요청을 위한 것이 아니라 fragment identifier(#service)의 고유 기능인 앵커(anchor)로 웹페이지 내부에서 이동을 위한 것이기 때문이다.
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





# 예외처리

- try, catch, finally를 사용하여 예외처리

  ```js
  try {
  //정상이라면 이 코드는 아무런 문제없이 블록의 시작부터 끝까지 실행됨.
  
  } catch(error) {
  //이 블록 내부의 문장들은 오직 try 블록에서 예외가 발생할 경우에만 실행된다.
  
  } finally(){
  //try 블록에서 일어난 일에 관계없이 무조건 실행될 코드가 위치한다.
  }
  ```

