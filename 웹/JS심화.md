# 심화

- JS로 HTML파일 작성하기

  - HTML로 작성할 수도 있는데 굳이 JS로 작성하는 이유는 HTML은 정적으로 보여주는 것 밖에 할 수 없으나 JS는 보다 동적으로 작동하게 할 수 있기 때문이다.
  - 예를 들어 게시글을 추가하는 페이지를 만든다고 하면 HTML로만 작성할 경우 HTML은 제출 버튼, 입력 창 등을 띄울 수 있으나 입력창에 글을 입력하고 제출버튼을 누른다고 해서 그 게시글이 등록되게 할 수는 없다. 그러나 JS는 실제로 등록되게 하는 것이 가능하다.
  - JS로 태그를 만드는 방법
    - 아래와 같이 할 경우 변수에는 object가 담기게 된다.
    - `.`으로 접근할 수 있는 이유가 바로 이것이다. 모두 오브젝트 안에 오브젝트가 있는 형태이기 때문에 ` .`으로 접근이 가능하다.

  ```JS
  const 변수명 = document.createElement('태그명')
  
  //e.g.
  const newLabel = document.createElement('label')
  
  console.log(typeof(newLabel))
  
  out
  object
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
  
  
  
  //어트리뷰트 노드에의 접근/수정(클래스 또는 스타일 속성 부여)은 조금 다르다.
  변수명.classList.add(클래스 또는 스타일1, 클래스 또는 스타일2.....)
  
  
  // HTML 콘텐츠 조작(Manipulation)
  //innerHTML과 innerTEXT의 차이
  const cardTitle = document.createElement('h5')
  cardText.innerHTML = '<a>hi</a>'  //hi가 출력
  cardText.innerText = '<a>hi</a>'  //<a>hi</a>가 출력
  ```

  - 예시

  ```html
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
      card.classList.add('card','col-4')  //1에서 class="card" style="width: 18rem 부분
      
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
      cardBody.append(cardTitle,cardText,cardButton) //cardBody에 들어가야 할 것들을 추가
      card.append(cardImage,cardBody)  //card에 들어가야 할 것을 추가
      }
      //여기까지 완성된 시점에서 console창에 createCard()를 입력하면 카드가 생성된다. 그러나 개발자		가 아닌 사람에게 이렇게 카드를 생성하라고 할 수 는 없으므로 버튼은 만들어 준다.
      
      //card 생성을 위한 버튼
      const createCardButton = document.querySelector('#createCardButton')
      
      createCardButton.addEventListener('click', function() {
        const cardTitleInput = document.querySelector('#cardTitleInput')
        const cardTextInput = document.querySelector('#cardTextInput')
        createCard(cardTitleInput.value, cardTextInput.value)
        cardTitleInput.value = null
        cardTextInput.value = null
      })
  </script>
  ```

  

- 기본적인 순서

  - 태그를 담을 변수 생성(실제로 변수에 담기는 것은 object이다).
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



- callback 함수

  - 이벤트 리스너를 배우기 위해 callback 함수에 대한 이해가 필요

  - 함수를 직접 실행하지 않고 인자로 넘기는 것(JS의 함수는 1급 객체로 함수의 인자가 될 수 있다)

  - Array Helper Methods: callback 함수의 일종

    - map,forEach,filter 등이 있다.
    - 인자로 함수를 받아온다.

    ```python
    number = [0,9,99]
    def add_one(number):
        return number+=1
    
    print(list(map(add_one,number)))  #add_one이라는 함수가 map이라는 함수의 인자가 됨
    
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
    const numbers = [0,99,999]
    function addOne(number){
        return number+1
    }
    const newNumbers1 = numbers.map(addOne)
    
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
    
    
    //3.filter
    const odds = [1,2,3].filter(function(number){
        //각 요소를 number 자리에 넣고
        //return이 true인 요소들만 모아서 새로운 배열로 리턴
        return number%2
    })
    ```

    

- EventListener

  - 요소가 이벤트를 기다리다 이벤트가 발생하면 특정 일을 하는 것.

  - callback 함수로 작성한다.

  - addEventListener()의 첫 번째 인자에는 조건이 되는 이벤트를, 두 번째 인자에는 어떤 일(함수)을 할 지를 넣는다.

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
          confirm('얍?')
        }
        // 요소.addEventListener('이벤트', 이벤트 발생시 실행할 함수)
        myButton.addEventListener('click', confirmMessage)
          
        //위 코드는 아래 코드와 동일하다.
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
    - change: 변경이 일어났을 때



- this

  - window는 JS의 최상위 객체이다.
  - JS는 객체지향(OOP)언어다.
  - this는 무조건 자신을 호출한 어떤 object(객체)를 지칭한다.
  - method는 객체 안에 정의된 함수를 말한다(`.메소드이름()`의 형태로 실행하는 함수).
  - function에 method가 포함되지만(객체 안에 저장된 '함수'가 메소드이므로) 설명의 편의를 위해 아래에서 말하는 function은 method가 아닌 함수를 의미한다.

  - fucntion을 정의할 때 this가 가리키는 객체가 window가 아닌 경우
    - method 안의 this: method 안의 this는 해당 method가 정의된 객체를 말한다.
    - 생성자 함수 안의 this





