

# 이벤트

- 이벤트(event)
  - 브라우저에서의 이벤트란 예를 들어 사용자가 버튼을 클릭했을 때, 웹페이지가 로드되었을 때와 같은 것인데 이것은 DOM 요소와 관련이 있다.
  - 이벤트가 발생하는 시점이나 순서를 사전에 인지할 수 없으므로 일반적인 제어 흐름과는 다른 접근 방식이 필요하다. 
  - 즉, 이벤트가 발생하면 누군가 이를 감지할 수 있어야 하며 그에 대응하는 처리를 호출해 주어야 한다.
    - 이벤트가 발생하면 그에 맞는 반응을 하여야 한다. 
    - 이를 위해 이벤트는 일반적으로 함수에 연결되며 그 함수는 이벤트가 발생하기 전에는 실행되지 않다가 이벤트가 발생되면 실행된다. 
    - 이 함수를 **이벤트 핸들러**라 하며 이벤트에 대응하는 처리를 기술한다.
  - 브라우저는 이벤트를 감지할 수 있으며 이벤트 발생 시에는 통지해 준다. 이 과정을 통해 사용자와 웹페이지는 상호작용(Interaction)이 가능하게 된다.



- 이벤트 루프와 동시성
  - 브라우저는 단일 쓰레드(single-thread)에서 이벤트 드리븐(event-driven) 방식으로 동작한다.
    - 단일 쓰레드는 쓰레드가 하나뿐이라는 의미이며 이말은 곧 하나의 작업(task)만을 처리할 수 있다는 것을 의미한다.
  - 하지만 실제로 동작하는 웹 애플리케이션은 많은 task가 동시에 처리되는 것처럼 느껴진다. 
  - 이처럼 자바스크립트의 동시성(Concurrency)을 지원하는 것이 바로 **이벤트 루프(Event Loop)**이다.



- 구글의 V8을 비롯한 대부분의 자바스크립트 엔진은 크게 2개의 영역으로 나뉜다.

  - Call Stack(호출 스택)
    - 작업이 요청되면(함수가 호출되면) 요청된 작업은 순차적으로 Call Stack에 쌓이게 되고 순차적으로 실행된다. 
    - 자바스크립트는 단 하나의 Call Stack을 사용하기 때문에 해당 task가 종료하기 전까지는 다른 어떤 task도 수행될 수 없다.
  - Heap
    - 동적으로 생성된 객체 인스턴스가 할당되는 영역이다.
  - 자바스크립트 엔진은 단순히 작업이 요청되면 Call Stack을 사용하여 요청된 작업을 순차적으로 실행할 뿐이다. 
  - 동시성(Concurrency)을 지원하기 위해 필요한 비동기 요청(이벤트를 포함) 처리는 자바스크립트 엔진을 구동하는 환경 즉 **브라우저(또는 Node.js)가 담당**한다.
  - Event Queue(Task Queue)
    - 비동기 처리 함수의 콜백 함수, 비동기식 이벤트 핸들러, Timer 함수(`setTimeout()`, `setInterval()`)의 콜백 함수가 보관되는 영역.
    - **이벤트 루프(Event Loop)에 의해 특정 시점(Call Stack이 비어졌을 때)에 순차적으로 Call Stack으로 이동되어 실행**된다.

  - Event Loop(이벤트 루프)
    - Call Stack 내에서 현재 실행중인 task가 있는지 그리고 Event Queue에 task가 있는지 반복하여 확인한다. 
    - 만약 Call Stack이 비어있다면 Event Queue 내의 task가 Call Stack으로 이동하고 실행된다.
  - 예시1
    - 함수 `func1`이 호출되면 함수 func1은 Call Stack에 쌓인다.
    - 함수 `func1`은 함수 `func2`을 호출하므로 함수 `func2`가 Call Stack에 쌓이고 `setTimeout`이 호출된다.
    - `setTimeout`의 콜백함수는 즉시 실행되지 않고 지정 대기 시간만큼 기다리다가 “tick” 이벤트가 발생하면 태스크 큐로 이동한 후 Call Stack이 비어졌을 때 Call Stack으로 이동되어 실행된다.

  ```javascript
  function func1() {
      console.log('func1')
      func2()
  }
  
  function func2() {
      setTimeout(function () {
          console.log('func2')
      }, 0)
  
      func3()
  }
  
  function func3() {
      console.log('func3')
  }
  
  func1()
  ```

  - 예시2
    - 함수 `func1`이 호출되면 함수 func1은 Call Stack에 쌓인다.
    - 함수 `func1`은 함수 `func2`을 호출하므로 함수 `func2`가 Call Stack에 쌓이고 addEventListener가 호출된다.
    - **addEventListener의 콜백함수는 foo 버튼이 클릭되어 click 이벤트가 발생하면 태스크 큐로 이동한 후 Call Stack이 비어졌을 때 Call Stack으로 이동되어 실행된다.**

  ```javascript
  function func1() {
      console.log('func1')
      func2()
  }
  
  function func2() {
      const elem = document.querySelector('.foo')
  
      elem.addEventListener('click', function () {
          this.style.backgroundColor = 'indigo'
          console.log('func2')
      })
  
      func3()
  }
  
  function func3() {
      console.log('func3')
  }
  
  func1()
  ```



## 이벤트의 종류

> https://developer.mozilla.org/en-US/docs/Web/Events 참고

- UI 이벤트

    | Event  | Description                                                  |
    | ------ | ------------------------------------------------------------ |
    | load   | 웹페이지의 로드가 완료되었을 때                              |
    | unload | 웹페이지가 언로드될 때(주로 새로운 페이지를 요청한 경우)     |
    | error  | 브라우저가 자바스크립트 오류를 만났거나 요청한 자원이 존재하지 않는 경우 |
    | resize | 브라우저 창의 크기를 조절했을 때                             |
    | scroll | 사용자가 페이지를 위아래로 스크롤할 때                       |
    | select | 텍스트를 선택했을 때                                         |




- KeyBoard 이벤트

    | Event    | Description            |
    | -------- | ---------------------- |
    | keydown  | 키를 누르고 있을 때    |
    | keyup    | 누르고 있던 키를 뗄 때 |
    | keypress | 키를 누르고 뗏을 때    |




- Mouse 이벤트

    | Event     | Description                                                  |
    | --------- | ------------------------------------------------------------ |
    | click     | 마우스 버튼을 클릭했을 때                                    |
    | dbclick   | 마우스 버튼을 더블 클릭했을 때                               |
    | mousedown | 마우스 버튼을 누르고 있을 때                                 |
    | mouseup   | 누르고 있던 마우스 버튼을 뗄 때                              |
    | mousemove | 마우스를 움직일 때 (터치스크린에서 동작하지 않는다)          |
    | mouseover | 마우스를 요소 위로 움직였을 때 (터치스크린에서 동작하지 않는다) |
    | mouseout  | 마우스를 요소 밖으로 움직였을 때 (터치스크린에서 동작하지 않는다) |




- Focus 이벤트

    | Event          | Description               |
    | -------------- | ------------------------- |
    | focus/focusin  | 요소가 포커스를 얻었을 때 |
    | blur/foucusout | 요소가 포커스를 잃었을 때 |




- Form 이벤트

    | Event  | Description                                                  |
    | ------ | ------------------------------------------------------------ |
    | input  | input 또는 textarea 요소의 값이 변경되었을 때, contenteditable 어트리뷰트를 가진 요소의 값이 변경되었을 때 |
    | change | select box, checkbox, radio button의 상태가 변경되었을 때    |
    | submit | form을 submit할 때 (버튼 또는 키)                            |
    | reset  | reset 버튼을 클릭할 때 (최근에는 사용 안함)                  |




- Clipboard 이벤트

    | Event | Description            |
    | ----- | ---------------------- |
    | cut   | 콘텐츠를 잘라내기할 때 |
    | copy  | 콘텐츠를 복사할 때     |
    | paste | 콘텐츠를 붙여넣기할 때 |





## 이벤트 핸들러 등록

- 이벤트 핸들러를 이벤트에 등록하는 방법은 아래와 같이 3가지 이다.



- 인라인 이벤트 핸들러 방식

  - HTML 요소의 이벤트 핸들러 어트리뷰트에 이벤트 핸들러를 등록하는 방법.

  - 이 방식은 더 이상 사용되지 않으며 사용해서도 안된다. 

    - 오래된 코드에서 간혹 이 방식을 사용한 것이 있기 때문에 알아둘 필요는 있다. 

    - HTML과 Javascript는 관심사가 다르므로 분리하는 것이 좋다.
    - Angular,React,Vue.js와 같은 프레임워크/라이브러리에서는 인라인 이벤트 핸들러 방식으로 이벤트를 처리한다. 
    - 이들은 HTML, CSS, 자바스크립트를 뷰를 구성하기 위한 구성 요소로 보기 때문에 관심사가 다르다고 생각하지 않는다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <button onclick="myHandler()">Click me</button>
    <script>
      function myHandler() {
        alert('Thank You!');
      }
    </script>
  </body>
  </html>
  ```

  - 주의할 것은 onclick과 같이 on으로 시작하는 이벤트 어트리뷰트의 값으로 함수 호출을 전달(`onclick="myHandler()"`)한다는 것이다.
    - 다음에 살펴볼 이벤트 핸들러 프로퍼티 방식에는 DOM 요소의 이벤트 핸들러 프로퍼티에 함수 호출이 아닌 함수를 전달한다.
    - 이벤트 어트리뷰트의 값으로 전달한 함수 호출이 즉시 호출되는 것은 아니다. 
    - 사실은 이벤트 어트리뷰트 키를 이름으로 갖는 함수를 암묵적으로 정의하고 그 함수의 몸체에 이벤트 어트리뷰트의 값으로 전달한 함수 호출을 문으로 갖는다.
    - 위 예제의 경우, button 요소의 onclick 프로퍼티에 함수 `function onclick(event) { myHandler(); }`가 할당된다.
    - 즉, 이벤트 어트리뷰트의 값은 암묵적으로 정의되는 이벤트 핸들러의 문이다. 따라서 아래와 같이 여러 개의 문을 전달할 수 있다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <button onclick="myHandler1(); myHandler2();">Click me</button>
    <script>
      function myHandler1() {
        alert('myHandler1');
      }
      function myHandler2() {
        alert('myHandler2');
      }
    </script>
  </body>
  </html>
  ```

  

- 이벤트 핸들러 프로퍼티 방식

  - 인라인 이벤트 핸들러 방식처럼 HTML과 Javascript가 뒤섞이는 문제는 해결할 수 있는 방식이다. 
  - 하지만 이벤트 핸들러 프로퍼티에 하나의 이벤트 핸들러만을 바인딩할 수 있다는 단점이 있다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <button class="btn">Click me</button>
    <script>
      const btn = document.querySelector('.btn')
  	
      // 인라인 이벤트 핸들러 방식과 달리 함수 호출이 아닌 함수 자체를 전달한다.
      // 이벤트 핸들러 프로퍼티 방식은 이벤트에 하나의 이벤트 핸들러만을 바인딩할 수 있다
      // 첫번째 바인딩된 이벤트 핸들러 => 실행되지 않는다.
      btn.onclick = function () {
        alert('① Button clicked 1')
      }
  
      // 두번째 바인딩된 이벤트 핸들러
      btn.onclick = function () {
        alert('① Button clicked 2')
      }
    </script>
  </body>
  </html>
  ```



- `addEventListener` 메소드 방식

  - `addEventListener`메소드를 이용하여 대상 DOM 요소에 이벤트를 바인딩한 후, 해당 이벤트가 발생했을 때 실행 될 콜백 함수(이벤트 핸들러)를 지정한다.

  ```javascript
  // 세 번째 매개 변수를 true로 설정하면 캡처링으로 전파되는 이벤트를 캐치하고, false로 설정하거나 미설정하면 버블링으로 전파되는 이벤트를 캐치한다.
  EvnetTarget.addEventListner('eventType',functionName(또는 함수 자체),boolean)
  ```

  - `addEventListener` 함수 방식은 이전 방식에 비해 아래와 같이 보다 나은 장점을 갖는다.
    - 하나의 이벤트에 대해 하나 이상의 이벤트 핸들러를 추가할 수 있다.
    - 캡처링과 버블링을 지원한다.
    - HTML 요소뿐만아니라 모든 DOM 요소(HTML, XML, SVG)에 대해 동작한다. 브라우저는 웹 문서(HTML, XML, SVG)를 로드한 후, 파싱하여 DOM을 생성한다.
  - IE9 이상에서 동작한다. IE8 이하에서는 `attachEvent` 메소드를 사용한다.
  - 대상 DOM 요소(target)를 지정하지 않으면 전역객체 window, 즉 DOM 문서를 포함한 브라우저의 윈도우에서 발생하는 click 이벤트에 이벤트 핸들러를 바인딩한다. 
    - 따라서 브라우저 윈도우 어디를 클릭하여도 이벤트 핸들러가 동작한다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <script>
      addEventListener('click', function () {
        alert('Clicked!')
      })
    </script>
  </body>
  </html
  ```

  - `addEventListener` 메소드의 두번째 매개변수는 이벤트가 발생했을 때 호출될 이벤트 핸들러이다. 
    - 이때 두번째 매개변수에는 함수 호출이 아니라 함수 자체를 지정하여야 한다.
    - 따라서 이벤트 핸들러 프로퍼티 방식과 같이 이벤트 핸들러 함수에 인수를 전달할 수 없는 문제가 발생한다. 
    - 이를 우회하는 방법은 아래와 같다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <label>User name <input type='text'></label>
    <em class="message"></em>
  
    <script>
      const MIN_USER_NAME_LENGTH = 2; // 이름 최소 길이
  
      const input = document.querySelector('input[type=text]');
      const msg = document.querySelector('.message');
  
      function checkUserNameLength(n) {
        if (input.value.length < n) {
          msg.innerHTML = '이름은 ' + n + '자 이상이어야 합니다';
        } else {
          msg.innerHTML = '';
        }
      }
  
      input.addEventListener('blur', function () {
        // 이벤트 핸들러 내부에서 함수를 호출하면서 인수를 전달한다.
        checkUserNameLength(MIN_USER_NAME_LENGTH);
      });
  
      // 이벤트 핸들러 프로퍼티 방식도 동일한 방식으로 인수를 전달할 수 있다.
      // input.onblur = function () {
      //   // 이벤트 핸들러 내부에서 함수를 호출하면서 인수를 전달한다.
      //   checkUserNameLength(MIN_USER_NAME_LENGTH);
      // };
    </script>
  </body>
  </html>
  ```





## 이벤트 핸들러 함수 내부의 this

- 인라인 이벤트 핸들러 방식

  - 인라인 이벤트 핸들러 방식의 경우, 이벤트 핸들러는 일반 함수로서 호출되므로 이벤트 핸들러 내부의 **this는 전역 객체 window**를 가리킨다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <button onclick="foo()">Button</button>
    <script>
      function foo () {
        console.log(this) // window
      }
    </script>
  </body>
  </html>
  ```



- 이벤트 핸들러 프로퍼티 방식

  - 이벤트 핸들러 프로퍼티 방식에서 이벤트 핸들러는 메소드이므로 이벤트 핸들러 내부의 **this는 이벤트에 바인딩된 요소**를 가리킨다. 
  - 이것은 이벤트 객체의 currentTarget 프로퍼티와 같다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <button class="btn">Button</button>
    <script>
      const btn = document.querySelector('.btn')
  
      btn.onclick = function (e) {
        console.log(this) // <button id="btn">Button</button>
        console.log(e.currentTarget) // <button id="btn">Button</button>
        console.log(this === e.currentTarget) // true
      }
    </script>
  </body>
  </html>
  ```



- `addEventListener` 메소드 방식

  - addEventListener 메소드에서 지정한 이벤트 핸들러는 콜백 함수이지만 이벤트 핸들러 내부의 **this는 이벤트 리스너에 바인딩된 요소(currentTarget)**를 가리킨다. 
  - 이것은 이벤트 객체의 currentTarget 프로퍼티와 같다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <button class="btn">Button</button>
    <script>
      const btn = document.querySelector('.btn')
  
      btn.addEventListener('click', function (e) {
        console.log(this) // <button id="btn">Button</button>
        console.log(e.currentTarget) // <button id="btn">Button</button>
        console.log(this === e.currentTarget) // true
      })
    </script>
  </body>
  </html>
  ```





## 이벤트의 흐름

- 버블링과 캡처링

  - 계층적 구조에 포함되어 있는 HTML 요소에 이벤트가 발생할 경우 연쇄적 반응이 일어난다. 
  - 즉, 이벤트가 전파(Event Propagation)되는데 전파 방향에 따라 **버블링(Event Bubbling)**과 캡처링**(Event Capturing)**으로 구분할 수 있다.
  - 주의할 것은 버블링과 캡처링은 둘 중에 하나만 발생하는 것이 아니라 캡처링부터 시작하여 버블링으로 종료한다는 것이다.
  - 즉, 이벤트가 발생했을 때 캡처링과 버블링은 순차적으로 발생한다.

  ```html
  <!DOCTYPE html>
  <html>
  <head>
    <style>
      html { border:1px solid red; padding:30px; text-align: center; }
      body { border:1px solid green; padding:30px; }
      .top {
        width: 300px; height: 300px;
        background-color: red;
        margin: auto;
      }
      .middle {
        width: 200px; height: 200px;
        background-color: blue;
        position: relative; top: 34px; left: 50px;
      }
      .bottom {
        width: 100px; height: 100px;
        background-color: yellow;
        position: relative; top: 34px; left: 50px;
        line-height: 100px;
      }
    </style>
  </head>
  <body>
    body
    <div class="top">top
      <div class="middle">middle
        <div class="bottom">bottom</div>
      </div>
    </div>
    <script>
    const useCature = true
  
    const handler = function (e) {	// e에는 event 객체가 들어간다.
      const phases = ['capturing', 'target', 'bubbling']
      const node = this.nodeName + (this.className ? '.' + this.className : '')
      // eventPhase: 이벤트 흐름 상에서 어느 phase에 있는지를 반환한다.
      // 0 : 이벤트 없음 / 1 : 캡처링 단계 / 2 : 타깃 / 3 : 버블링 단계
      console.log(node, phases[e.eventPhase - 1])
      alert(node + ' : ' + phases[e.eventPhase - 1])
    }
  
    document.querySelector('html').addEventListener('click', handler, useCature)
    document.querySelector('body').addEventListener('click', handler, useCature)
  
    document.querySelector('div.top').addEventListener('click', handler, useCature)
    document.querySelector('div.middle').addEventListener('click', handler, useCature)
    document.querySelector('div.bottom').addEventListener('click', handler, useCature)
    </script>
  </body>
  </html>
  ```

  

- 버블링

  - 자식 요소에서 발생한 이벤트가 부모 요소로 전파되는 것.
  - 아래 코드는 모든 이벤트 핸들러가 이벤트 흐름을 버블링만 캐치한다. 
    - 즉, 캡쳐링 이벤트 흐름에 대해서는 동작하지 않는다. 
    - 따라서 button에서 이벤트가 발생하면 모든 이벤트 핸들러는 버블링에 대해 동작하여 button, paragraph, body 순으로 로그된다.
    - 만약 p요소에서 이벤트가 발생한다면 p 요소와 body 요소의 이벤트 핸들러는 버블링에 대해 동작하여 paragraph, body 순으로 로그된다.

  ```html
  <!DOCTYPE html>
  <html>
  <head>
    <style>
      html, body { height: 100%; }
    </style>
  <body>
    <p>버블링 이벤트 <button>버튼</button></p>
    <script>
      const body = document.querySelector('body');
      const para = document.querySelector('p');
      const button = document.querySelector('button');
  
      // 버블링
      body.addEventListener('click', function () {
        console.log('Handler for body.');
      });
  
      // 버블링
      para.addEventListener('click', function () {
        console.log('Handler for paragraph.');
      });
  
      // 버블링
      button.addEventListener('click', function () {
        console.log('Handler for button.');
      });
    </script>
  </body>
  </html>
  ```

  



- 캡처링

  - 자식 요소에서 발생한 이벤트가 부모 요소부터 시작하여 이벤트를 발생시킨 자식 요소까지 도달하는 것.
  - 캡처링은 IE8 이하에서 지원되지 않는다.
  - 아래 코드는 모든 이벤트 핸덜러가 이벤트 흐름을 캡처링만 캐치한다.
    - 즉, 버블링 이벤트 흐름에 대해서는 동작하지 않는다. 
    - 따라서 button에서 이벤트가 발생하면 모든 이벤트 핸들러는 캡처링에 대해 동작하여 body, paragraph, button 순으로 로그된다.
    - 만약 p 요소에서 이벤트가 발생한다면 p 요소와 body 요소의 이벤트 핸들러는 캡처링에 대해 동작하여 body, paragraph 순으로 로그된다.

  ```html
  <!DOCTYPE html>
  <html>
  <head>
    <style>
      html, body { height: 100%; }
    </style>
  <body>
    <p>캡처링 이벤트 <button>버튼</button></p>
    <script>
      const body = document.querySelector('body')
      const para = document.querySelector('p')
      const button = document.querySelector('button')
  
      // 캡처링
      body.addEventListener('click', function () {
        console.log('Handler for body.')
      }, true)
  
      // 캡처링
      para.addEventListener('click', function () {
        console.log('Handler for paragraph.')
      }, true)
  
      // 캡처링
      button.addEventListener('click', function () {
        console.log('Handler for button.')
      }, true)
    </script>
  </body>
  </html>
  ```

  

- 캡처링과 버블링이 혼용되는 경우

  - 캡처링이 먼저 발생하고 버블링이 후에 발생한다.
  - body, button 요소는 버블링 이벤트 흐름만을 캐치하고 p 요소는 캡처링 이벤트 흐름만을 캐치한다.
  - 따라서 button에서 이벤트가 발생하면 먼저 캡처링이 발생하므로 p 요소의 이벤트 핸들러가 동작하고, 그후 버블링이 발생하여 button, body 요소의 이벤트 핸들러가 동작한다.
  - 만약 p 요소에서 이벤트가 발생한다면 캡처링에 대해 p 요소의 이벤트 핸들러가 동작하고 버블링에 대해 body 요소의 이벤트 핸들러가 동작한다.

  ```html
  <!DOCTYPE html>
  <html>
  <head>
    <style>
      html, body { height: 100%; }
    </style>
  <body>
    <p>버블링과 캡처링 이벤트 <button>버튼</button></p>
    <script>
      const body = document.querySelector('body')
      const para = document.querySelector('p')
      const button = document.querySelector('button')
  
      // 버블링
      body.addEventListener('click', function () {
        console.log('Handler for body.')
      })
  
      // 캡처링
      para.addEventListener('click', function () {
        console.log('Handler for paragraph.')
      }, true)
  
      // 버블링
      button.addEventListener('click', function () {
        console.log('Handler for button.')
      })
    </script>
  </body>
  </html>
  ```

  

## 이벤트 객체

- 이벤트 객체

  - event 객체는 이벤트를 발생시킨 요소와 발생한 이벤트에 대한 유용한 정보를 제공한다. 
  - 이벤트가 발생하면 event 객체는 동적으로 생성되며 이벤트를 처리할 수 있는 이벤트 핸들러에 인자로 전달된다.
    - event 객체는 이벤트 핸들러에 암묵적으로 전달된다. 
    - 그러나 이벤트 핸들러를 선언할 때, event 객체를 전달받을 첫번째 매개변수를 명시적으로 선언하여야 한다. 
    - 예시에서 e라는 이름으로 매개변수를 지정하였으나 다른 매개변수 이름을 사용하여도 상관없다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <p>클릭하세요. 클릭한 곳의 좌표가 표시됩니다.</p>
    <em class="message"></em>
    <script>
    function showCoords(e) { // e: event object
      const msg = document.querySelector('.message');
      msg.innerHTML =
        'clientX value: ' + e.clientX + '<br>' +
        'clientY value: ' + e.clientY;
    }
    addEventListener('click', showCoords);
    </script>
  </body>
  </html>
  ```

  - 다른 인수를 받아야 하는 경우

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <em class="message"></em>
    <script>
    function showCoords(e, msg) {
      msg.innerHTML =
        'clientX value: ' + e.clientX + '<br>' +
        'clientY value: ' + e.clientY;
    }
  
    const msg = document.querySelector('.message');
  
    addEventListener('click', function (e) {
      showCoords(e, msg);
    });
    </script>
  </body>
  </html>
  ```

  

- Event Property

  - `Event.target`
    - 실제로 이벤트를 발생시킨 요소를 가리킨다.
    - **`Event.target`은 `this`와 반드시 일치하지는 않는다.**
    - 함수를 특정 노드에 한정하여 사용하지 않고 범용적으로 사용하기 위해 사용한다.
    - 하지만 아래 예제의 경우 버튼별로 이벤트를 바인딩하고 있기 때문에 버튼이 많은 경우 위 방법은 바람직하지 않아 보인다.
    - 이벤트 위임을 통해 수정이 가능하다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <div class="container">
      <button id="btn1">Hide me 1</button>
      <button id="btn2">Hide me 2</button>
    </div>
  
    <script>
      function hide(e) {
        e.target.style.visibility = 'hidden'
        // this와 동일하게 동작한다.
        // this.style.visibility = 'hidden'
      }
      document.getElementById('btn1').addEventListener('click', hide)
      document.getElementById('btn2').addEventListener('click', hide)
    </script>
  </body>
  </html>
  ```

  ```html
  <!DOCTYPE html>
  <!--이벤트 위임-->
  <html>
  <body>
    <div class="container">
      <button id="btn1">Hide me 1</button>
      <button id="btn2">Hide me 2</button>
    </div>
  
    <script>
      const container = document.querySelector('.container')
  
      function hide(e) {
        // e.target은 실제로 이벤트를 발생시킨 DOM 요소를 가리킨다.
        e.target.style.visibility = 'hidden';
        // this는 이벤트에 바인딩된 DOM 요소(.container)를 가리킨다. 따라서 .container 요소를 감춘다.
        // this.style.visibility = 'hidden';
        // 즉, `Event.target`은 `this`와 반드시 일치하는 것은 아니다.
      }
  
      container.addEventListener('click', hide)
    </script>
  </body>
  </html>
  ```

  - `Event.currentTarget`
    - 이벤트에 바인딩된 DOM 요소를 가리킨다. 즉, `addEventListener` 앞에 기술된 객체를 가리킨다.
    - `addEventListener` 메소드에서 지정한 이벤트 핸들러 내부의 this는 이벤트에 바인딩된 DOM 요소를 가리키며 이것은 이벤트 객체의 `currentTarget` 프로퍼티와 같다. 따라서 **이벤트 핸들러 함수 내에서 `currentTarget`과 `this`는 언제나 일치**한다.

  ```html
  <!DOCTYPE html>
  <html>
  <head>
    <style>
      html, body { height: 100%; }
      div { height: 100%; }
    </style>
  </head>
  <body>
    <div>
      <button>배경색 변경</button>
    </div>
    <script>
      function bluify(e) {
        // this: 이벤트에 바인딩된 DOM 요소(div 요소)
        console.log('this: ', this)
        // target: 실제로 이벤트를 발생시킨 요소(button 요소 또는 div 요소)
        console.log('e.target:', e.target)
        // currentTarget: 이벤트에 바인딩된 DOM 요소(div 요소)
        console.log('e.currentTarget: ', e.currentTarget)
  
        // 언제나 true
        console.log(this === e.currentTarget)
        // currentTarget과 target이 같은 객체일 때 true
        console.log(this === e.target)
  
        // click 이벤트가 발생하면 이벤트를 발생시킨 요소(target)과는 상관없이 this(이벤트에 바인딩된 div 요소)의 배경색이 변경된다.
        this.style.backgroundColor = '#A5D9F3'
      }
  
      // div 요소에 이벤트 핸들러가 바인딩되어 있다.
      // 자식 요소인 button이 발생시킨 이벤트가 버블링되어 div 요소에도 전파된다.
      // 따라서 div 요소에 이벤트 핸들러가 바인딩되어 있으면 자식 요소인 button이 발생시킨 이벤트를 div 요소에서도 핸들링할 수 있다.
      document.querySelector('div').addEventListener('click', bluify)
    </script>
  </body>
  </html>
  ```

  - `Event.type`
    - 발생한 이벤트의 종류를 나타내는 문자열을 반환한다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <p>키를 입력하세요</p>
    <em class="message"></em>
    <script>
    const body = document.querySelector('body')
  
    function getEventType(e) {
      console.log(e)
      document.querySelector('.message').innerHTML = `${e.type} : ${e.keyCode}`
    }
  
    body.addEventListener('keydown', getEventType)
    body.addEventListener('keyup', getEventType)
    </script>
  </body>
  </html>
  ```

  - `Event.cancelable`
    - 요소의 기본 동작을 취소시킬 수 있는지 여부(true/false)를 나타낸다.
    - 아래 예제의 경우 true가 뜨는데 이는 \<a\> 태그의 기본 동작인 해당 주소로의 이동을 취소시킬 수 있다는 것을 의미한다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <a href="poiemaweb.com">Go to poiemaweb.com</a>
    <script>
    const elem = document.querySelector('a')
  
    elem.addEventListener('click', function (e) {
      console.log(e.cancelable)	// true
      // 기본 동작을 중단시킨다.
      e.preventDefault()
    })
    </script>
  </body>
  </html>
  ```

  - `Event.eventPhase`
    - 이벤트 흐름(event flow) 상에서 어느 단계(event phase)에 있는지를 반환한다.

  | 반환값 | 의미        |
  | ------ | ----------- |
  | 0      | 이벤트 없음 |
  | 1      | 캡쳐링 단계 |
  | 2      | 타깃        |
  | 3      | 버블링 단계 |

  

## Event Delegation

- 이벤트 위임

  - 다수의 자식 요소에 각각 이벤트 핸들러를 바인딩하는 대신 하나의 부모 요소에 이벤트 핸들러를 바인딩하는 방법
  - 이는 이벤트가 이벤트 흐름에 의해 이벤트를 발생시킨 요소의 부모 요소에도 영향(버블링)을 미치기 때문에 가능한 것이다.
  - 이벤트 위임을 사용하지 않을 경우
    - 모든 li 요소가 클릭 이벤트에 반응하는 처리를 구현하고 싶은 경우, li 요소에 이벤트 핸들러를 바인딩하면 총 3개의 이벤트 핸들러를 바인딩하여야 한다.
    - 만일 li 요소가 100개라면 100개의 이벤트 핸들러를 바인딩하여야 한다. 이는 실행 속도 저하의 원인이 될 뿐 아니라 코드 또한 매우 길어지며 작성 또한 불편하다.
    - 그리고 **동적으로 li 요소가 추가되는 경우, 아직 추가되지 않은 요소는 DOM에 존재하지 않으므로 이벤트 핸들러를 바인딩할 수 없다.**
    - 이러한 경우 이벤트 위임을 사용한다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <ul class="post-list">
      <li id="post-1">Item 1</li>
      <li id="post-2">Item 2</li>
      <li id="post-3">Item 3</li>
    </ul>
    <script>
      document.querySelector('#post-1').addEventListener('click', printId)
      document.querySelector('#post-2').addEventListener('click', printId)
      document.querySelector('#post-3').addEventListener('click', printId)
    </script>
  </body>
  </html>
  ```

  - 이벤트 위임 사용
    - 실제로 이벤트를 발생시킨 요소를 알아내기 위해서는 `Event.target`을 사용한다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <ul class="post-list">
      <li id="post-1">Item 1</li>
      <li id="post-2">Item 2</li>
      <li id="post-3">Item 3</li>
    </ul>
    <div class="msg">
    <script>
      const msg = document.querySelector('.msg');
      const list = document.querySelector('.post-list')
  
      list.addEventListener('click', function (e) {
        // 이벤트를 발생시킨 요소
        console.log('[target]: ' + e.target);
        // 이벤트를 발생시킨 요소의 nodeName
        console.log('[target.nodeName]: ' + e.target.nodeName);
  
        // li 요소 이외의 요소에서 발생한 이벤트는 대응하지 않는다.
        if (e.target && e.target.nodeName === 'LI') {
          msg.innerHTML = 'li#' + e.target.id + ' was clicked!';
        }
      });
    </script>
  </body>
  </html>
  ```

  

## 기본 동작의 변경

- 이벤트 객체는 요소의 기본 동작과 요소의 부모 요소들이 이벤트에 대응하는 방법을 변경하기 위한 메소드는 가지고 있다.



- `Event.preventDefault()`

  - 폼을 submit하거나 링크를 클릭하면 다른 페이지로 이동하게 된다. 
  - 이와 같이 요소가 가지고 있는 기본 동작을 중단시키기 위한 메소드가 preventDefault()이다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <a href="http://www.google.com">go</a>
    <script>
    document.querySelector('a').addEventListener('click', function (e) {
      console.log(e.target, e.target.nodeName)
      // a 요소의 기본 동작을 중단한다.
      e.preventDefault()
    })
    </script>
  </body>
  </html>
  ```



- `Event.stopPropagation()`

  - 어느 한 요소를 이용하여 이벤트를 처리한 후 이벤트가 부모 요소로 이벤트가 전파되는 것을 중단시키기 위한 메소드이다. 
  - 부모 요소에 동일한 이벤트에 대한 다른 핸들러가 지정되어 있을 경우 사용된다.
  - 아래 코드를 보면, 부모 요소와 자식 요소에 모두 mousedown 이벤트에 대한 핸들러가 지정되어 있다. 
    - 하지만 부모 요소와 자식 요소의 이벤트를 각각 별도로 처리하기 위해 button 요소의 이벤트의 전파(버블링)를 중단시키기 위해서는`stopPropagation` 메소드를 사용하여 이벤트 전파를 중단할 필요가 있다.

  ```html
  <!DOCTYPE html>
  <html>
  <head>
    <style>
      html, body { height: 100%;}
    </style>
  </head>
  <body>
    <p>버튼을 클릭하면 이벤트 전파를 중단한다. <button>버튼</button></p>
    <script>
      const body = document.querySelector('body')
      const para = document.querySelector('p')
      const button = document.querySelector('button')
  
      // 버블링
      body.addEventListener('click', function () {
        console.log('Handler for body.')
      })
  
      // 버블링
      para.addEventListener('click', function () {
        console.log('Handler for paragraph.')
      })
  
      // 버블링
      button.addEventListener('click', function (event) {
        console.log('Handler for button.')
  
        // 이벤트 전파를 중단한다.
        event.stopPropagation()
      })
    </script>
  </body>
  </html>
  ```



- ` preventDefault` & `stopPropagation`

  - 기본 동작의 중단과 버블링 또는 캡처링의 중단을 동시에 실시하는 방법은 아래와 같다.
    - 단 이 방법은 jQuery를 사용할 때와 아래와 같이 사용할 때만 적용된다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <a href="http://www.google.com" onclick='return handleEvent()'>go</a>
    <script>
    function handleEvent() {
      return false	// false를 return하면 된다.
    }
    </script>
  </body>
  </html>
  ```

  - JQuery를 사용할 떄

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <div>
      <a href="http://www.google.com">go</a>
    </div>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.3/jquery.min.js"></script>
    <script>
  
    // within jQuery
    $('a').click(function (e) {
      e.preventDefault()
    })
  
    $('a').click(function () {
      return false
    })
  
    // pure js
    document.querySelector('a').addEventListener('click', function(e) {
      return false       // 이렇게 사용할 수는 없다.
    })
    </script>
  </body>
  </html>
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


