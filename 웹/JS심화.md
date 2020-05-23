# 심화

- JS로 HTML파일 작성하기

  - HTML로 작성할 수도 있는데 굳이 JS로 작성하는 이유는 HTML은 정적으로 보여주는 것 밖에 할 수 없으나 JS는 보다 동적으로 작동하게 할 수 있기 때문이다.
  - 예를 들어 게시글을 추가하는 페이지를 만든다고 하면 HTML로만 작성할 경우 HTML은 제출 버튼, 입력 창 등을 띄울 수 있으나 입력창에 글을 입력하고 제출버튼을 누른다고 해서 그 게시글이 등록되게 할 수는 없다. 그러나 JS는 실제로 등록되게 하는 것이 가능하다.
  - JS로 태그를 지정하는 방법

  ```html
  <h1>hello world</h1>
  <h2 class="class1 class2 class3">hi!!</h2>
  
  <script>
   //1.태그를 지정하는 방법
  const newH1 = document.querySelector('h1')
  console.log(newH1)
  console.log(newH1.innerText)
      
  //2.지정한 태그를 활용하는 방법
  const inText = newH1.innerText
  console.log(inText)
      
  //3.지정된 클래스를 보는 방법
  const newH2 = document.querySelector('h2')
  console.log(newH2.classList)
      
  //4.클래스를 추가하는 방법
  newH2.classList.add('class4')
  console.log(newH2.classList)
  </script>
  
  out
  <!--1-->
  <h1>hello world</h1> 
  hello world
  <!--2-->
  hello world
  <!--3-->
  <!--"class1 class2 class3"라는 문자열이 parsing되어 object형태로 들어가게 된다.-->>
  DOMTokenList(3) ["class1", "class2", "class3", value: "class1 class2 class3"]
  <!--4-->
  DOMTokenList(3) ["class1", "class2", "class3", "class4", value: "class1 class2 class3 class4"]
  ```

  - JS로 태그를 만드는 방법
    - 아래와 같이 할 경우 변수에는 object가 담기게 된다.
    - `.`으로 접근할 수 있는 이유가 바로 이것이다. 모두 오브젝트 안에 오브젝트가 있는 형태이기 때문에 ` .`으로 접근이 가능하다.

  ```JS
  //방법1. createElement활용
  const 변수명 = document.createElement('태그명')
  
  //e.g.
  const myH1 = document.createElement('h1')
  myH1.innerText = "hello world"
  console.log(myH1)
  console.log(typeof(myH1))
  console.log(myH1.classList)
  
  
  out
  <h1>hello world</h1>
  object
  DOMTokenList [value: ""]
  
  
  
  //방법2-1. innerHTML 활용
  //innerHTML은 지정한 태그의 하부에 태그를 넣는 것이므로 상부 태그가 있을 경우 하부 태그 생성이 가능하다.
  //일반적으로 대부분의 태그들은 <body>태그 안에 생성이 되므로 body태그를 지정하고
  const myBody = document.querySelector('body')
  //그 자식태그로 <h1>태그를 넣는다.
  myBody.innerHTML="<h1>hello world</h1>"
  console.log(myBody.innerHTML)
  console.log(typeof(myBody.innerHTML))
  console.log(myBody.innerHTML.classList)
  
  
  out
  //아래에서는 잘 구분이 안되지만 브라우저에서 출력해보면 태그가 아니라 문자열로 나오는 것을 알 수 있다.
  <h1>hello world</h1>
  string
  undefined  //태그(오브젝트)가 아닌 문자열이므로 classList가 있을 수 없다.
  
  
  //방법2-2.문자열이 아닌 태그로 만드는 방법
  //앞 부분은 2-1과 동일
  const myBody = document.querySelector('body')
  myBody.innerHTML="<h1>hello world</h1>"
  //이를 변수에 담고 출력하면
  const myH1=document.querySelector('h1')
  console.log(myH1)
  console.log(typeof(myH1))
  console.log(myH1.classList)
  
  
  out
  <h1>hello world</h1>
  object
  DOMTokenList [value: ""]
  ```

  - 태그에 각종 속성을 부여하는 방법

  ```javascript
  //방법1
  변수명.속성명='속성값'
  //e.g. LiCheck.type = 'checkbox'      아래 코드와 같은 코드다.
  
  //방법2
  변수명.setAttribute('속성명','속성값')
  //e.g. newLiCheck.setAttribute('type','checkbox')
  //방법1,2는 속도에서 차이가 난다.
  
  
  
  //어트리뷰트 노드에의 접근/수정(클래스부여)은 조금 다르다.
  //그냥 class가 아닌 classList를 쓴다.
  변수명.classList.add(클래스1, 클래스2.....)
  
  
  // HTML 콘텐츠 조작(Manipulation)
  //innerHTML과 innerTEXT의 차이
  const cardTitle = document.createElement('h5')
  cardText.innerHTML = '<a>hi</a>'  //hi가 출력
  cardText.innerText = '<a>hi</a>'  //<a>hi</a>가 출력
  ```

  - 예시

  ```html
  <!--card 만들기-->
  <!--bootstrap 코드-->
  <div class="card" style="width: 18rem;">   <!--1-->
    <img src="https://picsumphotos/200" class="card-img-top" alt="random-image">  <!--2-->
    <div class="card-body">
      <h5 class="card-title">Card title</h5>
      <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
      <a href="#" class="btn btn-primary">Go somewhere</a>
    </div>
  </div>
  
  
  <!--JS로 구현-->
      <div class="form-group">
          <label for="cardTitleInput">Card Title</label>
          <input id="cardTitleInput" class="form-control" type="text">
          <label for="cardtextInput">Card Text</label>
          <input type="text" id="cardTextInput" class="form-control">
      </div>
      <button id="createCardButton" class="btn btn-primary">CreateCard</button>
  
      <div class="container mt-3">
          <div id="cardArea" class="row">
              <!-- Card가 들어가는 곳 -->
          </div>
      </div>
  
  <script>
      //card를 생성하는 함수
      function createCard(title, content){
          const card = document.createElement('div')   //1에서 div 태그를 만드는 부분
          card.classList.add('card','col-4')  
          //1에서 class="card" style="width: 18rem 부분
          //col-4도 classList에 추가하는 이유는 style이 아닌 bootstrap class기 때문이다.
          
          const cardImage = document.createElement('img') //2에서 img 태그를 만드는 부분
          cardImage.src = "https://picsumphotos/200"  //2에서 src,class,alt를 설정하는 부분
          cardImage.classList.add("card-img-top")
          cardImage.alt = 'random-image'
  
          const cardBody = document.createElement('div')
          cardBody.classList.add('card-body')
  
          const cardTitle = document.createElement('h5')
          cardTitle.classList.add('card-title')
          catdTitle.innerText = title
  
          const cardText = document.createElement('p')
          cardText.classList.add('card-text')
          cardText.innerHTML = content
  
          const cardButton = document.createElement('a')
          cardButton.classList.add('btn','btn-primary')
          cardButton.href = '#'
          cardButton.innerText = 'Go somewhere'
  
          //appendChild:Node 한개만 추가 가능
          //append:Node 여러 개 추가 가능, Text도 추가 가능
          //cardBody에 들어가야 할 것들을 추가
          cardBody.append(cardTitle,cardText,cardButton)
          //card에 들어가야 할 것을 추가
          card.append(cardImage,cardBody)  
          
          //마지막으로 카드가 들어갈 div태그를 id를 활용하여 지정한 후 card를 추가
          const cardArea = document.querySelector('#cardArea')
          cardArea.appendChild(card)
      }
      //여기까지 완성된 시점에서 console창에 createCard()를 입력하면 카드가 생성된다. 그러나 개발자		가 아닌 사람에게 이렇게 카드를 생성하라고 할 수 는 없으므로 버튼은 만들어 준다.
      
      //card 생성을 위한 버튼
      const createCardButton = document.querySelector('#createCardButton')
      
      createCardButton.addEventListener('click', function() {
        const cardTitleInput = document.querySelector('#cardTitleInput')
        const cardTextInput = document.querySelector('#cardTextInput')
        //<input>태그의 값에 접근할 때는 innerText, innerHTML이 아닌 value를 써야 한다.
        createCard(cardTitleInput.value, cardTextInput.value)
        cardTitleInput.value = null
        cardTextInput.value = null
      })
  </script>
  ```

  

- 기본적인 순서

  - 아래 과정을 요약하면 "요소를 잡아서(혹은 만들어서) 꾸미고 붙인다."로 요약할 수 있다. 
  - 태그를 담을 변수 생성 혹은 지정(실제로 변수에 담기는 것은 object이다).
  - 태그에 속성 부여
- 생성한 태그를  조상 태그에 넣기
  
  ```html
  <!DOCTYPE html>
  <html lang="ko">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>0518 exercise & workshop</title>
  </head>
  <body>
    <h2>Add New Todo</h2>
    <p id='newTodo'></p> <!--id를 주는 이유는 다른 p태그들과 구분하기 위함이다. id는 한 html 파일 내에서 유일한 값이기 때문에 겹칠 일이 없다. JS에서 주로 쓰이며 bootstrap등을 봐도 id의 사용을 거의 찾아볼 수 없는데 이는 JS에서 사용할 수 있도록 양보한 것이라고 볼 수 있다.-->
  
    <script>
      //<label>태그를 담을 변수를 만들고
      const newTodoLabel = document.createElement('label') //객체를 생성하는것
      //라벨 테그에 text 입력
      //<label>Add New Todo: </label>과 동일한 코드
      newTodoLabel.innerText = 'Add New Todo: '
        
      console.log(typeof(newTodoLabel))  //object라고 나온다.
      /*
      {
        innerText:'Add New Todo: '
        tagName:'label'
      }
      오브젝트형
      이런 모양으로 생겼을 것이다. 실제 이렇게 생겼는지는 모른다.
      */
  	
      //input태그를 담을 변수 생성
      const newTodoInput = document.createElement('input')
      //라벨을 누르면 입력창이 활성화 되는 기능을 구현하기 위한 코드 1
      newTodoInput.id = 'newTodoInput'
      //라벨을 누르면 입력창이 활성화 되는 기능을 구현하기 위한 코드 2
      newTodoLabel.htmlFor = 'newTodoInput' 
      //htmlFor는 label 태그를 생성하면 있는 for와 동일하다.
  	
      //button태그를 담을 변수 생성
      const newTodoButton = document.createElement('button')
      newTodoButton.innerText = 'Add'
  	
      //위에서 생성한 태그들을 담을 변수 생성
      const newTodo = document.querySelector('#newTodo') //위에서 설정한 id값을 활용
      newTodo.append(newTodoLabel,newTodoInput,newTodoButton)
    </script>
  </body>
  </html>
  ```
  
  - DOM에서 특정 요소를 선택할 때는 아래의 두 개를 사용한다. 
    - document.querySelector():  CSS셀렉터를 이용하여 노드를 선택함, querySelector()는 일치되는 첫 번째 노드만을 반환
    - document.querySelectorall(): CSS셀렉터를 이용하여 노드를 선택함, querySelectorAll()는 일치하는 모든 노드를 배열로 반환
  - DOM 조작
    - createElement(), createTextNode(): 요소와 텍스트노드의 생성
    - appendChild(): 특정 노드의 자식으로 노드를 삽입하기 위해 사용, Node 한개만 추가 가능
    - append(): Node 여러 개 추가 가능, Text도 추가 가능
  - HTML 콘텐츠 조작(Manipulation)
    - innerHTML: html 문서의 지정된 태그 안에 교체할 html의 코드 값을 갖는 것. 문자열을 html로 인식하여 출력됨. createElement(), createTextNode(), appendChild()를 한꺼번에 처리하는 효과
  - InnerHTML와 appendChild의 차이
    - InnerHTML은 Property, appendChild는 Method.
    - InnerHTML은 교체, appendChild는 추가.



- callback 함수(ES의 영역)

  - 이벤트 리스너를 배우기 위해 callback 함수에 대한 이해가 필요
  - 콜백 함수(A)는 다른 함수(B)의 인자로 넘겨지는 함수로 다른 함수(B)의 내부에서 실행되는 함수(A)를 말한다(JS의 함수는 1급 객체로 함수의 인자가 될 수 있다)
  - Array Helper Methods
    - array에 사용할 수 있는 method
    - callback 함수의 일종(인자로 함수를 받아온다.)
    - map,forEach,filter 등이 있다.

  ```python
  #python 예시
  number = [0,9,99]
  def add_one(number):
     return number+=1
      
  print(list(map(add_one,number)))  #add_one이라는 함수가 map이라는 함수의 인자가 됨
  #함수를 실행한게 아니라 그냥 넘긴 것이다.
      
  out
  [1,10,100]
      
  #위처럼 리스트를 선언하고, 함수를 선언하는 복잡한 코드는 아래와 같이 한 줄에 쓸 수 있다.
  print(list(map(lamda n: n+1,[0,9,99])))
      
  out
  [1,10,100]
  ```

  ```javascript
  //1.JS의 map 함수
  ['1','2','3'].map(Number)
  
  out
  [1,2,3] //문자에서 숫자로 바뀜
  
  //위 파이썬 코드와 동일한 코드
  const numbers = [0,9,99]
  function addOne(number){
      return number+1
  }
  const newNumbers1 = numbers.map(addOne)
  console.log(newNumbers1)
  
  out
  [1,10,100]
  
  //위처럼 리스트를 선언하고, 함수를 선언하는 복잡한 코드는 아래와 같이 쓸 수 있다.
  const newNumbers2 = [0,9,99].map(fuction(number){
      //[0,9,99]를 순회하며, 각 요소를 (number) 자리에 넣는다.
      //그리고 리턴된 값을 새로운 배열에 넣고 마지막에 리턴한다.
      return number+1
  })
  
  out
  [1,10,100]
  
  
  //2.forEach를 활용, forEach는 return이 없다.
  let sum = 0
  const newNumbers = [1,2,3]
  newNumbers.forEach(function(number){
      //numbers의 각 요소를 number 자리에 넣고,
      //나머지는 원하는 대로 구현한다. 리턴이 존재하지 않는다.
      sum+=number
  })
  console.log(sum)
  
  out
  6
  //2-2.만일 아래와 같이 쓸 경우 error가 발생
      let sum = 0
      [1,2,3].forEach(function(number){
          sum+=number
      })
      //error가 발생하는 이유는 ;을 붙이지 않았기 때문이다. ;를 붙이지 않았기 때문에 JS는 위 코드를 아래와 같이 해석한다.
      let sum = 0[1,2,3].forEach(function(number){
          sum+=number
      })
      //따라서 ;을 붙여줘야 한다. 이런 문제가 있음에도 ;를 붙이지 않아도 된다고 하는 이유는 위와 같은 코드를 짤 일이 거의 없기 때문이다.
      let sum = 0;
      [1,2,3].forEach(function(number){
          sum+=number
      })
  
  
  //3.filter
  const odds = [1,2,3].filter(function(number){
      //각 요소를 number 자리에 넣고
      //return이 true인 요소들만 모아서 새로운 배열로 리턴
      return number%2
  })
  console.log(odds)
  
  out
  [1,3]
  ```


​    

- EventListener(DOM의 영역)

  - 요소가 이벤트를 기다리다 이벤트가 발생하면 특정 일을 하는 것.

  - callback 함수로 작성한다.

  - addEventListener()의 첫 번째 인자에는 조건이 되는 이벤트를, 두 번째 인자에는 어떤 일(함수)을 할 지를 넣는다.

    ```js
    //기본형
    요소.addEventListener('이벤트', 이벤트 발생시 실행할 함수)
    //상세
    요소.addEventListener('이벤트', function(A) {
          실행할 내용
      })
    //함수를 정의하는 것이므로 A자리에는 아무거나 넣어도 되고 심지어 비워둬도 된다. 그러나 event로 적는 것이 권장된다.
    ```
    
    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>event Listener</title>
    </head>
    <body>
    <button id="myButton">얍</button>
    
    <script>
    const myButton = document.querySelector('#myButton')
    function confirmMessage(event)  {
    confirm('얍?')  //confirm은 상단에 메세지 창을 띄우는 함수다.
    }
    myButton.addEventListener('click', confirmMessage)
    
    //위 코드는 아래 코드와 동일하다.
    const myButton = document.querySelector('#myButton')
    myButton.addEventListener('click', function(event) {
    confirm('얍!')
    })
    </script>
    </body>
    </html>
    ```

  - `urls.py`에 작성하는 코드와 유사하다.

    ```python
    #articles라는 경로로 접근하면 index함수를 실행한다.
    path('artilces/',views.index)
    ```

  - event의 종류
    - click: 포인팅 장치 버튼이 엘리먼트에서 눌렸다가 놓였을 때.
    - mouseover: 포인팅 장치가 리스너가 등록된 엘리먼트나 그 자식 엘리먼트의 위로 이동했을 때.
    - mouseout: 포인팅 장치가 리스너가 등록된 엘리먼트 또는 그 자식 엘리먼트의 밖으로 이동했을 때.
    - keypress:  쉬프트, Fn, CapsLock 을 제외한 키가 눌린 상태일 때(연속적으로 실행).
    - keydown: 키가 눌렸을 때
    - keyup: 키 누름이 해제될 때
    - load:  이미지 등의 리소스와 그 의존 리소스의 로딩이 끝났을 때
    - scroll:  다큐먼트 뷰나 엘리먼트가 스크롤되었을 때. 
    - change: 모든 종류의 input태그 값의 변경이 일어났을 때(type="text"일 경우에는 포커스 아웃되거나 엔터를 눌렀을 때)



- this

  - window는 JS의 최상위 객체이다.
  - JS는 객체지향(OOP)언어다.
  - this는 무조건 자신을 호출한 어떤 object(객체)를 지칭한다. 따라서 this는 객체다(this가 지칭하는 객체). 기본적으로 window를 지칭한다.
  
  ```js
console.log(this)
  
  out
  Window {parent: Window, opener: null, top: Window, length: 0, frames: Window, …}
  ```
  
  - method는 객체 안에 정의된 함수를 말한다(`객체.메소드이름()`의 형태로 실행하는 함수).
  - function에 method가 포함되지만(객체 안에 저장된 '함수'가 메소드이므로) 설명의 편의를 위해 아래에서 말하는 function은 method가 아닌 함수를 의미한다.
  - fucntion을 정의할 때 this가 가리키는 객체가 window가 아닌 경우 2가지
    - method 안의 this: method 안의 this는 해당 method가 정의된 객체를 가리킨다.
    - 생성자 함수 안의 this
  
  ```js
  const obj = {
        name: 'obj',
        method1: function () {
          console.log(this)  // obj
        },
        objInObj: {
          name: 'object in object',
          // 아래 코드는 oioMethod: function () {} 이 코드와 완전히 같다.
          oioMethod () {  // 코드를 짧고 간결하게 작성하게 해주는 ES6 문법설탕
            console.log(this) // objInObj
          }
        },
        arr: [0, 1, 2],
          newArr: [],
          method2 () {
            this.arr.forEach(
              /* 아래 function 은 메소드인가? No. 그러므로 this 는 window
                function(number) {
                  // console.log(this)
                  this.newArr.push(number * 100)
                  }.bind(this) //bind는 한 스코프 위의 객체를 가리키게 한다
                */
                //아래 화살표 함수는 bind를 해야하는 불편을 해소하기 위함이다.
               (number) => {
                 this.newArr.push(number * 100)
                }
              )
            }
          }
  
          obj.method1() // obj
          obj.objInObj.oioMethod() // objInObj
          obj.method2()  // 
  ```
  
  ```js
  //this와 .target은 역할이 유사하다.
  
  myButton.addEventListener('click', 
     function(event) {
        this.classList.add('btn','btn-primary')        //이 코드와
        event.target.classList.add('btn','btn-primary') //이 코드는 동일하다.
        confirm('얍')									//둘 다 myButton을 가리킨다.
     })
  
  //그러나 this보다 target을 쓰는 것이 권장된다. this는 어느 메소드에 쓰였냐에 따라 달라지지만 target은 정확히 하나를 지정하기 때문이다.
  
  
  //아래와 같이 화살표 함수로 정의했을 경우 this는 작동하지 않는다. 따라서 target을 쓰는 것이 권장됨
  myButton.addEventListener('click', 
     (event) => {
        this.classList.add('btn','btn-primary')       
        event.target.classList.add('btn','btn-primary') 
        confirm('얍')									
     })
  ```





# AJAX

- AJAX: Asynchronous Javascript And Xml, 비동기식 자바스크립트와 xml
  - JS로 비동기 요청을 보내는 것
  - 지금까지는 요청이 올 때마다 응답을 보내고 페이지를 새로고침하는 방식을 사용. 즉 분절이 존재했다.
  - 비동기 요청은 새로고침(분절) 없이 요청과 응답이 이루어지는 것이다.
    - 예를 들어 검색창에 검색어를 입력하면 새로고침 없이도 연관검색어가 뜬다.

- AJAX 요청(비동기 요청)은 결과적으로 XHR(XML Http Requests)을 통해서 이루어진다(axios를 사용하지만 실제로 요청은 XHR이 보내진다.).
  
  - XHR은 AJAX를 보낼 수 있는 유일한 XHR이다.
  - 실제 크롬 콘솔 창에서 `Log XMLHTTPRequests`옵션을 체크한 후 검색창에 검색어 한 글자를 입력할 때마다 XHR요청이 가는 것을 확인할 수 있다.
  
- Non-Blocking

  - Non-Blocking이란 이전 코드가 완전히 끝나기 전에 다음 코드로 넘어가는 것을 의미한다.
  - 자바스크립트는 기본적으로 Blocking하다. 그러나 경우에 따라 Non-Blocking하게 작동한다.
    - XHR은 Non-Blocking하다.

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Document</title>
  </head>
  <body>
    <script>
      // Non-Blocking
  	const xhr = new XMLHttpRequest()
  	xhr.open('GET', 'https://koreanjson.com/posts/1')
  	xhr.send() //요청을 보낸다.
  
  	// 요청을 보낸 이후 응답이 제대로 도착하지 않았지만, 바로 res 에 값을 할당한다.
  	const res = xhr.response
  	console.log('RES: ', res)
    </script>
  </body>
  </html>
  
  
  out
  RES: 
  <!--만일 blocking하다면 응답을 받은 후 다음 코드가 실행되어 res에는 응답 내용이 담겼을 것이나 
  //non-blocking하기에 응답을 받기 전에 다음 코드가 실행되어 res에는 아무것도 담기지 않게 된다.-->
  ```

  - non-blocking하게 작업이 이루어지는 경우는 외부에 요청을 보내는 경우(XHR)와 기다리는 경우(settimeout) 2가지 이다. 외부에 요청을 보내고 그 요청에 대한 응답을 한없이 기다리면 브라우저가 제대로 작동을 할 수 없으므로 non-blocking하게 작업이 이루어진다.

  - Non-Blocking하게 작업이 이루어지는 이유
    - 스레드: 한 프로그램 내에서, 특히 프로세스 내에서 실행되는 흐름의 단위를 말한다. 일꾼이라고 생각하면 된다. 프로그램 사용자의 컴퓨터 CPU를 자원으로 활용한다.
    - JS가 사용되는 환경인 브라우저는 싱글 스레드다. 한 탭에 하나의 스레드만 존재한다. 이렇게 구현한 이유에는 여러가지 설이 있으나 무한으로 줄 경우 브라우저에서 여러가지 작업을 하면 브라우저 이외의 프로그램에서 사용할 자원이 부족해질 수 있기 때문(CPU를 자원으로 활용하므로)이다.
    - 싱글 스레드의 경우 페이지 내에서 console창에 while문을 활용하여 무한루프를 발생시키면 페이지 로딩, 클릭 등이 전부 막히게 된다. 싱글 스레드는 일꾼 한 명이라고 볼 수 있으므로 일꾼 한 명이 while문을 돌리느라 다른 요청을 처리하지 못하기 때문이다. 
  - non-blocking한 비동기 작업을 한다면 콜백 함수를 쓸 수 밖에 없도록 설계되어 있다.
    - 콜백함수는 지금 당장 실행되는 것이 아니라 훗날 언젠가 실행되는 함수다. non-blocking 역시 언제 끝날지 모르는 작업을 기다리는 대신 다음 작업으로 넘어가서 그 작업을 먼저 처리하는 것이므로 non-blocking한 비동기 작업에는 콜백 함수가 쓰인다.
    - 콜백 함수를 쓴다고 non-blocking한 비동기 작업을 한다는 것은 아니다.
  - Non-Blocking방식이 더 합리적일 때도 있다.

  ```python
  def 메일 보내기():
      보내기
      답장받기
      답장확인하기
      
  def 점심먹기():
      메뉴정하기
      밥먹기
      설거지하기
      
  def 공부하기():
      공부하기
  
  메일보내기()
  점심먹기()
  공부하기()
  
  #위와 같이 우리의 일상을 함수로 나타냈을 때 만일 우리가 Blocking하게 움직인다면 상식적으로 이해가 가지 않게 행동할 것이다. 코드는 위에서 부터 순차적으로 실행되므로 우리는 메일을 보내고 답장이 오기 전까지 아무 행동도 하지 않을 것이고 점심을 먹을때는 공부 등의 다른 행동을 하지 않고 밥만 먹을 것이다.
  
  #그러나 실제로 우리는 메일을 보내 놓고 답이 오기 전까지 점심을 먹거나 공부를 한다. 또한 점심을 먹으면서 공부를 하기도 하고 그것이 더 합리적이라고 생각한다.
  
  #따라서 Non-Blocking하다고 비합리적인 것은 아니다.
  ```

  

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
        //axio는 2번째 인자로 오브젝트를 넣을 수 있다. 그 오브젝트 안에 또 params라는 오브젝트를 넣         고 params 오브젝트의 키, 밸류를 설정하면 값을 함께 넘길 수 있다.
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
  
  