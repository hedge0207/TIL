# 브라우저 & JS의 역사

- 1위 브라우저였던 Netscape사에서 문서를 동적으로 동작하게 하기 위해 자사의 개발자인 Brandon Eich에게 새로운 언어 개발을 지시
  - Mocha에서 LiveScript에서 JavaScript로변경
  - 홍보 목적으로 당시 유행하던 언어인 Java를 붙임
  - 국제적인 표준으로 만들기 위해 유럽 컴퓨터 제조 협회(ECMA)에서 승인을 받으려 함
    - Java를 만든 회사인 Sun micorsystems에서 이름을 문제삼음
    - 결국 ECMA Ver.1이라 이름 붙임(줄여서 ES1)
  - JavaScript는 ECMAScript 표준(ECMA-262)을 바탕으로 구현된 언어



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
  
  - 이런 과정에서 발전한 만큼 JS코드는 브라우저마다 언제나 같게 동작하지는 않는다.
  



- node js
  - Javascript는 브라우저에서 쓸 수 없다는 태생적 한계가 존재, 타 언어와 같이 컴퓨터 자체를 조작하는 것이 불가능했음
  - Ryan Dahl이라는 개발자는 Javascript가 컴퓨터 조작을 할 수 있도록 개발 환경을 만들어주는 node js를 개발(V8엔진을 활용)
  - 서버 조작에 사용됨, DOM,BOM 조작과 무관
  - npm은 자바스크립트 패키지 매니저로 Node.js에서 사용할 수 있는 모듈들을 패키지화 하여 모아둔 저장소 역할과 패키지 설치 및 관리를 위한 CLI(Commant Line interface)를 제공한다.



- Javascript가 여러 문제(정치적 이슈 등)로 인해 10년 넘게 새로운 버전이 나오지 못함
  - 따라서 이 때 까지도 표준이 정해지지 못하여 크로스 브라우징 이슈가 사라지지 않음
  - jQuery는 동일한 코드로 Javascript로도 변환이 되고 JScript로도 변환이 되어 주목을 받음
  - 그러나 2009년 1999년 개발 된 ES3 이후 10년 만에 ES5(ES4는 개발 중에 폐기됨)가 개발됨
  - 2015년 ES6부터 2019년 ES10까지 매 년 새로운 버전이 공개됨
    - 이 시기에는 큰 변화가 없어 이 시기의 Javascript를 ES6+라 부름



- Vanilla.js
  - Javascript관련 라이브러리가 굉장히 많이 존재, 각 라이브러리들이 서로 의존성을 가지기 시작하면서 한 라이브러리를 사용하려면 다른 라이브러리를 사용해야 하는 상황이 발생. 속도가 저하되기 시작
  - 어떤 라이브러리도 설치하지 않은 Javascript인 Vanilla.js가 각광
  - node JS가 서버를 조작하는 데 쓰인다면, Vanilla.js는 브라우저 조작에 사용(서버 조작에 사용할 수 없고 오직 브라우저 내에서만 사용 가능하다).





# 소개

- Javascript는 브라우저 단위로 작동하는 것이 아닌 탭 단위로 작동한다.



- HTML과 CSS 그리고 JavaScript
  - HTML과 CSS는 웹 문서의 구조와 외형을 정의하는 것이며 둘은 문법이 서로 달라 각기 작성하여 연결해서 사용해야한다.
  - JavaScript는 문서의 기능을 정의한다.



- JavaScript의 특징

  - 컴파일 언어와 스크립트 언어

    | 컴파일 언어                    | 스크립트 언어                     |
    | ------------------------------ | --------------------------------- |
    | 컴파일 후 실행                 | 인터프리터를 통해 바로 실행       |
    | 데이터 타입과 형 변환에 엄격함 | 데이터 타입, 형 변환 수월         |
    |                                | 속도가 느리고 실행환경이 제한적임 |

  - 자바스크립트는 스크립트 언어이다.

  - 함수형 언어이다(함수형 프로그래밍을 선언적 프로그래밍이라고도 한다)

    - 함수를 기본으로 프로그래밍 한다.
    - 선언적 프로그래밍이기에 쉽고 효율적으로 HTML요소를 동적으로 처리할 수 있다.
    - 1급 함수이다, 함수 자체를 데이터처럼 사용 가능하다.
    - 변수의 유효 범위 = 함수의 유효 범위

  - Java와는 전혀 다른 프로그래밍 언어이다.

    - 마케팅 목적으로 Java라이센스를 사용할 뿐이다.
    - JavaScript를 의미하는 다른 이름으로는 ECMA-262이다.

  - 초보적인 언어가 아니다.

    - 컴파일 방식에 비해 언어가 엄격하지 않고 고급  프로그래밍 기술을 지원하지 않아 생긴 오해
    - 현재 모바일, 웹 브라우저 등의 기술과 표현이 발전하면서 사용범위 확대
    - 학습 초기에는 쉽지만 복잡한 서비스 구축에 사용될 만큼 강력함

  - 웹 표준이다.

    - HTML, CSS와 더불어 웹 표준이다.
    - HTML5의 JavaScript에 대한 의존도가 높다.

  - 장점

    - 텍스트 에디터와 웹 브라우저만 있으면 프로그래밍이 가능하다.
    - 데이터 타입 및 형 변환이 쉬워 쉽게 학습 가능하다.
    - 컴파일을 거치지 않아 작성한 코드 테스트가 수월하다.



- 브라우저의 구성 요소

  - BOM(Browser Object Model): window, 브라우저 창 자체

  - DOM(Document Object Model): 브라우저 창에 표시되는 document, BOM의 하위요소

    - 브라우저에서 document란 html파일을 의미한다. html파일은 기본적으로 문자열이다.

    - 같은 html문서라도 어떤 프로그램으로 실행시키냐에 따라 그냥 문자열이 될 수 도 있고 문자열을 해석해 해당 정보를 보여주는 창이 될 수도 있다. 예를 들어 html파일을 메모장으로 켜면 그냥 텍스트의 나열이지만 브라우저로 켜면 html 파일을 해석하하고 구조화하여 창으로 표현해준다.

    - 파이썬에서는 `.loads`,  JS에서는 `.parse`를 사용하여 문자열을 각기 dict, 오브젝트로 치환한다.

    - 브라우저는 문자열인 HTML 파일을 객체(object, 파이썬의 딕셔너리와 대응)로 치환(문서를 객체로 모델링)하고 해석한다.  치환된 이후의 document는 HTML파일(문자열)이 아닌 Obejcect를 뜻한다.
  
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

    - DOM트리의 노드를 탐색하는 방법
  
      ```js
      //방법1. 직접 탐색하는 방법
      document.body.ul.li
      
      //방법2. querySelector, querySelectorAll을 활용하는 방법
      document.querySelector('li')
      //방법1 보다 효율적이고 방법3보다 유연하다.
      
      //방법3. 그 밖의 탐색 방법(getElementByid, getElementByTagName 등)
      document.getElementByid('id값') 
      //id값이 없을 경우 원하는 태그 잡지 못함
      document.getElementsByTagName('tag명') 
      //다수의 동일한 tag명이 있을 경우 원하는 태그 잡지 못함
      ```
  
    - 이렇게 해석하고 구조화한 HTML파일을 rendering한다.
  
  - ES(ECMAScript): DOM을 조작하기 위한 프로그래밍 언어, JS



- window

  - js의 최상위 객체가 window라면 node js의 최상위 객체는 global이다.
  - window는 하나의 탭을 의미하며 브라우저는 탭 단위로 동작한다.
  - 브라우저의 최상위 객체는 window고 document가 그 아래 존재하며 그 아래 함수가 존재하는 형태다.
  - document는 윈도우(탭)에서 띄우고 있는 문서를 의미한다.
  - print(),close(), console 함수 등 document에 속하지 않는 함수들도 있다.



- 모든 명령어는 window를 써야 하므로 생략해도 동작한다. 

  ```js
  window.document.함수
  //window객체의 하부 객체 중 document객체의 하부 객체 중 함수 객체를 사용
  
  //아래와 같이 작성해도 된다.
  document.함수
  ```



- 스타일 가이드

  > https://github.com/airbnb/javascript/tree/master/css-in-javascript

  - airbnb나 google에서 사용하는 style을 주로 사용
    - Naming Convention은 lowerCamelCase(첫 글자는 소문자, 이후 단어 시작마다 대문자)
    - 오브젝트는 `-`를 허용하지 않는다(하면 오류가 발생한다).
    - cf. 자바스크립트는 웹에서 사용하는 언어이므로 vscode에서 작상할 경우 vscode저장-웹 페이지 새로고침을 해야 작성 결과를 볼 수 있다. 그러나 vscode에서 Live Server를 설치하면 VScode에서 저장만 하면 자동으로 새로고침이 된다. vscode의 코드 창에서 우클릭 후 Open With Live Server를 클릭하면 된다.





# 기초

- JavaScript의 구문(규칙)
  - 해석순서: 인터프리터(프로그램 언어로 적혀진 프로그램을 기계어로 변환)에 의해 해석되고 실행된다. 위에서부터 아래로 읽어 나간다.
  - 대소문자 구분: HTML과 달리 대소문자를 구분한다. 따라서 둘 사이의 차이로 발생하는 문제를 방지하기 위해 HTML에서도 어느 정도 구분해서 쓰는 것이 좋다.
  - 구문 끝: 세미콜론으로 문장이 끝났다는 것을 표시한다. 생략이 가능하지만 생략하면 안되는 경우가 있다.
  - 공백과 들여쓰기: JavaScript에서 공백은 키워드와 데이터를 구별해주는 역할을 한다.
    - 변수를 정의하거나 함수를 선언할 때 반드시 공백이 들어간다.
    - 키워드 뒤에 쉼표, 괄호, 연산자가 모두 존재하면 공백을 넣지 않아도 된다.
    - 필요할때가 아니라도 공백과 들여쓰기를 사용하면 코드의 가독성을 높여준다.
  - 주석: 코드에 대한 설명과 노트
    - 여러줄 주석: /\*\*/
    - 한 줄 주석: //
  



# 변수의 선언

- 변수를 선언하고 해당 변수에 리터럴을 값으로 할당한다.

  - `var a = "hello"`와 같이 썼을 때, a는 변수, hello는 리터럴이다.
  - 값은 프로그램에 의해 조작될 수 있는 대상을 말한다.
  - 위와 같이 변수를 선언함과 동시에 그 값을 지정해주는 리터럴 표기법을 사용하여 값을 생성할 수 있다.
  



- 리터럴
  - 변수 및 상수에 저장되는 값 그 자체를 리터럴이라 부른다.
  - 값과의 차이는 리터럴은 조작될 수 있는 대상이 아니지만 값은 조작될 수 있는 대상이라는 점이다.
  - 예를 들어 숫자 2와 3은 그 자체로는 아직 어떠한 조작의 대상도 아니므로 리터럴이다.
  - 그러나 2+3과 같이 쓰는 순간 연산자의 피연산자가 되어 조작의 대상이 되었으므로 값이다.



- 자바스크립트는 동적 타이핑 언어다.
  - 변수를 선언할 때 타입을 지정해 주지 않는다.
  - 파이썬과 동일하다.



- 변수 선언시 키워드(var, const, let 등)를 쓰지 않으면 암묵적 전역으로 설정되므로 반드시 키워드를 설정해야 한다.
  
  - 키워드는 수행할 동작을 규정한 것으로 var, const, let, function, return, while 등이 이에 속한다.
    
  - 변수의 유효 범위는 함수를 기준으로 결정된다.
  
  - 지역변수: 함수 안에 선언된 변수로 함수 내부로 사용이 제한된다. 함수 내부에서 선언된 변수는 함수 내부의 모든 곳에서 사용이 가능하지만 만약 중첩된 함수 내부에서 부모 함수의 변수와 같은 이름의 변수 선언 시 부모 함수의 변수에 가려진다.
  
  - 전역변수: 모든 함수에서 사용할 수 있는 변수, 전역 변수가 다른 코드에 영향을 주어 오류 발생 위험 존재, 따라서 최소한의 전여 변수만 사용할 것을 권장. 전역변수의 정의는 최상위 위치에서 변수를 선언하여 이루어진다.
  
  - 대부분의 변수 선언은 호이스팅 방지를 위해 let과 const를 통해 이루어진다.
  
  - 변수는 어떠한 데이터 타입이라도 담을 수 있다.
  
    - 단 변수는 그 크기가 정해져 있으므로 숫자나 boolean 등의 고정된 크기의 데이터 타입은 그대로 담을 수 있지만 문자열이나 객체 같은 크기가 정해져 있지 않은 데이터 타입은 변수에 담을 수 없다. 대신 문자열이나 객체의 참조만을 가지고 있다. 이런 종류의 데이터 타입을 참조 타임이라 부른다.
  
    ```javascript
    //기본 타입
    var a=true;
    var b=a;
    a=false;
    document.writeln(b);
    
    out
    true  //a의 값을 바꿔도 b의 값에는 영향이 없음, b는 a를 참조하는 것이 아니라 아예 새로운 변수이기 때문이다.
    
    //참조 타입
    var a=[1,2,3,4];
    var b=a
    a[0]=100
    document.writeln(b);
    
    out
    100,2,3,4   //a의 값을 바꾸면 b의 값도 함께 바뀐다. b는 a를 참조하기 때문이다.
    ```
  
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
    
    //아래와 같이 ,로 구분하여 복수의 변수 선언 가능
    var a2 = "aa",a3="ㅁㅁ"
    console.log(a2,a3)  //aa ㅁㅁ
    
    //값 없이 변수 선언 가능
    var a4
    console.log(a4)  //undefined
    ```
  
  - const: 재할당, 재선언이 불가능, 값이 변화하지 않는다는 의미가 아니다.
  
    ```javascript
    const x = 1
    
    // 민일 재선언하면 오류가 발생
    
    const x = 1
    x = 2
    
    Uncaught SyntaxError: Identifier 'x' has already been declared
    
    // 변화는 가능하다.
    // ∵array,object 등은 참조형 데이터로 array,object 자체가 변수에 할당된 것이 아닌 이들의 주소가 변수에 저장된 것이기 때문이다. 즉, 주소 자체를 변경시키는 것은 불가능하지만 주소값을 타고 내부의 데이터를 변경시키는 것은 가능하다.
    // 객체도 마찬가지로 객체가 참조하는 주소값 자체를 변경하는 것은 불가능하지만 객체의 프로퍼티를 변경하는 것은 가능하다.
    const arr [1,2,3]
    arr.push(10)
    console.log(arr)
    
    out
    [1,2,3,10]
    
    
    //아래와 같이 ,로 구분하여 복수의 변수 선언 가능
    const b2 = "aa",b3="ㅁㅁ"
    console.log(b2,b3)   //aa ㅁㅁ
    
    //값 없이 변수 선언 불가
    const b4
    console.log(b4) //에러 발생
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
    
    
    //아래와 같이 ,로 구분하여 복수의 변수 선언 가능
    let c2 = "aa",c3="ㅁㅁ"
    console.log(c2,c3)    //aa ㅁㅁ
    
    //값 없이 변수 선언 가능
    let c4
    console.log(c4)   //undefined
    ```



- 호이스팅(Hoisting)

  - 정의: var 선언문이나 function 선언문 등 모든 선언문이 해당 Scope의 선두로 옮겨진 것처럼 동작하는 특성.
  - JavaScript는 모든 선언문(var, let, const, function, class 등)이 선언되기 이전에 참조 가능하다.
  - 파이썬과 달리 변수를 선언하기 전에 활용할 수 있다.
  - 얼핏 편리해 보이지만 많은 오류를 발생시킬 수 있기에 사용해선 안되는 기능이다.

  ```javascript
  console.log(a) //undefined  
  var a = 3 
  console.log(a) //3
  
  //함수 호출 전에 함수를 사용했음에도 결과가 정상적으로 나오는데 이는 호이스팅 때문이다.
  console.log(f(3))  //13
  function f(a){
      return 10+a
  }
  ```

  - 변수는 3 단계에 걸쳐 생성된다.
    - 선언 단계: 변수 객체에 변수를 등록한다. 이 변수 객체는 스코프가 참조하는 대상이 된다.
    - 초기화 단계: 변수 객체에 등록된 변수를 메모리에 할당한다. 이 단계에서 변수는 undefined로 초기화된다.
    - 할당 단계: undefined로 초기화된 변수에 실제값을 할당한다.
    - `var` 키워드로 선언된 변수는 선언 단계와 초기화 단계가 한 번에 이루어진다. 즉, 스코프에 변수가 등록되고 변수는 메모리에 공간을 확보한 후 undefined로 초기화된다. 따라서 변수 선언문 이전에 변수에 접근하여도 변수 객체에 변수가 존재하기 때문에 에러가 발생하지 않는다. 다만 undefined를 반환한다.
  - 위 예시에서 호이스팅이 발생하는 과정
    - 첫 번째 줄이 실행되기 이전에  `var a = 3 `이 호이스팅 되어 첫 번째 줄 앞에 `var a = 3 `가 옮겨진다.
    - 실제로 변수 선언이 코드 레벨(코드 상에서)로 옮겨진 것은 아니고 변수 객체에 등록되고 undefined로 초기화 된 것이다.
    - 세 번째 줄이 실행 될 때는 변수에 값이 할당되었기에 3이 출력된다. 

# 타입

- 타입이란
  - 변수는 값의 위치(주소)를 기억하는 저장소이다.
  - 즉, 변수란 값이 위치하고 있는 메모리 주소에 접근하기 위해 사람이 이해할 수 있는 언어로 명명한 식별자이다.
  - 값의 종류에 따라 확보해야 할 메모리의 크기가 다르기에, 메모리에 값을 저장하기 위해서는 먼저 확보해야 할 메모리의 크기를 알아야 한다.
  - 이때 값의 종류, 즉 데이터의 종류를 데이터 타입이라 한다.



- 변경불가성(immutability)

  - 정의: 객체가 생성된 이후 그 상태를 변경할 수 없는 디자인 패턴
    - 함수형 프로그래밍의 핵심 원리이다.
    - 원시타입은 변경 불가능한 값이다.
    - 객체 타입은 변경 가능한 값이다.
  - 개념이 생겨난 이유
    - 객체는 참조 형태로 전달하고 전달 받는다. 객체가 참조를 통해 공유되어 있다면 그 상태가 언제든지 변경될 수 있기 때문에 문제가 될 가능성도 커지게 된다.
    - 이는 객체의 참조를 가지고 있는 어떤 장소에서 객체를 변경하면 참조를 공유하는 모든 장소에서 그 영향을 받기 때문인데 이것이 의도한 동작이 아니라면 참조를 가지고 있는 다른 장소에 변경 사실을 통지하고 대처하는 추가 대응이 필요하다.
    - 의도하지 않은 객체의 변경이 발생하는 원인의 대다수는 “레퍼런스를 참조한 다른 객체에서 객체를 변경”하기 때문이다. 
    - 이 문제의 해결 방법은 비용은 조금 들지만 객체를 불변객체로 만들어 프로퍼티의 변경을 방지하며 객체의 변경이 필요한 경우에는 참조가 아닌 객체의 방어적 복사(defensive copy)를 통해 새로운 객체를 생성한 후 변경한다.

  - 예시1.

  ```javascript
  //첫 번째 구문이 실행되면 메모리에 문자열 'Hello'가 생성되고 식별자 str은 메모리에 생성된 문자열 'Hello'의 메모리 주소를 가리킨다.
  var str = 'Hello';
  //두 번째 구문이 실행되면 이전에 생성된 문자열 'Hello'를 수정하는 것이 아니라 새로운 문자열 'World'를 메모리에 생성하고 식별자 str은 이것을 가리키게 된다.
  str = 'World';
  
  //즉  문자열 'Hello'와 'World'는 모두 메모리에 존재하고 있고, 변수 str은 문자열 'Hello'를 가리키고 있다가 'World'를 가리키도록 변경된 것 뿐이다.
  ```

  - 예시2.

  ```javascript
  //someStr은 str 변수에 저장된 문자열을 실제로 변경하는 것이 아니라 새로운 문자열을 생성하여 반환하는 것이다.
  //문자열은 변경할 수 없는 immutable value이기 때문이다.
  var str = "Hello World!"
  var someStr = str.slice(2,5)
  console.log(someStr) //llo
  
  //배열은 객체이므로 mutable value이기 때문에 arr값 자체를 변경 가능하다.
  //따라서 아래와 같이 array의 메서드는 직접 대상이 되는 배열을 변경한다.
  var arr = [];
  console.log(arr.length); // 0
  
  var arrLength = arr.push(2);    // .push()는 메소드 실행 후 array의 length를 반환한다.
  console.log(arr.length); // 1
  ```

  - 예시3.

  ```javascript
  var person = {
      name: 'Cha',
      pet: {
          dog: 'Spring',
      }
  }
  
  var myName = person.name;
  
  //person.name은 문자열로 immutable한 값이기에 myName이 참조하는 person.name 자체가 변하지 않고 메모리에 새로운 값인 Lee가 생성된다.
  person.name = 'Lee';
  console.log(myName);  //Cha
  
  myName = person.name;
  console.log(myName)   //Lee
  
  
  // 변수 somePerson은 객체 타입이다.immutable한 값이 아니기에 객체 somePerson은 변경된다. 그런데 person과 someperson은 같은 어드레스를 참조하고 있기에 person도 변경된다.
  var somePerson = person;
  somePerson.name = "Lee";
  console.log(person.name);       //Lee  
  console.log(somePerson.name);   //Lee
  ```



- 불변 데이터 패턴(immutable data pattern)

  - 의도하지 않은 객체의 변경이 발생하는 원인의 대다수는 레퍼런스를 참조한 다른 객체에서 객체를 변경하기 때문이다. 이 문제의 해결 방법은 다음과 같다.
  - 객체의 방어적 복사(새로운 객체를 생성한 후 변경)
    - `Object.assign(target, source)`은 타깃 객체로 소스 객체의 프로퍼티를 복사한다.
    - 이때 객체의 프로퍼티와 동일한 프로퍼티를 가진 타겟 객체의 프로퍼티들은 소스 객체의 프로퍼티로 덮어쓰기가 된다.
    - 리턴값으로 타깃 객체를 반환한다. ES6에서 추가된 메소드이며 Internet Explorer는 지원하지 않는다.
    - 완전한 깊은 복사(deep copy)를 지원하지 않는다. 객체 내부의 객체(Nested Object)는 얕은 복사(Shallow copy) 된다.

  ```javascript
  // 복사
  const obj = { x: 1 };
  const copy = Object.assign({}, obj);
  console.log(copy);		  //{ x: 1 }
  console.log(obj == copy); //false
  
  // 병합
  const obj1 = {x:1};
  const obj2 = {y:2};
  const obj3 = {z:3};
  const merge1 = Object.assign(obj1,obj2,obj3)
  //타깃 객체인 obj1을 반환한다.
  console.log(merge1) //{ x: 1, y: 2, z: 3 }
  //타깃 객체인 obj1만 변경된다.
  console.log(obj1)   //{ x: 1, y: 2, z: 3 }
  console.log(obj2)   //{ y: 2 }
  
  
  //얕은 복사(Shallow copy)
  const user1 = {
      name: 'Cha',
      address: {
          city: 'Seoul'
      }
  };
  
  const user2 = Object.assign({}, user1);
  //참조값이 다르다
  console.log(user1 === user2); //false
  
  user2.name = 'Park';
  console.log(user1.name);  //Cha
  console.log(user2.name);  //Park
  
  //객체 내부의 객체는 얕은 복사 된다.
  console.log(user1.address === user2.address);  //true
  
  user1.address.city = 'Daegu';
  console.log(user1.address.city);  //Daegu
  console.log(user2.address.city);  //Daegu
  ```

  - 불변객체화를 통한 객체 변경 방지
    - `Object.freeze()`를 사용하여 불변 객체로 만들수 있다.
    - `Object.isFrozen()`을 사용하여 불변 객체인지 확인할 수 있다.
    - 내부 객체까지 변경 불가능하려면 Deep freeze를 하여야 한다.

  ```javascript
  const user1 = {
      name: 'Cha',
      address: {
          city: 'Daejeon'
      }
  }
  
  const user2 = Object.assign({},user1,{name:'Park'})
  
  console.log(user1.name)   //Cha
  console.log(user2.name)   //Park
  
  Object.freeze(user1)
  
  user1.name="Lee" 
  user1.address.city = 'Deagu'
  
  //변경 되지 않았다.
  console.log(user1.name)  //Cha
  console.log(Object.isFrozen(user1))  //true
  
  //객체 내부의 객체는 변경된다.
  console.log(user1.address.city)  //Deagu
  
  
  //Deep freeze
  function deepFreeze(obj) {
      const props = Object.getOwnPropertyNames(obj);
  
      props.forEach((name) => {
          const prop = obj[name];
          if(typeof prop === 'object' && prop !== null) {
              deepFreeze(prop);
          }
      });
      return Object.freeze(obj);
  }
  
  const user = {
      name: 'Cha',
      address: {
          city: 'Seoul'
      }
  };
  
  deepFreeze(user);
  
  user.name = 'Lee';           
  user.address.city = 'Ulsan';
  
  // 변경이 전부 무시된다.
  console.log(user);  //{ name: 'Cha', address: { city: 'Seoul' } }
  ```

  - Immutable.js
    - 위 두 방법은 번거러울 뿐더러 성능상 이슈가 존재하기에 큰 객체에는 사용하지 않는 것이 좋다.
    - Facebook에서 제공하는 Immutable.js를 사용하는 방법이 있다.

  ```bash
  # 먼저 설치를 해야 한다.
  $ npm install immutable
  ```

  ```javascript
  //Immutable.js의 Map 모듈을 임포트하여 사용한다.
  const { Map } = require('immutable')
  const map1 = Map({ a: 1, b: 2, c: 3 })
  const map2 = map1.set('b', 50)
  // 깊은 복사가 되었다.
  map1.get('b') // 2
  map2.get('b') // 50
  ```

  



- 원시타입과 객체 타입

  - 원시타입(primitive)

    - 변경 불가능한 값(immutable)

    - 불린, 숫자, null undefined, 문자열, symbol이 해당

  - 객체타입(object)

    - 원시타입을 제외한 모든 데이터
    - 변경 가능한 값(mutable)
    - 객체란 키와 값으로 구성된 속성(property)의 집합이며, 프로퍼티 값이 함수일 경우 구분을 위해 메소드라고 부른다.
    - 일반객체, function,array,data,RegExp

## 기본 데이터 타입

- Number

  - 정수와 실수 구분 하지 않음, 더 정확히는 정수 타입이 별도로 존재하지 않음.
  - 정수 리터럴과 실수 리터럴 표현 시 범위가 다르다(단, 크게 문제가 되지는 않는다)
  - 양수, 음수, 소수, e지수 표기(과학적 표기법), Infinity, -Infinity, NaN, 상수 전부 가능
  
- NaN(Not a Number): 숫자가 아님을 표시하는 것으로 자신을 포함한 어떤 것과도 같지 않다.따라서 어떤 변수가 NaN인지는 `if (a==NaN)`으로 확인할 수 없고 `isNaN(a)`함수를 사용해야 한다. 반변에 undefined과 null는 동등연산자로 비교시 같다고 나온다. NaN은 자신과 일치하지 않는 유일한 값이다. 타입은 number로 뜬다.
  - 상수란 미리 정해져 있는 숫자로 원주율이나 중력가속도 등이 이에 속한다.

  - JavaScript에서 상수를 사용할 때는 대소문자 구분이 완벽해야 한다.

  - 파이썬과 달리 0으로 나눌 경우 에러를 발생시키는 것이 아니라 Infinity를 반환

  ```javascript
  var x = 1  //var는 요즘은 쓰지 않지만 명시적 표기를 위해 적는다.
  ```

  

- String: 큰 따옴표, 작은 따옴표로 생성

  - JavaScript에는 char 데이터 타입이 없음
  - 문자열 리터럴은 따옴표로 둘러싸인 문자 집합이다.
  - 이스케이프 시퀀스는 파이썬과 마찬가지로 \키를 쓴다.
  
  ```javascript
  var x = '문자열1'
  var y = "문자열2"
  ```
  
  - Template Literal
  
  ```javascript
  // 큰 따옴표와 작은 따옴표를 혼용 가능
  const tl = `'작은따옴표'와 "큰따옴표" 혼용 가능`
  
  // 줄 바꿈: 따옴표가 아닌 ``를 사용
  const x = `자바스크
   립트`
  console.log(x)
  
  out
  자바스크
     립트
     
  // 문자열 내에 변수 사용: `${변수}`
  const message1 = 'hi'
  const message2 = `I said, ${message1}`
  ```
  
  - 문자열은 유사 배열이다.
    - 유사배열: 배열처럼 인덱스를 통해 접근할 수 있는 데이터
    - 이미 생성된 문자열의 일부 문자를 변경해도 반영되지 않는다(에러는 발생하지 않는다).
  
  ```javascript
  var str = 'String'
  console.log(str[0])   //S
  
  str[0] = 'D'
  console.log(str)      //String
  ```



- Boolean: 소문자 true,false(파이썬과 달리 소문자로 적는다)

  - 문자와 숫자 변환이 자동으로 이루어진다.
  - 빈 문자열, null, undefined, 숫자 0은 false로 간주된다.

  ```javascript
  var x = true
  var y = false
  ```



- Empty Value: null, undefined
  
    - null: 어떠한 데이터 타입도 가지고 있지 않음, 변수에 아무 값이 담겨있지 않음, 의도적으로 변수에 값이 없다는 것을 명시하기 위해 사용
    - undefine: 정의되어 있지 않음, 값이 할당된 적 없는 변수, 생성되지 않는 객체에 접근할 때 나옴, 선언 이후 값을 할당하지 않으면 undefine이 디폴트 값으로 할당됨. 즉 null은 의도적으로 변수에 값을 지정하지 않겠다고 표시한 것이라면 undefine은 변수에 값을 아직, 혹은 실수로 할당하지 않은 것이다.
    - empty value를 둘이나 설정한 것은 JS 개발자들의 실수다.
  - 둘의 타입은 다르다. 이 역시 JS 개발자들의 실수다
  
  ```javascript
  var empty1 = null
  var empty2 = undefined
  
  console.log(typeof(empty1))
  console.log(typeof(empty2))
  
  out
  object
  undefined
  ```



- symbol

  - ES6에서 새롬게 추가된 타입
  - 주로 이름의 충돌 위험이 없는 유일한 객체의 프로퍼티 키를 만들기 위해 사용한다.
  - `Symbol()` 함수를 호출해 생성한다.
  - 생성된 심볼 값은 다른 심볼 값들과 다른 유일한 심볼 값이다.

  ```javascript
  var k = Symbol('key')
  console.log(typeof k)   //symbol
  
  var obj = {}
  obj[k] = 'value'
  console.log(obj         //{Symbol(key): "value"}
  console.log(obj[k])     //value
  ```



## 타입 변환

- 명시적 타입 변환

  - 개발자에 의해 의도적으로 값의 타입을 변경하는 것
  - 타입 캐스팅이라고도 한다.

  ```javascript
  var x = 123;
  
  var xStr = x.toString()
  console.log(typeof xStr)  //string
  ```

  - 문자열 타입으로 변환
    - String 생성자 함수를 new 연산자 없이 호출
    - Object.prototype.toString 메소드를 사용

  ```javascript
  console.log(String(10))  	    //"10"
  console.log(String(NaN)) 	    //"NaN"
  
  console.log((10).toString());   //"10"
  console.log((NaN).toString());  //"NaN"
  ```

  - 숫자 타입으로 변환
    - Number 생성자 함수를 new 연산자 없이 호출
    - parseInt, parseFloat 함수를 사용(문자열만 변환 가능)
    - 단항 연결 연산자를 이용

  ```javascript
  console.log(Number('10'));    //10
  console.log(Number(true));    //1
  
  console.log(parseInt('10'));  //10
  
  console.log(+'10');           //10
  console.log(+true);           //1
  ```

  - Boolean 타입으로 변환
    - Boolean 생성자 함수를 new 연산자 없이 호출
    - `! `부정 논리 연산자를 두번 사용

  ```javascript
  console.log(Boolean(1));     //true
  console.log(Boolean(''));    //false
  console.log(Boolean([]));    //true
  
  console.log(!!0);            //false
  console.log(!!1);            //true
  ```

  



- 암묵적 타입 변환

  - 개발자의 의도와 무관하게 JS의 엔진에 의해 암묵적으로 타입이 자동으로 변환
  - 타입 강제 변환이라고도 한다.

  ```javascript
  var x = 123;
  var xStr = x + ''
  console.log(typeof xStr, xStr)  // string 123
  
  //변수 x의 값이 변경되지는 않는다.
  console.log(x)					// 123
  ```

  - 문자열 타입으로 변환
    - `+` 연산자는 피연산자 중 하나 이상이 문자열이면 문자열 연결 연산자로 동작하여 결과값이 문자열이 된다는 점을 이용.

  ```javascript
  1+''              // "1"
  NaN + ''          // "NaN"
  Infinity + ''     // "Infinity"
  true + ''         // "true"
  null + ''         // "null"
  undefined + ''    // "undefined"
  (Symbol()) + ''     // TypeError: Cannot convert a Symbol value to a string
  ({}) + ''           // "[object Object]"
  (function(){}) + '' // "function(){}"
  Array + ''          // "function Array() { [native code] }"
  ```

  - 숫자 타입으로 변환
    - `+`를 제외한 산술 연산자는 숫자 값을 만드는 것이라는 점을 이용
    - 단, 피연산자는 문맥 상 숫자 타입이어야 한다.

  ```javascript
  3 - '2'    //1
  3 * '2'    //6
  3 / '1'    //3
  3 - 'one'  //NaN
  ```

  - Boolean 타입으로 변환
    - 빈 문자열, 0, -0, NaN, null, undefined는 Falsy값(거짓으로 인식할 값)으로 false로 변환된다.
    - 비어 있지 않은 문자열, 0이 아닌 숫자 등은 Truthy값(참으로 인식할 값)으로 true로 변환된다. 



## 타입 확인

- `typeof 변수명`

  - 피연산자의 변수 타입을 문자열로 반환한다. 
  - 그러나, null과 배열, 그리고 거의 모든 객체를 object를 반환하므로 객체의 종류까지는 체크하지 못한다.

  ```javascript
  typeof [];   //object
  typeof null; //object
  typeof {};   //object
  ```




- `Object.prototype.toString.call`

  - 피연산자 변수 타입을 문자열로 반환한다.
  - `Object.prototype.toString.call`를 활용하여 객체의 종류를 알아낼 수 있다.
  - 그러나 이 경우에도 객체의 상속 관계까지는 알 수 없다.

  ```javascript
  Object.prototype.toString.call([]);    // [object Array]
  Object.prototype.toString.call(null);  // [object Null]
  Object.prototype.toString.call({});    // [object Object]
  ```




- `X instanceof Y`

  - X가 Y 타입의 인스턴스인지 알려준다.

  ```javascript
  function A(){}
  function B(){}
  
  const a = new A();
  
  a instanceof A       //true
  a instanceof B       //false
  a instanceof Object  //true
  ```



- 유사배열객체

  - 유사배열객체(array-like object): length 프로퍼티를 갖는 객체
  - 문자열, arguments, HTMLCollection, NodeList 등은 유사 배열이다.
  - length 프로퍼티가 있으므로 순회할 수 있으며 call, apply 함수를 사용하여 배열의 메소드를 사용할 수도 있다.
  - 어떤 객체가 유사 배열인지 체크하는 방법
    - 우선 length 프로퍼티를 갖는지를 확인한다.
    - length 프로퍼티의 값이 정상적인지 확인한다.
    - 배열의 인덱스는 32bit 정수로 `2**32-1`이다.
    - 유사 배열의 인덱스는 자바스크립트로 표현할 수 있는 양의 정수로 `2**53-1`이다.
    - 아래 함수로는 배열의 인덱스 값이  `2**32-1` 보다 작거나 같을 경우 배열과 유사배열을 구분하지는 못한다.

  ```javascript
  function isArrayLike(para){
      const MAX_ARRAY_INDEX = Math.pow(2,53)-1
      
      // ara가 null이 아니면 para.length를 반환하고 null이면 undefined를 반환
      // 빈 문자열은 유사배열이다.
      const length = para == null ? undefiend : para.lenght
      
      //배열의 길이의 타입이 숫자형이고 그 길이가 0보다 크거나 같고, 유사 배열 인덱스의 최대치보다 작거나 같으면 유사배열이다.
      return typeof length === 'number' && length >= 0 && length <= MAX_ARRAY_INDEX;
  }
  
  console.log(isArrayLike('abc'));
  console.log(isArrayLike(''));
  ```








# 연산자

## 할당 연산자

- 할당 연산자

  - 우항에 있는 피연산자의 평가 결과를 좌항에 있는 변수에 할당

  ```javascript
  // =
  var one = 8
  
  // +=
  one += 1 // 9
  
  // -=
  one -=1 //7
  
  // *=
  one *= 2 //16
  
  // /=
  one /= 2 //4
  
  // %=
  one %= 3 //2
  ```



## 산술 연산자


- 단항 산술 연산자


  - `+`,`-`: 양수, 음수 변경 및 표현, 단, "+"는 음수를 양수로 변경하지 않는다.
  - 숫자 형 문자열의 경우 숫자로 자동 형변환된다.
  - `++`,`--`: 증가 연산자와 감소 연산자. 피연산자 앞에 오는지 뒤에 오는지에 따라 효과가 달라진다.

  ```javascript
var x = 5, result;
// 선대입 후증가 (Postfix increment operator)
result = x++;
console.log(result, x); // 5 6

// 선증가 후대입 (Prefix increment operator)
result = ++x;
console.log(result, x); // 7 7

// 선대입 후감소 (Postfix decrement operator)
result = x--;
console.log(result, x); // 7 6

// 선감소 후대입 (Prefix decrement operator)
result = --x;
console.log(result, x); // 5 5 


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

  

  

  

- 이항 산술 연산자

  - 자동형변환으로 피 연산자에 문자가 포함되어도 연산 가능

  ```javascript
  var a = '5',b=2
  var str1='str1',str2='str2'
  
  //덧셈 연산자
  //피 연산자 모두 숫자면 덧셈 연산을 수행하지만
  //피 연산자 중 하나라도 문자열이면 피연산자가 연결된 문자열이 나온다.
  //둘 다 숫자가 아닌 문자열일 경우에도 피연산자가 연결된 문자열이 나온다.
  console.log(a+b)			//52
  console.log(typeof(a+b))	//string
  console.log(str1+str2)		//str1str2
  console.log(typeof(str1+str2)) //string
  
  //피연산자가 숫자인 문자열이면 뺄셈을 수행, 숫자가 아닌 문자열이면 NaN을 반환
  //덧셈을 제외한 모든 연산이 이와 동일
  console.log(a-b)			//3
  console.log(typeof(a-b))	//number
  console.log(str1-str2)		//NaN
  console.log(typeof(str1-str2))  //number
  
  console.log(a*b)			//10
  console.log(typeof(a*b))	//number
  console.log(str1*str2)		//NaN
  console.log(typeof(str1*str2))	//number
  
  console.log(a/b)			//2.5
  console.log(typeof(a/b))	//number
  console.log(str1/str2)		//NaN
  console.log(typeof(str1/str2))	//number
  
  console.log(a%b)			//1
  console.log(typeof(a%b))	//number
  console.log(str1%str2)		//NaN
  console.log(typeof(str1%str2))	//number
  ```

  - 나눗셈 연산자
    - 피 연산자 모두가 정수라 할지라도 결과는 실수가 나올 수 있음(자바스크립트는 정수 타입이 별도로 존재하지 않음). 
    - 0으로 나누면 Infinity를 반환

  ```javascript
  var a=3,b=0
  console.log(a/b) //Infinity
  ```

  - 나머지 연산자
    - 나머지를 결과값으로 취함
    - 0으로 나머지 연산을 하면 NaN을 반환

  ```javascript
  var a=5,b=2
  console.log(a%b)  //1
  
  //
  var a=3,b=0
  console.log(a%b)  //NaN
  ```

  



  

## 비교 연산자

- 대소 관계 비교 연산자

  - 피연산자가 숫자일 경우 일반적인 상식대로 대소를 비교한다.
  - 피연산자가 문자일 경우 문자 코드의 순서대로 크기를 비교한다. 따라서 대문자가 소문자보다 작다고 판단된다.
  - 피연산자가 객체일 경우 객체를 숫자나 문자로 자동 변환하려고 시도하고 변환되지 않으면 false반환

  ```javascript
  console.log(3<2)
  console.log(3>=3)
  console.log(3>2)
  console.log(3<=3)
  console.log("가">"나")
  console.log("a">"b")
  
  out
  false
  true
  true
  true
  false   //가, a는 각기 나, b 보다 사전순으로 앞에 있으므로 더 작다고 본다.
  false
  ```

  




- 동등 연산자, 일치 연산자

  ```js
  const a = 1
  const b = '1'
    
  //동등 연산자
  console.log(a==b)   //형 변환 결과 같아질 수 있으면 true를 반환
    
  //일치 연산자
  console.log(a===b)  //python의 == 연산자와 동일
    
  out
  true
  false
    
    
  
  0==''  /*true*/
  0=='0' /*true*/
  ''=='0'/*false*/
    
  //삼단 논법에 따르면 마지막도 true여야 하지만 false가 출력된다.
  //즉, 논리적으로 모순이 생길 수 있으므로 엄격하게 비교하는 ===를 쓰는 것이 좋다.
  ```




## 그 외 연산자

- 삼항 연산자: 조건에 따라 어떤 값을 할당할지 결정

  - `조건식 ? 조건식이 true일 때 반환할 값 : 조건식이 false일 때 반환할 값`

  ```javascript
  const result = Math.Pi > 4 ? 'pi가 4보다 크다':'pi가 4보다 크지 않다'
  console.log(result)  //pi가 4보다 크지 않다
  
  
  //아래와 같이 쓸 수도 있다.
  const name="C"
  function nameState(name) {
      return name.length > 2 ? true : false
  }
  console.log(nameState(name))  //false
  ```



- 논리 연산자

  - 우항과 좌항의 피연산자를 논리 연산한다.
  - 논리 부정(`!`) 연산자는 언제나 boolean 값을 반환한다.
  - 논리합(`||`) 연산자와 논리곱(`&&`) 연산자는 일반적으로 boolean 값을 반환하지만 반드시 boolean 값을 반환해야 하는 것은 아니다(단축 평가).

  ```javascript
  console.log(!true)   //false
  console.log(!false)  //true
  
  console.log(true || false)   //true
  console.log(false || false)  //false
  
  console.log(true && true)    //true
  console.log(true && false)   //false
  
  ```

  - 단축 평가
    - 논리합 연산자와 논리곱 연산자에는 단축평가가 적용된다.
    - 단축평가: 논리 평가(true인가 false인가)를 결정한 피연산자의 평가 결과를 그대로 반영하는 것.

  ```javascript
  // 논리합 연산자는 두 피연산자 중 하나만 true라도 true를 반환한다.
  // 'apple'은 빈 문자열이 아니므로 true이다.
  // 'apple'이 true이므로 뒤의 피연산자가 true인지 false인지와 무관하게 연산의 결과는 true이다.
  // 따라서 뒤의 피연산자는 굳이 확인하지 않는다.
  // 결국 논리 평가를 결정한 피연산자는 'apple'이 된다.
  console.log('apple' || 'banana')  //apple
  
  // 아래도 마찬가지 이유로 banana가 반환된다.
  console.log(0 || 'banana')       //banana
  
  
  // 논리곱 연산자는 두 피연산자 모두 true여야 true를 반환한다.
  // 'apple'은 빈 문자열이 아니므로 true이다.
  // 그러나 두 피연산자 모두 true여야 true를 반환하므로 이것만으로는 true인지 false인지 구분할 수 없다.
  // 따라서 뒤의 피연산자 'banana'까지 확인을 한다.
  // 결국 논리 평가를 결정한 피연산자는 'banana'가 된다.
  console.log('apple' && 'banana')  //banana
  
  // 아래도 마찬가지 이유로 0이 반환된다.
  console.log(0 && 'banana') //0
  ```



- 쉼표 연산자

  - 왼쪽 피연산자부터 차례대로 피연산자를 평가하고 마지막 피연산자의 평가가 끝나면 마지막 피연산자의 평가 결과를 반환

  ```javascript
  var a, b, c;
  a = 1, b = 2, c = 3;  //3
  ```



- 그룹 연산자
  - `()` : 그룹 내(괄호 안)의 표현식을 최우선으로 평가한다.





# 제어문

- 표현식

  - 표현식
    - 하나의 값으로 평가된다.
    - 표현식은 하나의 값이 되기 때문에 다른 표현식의 일부가 되어 조금 더 복잡한 표현식을 구성할 수도 있다.

  ```javascript
  // 표현식
  5 + 5  //10
  // 5+5라는 표현식이 또 다른 표현식의 일부가 된다.
  5 + 5 >8 //true
  ```

  - 표현식과 문의 차이
    - 문이 자연어에서 완전한 문장이라면 표현식은 문을 구성하는 요소이다.
    - 표현식은 그 자체로 하나의 문이 될 수도 있다.
    - 표현식은 평가되어 값을 만들지만 그 이상의 행위는 할 수 없다. 
    - 문은 var, function과 같은 선언 키워드를 사용하여 변수나 함수를 생성하기도 하고 if, for 문과 같은 제어문을 생성하여 프로그램의 흐름을 제어하기도 한다.

  ```javascript
  // 아래 자체가 표현식이지만 완전한 문이기도 하다.
  a = 10; 
  ```

  

- 블록문

  - 0개 이상의 문들을 중괄호로 묶은 것.
  - 코드 블록 또는 블록이라고 부르기도 한다.
  - 문의 끝에는 세미콜론을 붙이는 것이 일반적이지만 블록문은 세미 콜론을 붙이지 않는다.



- 조건문

  - `if`, `else if`, `else`

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

  - while: ()안의 조건의 결과가 true이면 계속 실행하고 false면 멈춘다.

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

  - `do...while`
    - 코드 블록을 싱행하고 조건식을 평가
    - 따라서 코드 블록은 무조건 한 번 이상 실행된다.

  ```javascript
  var cnt = 0;
  
  do {
      console.log(cnt)    // 0
      cnt++
  } while (false){
      console.log("hi!")  // 조건이 false임에도 일단 실행이 된다.
  }
  ```

  

  - `for`
    - 조건식이 거짓일 때까지 코드 블록을 반복 실행

  ```javascript
  /*
  for문 구조
  for(초기화식;조건식;증감식){
  실행코드;
  }
  카운트 변수 초기화: 변수 선언과 함께 꼭 키워드 재할당 가능한 var나 let을 붙임
  제어 조건: 카운트 변수에 대한 조건
  변수 증가: ++,-- 사용
  두 번째 실행부터는 변수 초기화 생략하고 실행
  */
  
  for (let i=0;i<3;i++){
      console.log(i)
  }
  
  out
  0
  1
  2
  
  //중첩도 가능하다.
  //중첩된 for문에서 내부, 외부 for문 중 어떤 for문에 break를 걸지를 레이블 문을 통해 설정 가능하다(문서 참조).
  for (let i=1;i<=6;i++){
      for (let j=1;j<=6;j++){
        if (i+j===6){
          console.log([i,j])
      }
    }
  }
  
  out
  [1,5]
  [2,4]
  [3,3]
  [4,2]
  [5,1]
  ```

  - for of
    - 배열의 요소를 순회하기 위해 사용.

  ```js
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
    - 객체의 문자열 키(key)를 순회하기 위한 문법.
    - 배열에는 사용하지 않는 것이 좋다.
    - 배열은 순서를 보장하는 데이터 구조이지만 for in은 객체에 사용할 것을 염두했기에 순서를 보장하지 않기 때문이다.

  ```javascript
  //객체
  const fruits = {
      apple:2,
      banana:10,
      tomato:10,
      watermelon:2,
  }
  
  for (const fruit in fruits){
      console.log(fruit,fruits[fruit])
  }
  /*
    apple 2
    banana 10
    tomato 10
    watermelon 2
    */
  
  
  //배열
  var lst = ['one', 'two', 'three']
  
  for (var ldx in lst) {
      console.log(idx+': '+lst[idx])
  }
  
  /*
    0: one
    1: two
    2: three
    */
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

  





# 자료구조

## Array

- Array(파이썬의 리스트)

  - 파이썬과 마찬가지로 동적(배열 크기가 정해져 있지 않음)으로 배열의 추가와 삭제가 가능
  - 참조형 데이터로 데이터 자체가 변수에 저장되는 것이 아니라 변수에는 해당 데이터를 찾기 위한 참조(주소)만 저장된다.
  - 자바스크립트에서 배열은 객체이다.

  ```js
  const arr = [0,1,2,3]
  
  
  //배열인지 확인
  Array.isArray(arr)  //true
  
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
  
  
  //자바스크립트의 배열은 이상하게 작동한다.
  //[1,111,11,222,22,2]를 정렬하면 [1,11,111,2,22,222]로 정렬된다. 문자열로 인식해서 맨 앞 글자만 보고 정렬하기 때문이다.
  //원하는 대로 정렬 하기 위해서는 아래와 같이 해야 한다.
  arr.sort((a,b) => a - b)
  
  //위 코드가 가능한 것 역시 Js의 이상한 사칙연산 때문이다.
  //위의 이항 연산자 부분 참고
  
  
  //배열 합치기
  const a=[1,2,3]
  const b=[4,5,6]
  console.log(a.push(b))  //[1,2,3,[4,5,6]]
  console.log(a+b)        //"1,2,34,5,6"
  
  console.log(a.concat(b))  //[1,2,3,4,5,6]
  console.log([...a, ...b]) //[1,2,3,4,5,6]
  const c = a.push(...b)    //[1,2,3,4,5,6]
  //세 방법 중 어느 방법이 가장 나을지는 아래 사이트를 참고
  //https://www.measurethat.net/Benchmarks/Show/4223/0/array-concat-vs-spread-operator-vs-push
  
  
  
  //복사
  //얕은 복사
  newNumbers = numbers      //numbers가 바뀌면 newNumbers도 바뀐다.
  //깊은 복사
  newNumbers = [...numbers] //newNumbers가 새로운 리스트가 된다.
  ```

  - Array helper methods

    - filter: 원하는 요소 정리하여 새로운 배열 반환

    ```js
    a = [1,2,3,4,5,6]
    const b = a.filter((x) => {
      return x%2==1  //결과가 true인 것만 b에 들어가게 된다.
    })
    console.log(b)
    
    
    out
    [1,3,5]
    ```

    - forEach: 배열의 엘리먼트 하나하나 조작 시 사용, 엘리먼트 하나하나 콜 백 함수에 전달하여 처리

    - map: 배열 요소 하나 하나에 콜 백 함수 처리 후 새로운 배열 반환



## Object

- 자바스크립트는 객체 기반의 스크립트 언어이며 자바스크립트를 이루고 있는 거의 모든 것이 객체이다.

  - 원시 타입을 제외한 나머지 값들은 모두 객체이다.
  - object type을 객체 타입 또는 참조 타입이라 한다.
    - 참조 타입은 객체의 모든 연산이 실제값이 아닌 참조값으로 처리됨을 의미한다.
  - 객체는 프로퍼티를 변경, 추가, 삭제가 가능하므로 변경 가능(mutable)한 값이라 할 수 있다.
    - 따라서 객체 타입은 동적으로 변화할 수 있으므로 어느 정도의 메모리 공간을 확보해야 하는지 예측할 수 없기 때문에 런타임에 메모리 공간을 확보하고 메모리의 힙 영역(Heap Segment)에 저장된다.
    - 이에 반해 원시 타입은 값(value)으로 전달된다. 즉, 복사되어 전달된다. 이를 **pass-by-value**라 한다.

  - **Pass-by-reference**
    - 변수에 값 자체를 저장하고 있는 것이 아니라, 생성된 데이터의 참조값(address)를 저장하고 참조 방식으로 전달하는 것



- JavaScript의 객체
  - 키(key)와 값(value)로 구성된 프로퍼티들의 집합이다.
  - 프로퍼티의 값으로 JS에서 사용할 수 있는 모든 값을 사용할 수 있다.
  - JavaScript의 함수는 일급 객체이므로 값으로 취급할 수 있다. 따라서 프로퍼티 값으로 함수를 사용할 수도 있으며, 프로퍼티 값이 함수일 경우, 일반 함수와 구분하기 위해 **메서드**라 부른다.
  - JS의 객체는 객체지향의 상속을 구현하기 위해 **프로토타입**이라고 불리는 객체의 프로퍼티와 메서드를 상속받을 수 있다.



- 프로퍼티
  - 프로퍼티는 프로퍼티 키(이름)와 프로퍼티 값으로 구성된다.
  - 프로퍼티는 프로퍼티 키로 유일하게 식별할 수 있다. 즉, 프로퍼티 키는 프로퍼티를 식별하기 위한 식별자(identifier)다.
  - 프로퍼티 키와 값의 명명 규칙
    - 키: 빈 문자열을 포함하는 모든 문자열 또는 symbol 값
    - 값: 모든 값
    - 프로퍼티 키에 문자열이나 symbol값 이외의 값을 지정하면 암묵적으로 타입이 변환되어 문자열이 된다.
    - 이미 존재하는 프로퍼티 키를 중복 선언하면 나중에 선언한 프로퍼티가 먼저 선언한 프로퍼티를 덮어쓴다.
    - 표현식을 프로퍼티 키로 사용할수도 있다. 이 경우 표현식을 반드시 `[]`로 묶어야 한다.
    - 예약어를 프로퍼티키로 사용하여도 에러가 발생하지는 않지만, 하지 않는 것이 좋다.
  - 프로퍼티 키는 문자열이므로 본래 따옴표를 사용하여야 한다.
    - 그러나 자바스크립트에서 사용 가능한 유효한 이름인 경우, 따옴표를 생략할 수 있다.
    - 반대로 말하면 자바스크립트에서 사용 가능한 유효한 이름이 아닌 경우, 반드시 따옴표를 사용하여야 한다.
    - `first_name`은 따옴표가 생략 가능하지만 `"first-name"`은 생략 불가능하다.



- 객체 생성 방법

  - Java와의 차이점
    - Java와 같은 클래스 기반 객체 지향 언어는 클래스를 사전에 정의하고 필요한 시점에 new 연산자를 사용하여 인스턴스를 생성하는 방식으로 객체를 생성한다.
    - JS는 프로토타입 기반 객체 지향 언어로서 클래스라는 개념이 없어, 별도의 객체 생성 방법이 존재한다.
    - ECMAScript 6에서 새롭게 클래스가 도입되었다. 그러나  ES6의 클래스가 새로운 객체지향 모델을 제공하는 것이 아니며 클래스도 사실 함수이고 기존 프로토타입 기반 패턴의 문법적 설탕(Syntactic sugar)이다.

  - 객체 리터럴
    - 가장 일반적인 객체 생성 방식
    - `{}`를 사용하여 객체를 생성하며 중괄호 내에 1개 이상의 프로퍼티를 기술하면 해당 프로퍼티가 추가된 객체를 생성할 수 있고 아무것도 기술하지 않으면 빈 객체가 생성된다.
    - 프로퍼티의 값으로 변수를 넣을 경우 키를 입력하지 않으면 `변수명 : 할당된 값`의 형태로 프로퍼티가 생성된다.

  ```javascript
  var emptyObj = {}
  console.log(typeof emptyObj)     //object
  
  var student = {
      name: 'Cha',
      gender: 'male',
      sayHello: function () {
          console.log('Hello! ' + this.name)
      }
  }
  console.log(typeof student)     //object
  student.sayHello()              //Hello! Cha
  
  
  // 프로퍼티의 값으로 변수를 넣을 경우
  var first = 1
  var second = 2
  var third = 3
  
  const ordinal = {
      first,
      second,
      third,
  }
  console.log(ordinal)  //{ first: 1, second: 2, third: 3 }
  ```

  - Object 생성자 함수
    - `new` 연산자와 Object 생성자 함수를 호출하여 빈 객체를 생성하고, 이후에 프로퍼티 또는 메서드를 추가하여 객체를 완성하는 방법
    - 생성자(constructor) 함수: new 키워드와 함께 객체를 생성하고 초기화하는 함수를 말한다.
    - 생성자 함수를 통해 생성된 객체를 인스턴스(instance)라 한다.
    - 자바스크립트는 Object 생성자 함수 이외에도 String, Number, Boolean, Array, Date, RegExp 등의 빌트인 생성자 함수를 제공한다.
    - **객체 리터럴 방식으로 생성된 객체는 결국 Object 생성자 함수로 객체를 생성하는 것을 단순화시킨 축약 표현이다.**
    - 개발자가 일부러 Object 생성자 함수를 사용해 객체를 생성해야 할 일은 거의 없다.

  ```javascript
  // 빈 객체 생성
  var someone = new Object();
  
  // 프로퍼티 추가
  someone.name = 'Cha';
  someone.gender = 'male';
  someone.sayHello = function () {
      console.log('Hello! ' + this.name);
  };
  
  console.log(typeof someone); // object
  
  someone.sayHello();          //Hello! Cha
  ```

  - 생성자 함수
    - 위 두 방식으로 객체를 생성하는 것은 프로퍼티 값만 다른 여러 개의 객체를 생성할 때 불편하다.
    - 생성자 함수를 사용하면 마치 객체를 생성하기 위한 템플릿(클래스)처럼 사용하여 프로퍼티가 동일한 객체 여러 개를 간편하게 생성할 수 있다.
    - 일반 함수와 생성자 함수를 구분하기 위해 생성자 함수의 이름은 파스칼 케이스(PascalCase)를 사용하는 것이 일반적이다.
    - 프로퍼티 또는 메서드명 앞에 기술한 `this`는 생성자 함수가 생성할 인스턴스를 가리킨다.
    - this에 연결되어 있는 프로퍼티와 메서드는 `public`(외부에서 참조 가능)하다.
    - 생성자 함수 내에서 선언된 일반 변수는 `private`(외부에서 참조 불가능)하다.

  ```javascript
  // 객체 리터럴 방식으로 생성
  var student1 = {
      name: 'Kim',
      gender: 'male',
      sayHello: function () {
          console.log('Hello! ' + this.name)
      }
  }
  
  var student1 = {
      name: 'Lee',
      gender: 'female',
      sayHello: function () {
          console.log('Hello! ' + this.name)
      }
  }
  
  
  //생성자 함수 방식으로 생성
  function Student(name,gender) {
      this.name = name
      this.gender = gender
      this.sayHello = function(){
          console.log('Hello! ' + this.name)
      }
  }
  // 인스턴스 생성
  var student1 = new Student('Kim','male')
  var student2 = new Student('Lee','female')
  
  
  //public, private
  function Person(name,gender) {
      var address = 'Daejeon'
      this.name = name
      this.gender = gender
      this.sayHello = function(){
          console.log('Hello! ' + this.name)
      }
  }
  
  var person = new Person('Cha', 'male')
  
  console.log(person.name);     // Cha
  console.log(person.address)   // undefined
  ```



- 객체 프로퍼티 접근

  - 마침표 표기법
    - 프로퍼티 키가 유효한 자바스크립트 이름인 경우에만 사용 가능
  - 대괄호 표기법
    - 프로퍼티 키가 유효한 자바스크립트 이름이 아닌 경우에도 사용 가능
    - 대괄호 내에 들어가는 프로퍼티 이름은 반드시 문자열이어야 한다.

  ```javascript
  //프로퍼티 값 일기
  var student = {
      'last-name': 'Cha',
      gender: 'male',
      10:1000    //프로퍼티의 키로 온 숫자 10은 문자열 '10'으로 자동 변환 된다.
  }
  
  console.log(student.last-name)      //error
  console.log(student[last-name])     //error
  console.log(student['last-name'])   //Cha
  
  console.log(student.gender)         //male
  console.log(student[gender])        //error
  console.log(student['gender'])      //male
  
  console.log(student.10)         //error
  console.log(student[10])        //1000
  console.log(student['10'])      //1000
  ```



- 프로퍼티 값 갱신

  - 객체가 소유하고 있는 프로퍼티에 새로운 값을 할당하면 프로퍼티 값은 갱신된다.

  ```javascript
  var student = {
      name: 'Cha',
      gender: 'male',
  }
  
  student.name = 'Kim'
  console.log(student.name) //Kim
  ```



- 프로퍼티 동적 생성

  - 객체가 소유하고 있지 않은 프로퍼티 키에 값을 할당하면 하면 주어진 키와 값으로 프로퍼티를 생성하여 객체에 추가한다.

  ```javascript
  var student = {
      name: 'Cha',
      gender: 'male',
  }
  
  student.age = 28
  console.log(student.age)  //28
  ```



- 프로퍼티 삭제

  - `delete` 연산자를 사용, 피연산자는 프로퍼티 키이다.

  ```javascript
  var student = {
      name: 'Cha',
      gender: 'male',
  }
  
  delete student.name
  console.log(student.name)  //undifined
  ```



- 프로퍼티의 키, 값 조회

  - 프로퍼티의 키, 값, 키와 값 쌍을 배열로 반환

  ```javascript
  var student = {
      name: 'Cha',
      gender: 'male',
  }
  console.log(Object.keys(student))      //[ 'name', 'gender' ]
  console.log(Object.values(student))    //[ 'Cha', 'male' ]
  console.log(Object.entries(student))   //[ [ 'name', 'Cha' ], [ 'gender', 'male' ] ]
  ```



- 객체 안에서 key를 `[]`로 감싸면 그 안에 넣은 레퍼런스가 가리키는 실제 값이 key 값으로 사용된다.

  ```javascript
  const name = "Cha"
  const obj = {
      [name]: 'Developer'
  }
  console.log(obj)	// { Cha: 'Developer' }
  ```



- JSON과 객체의 치환

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





