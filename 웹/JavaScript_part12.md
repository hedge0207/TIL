# strict mode

- strict mode

  - 암묵적 전역과 같이 프로그래밍을 하면서 실수는 언제나 발생할 수 있으므로 실수를 줄이기 위해서는 근본적인 접근이 필요하다.
  - 잠재적 오류를 발생시키기 어려운 개발 환경을 만들고, 그 환경에서 개발하는 것이 근본적인 해결책이다.
  - 이를 지원하는 것이 ES5에서 추가된 strict mode다.
  - strict mode는 JavaScript의 문법을 보다 엄격히 적용하여 기존에 무시되던 다음과 같은 코드들에 대해 명시적 에러를 발생시킨다.
    - 오류를 발생시킬 가능성이 높다.
    - JS 엔진의 최적화 작업에 문제를 일으킬 수 있다.

  - `ESLint`와 같은 린트 도구도 strict mode와 유사한 효과를 얻을 수 있다.
    - 린트 도구: 정적 분석 기능을 통해 소스 코드를 실행하기 전에 소스코드를 스캔하여 문법적 오류 뿐만 아니라 잠재적 오류까지 찾아내고 오류의 이유를 리포팅해주는 도구.
    - 위와 같은 오류 뿐만 아니라 코딩 컨벤션을 설정 파일 형태로 정의하고 강제하는 기능도 존재한다.
  - IE 9 이하는 지원하지 않는다.



- 적용 방법

  - 전역의 선두 또는 함수 몸체의 선두에 `'use strict';`를 추가한다.
    - 전역의 선두에 추가하면 스크립트 전체에 적용된다.
    - 전역에 적용하는 방법은 바람직하지 않다.
    - 함수의 선두에 추가하면 함수와 해당 함수의 중첩된 내부 함수에도 적용된다.
    - 선두에 위치시키지 않으면 제대로 동작하지 않는다.

  ```javascript
  function foo(){
      x = 10
  }
  foo()
  console.log(x)      // 10
  
  function bar(){
      'use strict'
      y = 20
  }
  bar()               // ReferenceError: y is not defined
  ```



- 전역에 적용하는 것은 피해야 한다.

  - 아래의 경우 다른 스크립트에는 영향을 주지 않고 입력된 스크립트에 한정되어 적용된다.
  - 그러나 이와 같이 strict mode와 non-strict mode 스크립트를 혼용하는 것은 오류를 발생시킬 수 있다.
    - 외부 서드 파티 라이브러리의 경우, 라이브러리가 non-strict mode일 경우도 있기 때문에 전역에 적용하는 것은 특히 바람직하지 않다.
    - 이러한 경우, 즉시 실행 함수로 스크립트 전체를 감싸서 스코프를 구분하고 즉시 실행 함수의 선두에 strict mode를 적용한다.

  ```javascript
  // 즉시실행 함수에 strict mode 적용
  (function () {
    'use strict';
  	
  }());
  ```



- 함수 단위로 적용하는 것도 피해야 한다.

  - 어떤 함수는 strict mode를 적용하고 어떤 함수는 strict mode를 적용하지 않는 것은 바람직하지 않으며 모든 함수에 일일이 strict mode를 적용하는 것은 번거로운 일이다. 
  - strict mode가 적용된 함수가 참조할 함수 외부의 컨텍스트에 strict mode를 적용하지 않는다면 이 또한 문제가 발생할 수 있다.
  - 따라서 strict mode는 즉시실행함수로 감싼 스크립트 단위로 적용하는 것이 바람직하다.

  ```javascript
  function foo() {
      // non-strict mode
      var lеt = 10
  
      function bar() {
          'use strict'
          // 아래와 같이 본래 error가 발생하지 않을 상황에서도 error가 발생한다.
          let = 20;	// SyntaxError: Unexpected strict mode reserved word
      }
      bar();
  }
  foo()
  ```



- strict mode가 발생시키는 에러

  - 암묵적 전역 변수
    - 선언하지 않은 변수를 참조하면 `ReferenceError`가 발생한다.

  ```javascript
  (function () {
    'use strict'
  
    x = 1
    console.log(x) // ReferenceError: x is not defined
  }())
  ```

  - 매개변수 이름의 중복
    - 중복된 함수 파라미터 이름을 사용하면 `SyntaxError`가 발생한다.

  ```javascript
  (function () {
    'use strict';
    
    function foo(x, x) {		//SyntaxError: Duplicate parameter name not allowed in this context
      return x + x;
    }
    console.log(foo(3, 2));
  }());
  ```

  - `with`문의 사용
    - with 문을 사용하면 `SyntaxError`가 발생한다.

  ```javascript
  (function () {
    'use strict';
  
    with({ x: 1 }) {		// SyntaxError: Strict mode code may not include a with statement
      console.log(x);
    }
  }());
  ```

  - 생성자 함수가 아닌 일반 함수에서의 `this` 사용
    - 에러가 발생하지는 않지만 this에 undefined가 바인딩된다.

  ```javascript
  (function () {
    'use strict';
  
    function foo() {
      console.log(this); // undefined
    }
    foo();
  
    function Foo() {
      console.log(this); // Foo
    }
    new Foo();
  }());
  ```






# 화살표 함수

- 화살표 함수의 선언

  - 화살표 함수(Arrow function)는 function 키워드 대신 화살표(=>)를 사용하여 보다 간략한 방법으로 함수를 선언할 수 있다. 
  - 하지만 모든 경우 화살표 함수를 사용할 수 있는 것은 아니다.

  ```javascript
  // 매개변수 지정 방법
  () => { ... } 		// 매개변수가 없을 경우
  x => { ... } 		// 매개변수가 한 개인 경우, 소괄호를 생략할 수 있다.
  (x, y) => { ... } 	// 매개변수가 여러 개인 경우, 소괄호를 생략할 수 없다.
  
  // 함수 몸체 지정 방법
  x => { return x * x }  // single line block
  x => x * x             // 함수 몸체가 한줄의 구문이라면 중괄호를 생략할 수 있으며 암묵적으로 return된다. 위 표현과 동일하다.
             
  () => { return { a: 1 }; }
  () => ({ a: 1 })  // 위 표현과 동일하다. 객체 반환시 소괄호를 사용한다.
  
  // multi line block.
  () => {           
    const x = 10;
    return x * x;
  };
  ```



- 화살표 함수의 호출

  - 화살표 함수는 익명 함수로만 사용할 수 있다. 
    - 따라서 화살표 함수를 호출하기 위해서는 함수 표현식을 사용한다.

  ```javascript
  // 일반적인 함수 선언과 호출
  var pow = function (x) { return x * x; }
  console.log(pow(5)) // 25
  
  // 화살표 함수 선언과 호출
  var pow = x => x * x
  console.log(pow(5)) // 25
  ```

  - 또는 콜백 함수로 사용할 수 있다. 
    - 이 경우 일반적인 함수 표현식보다 표현이 간결하다.

  ```javascript
  const arr = [1, 2, 3]
  const pow = arr.map(x => x * x)
  
  console.log(pow)	//[ 1, 4, 9 ]
  ```

  

- 화살표 함수에서의 `this`

  - function 키워드로 생성한 일반 함수와 화살표 함수의 가장 큰 차이점은 `this`이다.
  - 일반 함수는 함수를 선언할 때 this에 바인딩할 객체가 정적으로 결정되는 것이 아니고, 함수를 호출할 때 함수가 어떻게 호출되었는지에 따라 this에 바인딩할 객체가 동적으로 결정된다.
    - 콜백 함수 내부의 this는 전역 객체 window를 가리킨다.
    - 콜백 함수 내부의 this가 메소드를 호출한 객체(생성자 함수의 인스턴스)를 가리키게 하는 여러 방법 중 하나는 아래와 같다.

  ```javascript
  // Function.prototype.bind()로 this를 바인딩한다.
  function Prefixer(prefix) {
    this.prefix = prefix
  }
  
  Prefixer.prototype.prefixArray = function (arr) {
    return arr.map(function (x) {
      return this.prefix + ' ' + x
    }.bind(this)) // this: Prefixer 생성자 함수의 인스턴스
  };
  
  var pre = new Prefixer('Hi')
  console.log(pre.prefixArray(['Lee', 'Kim']))
  ```

  - 화살표 함수는 함수를 선언할 때 this에 바인딩할 객체가 정적으로 결정된다. 
    - 동적으로 결정되는 일반 함수와는 달리 화살표 함수의 `this`는 언제나 상위 스코프의 `this`를 가리킨다. 이를 **Lexical this**라 한다. 
    - 화살표 함수는 앞서 살펴본 `Function.prototype.bind()`로 `this`를 바인딩하는 방법의  Syntactic sugar이다.
    - 화살표 함수는 `call`, `apply`, `bind` 메소드를 사용하여 `this`를 변경할 수 없다.

  ```javascript
  function Prefixer(prefix) {
    this.prefix = prefix
  }
  
  Prefixer.prototype.prefixArray = function (arr) {
    // this는 상위 스코프인 prefixArray 메소드 내의 this를 가리킨다.
    return arr.map(x => `${this.prefix}  ${x}`)
  }
  
  const pre = new Prefixer('Hi')
  console.log(pre.prefixArray(['Lee', 'Kim']))
  
  
  // 화살표 함수는 `call`, `apply`, `bind` 메소드를 사용하여 `this`를 변경할 수 없다.
  window.x = 1
  const normal = function () { return this.x; }
  const arrow = () => this.x
  
  console.log(normal.call({ x: 10 })) // 10
  console.log(arrow.call({ x: 10 }))  // 1
  ```

  

- 화살표 함수를 사용해서는 안되는 경우

  - 화살표 함수는 Lexical this를 지원하므로 콜백 함수로 사용하기 편리하다. 
    - 하지만 화살표 함수를 사용하는 것이 오히려 혼란을 불러오는 경우도 있으므로 주의하여야 한다.
  - 메소드
    - 화살표 함수로 메소드를 정의하는 것은 피해야 한다.
    - 메소드로 정의한 화살표 함수 내부의 this는 메소드를 소유한 객체, 즉 메소드를 호출한 객체를 가리키지 않고 상위 컨택스트인 전역 객체 window를 가리킨다.

  ```javascript
  const person = {
    name: 'Lee',
    sayHi: () => console.log(`Hi ${this.name}`)
  }
  
  person.sayHi() // Hi undefined
  ```

  - 프로토타입
    - 화살표 함수로 정의된 메소드를 prototype에 할당하는 경우도 동일한 문제가 발생한다.
    - 화살표 함수로 객체의 메소드를 정의하였을 때와 같은 문제가 발생한다. 
    - 따라서 prototype에 메소드를 할당하는 경우, 일반 함수를 할당해야 한다.

  ```javascript
  const person = {
    name: 'Lee',
  }
  
  Object.prototype.sayHi = () => console.log(`Hi ${this.name}`)
  
  person.sayHi() // Hi undefined
  ```

  - 생성자 함수
    - 화살표 함수는 생성자 함수로 사용할 수 없다. 
    - 생성자 함수는 prototype 프로퍼티를 가지며 prototype 프로퍼티가 가리키는 프로토타입 객체의 constructor를 사용한다. 
    - 하지만 화살표 함수는 prototype 프로퍼티를 가지고 있지 않다.

  ```javascript
  const Foo = () => {}
  
  // 화살표 함수는 prototype 프로퍼티가 없다
  console.log(Foo.hasOwnProperty('prototype')) // false
  
  const foo = new Foo() // TypeError: Foo is not a constructor
  ```

  - `addEventListener` 함수의 콜백 함수
    - 화살표 함수로 정의하면 this가 상위 컨택스트인 전역 객체 window를 가리킨다.

  ```javascript
  var button = document.getElementById('myButton')
  
  button.addEventListener('click', () => {
    console.log(this === window) // true
    this.innerHTML = 'Clicked button'
  })
  ```

  

