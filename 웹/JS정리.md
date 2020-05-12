# 브라우저 & JS의 역사

- 1위 브라우저였던 Netscape사에서 문서를 동적으로 동작하게 하기 위해 자사의 개발자인 Brandon Eich에게 새로운 언어 개발을 지시
  - Mocha에서 LiveScript에서 JavaScript로변경
  - 홍보 목적으로 당시 유행하던 언어인 Java를 붙임
  - 국제적인 표준으로 만들기 위해 유럽 컴퓨터 제조 협회(ECMA)에서 승인을 받으려 함
    - Java를 만든 회사인 Sun micorsystems에서 이름을 문제삼음
    - 결국 ECMA Ver.1이라 이름 붙임(줄여서 ES1)



- MS에서 윈도우즈에 익스플로러를 끼워 팔기 시작(1998-1999, 1차 브라우저 전쟁)
  - MS는 Javascript를 살짝 변경한 JScript를 개발하여 익스플로러를 개발
  - 각 브라우저가 서로 다른 언어로 개발 됐으므로 브라우저에 따라 코드가 동작하지 않는 현상이 발생(크로스 브라우징 이슈)
  - 결국 마이크로소프트의 승리로 끝남
  - MS가 Netscape를 인수
    - 일부 개발자는 Netscape를 나와 Mozilla를 설립하고 파이어 폭스를 개발
  - Java를 개발한 Sun microsystems와 JavaScript의 상표권을 Oracle이 가져감



- 브라우저의 발전
  - Google에서 Google Maps외 Google Earth를 개발
    - Javascript, XML을 활용
    - 별도의 프로그램 설치 없이 지도를 볼 수 있다는 것이 당시에는 충격적이었음
    - Javascript의 성능이 입증됨
  - Apple이 아이폰을 공개 하면서 웹 서핑이 어디서나 가능해진다.
    - flash를 아이폰에서 지원하지 않으면서 Javascript가 부상
  - 2008년 Chrome이 등장
    - 타 브라우저 대비 빠른 속도와 표준을 지키는 개발로 주목을 받기 시작
    - 빠른 속도는 HTML,CSS,Javascript를 받아서 브라우저가 처리하는 속도가 빨랐기 때문, 특히 Javascript 처리 속도가 빨랐다(V8 엔진을 사용하여 Javascript를 읽고 처리).
    - 이로 인해 Javascript가 느리다는 인식이 변화



- Javascript는 브라우저에서 쓸 수 없다는 태생적 한계가 존재, 타 언어와 같이 컴퓨터 자체를 조작하는 것이 불가능했음
  - Ryan Dahl이라는 개발자는 Javascript가 컴퓨터 조작을 할 수 있도록 개발 환경을 만들어주는 node js를 개발(V8엔진을 활용)
  - 서버 조작에 사용됨, DOM,BOM 조작과 무관



- Javascript가 여러 문제(정치적 이슈 등)로 인해 10년 넘게 새로운 버전이 나오지 못함
  - 따라서 이 때 까지도 표준이 정해지지 못하여 크로스 브라우징 이슈가 사라지지 않음
  - jQuery는 동일한 코드로 Javascript로도 변환이 되고 JScript로도 변환이 되어 주목을 받음
  - 그러나 2009년 1999년 개발 된 ES3 이후 10년 만에 ES5(ES4는 개발 중에 폐기됨)가 개발됨
  - 2015년 ES6부터 2019년 ES10까지 매 년 새로운 버전이 공개됨
    - 이 시기에는 큰 변화가 없어 이 시기의 Javascript를 ES6+라 부름



- Vanilla.js
  - Javascript관련 라이브러리가 굉장히 많이 존재, 각 라이브러리들이 서로 의존성을 가지기 시작하면서 한 라이브러리를 사용하려면 다른 라이브러리를 사용해야 하는 상황이 발생. 속도가 저하되기 시작
  - 어떤 라이브러리도 설치하지 않은 Javascript인 Vanilla.js가 각광
  - node JS가 서버를 조작하는 데 쓰인다면, Vanilla.js는 브라우저 조작에 사용





# 소개

- Javascript는 브라우저 단위로 작동하는 것이 아닌 탭 단위로 작동한다



- 브라우저의 구성 요소
  - BOM(Browser Object Model): window, 브라우저 창 자체

  - DOM(Document Object Model): 브라우저 창에 표시되는 document, BOM의 하위요소

    - 브라우저에서 document란 html파일을 의미한다. html파일은 기본적으로 문자열이다.

    - 같은 html문서라도 어떤 프로그램으로 실행시키냐에 따라 그냥 문자열이 될 수 도 있고 문자열을 해석해 해당 정보를 보여주는 창이 될 수도 있다. 예를 들어 html파일을 메모장으로 켜면 그냥 텍스트의 나열이지만 브라우저로 켜면 html 파일을 해석하하고 구조화하여 창으로 표현해준다.

    - 브라우저는 HTML 파일을 객체(object, 파이썬의 딕셔너리와 대응)로 치환(문서를 객체로 모델링)하고 해석한다.  치환된 이후의 document는 HTML파일(문자열)이 아닌 Obejcect를 뜻한다.

      ```javascript
      typeof document
      
      out
      "object"
      ```

    - 즉 DOM은 HTML파일을 컴퓨터가 이해할 수 있게 치환된 결과물인 object이다(DOM !== HTML). 따라서 DOM 조작과 HTML 조작은 다르다.

    - HTML파일을 트리의 형태로 구조화(DOM tree)한다고 생각하면 된다. 컴퓨터가 실제로 트리로 만든다는 것은 아니다. 단지 사람이 이해하기 쉽도록 트리로 표현하는 것이다.

      | html |       |      |      |      |      |      |      |
      | ---- | ----- | ---- | ---- | ---- | ---- | ---- | ---- |
      | head |       |      |      | body |      |      |      |
      | meta | style | link |      | div  | span | ul   |      |
      |      |       |      |      |      |      | li   | li   |

    - 이렇게 해석하고 구조화한 HTML파일을 rendering한다.

  - ES(ECMAScript): DOM을 조작하기 위한 프로그래밍 언어, JS



- 기본 명령어는 아래와 같다.
  - 윈도우가 최상단에 위치하고 그 아래 document가 존재하며 그 아래 함수가 존재하는 형태
  - 모든 명령어는 window를 써야 하므로 생략해도 동작한다. 
  
  ```javascript
  window.document.함수
  ```
  
  

- 스타일 가이드

  > https://github.com/airbnb/javascript/tree/master/css-in-javascript

  - airbnb나 google을 주로 기준으로 사용
  - Naming Convention은 lowerCamelCase(첫 글자는 소문자, 이후 단어 시작마다 대문자)





# 기초

- type of: 타입을 출력

- 변수의 선언 

  - var: 재할당, 재선언 모두 가능

    ```javascript
    var y = 10
    y = 20    //재할당
    console.log(y)
    
    var y = 30  //재선언
    console.log(y)
    
    out
    20
    30
    ```

  - const: 재할당, 재선언이 불가능, 값이 변화하지 않는다는 의미가 아니다.

    ```javascript
    const x = 1
    
    /*
    민일 재선언하면 오류가 발생
    */
    const x = 1
    x = 2
    
    Uncaught SyntaxError: Identifier 'x' has already been declared
    
    //변화는 가능하다.
    //∵array,object 등은 참조형 데이터로 array,object 자체가 변수에 할당된 것이 아닌 이들의 주소가 변수에 저장된 것이기 때문이다. 즉, 주소 자체를 변경시키는 것은 불가능하지만 주소값을 타고 내부의 데이터를 변경시키는 것은 가능하다.
    const arr [1,2,3]
    arr.push(10)
    console.log(arr)
    
    out
    [1,2,3,10]
    ```

  - let: 재할당이 가능, 재선언은 불가능

    ```javascript
    let y = 10
    y = 20
    console.log(y)

    out
    20
    
    
    let y = 30
    
    out
    Uncaught SyntaxError: Identifier 'y' has already been declared
    ```
    
    

- 타입과 연산자

  - Number

    - 양수, 음수, 소수, e지수 표기(과학적 표기법), Infinity, -Infinity, NaN 전부 가능
    - 파이썬과 달리 0으로 나눌 경우 에러를 발생시키는 것이 아니라 Infinity를 반환
    - NaN(Nano Number): 컴퓨터로 표기할 수  없는 수(e.g. 0/0)를 의미

    ```javascript
    var x = 1  //var는 요즘은 쓰지 않지만 명시적 표기를 위해 적는다.
    ```

  - String: 큰 따옴표, 작은 따옴표로 생성

    ```javascript
    var x = '문자열1'
    var y = "문자열2"
    ```

    - Template Literal

    ```javascript
    //줄 바꿈: 따옴표가 아닌 ``를 사용
    const x = `자바스크
       립트`
    console.log(x)
    
    out
    자바스크
       립트
       
    //문자열 내에 변수 사용: `${변수}`
    const message1 = 'hi'
    const message2 = `I said, ${message1}``
    ```

  - Boolean: 소문자 true,false(파이썬과 달리 소문자로 적는다)

    ```javascript
    var x = true
    var y = false
    ```

  - Empty Value: null, undefined

    - empty value를 둘이나 설정한 것은 JS 개발자들의 실수다.
    - 둘의 타입은 다르다. 이 역시 JS 개발자들의 실수다

    ```javascript
    var empty1 = null
    var empty2 = undefined
    
    console.log(typeof(empty1))
    console.log(typeof(empty1))
    
    out
    object
    undefined
    ```




- 연산자 

  - 할당 연산자

    ```javascript
    let c = 0
    c += 10
    console.log(c)
    c -= 3
    console.log(c)
    c++     //++는 +1을 해준다.
    console.log(c)
    c--		//--는 -1을 해준다.
    console.log(c)
    
    out
    10
    7
    8
    7
    ```

  - 비교 연산자

    ```javascript
    console.log(3<2)
    console.log(3>2)
    console.log("가">"나")
    console.log("a">"b")
    
    out
    false
    true
    false   //가, a는 각기 나, b 보다 사전순으로 앞에 있으므로 더 작다고 본다.
    false
    ```

  - 동등 연산자, 일치 연산자

    ```javascript
    const a = 1
    const b = '1'
    
    //동등 연산자
    console.log(a==b)   //형 변환 결과 같아질 수 있으면 true를 반환
    
    //일치 연산자
    console.log(a===b)  //python의 == 연산자와 동일
    
    out
    true
    false
    ```

  - 논리 연산자(단축평가가 적용 된다)

    ```javascript
    //and 는 &&로 표현
    console.log(true && false)
    //or 는 ||로 표현
    console.log(true || false)
    //not 은 !로 표현
    console.log(!true)
    
    //단축평가
    console.log(1 && false)
    console.log(0 && false)
    console.log(0 || false)
    console.log(1 || false)
    
    
    out
    false
    true
    false
    
    false
    0
    false
    1
    ```

  - 삼항 연산자: 조건에 따라 어떤 값을 할당할지 결정

    > ? 앞이 조건식, : 앞이 조건식이 참일 경우의 처리, : 뒤가 거짓을 경우의 처리 

    ```javascript
    const result = Math.Pi > 4 ? 'pi가 4보다 크다':'pi가 4보다 크지 않다'
    console.log(result)
    
    out
    pi가 4보다 크지 않다
    ```



- 조건문과 반복문

  - 조건문

    - if, else if, else

    ```javascript
    let day = 7
    let result
    if (day===1){
        result = '월요일'
    }
    else if (day===2){
        result = '화요일'
    }
    else if (day===3) result='수요일'  
    //중괄호 안에 들어갈 것이 한 줄이라면 위처럼 쓸수 있지만 가독성이 떨어져 쓰지 않는다.
    .
    .
    .
    else {
        result='일요일'
    }
    ```

    - switch

    ```javascript
    day = 2
    switch (day) {
        case 1:
            result = '월요일'
        case 2 :
            result = '화요일'
        case 3 :
            result = '수요일'
        default:
            result = '일요일'
    }
    console.log(result)
    
    out
    일요일
    // 위의 경우 day를 어떻게 설정해도 일요일이 출력됨. 순서대로 위에서부터 찾으면서 내려오는데 맨 밑에 디폴트 값으로 일요일이 있으므로 항상 변수에 일요일이 담기게 된다. 따라서 아래와 같이 break를 적어줘야 한다.
    
    day = 2
    switch (day) {
        case 1:
            result = '월요일'
            break
        case 2 :
            result = '화요일'
            break
        case 3 :
            result = '수요일'
            break
        default:
            result = '일요일'
            break
    }
    console.log(result)
    
    out
    화요일
    ```

  - 반복문

    - while

    ```javascript
    let num = 0
    while (num<3) {
        console.log(num++)
    }
    
    out
    0
    1
    2
    
    let num = 0
    while (num<3) {
        console.log(++num)
    }
    
    out
    1
    2
    3
    ```
    
  - for
    
  ```javascript
    for (let i=0;i<3;i++){
        console.log(i)
    }
    
    out
  0
    1
  2
    ```
    
    - for of
    
    ```javascript
    const arr = ['a','b','c']
    for (const n of arr){
        console.log(n)
    }
    
    out
  a
    b
  c
    ```
    
    - for in
    
    ```javascript
    const fruits = {
        'apple':2,
        'banana':10,
        'tomato':10,
        'watermelon':2,
    }
    
    //어차피 문자열이 올 것을 알고 있으므로 아래와 같이 문자열 안에 쓰지 않아도 된다.
    const fruits = {
        apple:2,
        banana:10,
        tomato:10,
        watermelon:2,
    }
    
    for (const fruit in fruits){
        console.log(fruit,fruits[fruit])
    }
    
    out
    apple 2
  banana 10
    tomato 10
  watermelon 2
    ```
    
    - continue
    
    ```javascript
    for (let i=0;i<4;i++){
        if (i===3) continue
        console.log(i)
    }
    
    out
  1
    2
    4
    ```
    
    

- 함수

  - Javascript의 객체는 1급 객체다.
    - 변수에 저장할 수 있다.
    - 함수의 리턴값이 될 수 있다.
    - 함수의 인자가 될 수 있다.

  ```javascript
  // 함수의 선언식
  // 인자 없이
  function f(){
      return 10
  }
  console.log(f())
  
  out
  10
  
  //인자가 있을 때
  function f(a){
      return 10+a
  }
  console.log(f(3))
  
  out
  13
  
  //디폴트값 설정
  function f(a=3){
      return 10+a
  }
  console.log(f())
  
  out
  13
  
  
  
  //함수의 표현식
  //익명함수(파이썬의 lamda와 유사), 주로 한 번 쓰고 쓰지 않을 함수를 지정할때 사용
  const bar = function(a,b){ //함수의 이름이 존재X
      return a+b
  }
  console.log(bar(10,20))  //변수로 함수를 실행시킨다.
  
  out
  30
  
  
  //함수명을 지정
  const bar = function bar(a,b){  
      //꼭 함수명을 변수명과 동일하게 할 필요는 없으나 일반적으로 동일하게 한다		
      return a+b
  }
  console.log(bar(10,20))
  
  out
  30
  
  
  //화살표 함수
  //화살표 함수는 함수의 선언식 & 표현식과 문법적으로 차이가 있고, 내부 동작도 다르다
  const ssum = (a,b) => {
      return a+b
  }
  console.log(ssum(10,20))
  
  out
  30
  
  //매개변수가 1개일 경우 괄호를 안쓰는 것도 가능하다.
  const pprint = a => {
      return a
  }
  
  // 중괄호 안에 들어가는 내용이 한 줄이면 중괄호 없이 가능하다
  const pprint = a => {
      return a
  }
  ```

  - 호이스팅: 가능은 하지만 사용해선 안된다.

  ```javascript
  console.log(f(3))
  function f(a){
      return 10+a
  }
  
  out
  13
  
  //함수 호출 전에 함수를 사용했음에도 결과가 정상적으로 나오는데 이는 호이스팅 때문이다.
  ```

  

- 자료구조

  - Array(파이썬의 리스트): 파이썬과 마찬가지로 동적(배열 크기가 정해져 있지 않음)으로 배열의 추가와 삭제가 가능
    - 참조형 데이터로 데이터 자체가 변수에 저장되는 것이 아니라 변수에는 해당 데이터를 찾기 위한 참조(주소)만 저장된다.

  ```javascript
  const arr = [0,1,2,3]
  
  //인덱스 접근
  console.log(arr[0],arr[3])
  
  out
  0 3
  
  
  // 맨 뒤에 추가
  arr.push(500)
  console.log(arr)
  
  out
  [0,1,2,3,500]
  
  
  //맨 앞에 추가
  arr.unshift(100)
  console.log(arr)
  
  out
  [100,0,1,2,3,500]
  
  //맨 앞의 요소 삭제
  arr.shift(100)
  console.log(arr)
  
  out
  100
  [0,1,2,3,500]
  
  //가장 우측의 요소삭제 후 반환
  console.log(arr.pop())
  console.log(arr)
  
  out
  500
  [0,1,2,3]
  
  
  //역순으로 재배열, 원본도 변한다
  console.log(arr.reverse())
  console.log(arr)
  out
  [3,2,1,0]
  [3,2,1,0]
  
  
  //포함 여부 확인
  console.log(arr.includes(0))
  console.log(arr.includes(10))
  
  out
  true
  false
  
  
  //배열 요소 전체를 연결하여 생성한 문자열을 반환, 구분자(separator)는 생략 가능, 기본 구분자는 ','
  console.log(arr.join())   //기본값은 ,
  console.log(arr.join(':'))
  console.log(arr.join(''))
  
  out
  3,2,1,0
  3:2:1:0
  3210
  
  
  //인자로 지정된 요소를 배열에서 검색하여 인덱스를 반환, 중복되는 요소가 있는 경우 첫번째 인덱스만 반환, 만일 해당하는 요소가 없는 경우, -1을 반환
  console.log(arr.indexOf(0))
  console.log(arr.indexOf(1))
```
  

  
  - Object(파이썬의 딕셔너리)
  - 참조형 데이터
  
  ```javascript
  const me = {
      name : '홍길동',  //오브젝트 안에서는 따옴표를 쓰지 않아도 된다.
      'phone number':'01012345678',  //그러나 이처럼 띄어쓰기 등을 쓰고자 하면 따옴표 써야 한다.
      electronics:{
      	phone:'galaxy s8',
      	laptop:'samsung notebook 11',
      	keyboards:['happyhacking','logitech']
  	}
  }
  console.log(me.name)
  console.log(me.electronics.keyboards[0])
  console.log(me.height) //설정하지 않은 키를 입력하면
  
  out
  홍길동
  happyhacking
  undefined  //undefined가 출력
  
  console.log(Object.keys(me))    //키만 배열로 반환
  console.log(Object.values(me))  //value만 배열로 반환
  console.log(Object.entries(me)) //key,value를 array에 넣어서 반환
  
  out
  ["name", "phone number", "electronics"]
  ["홍길동", "01012345678", {phone: "galaxy s8", laptop: "samsung notebook 11", keyboar...}]
  [["name", "홍길동"], ["phone number", "01012345678"], ["electronics", {…}]]
  
  
  
  //오브젝트 리터럴
  //키와 밸류가 같을 경우 하나만 적으면 된다.
  const a = 1
  const b = 2
  const c = 3
  
  const abc = {
      'a':a,
      'b':b,
      'c':c,
  }
  //위와 같이 쓰지 않고 아래와 같이 쓰는 것이 가능
  const abc = {
      a,
      b,
      c,
  }
  console.log(abc.a)
  
  out
  1
  ```



- JSON과 object의 치환

  ```javascript
  const color = {     //꼭 오브젝트가 아니라도 상관 없다.
      red : '빨강',
      blue : '파랑',
      yellow : '노랑',
  } 
  
  //object를 JSON으로 치환
  const jsonData = JSON.stringify(color)
  console.log(jsonData)
  console.log(typeof jsonData)
  
  out
  {"red":"빨강","blue":"파랑","yellow":"노랑"}
  string
  
  
  //JSON을 object로 치환
  const parsedData = JSON.parse(jsonData)
  console.log(parsedData)
  console.log(typeof parsedData)
  
  out
  {red: "빨강", blue: "파랑", yellow: "노랑"}
  object
  ```

  
