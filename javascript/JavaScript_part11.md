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
    }, 1000)
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



## axios

- axios

  > https://github.com/axios/axios

  - AJAX요청을 보내는 것을 도와주는 라이브러리, 즉 XHR 요청을 쉽게 보낼 수 있게 해주는 것이다.
  - django의 request와 역할이 완전히 같다고 할 수는 없지만 일반적으로 django에서 request가 올 자리에 온다고 보면 된다.
  - axios를 사용하려면 아래 코드를 입력해야 한다.

  ```html
  <!--변수 선언과 마찬가지로 axios를 사용하기 전에 코드를 입력해야 한다.-->
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
  ```

  - promise
    - `axios.get()`의 return 이 promise다.
    - 불확실하고 기다려야 하는 작업(AJAX, axios)을 비동기적으로 처리하기 위해서 사용한다.
    - 언제 끝날지 모른다는 불확실성, 성공할지 실패할지 모른다는 불확실성이 존재.
    - 예를 들어 메일을 보낼 때는 답장이 언제 올지 불확실하고 답장이 올지 안 올지도 불확실하다. 그러나 미래에 답장이 오거나 오지 않거나 둘 중 하나는 발생할 것이라는 것은 확실히 알 수 있다. 따라서 promise는 성공과 실패에 대한 시나리오를 쓴다.
      - 성공했을 때, 어떤 일을 할 것인가(`.then(함수)`)
      - 실패했을 때, 어떤 일을 할 것인가(`.catch(함수)`)
  - 요약하면 기다려야 하거나 외부에 요청을 보낼 경우 계속 기다리는 것이 아니라 다음에 해야 할 일을 수행하고(non-blocking) 기다리던 일이 발생하면 promise에 따라 다음 작업(함수)을 한다.

  ```html
  <!--예시-->
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
  </head>
  <body>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <script>
      console.log(1)
      //만일 성공적으로 요청을받는다면
      axios.get('https://koreanjson.com/posts/1')
      //함수에 그 응답이 인자로 들어가게 되고 그 응답의 data를 반환
      //인자로 들어가는 결과값은 아래와 같다.
      //{data: {…}, status: 200, statusText: "OK", headers: {…}, config: {…}, …}
        .then(function (r) { return r.data })
        
      //반일 성공적으로 반환 받는다면 반환값이 아래 함수의 인자로 들어가게 되고 그 값의 content를 반환
      //위 함수에서 반환한 data는 아래와 같은 object이다.
      /*
      data : {
      	UserId: 1
      	content: "모든 국민은 인간으로서의 존엄과 가치를 가지며..."
      	createdAt: "2019-02-24T16:17:47.000Z"
      	id: 1
      	title: "정당의 목적이나 활동이 민주적 기본질서에 위배될..."
      	updatedAt: "2019-02-24T16:17:47.000Z"
      }
      */
        .then(function (d) { return d.content } )
        
      //만일 성공적으로 반환 받는다면 반환 값이 아래 함수의 인자로 들어가게 되고 그 값을 출력
      //위 함수에서 반환받은 content에는 다음과 같은 값이 들어있다.
      //"모든 국민은 인간으로서의 존엄과 가치를 가지며..."
        .then(function (c) { console.log(c) })
      console.log(2)
      // callback 함수들 시작
    </script>
  </body> 
  </html>
  
  out
  1
  2 <!--console.log(2)가 더 뒤에 있음에도 먼저 출력된다.-->
  "모든 국민은 인간으로서의 존엄과 가치를 가지며..."
  ```

  - 일단 요청을 보내면 그 일이 아무리 빨리 끝날 지라도 다음 일을 먼저 처리한다. 
    - 요청을 보낸는 것은 1순위지만 그 응답을 받은 후의 처리는 1순위가 아니다.

  ```python
  def 메일 보내기():
      보내기
      답장받기
      답장확인하기
      
  def 점심먹기():
      메뉴정하기
      밥먹기
      정리하기
      
  def 공부하기():
      공부하기
  
  #예를 들어 메일을 보낸 즉시 답이 온다고 했을 때에도 그 응답을 기다리는 것이 아니라 점심을 먹고 공부를 한 후에 답장을 확인한다. 즉, 요청을 보내는 것은 1순위로 처리하지만 그 응답이 아무리 빨리온다고 해도 다음 일을 모두 처리한 후에 응답에 따른 작업(promise, 답장확인)을 수행한다.
  ```

  

- ping/pong 구현하기

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ping</title>
  </head>
  <body>
  
    <label for="myInput">input</label>: 
    <input id="myInput" type="text">
    <pre id="resultArea"> <!--div태그가 아닌 pre태그를 사용한 이유는 art 활용 때문이다.-->
  
    </pre>
  
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <script>
      /* 1. input#userInput 의 'input' 이벤트 때, */
      const myInput = document.querySelector('#myInput')
      myInput.addEventListener('input', function(event) {
        const myText = myInput.value  //input창에 입력된 값을 myText에 담는다.
        
        /* 2. value 값을 AJAX 요청으로 '/art/pong' 으로 보낸다. */
        //axio는 2번째 인자로 오브젝트를 넣을 수 있다. 그 오브젝트 안에 또 params라는 오브젝트를 넣고 params 오브젝트의 키, 밸류를 설정하면 값을 함께 넘길 수 있다.
        axios.get('/artii/pong/', {
          params: {
            myText: myText, //요청을 보낼 때 input창에 입력된 값을 함께 보낸다.
          },
        })
        //위 코드는 아래 코드와 동일하다(아래 코드는 쿼리스트링을 사용한 것)
        //axios.get(`artii/pong/?myText=${myText}`)
  
          /* 3. pong 이 받아서 다시 JSON 으로 응답을 보낸다. views.py 참고. 
         	res에 응답이 담기게 된다*/
          .then(function (res) { 
            /* 4. 응답 JSON 의 내용을 div#resultArea 에 표시한다. */
            const resultArea = document.querySelector('#resultArea')
            resultArea.innerText = res.data.ccontent 
          })
      })
    </script>
  </body>
  </html>
  ```

  - axios 요청은 DRF(Django Rest Framwork)를 사용한 view 함수로만 처리가 가능하다.

  ```python
  #views.py
  import art #art를 쓰기 위해선 별도의 install이 필요
  #제대로 출력되는 것을 보고 싶다면 크롬의 설정에서 고정 폭 글꼴을 적당한 다른 것으로 바꿔주면 된다.
  
  from django.shortcuts import render
  from django.http import JsonResponse
  
  def ping(request):
      return render(request, 'artii/ping.html')
  
  def pong(request):
      #위 html파일에서 GET 방식으로 넘어온 요청 중 key가 myText인 value가 my_input에 담긴다.
      my_input = request.GET.get('myText')
      art_text = art.text2art(my_input) #text2art는 art의 메소드 중 하나다.
      data = {
          'ccontent': art_text,
      }
      #JSON 으로 응답을 보낸다.
    return JsonResponse(data)
  ```





# 프로미스

- 프로미스
  - 자바스크립트는 비동기 처리를 위한 하나의 패턴으로 콜백 함수를 사용한다. 
    - 하지만 전통적인 콜백 패턴은 콜백 헬로 인해 가독성이 나쁘고 비동기 처리 중 발생한 에러의 처리가 곤란하며 여러 개의 비동기 처리를 한번에 처리하는 데도 한계가 있다.
  - ES6에서는 비동기 처리를 위한 또 다른 패턴으로 프로미스(Promise)를 도입했다. 
    - 프로미스는 비동기 작업을 위한 JS 객체이다.
    - 프로미스는 전통적인 콜백 패턴이 가진 단점을 보완하며 비동기 처리 시점을 명확하게 표현할 수 있다는 장점이 있다.





## 콜백 패턴의 단점

### 콜백 헬(Callback Hell)

- 비동기 처리를 위해 콜백 패턴을 사용하면 처리 순서를 보장하기 위해 여러 개의 콜백 함수가 네스팅(nesting, 중첩)되어 복잡도가 높아지는 것.

  - 콜백 헬은 가독성을 나쁘게 하며 실수를 유발하는 원인이 된다.

  ```javascript
  // 출처: https://velog.io/@yujo/JS%EC%BD%9C%EB%B0%B1-%EC%A7%80%EC%98%A5%EA%B3%BC-%EB%B9%84%EB%8F%99%EA%B8%B0-%EC%A0%9C%EC%96%B4
  setTimeout(
      (name) => {
          let coffeeList = name;
          console.log(coffeeList);
          setTimeout(
              (name) => {
                  coffeeList += ', ' + name;
                  console.log(coffeeList);
                  setTimeout(
                      (name) => {
                          coffeeList += ', ' + name;
                          console.log(coffeeList);
                          setTimeout(
                              (name) => {
                                  coffeeList += ', ' + name;
                                  console.log(coffeeList);
                              },
                              500,
                              'Latte',
                          );
                      },
                      500,
                      'Mocha',
                  );
              },
              500,
              'Americano',
          );
      },
      500,
      'Espresso',
  );
  ```



- 발생 이유

  - 비동기 처리 모델은 실행 완료를 기다리지 않고 즉시 다음 태스크를 실행한다. 
    - 따라서 비동기 함수(비동기를 처리하는 함수) 내에서 처리 결과를 반환(또는 전역 변수에의 할당)하면 기대한 대로 동작하지 않는다.

  ```html
  <!DOCTYPE html>
  <html>
      <body>
          <script>
              // 비동기 함수
              function get(url) {
                  // XMLHttpRequest 객체 생성
                  const xhr = new XMLHttpRequest()
  
                  // 서버 응답 시 호출될 이벤트 핸들러
                  xhr.onreadystatechange = function () {
                      // 서버 응답 완료가 아니면 무시
                      if (xhr.readyState !== XMLHttpRequest.DONE) return
  
                      if (xhr.status === 200) { // 정상 응답
                          console.log(xhr.response)
                          // 비동기 함수의 결과에 대한 처리는 반환할 수 없다.
                          return xhr.response //@
                      } else { // 비정상 응답
                          console.log('Error: ' + xhr.status)
                      }
                  };
  
                  // 비동기 방식으로 Request 오픈
                  xhr.open('GET', url)
                  // Request 전송
                  xhr.send()
              }
  
              // 비동기 함수 내의 readystatechange 이벤트 핸들러에서 처리 결과를 반환(@)하면 순서가 보장되지 않는다.
              const res = get('http://jsonplaceholder.typicode.com/posts/1')
              console.log(res)	// undefined #
          </script>
      </body>
  </html>
  ```

  - 예시의 비동기 함수 내의 `onreadystatechange` 이벤트 핸들러에서 처리 결과를 반환(`@`)하면 순서가 보장되지 않는다. 
    - 즉, `#`에서 `get` 함수가 반환한 값을 참조할 수 없다.
    - `get` 함수가 호출되면 `get` 함수의 실행 컨텍스트가 생성되고 호출 스택(Call stack,실행 컨텍스트 스택)에서 실행된다. 
    - `get` 함수가 반환하는 `xhr.response`는 `onreadystatechange` 이벤트 핸들러가 반환한다. 
    - `readystatechange` 이벤트는 발생하는 시점을 명확히 알 수 없지만 반드시 `get` 함수가 종료한 이후 발생한다.
    - `get` 함수의 마지막 문인 `xhr.send()`가 실행되어야 request를 전송하고, request를 전송해야 `readystatechange` 이벤트가 발생할 수 있기 때문이다.
    - `get` 함수가 종료하면 곧바로 `console.log`(`#`)가 호출되어 호출 스택에 들어가 실행된다. `console.log`가 호출되기 직전에 `readystatechange` 이벤트가 이미 발생했다하더라도 이벤트 핸들러는 `console.log`보다 먼저 실행되지 않는다.
    - `readystatechange` 이벤트의 이벤트 핸들러는 이벤트가 발생하면 즉시 실행되는 것이 아니다.
    - 이벤트가 발생하면 일단 태스크 큐( 혹은 Event Queue)로 들어가고, 호출 스택이 비면 그때 이벤트 루프에 의해 호출 스택으로 들어가 실행된다. 
    - `console.log` 호출 시점 이전에 `readystatechange` 이벤트가 이미 발생했다하더라도 `get` 함수가 종료하면 곧바로 `console.log`가 호출되어 호출 스택에 들어가기 때문에 `readystatechange` 이벤트의 이벤트 핸들러는 `console.log`가 종료되어 호출 스택에서 빠진 이후 실행된다. 
    - 만약 `get` 함수 이후에 `console.log`가 100번 호출된다면 `readystatechange` 이벤트의 이벤트 핸들러는 모든 `console.log`가 종료한 이후에나 실행된다.
    - 때문에 `get` 함수의 반환 결과를 가지고 후속 처리를 할 수 없다. 
    - 즉, 비동기 함수의 처리 결과를 반환하는 경우, 순서가 보장되지 않기 때문에 그 반환 결과를 가지고 후속 처리를 할 수 없다. 
    - 즉, 비동기 함수의 처리 결과에 대한 처리는 비동기 함수의 콜백 함수 내에서 처리해야 한다. 이로 인해 콜백 헬이 발생한다.







### 예외 처리의 한계

- 콜백 방식의 비동기 처리가 갖는 문제점 중에서 가장 심각한 것은 에러 처리가 곤란하다는 것이다. 

  ```javascript
  // 콜백 함수를 사용하지 않을 때
  try {
      throw new Error('Error!')
  } catch (e) {
      console.log('에러를 캐치한다.')	// 에러를 캐치한다.
      console.log(e)					// Error: Error!
  }
  
  // 콜백 함수 사용
  try {
    setTimeout(() => { throw new Error('Error!') }, 1000)
  } catch (e) {
    console.log('에러를 캐치하지 못한다.')
    console.log(e)
  }
  ```

  - `try` 블록 내에서 `setTimeout` 함수가 실행되면 1초 후에 콜백 함수가 실행되고 이 콜백 함수는 예외를 발생시킨다. 
  - 하지만 이 예외는 `catch` 블록에서 캐치되지 않는다.
    - 비동기 처리 함수의 콜백 함수는 해당 이벤트(timer 함수의 tick 이벤트, XMLHttpRequest의 readystatechange 이벤트 등)가 발생하면 태스트 큐(Task queue)로 이동한 후 호출 스택이 비어졌을 때, 호출 스택으로 이동되어 실행된다. 
    - `setTimeout` 함수는 비동기 함수이므로 콜백 함수가 실행될 때까지 기다리지 않고 즉시 종료되어 호출 스택에서 제거된다. 
    - 이후 tick 이벤트가 발생하면 `setTimeout` 함수의 콜백 함수는 태스트 큐로 이동한 후 호출 스택이 비어졌을 때 호출 스택으로 이동되어 실행된다. 
    -  `setTimeout` 함수의 콜백 함수를 호출한 것은 `setTimeout` 함수가 아니라 tick 이벤트이다.
    - 예외(exception)는 호출자(caller) 방향으로 전파된다. 
    - `setTimeout` 함수의 콜백 함수의 호출자(caller)는  tick 이벤트이므로 tick에 예외가 전파된다.
    - 따라서 `setTimeout` 함수의 콜백 함수 내에서 발생시킨 에러는 catch 블록에서 캐치되지 않아 프로세스는 종료된다.



## 프로미스 생성

- 프로미스는 `Promise` 생성자 함수를 통해 인스턴스화한다. 

  - `Promise` 생성자 함수는 비동기 작업을 수행할 콜백 함수를 인자로 전달받는다.
    - 이 콜백 함수는 executor라 불리는 `resolve`와 `reject` 콜백 함수 쌍을 인자로 전달받는다.
    - `resolve`: 기능을 정상적으로 수행하면 호출되어 최종 데이터를 전달하는 콜백함수.
    - `reject`: 기능을 수행하다 문제가 생기면 호출되는 콜백함수.
  - 새로운 프로미스 객체가 생성되면 프로미스 코드 블록이 자동으로 실행된다.

  ```javascript
  // Promise 객체의 생성
  const promise = new Promise((resolve, reject) => {
    // 비동기 작업을 수행한다.
  
    if (/* 비동기 작업 수행 성공 */) {
      resolve('result')
    }
    else { /* 비동기 작업 수행 실패 */
      reject('failure reason')
    }
  })
  ```



- 비동기 처리가 성공(fulfilled)하였는지 또는 실패(rejected)하였는지 등의 상태(state) 정보.

  | 상태      | 의미                                       | 구현                                               |
  | --------- | ------------------------------------------ | -------------------------------------------------- |
  | pending   | 비동기 처리가 아직 수행되지 않은 상태      | resolve 또는 reject 함수가 아직 호출되지 않은 상태 |
  | fulfilled | 비동기 처리가 수행된 상태 (성공)           | resolve 함수가 호출된 상태                         |
  | rejected  | 비동기 처리가 수행된 상태 (실패)           | reject 함수가 호출된 상태                          |
  | settled   | 비동기 처리가 수행된 상태 (성공 또는 실패) | resolve 또는 reject 함수가 호출된 상태             |



- Promise 생성자 함수가 인자로 전달받은 콜백 함수는 내부에서 비동기 처리 작업을 수행한다. 

  - 비동기 처리가 성공하면 콜백 함수의 인자로 전달받은 resolve 함수를 호출한다. 이때 프로미스는 ‘fulfilled’ 상태가 된다. 
  - 비동기 처리가 실패하면 reject 함수를 호출한다. 이때 프로미스는 ‘rejected’ 상태가 된다.

  ```javascript
  const promiseAjax = (method, url, payload) => {
      // 비동기 함수 내에서 Promise 객체를 생성
      return new Promise((resolve, reject) => {
          // 내부에서 비동기 처리를 구현
          const xhr = new XMLHttpRequest()
          xhr.open(method, url)
          xhr.setRequestHeader('Content-type', 'application/json');
          xhr.send(JSON.stringify(payload))
  
          xhr.onreadystatechange = function () {
              // 서버 응답 완료가 아니면 무시
              if (xhr.readyState !== XMLHttpRequest.DONE) return
  
              if (xhr.status >= 200 && xhr.status < 400) {
                  // resolve 메소드를 호출하면서 처리 결과를 전달
                  resolve(xhr.response) // Success!
              } else {
                  // reject 메소드를 호출하면서 에러 메시지를 전달
                  reject(new Error(xhr.status)) // Failed...
              }
          };
      });
  };
  ```

  

## 프로미스의 후속 메소드

- Promise로 구현된 비동기 함수는 Promise 객체를 반환하여야 한다. 
  - Promise로 구현된 비동기 함수를 호출하는 측(promise consumer)에서는 Promise 객체의 후속 처리 메소드(`then`, `catch`, `finally`)를 통해 비동기 처리 결과 또는 에러 메시지를 전달받아 처리한다. 
  - Promise 객체는 상태를 갖는다고 하였다. 이 상태에 따라 후속 처리 메소드를 체이닝 방식으로 호출한다.



- Promise의 후속 처리 메소드

  - `then`
    - then 메소드는 두 개의 콜백 함수를 인자로 전달 받는다. 
    - 첫 번째 콜백 함수는 성공(프로미스에서 `fulfilled`,`resolve` 함수가 호출된 상태) 시 호출되고 두 번째 함수는 실패(프로미스에서 `rejected`, `reject` 함수가 호출된 상태) 시 호출된다.
    - `then` 메소드는 Promise 또는 값을 반환한다. 반환 값을 따로 설정하지 않을 경우에는 프로미스 객체를, 설정하면 설정한 값을 반환한다.
  - `catch`
    - 프로미스에서 `rejected`, `reject` 함수가 호출되었거나 `then` 메소드에서 에러가 발생하면 호출된다. 
    - `catch` 메소드는 Promise를 반환한다.
  - 예시1, 2번 처럼 따로 따로 써야 하는 것은 아니다. 
    - 예시 3번 처럼 쓰는 것이 가능하다.
    - `then`, `catch`는 자신이 반환 받은 프로미스 객체(예시의 경우 `promise3`)를 다시 반환한다(프로미스 체이닝).
    - 결국 아래 코드에서 `promise3.then(value=>{console.log("then",value)}).catch(error=>{console.log("catch",error)})`의 `catch`는 `promise3.catch(error=>{console.log("catch",error)})`와 같다.
  - `finally`
    - 성공, 실패 여부와 무관하게 무조건 실행

  ```javascript
  // 예시1
  const promise1 = new Promise((resolve,reject)=>{
      setTimeout(()=>{
          resolve('Hi!!')
      },1000)
  })
  
  // value에는 resolve에서 넘긴 값이 담긴다.
  promise1.then(value=>{
      console.log(value) // Hi!!
  })
  
  
  // 예시2
  const promise2 = new Promise((resolve,reject)=>{
      setTimeout(()=>{
          reject('Hi!!')
      },1000)
  })
  
  promise2
    // then은 reject를 받지 못한다.
    .then(value=>{
        console.log("then",value)	// (node:20360) UnhandledPromiseRejectionWarning: Hi!!
    })
  
  
  // 예시3
  const promise3 = new Promise((resolve,reject)=>{
      setTimeout(()=>{
          reject('Hi!!')
      },1000)
  })
  
  promise3
    .then(value=>{
        console.log("then",value)
    })
    .catch(error=>{
        console.log("catch",error)  // Hi!!
    })
  ```



## 프로미스 체이닝

- 콜백 헬 해결
  - 비동기 함수의 처리 결과를 가지고 다른 비동기 함수를 호출해야 하는 경우, 함수의 호출이 중첩(nesting)이 되어 복잡도가 높아지는 콜백 헬이 발생한다. 
  - 프로미스는 후속 처리 메소드를 체이닝(chainning)하여 여러 개의 프로미스를 연결하여 사용할 수 있다. 
  - 이로써 콜백 헬을 해결한다.



- Promise 객체를 반환한 비동기 함수는 프로미스 후속 처리 메소드인 `then`이나 `catch` 메소드를 사용할 수 있다. 

  - 따라서 `then` 메소드가 Promise 객체를 반환하도록 하면(`then` 메소드는 기본적으로 Promise를 반환) 여러 개의 프로미스를 연결하여 사용할 수 있다.

  ```javascript
  const getHen = () => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>resolve('Chicken'),1000)
  })
  
  const getEgg = hen => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>resolve(`${hen} => Egg`),1000)
  })
  
  const cook = egg => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>resolve(`${egg} => Meal`),1000)
  })
  
  // 아래와 같이 받아온 값을 다른 함수로 바로 넘길 때에는 축약이 가능하다.
  getHen()
    .then(hen => getEgg(hen))	// getEgg 프로미스 객체를 반환
    // .then(getEgg) 으로 축약 가능
    .then(egg => cook(egg))	// cook 프로미스 객체를 반환
    // .then(cook) 으로 축약 가능
    .then(meal => console.log(meal))
    // .then(console.log) 로 축약 가능
  ```

  - `then` 메소드는 프로미스 객체 외에도 값을 반환할 수 있다.

  ```javascript
  const fetchNumber = new Promise((resolve,reject)=>{
      setTimeout(() => resolve(1),1000)
  })
  
  fetchNumber
    .then(num => num*2)	// 값을 반환
    .then(num => num*3)	// 값을 반환
    .then(num => {		// 프로미스 객체를 반환
      return new Promise((resolve,reject)=>{
          setTimeout(()=>resolve(num+1),1000)
      })
  })
  .then(num => console.log(num))
  ```

  

## 프로미스의 에러 처리

- 비동기 처리 결과에 대한 후속 처리는 Promise 객체가 제공하는 후속 처리 메서드`then`, `catch`, `finally`를 사용하여 수행한다. 



- 비동기 처리 시에 발생한 에러는 `then` 메서드의 두 번째 콜백 함수로 처리할 수 있다.

  - 단, `then` 메서드의 두 번째 콜백 함수는 첫 번째 콜백 함수에서 발생한 에러를 캐치하지 못하고 코드가 복잡해져서 가독성이 좋지 않다.
  - 따라서 에러 처리는 `then` 메서드에서 하지 말고 `catch` 메서드를 사용하는 것을 권장한다.

  ```javascript
  // 예시(위에서 정의 한 `promiseAjax` 사용)
  
  // 부적절한 URL이 지정되었기 때문에 에러가 발생한다.
  const wrongUrl = 'https://jsonplaceholder.typicode.com/XXX/1'
  
  promiseAjax(wrongUrl)
    .then(res => console.log(res), err => console.error(err))
  
  
  // 두 번째 콜백 함수는 첫 번째 콜백 함수에서 발생한 에러를 캐치하지 못한다.
  promiseAjax('https://jsonplaceholder.typicode.com/todos/1')
    .then(res => console.xxx(res), err => console.error(err))
  ```

  

- Promise 객체의 후속 처리 메서드 `catch`를 사용해서 처리할 수도 있다.

  - `catch` 메서드를 호출하면 내부적으로 `then(undefined, onRejected)`을 호출한다.
  - `catch` 메서드를 모든 `then` 메서드를 호출한 이후에 호출하면, 비동기 처리에서 발생한 에러(reject 함수가 호출된 상태)뿐만 아니라 `then` 메서드 내부에서 발생한 에러까지 모두 캐치할 수 있다.

  ```javascript
  // 예시(위에서 정의 한 `promiseAjax` 사용)
  
  // 부적절한 URL이 지정되었기 때문에 에러가 발생한다.
  const wrongUrl = 'https://jsonplaceholder.typicode.com/XXX/1'
  
  promiseAjax(wrongUrl)
    .then(res => console.log(res))
    .catch(err => console.error(err)) // Error: 404
  
  
  //위 예시는 결국 아래와 같다.
  const wrongUrl = 'https://jsonplaceholder.typicode.com/XXX/1'
  
  promiseAjax(wrongUrl)
    .then(res => console.log(res))
    .then(undefined, err => console.error(err)) // Error: 404
  
  
  // then 메서드 내부에서 발생한 에러까지 모두 캐치할 수 있다.
  promiseAjax('https://jsonplaceholder.typicode.com/todos/1')
    .then(res => console.xxx(res))
    .catch(err => console.error(err)) // TypeError: console.xxx is not a function
  ```

  

- 특정 시점에 예외 처리

  - `catch`를 사용하여 에러가 발생했을 때 다른 값을 넘겨주는 것도 가능하다.

  ```javascript
  const getHen = () => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>resolve('Chicken'),1000)
  })
  
  const getEgg = hen => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>reject(new Error('error가 발생')),1000)
  })
  
  const cook = egg => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>resolve(`${egg} => Meal`),1000)
  })
  
  getHen()
    .then(getEgg)
    .then(cook)
    .then(console.log)
    .catch(console.log)	// Error: error가 발생
  
  
  // 만일 에러가 발생했을 때 다른 값을 넘겨주고 싶다면 다음과 같이 하면 된다.
  const getHen = () => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>resolve('Chicken'),1000)
  })
  
  const getEgg = hen => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>reject(new Error('error가 발생')),1000)
  })
  
  const cook = egg => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>resolve(`${egg} => Meal`),1000)
  })
  
  getHen()
    .then(getEgg)
    .catch(error => {
      return 'Bread'
    })
    .then(cook)
    .then(console.log)	// Bread => Meal
  ```

  

## 프로미스의 정적 메소드

- `Promise.resolve` / `Promise.reject`

  - 존재하는 값을 Promise로 래핑하기 위해 사용한다.
  - 정적 메소드 `Promise.resolve` 는 인자로 전달된 값을 resolve하는 Promise를 생성한다.

  ```javascript
  // 위와 아래는 동일하게 동작한다.
  var resolvedPromise = Promise.resolve([1, 2, 3])
  resolvedPromise.then(console.log) // [ 1, 2, 3 ]
  
  var resolvedPromise = new Promise(resolve => resolve([1, 2, 3]))
  resolvedPromise.then(console.log) // [ 1, 2, 3 ]
  ```

  - `Promise.reject` 메소드는 인자로 전달된 값을 reject하는 프로미스를 생성한다.

  ```javascript
  // 위와 아래는 동일하게 동작한다.
  const rejectedPromise = Promise.reject(new Error('Error!'))
  rejectedPromise.catch(console.log) // Error: Error!
  
  const rejectedPromise = new Promise((resolve, reject) => reject(new Error('Error!')))
  rejectedPromise.catch(console.log) // Error: Error!
  ```



- `Promise.all`

  - `Promise.all` 메소드는 프로미스가 담겨 있는 배열 등의 이터러블을 인자로 전달 받는다. 
  - 그리고 전달받은 모든 프로미스를 병렬로 처리하고 그 처리 결과를 resolve하는 새로운 프로미스를 반환한다.
  - 예시
    - 첫번째 프로미스는 3초 후에 1을 resolve하여 처리 결과를 반환한다.
    - 두번째 프로미스는 2초 후에 2을 resolve하여 처리 결과를 반환한다.
    - 세번째 프로미스는 1초 후에 3을 resolve하여 처리 결과를 반환한다.

  ```javascript
  Promise.all([
    new Promise(resolve => setTimeout(() => resolve(1), 3000)),
    new Promise(resolve => setTimeout(() => resolve(2), 2000)),
    new Promise(resolve => setTimeout(() => resolve(3), 1000))
  ]).then(console.log) 	// [ 1, 2, 3 ]
    .catch(console.log)
  ```

  - `Promise.all` 메소드는 전달받은 모든 프로미스를 병렬로 처리한다.
    - 이때 모든 프로미스의 처리가 종료될 때까지 기다린 후 모든 처리 결과를 resolve 또는 reject한다.
    - 모든 프로미스의 처리가 성공하면 각각의 프로미스가 resolve한 처리 결과를 배열에 담아 resolve하는 새로운 프로미스를 반환한다. 
    - 이때 첫번째 프로미스가 가장 나중에 처리되어도 `Promise.all` 메소드가 반환하는 프로미스는 첫번째 프로미스가 resolve한 처리 결과부터 차례대로 배열에 담아 그 배열을 resolve하는 새로운 프로미스를 반환한다. 
    - 즉, **처리 순서가 보장된다.**
    - 프로미스의 처리가 하나라도 실패하면 가장 먼저 실패한 프로미스가 reject한 에러를 reject하는 새로운 프로미스를 즉시 반환한다.

  ```javascript
  Promise.all([
    new Promise((resolve, reject) => setTimeout(() => reject(new Error('Error 1!')), 3000)),
    new Promise((resolve, reject) => setTimeout(() => reject(new Error('Error 2!')), 2000)),
    new Promise((resolve, reject) => setTimeout(() => reject(new Error('Error 3!')), 1000))
  ]).then(console.log)
    .catch(console.log) // Error: Error 3!
  ```

  - `Promise.all` 메소드는 전달 받은 이터러블의 요소가 프로미스가 아닌 경우, `Promise.resolve` 메소드를 통해 프로미스로 래핑된다.

  ```javascript
  Promise.all([
    1, // => Promise.resolve(1)
    2, // => Promise.resolve(2)
    3  // => Promise.resolve(3)
  ]).then(console.log) // [1, 2, 3]
    .catch(console.log)
  ```



- `Promise.race`

  - 프로미스가 담겨 있는 배열 등의 이터러블을 인자로 전달 받는다. 
  - 모든 프로미스를 병렬 처리하는 것이 아니라 가장 먼저 처리된 프로미스가 resolve한 처리 결과를 resolve하는 새로운 프로미스를 반환한다.

  ```javascript
  Promise.race([
    new Promise(resolve => setTimeout(() => resolve(1), 3000)), // 1
    new Promise(resolve => setTimeout(() => resolve(2), 2000)), // 2
    new Promise(resolve => setTimeout(() => resolve(3), 1000))  // 3
  ]).then(console.log) // 3
    .catch(console.log)
  ```

  - 에러가 발생한 경우는 `Promise.all` 메소드와 동일하게 처리된다. 
    - 즉, `Promise.race` 메소드에 전달된 프로미스 처리가 하나라도 실패하면 가장 먼저 실패한 프로미스가 reject한 에러를 reject하는 새로운 프로미스를 즉시 반환한다.

  ```javascript
  Promise.race([
    new Promise((resolve, reject) => setTimeout(() => reject(new Error('Error 1!')), 3000)),
    new Promise((resolve, reject) => setTimeout(() => reject(new Error('Error 2!')), 2000)),
    new Promise((resolve, reject) => setTimeout(() => reject(new Error('Error 3!')), 1000))
  ]).then(console.log)
    .catch(console.log) // Error: Error 3!
  ```
