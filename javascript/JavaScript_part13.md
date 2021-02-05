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



# ECAMAScript6

## 화살표 함수

- 화살표 함수의 선언

  - 화살표 함수(Arrow function)는 `function` 키워드 대신 화살표(`=>`)를 사용하여 보다 간략한 방법으로 함수를 선언할 수 있다. 
  - 하지만 모든 경우 화살표 함수를 사용할 수 있는 것은 아니다.

  ```javascript
  // 매개변수 지정 방법
  () => { ... } 		// 매개변수가 없을 경우
  x => { ... } 		// 매개변수가 한 개인 경우, 소괄호를 생략할 수 있다.
  (x, y) => { ... } 	// 매개변수가 여러 개인 경우, 소괄호를 생략할 수 없다.
  
  // 함수 몸체 지정 방법
  x => { return x * x }  // single line block
  x => x * x             // 함수 몸체가 한줄의 구문이라면 중괄호를 생략할 수 있으며 암묵적으로 return된다. 위 표현과 동일하다.
  x => { x * x }		   // error가 발생한다. {}를 써줬으면 반드시 내부에 return 값이 있어야 한다.
             
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
    - 따라서 화살표 함수를 선언하기 위해서는 함수 표현식을 사용다.

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
  // 일반적인 함수를 콜백 함수로 사용했을 경우
  const arr = [1, 2, 3];
  const pow = arr.map(function (x) {
    return x * x;
  });
  
  console.log(pow);  //[ 1, 4, 9 ]
  
  // 화살표 함수를 콜백 함수로 사용했을 경우
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





## 이터레이션

- 이터레이션 프로토콜
  - ES6에서 도입된 이터레이션 프로토콜(iteration protocol)은 데이터 컬렉션을 순회하기 위한 프로토콜(미리 약속된 규칙)이다.
  - 이터레이션 프로토콜을 준수한 객체는 **for…of** 문으로 순회할 수 있고 **Spread 문법**의 피연산자가 될 수 있다.
  - 이터레이션 프로토콜에는 **이터러블 프로토콜(iterable protocol)**과 **이터레이터 프로토콜(iterator protocol)**이 있다.



- 이터러블

  - 이터러블 프로토콜을 준수한 객체를 이터러블이라 한다. 
  - 이터러블은 `Symbol.iterator` 메소드를 구현하거나 프로토타입 체인에 의해  `Symbol.iterator` 메소드를 상속한 객체를 말한다.
    - `Symbol.iterator` 메소드는 이터레이터를 반환한다.
    - 배열은 `Symbol.iterator` 메소드를 소유한다. 따라서 배열은 이터러블 프로토콜을 준수한 이터러블이다.
    - 일반 객체는 Symbol.iterator 메소드를 소유하지 않는다. 따라서 일반 객체는 이터러블 프로토콜을 준수한 이터러블이 아니다.
    - 하지만 일반 객체도 이터러블 프로토콜을 준수하도록 구현하면 이터러블이 된다.

  ```javascript
  const arr = [1, 2, 3]
  
  // 배열은 Symbol.iterator 메소드를 소유한다.
  // 따라서 배열은 이터러블 프로토콜을 준수한 이터러블이다.
  console.log(Symbol.iterator in arr) // true
  
  // 이터러블 프로토콜을 준수한 배열은 for...of 문에서 순회 가능하다.
  for (const i of arr) {
    console.log(i)
  }
  
  const obj = { a: 1, b: 2 }
  
  // 일반 객체는 Symbol.iterator 메소드를 소유하지 않는다.
  // 따라서 일반 객체는 이터러블 프로토콜을 준수한 이터러블이 아니다.
  console.log(Symbol.iterator in obj) // false
  
  // 이터러블이 아닌 일반 객체는 for...of 문에서 순회할 수 없다.
  // TypeError: obj is not iterable
  for (const p of obj) {
    console.log(p)
  }
  ```



- 이터레이터

  - 이터레이터 프로토콜은 `next` 메소드를 소유하고  `next` 메소드를 호출하면 이터러블을 순회하며 `value`, `done` 프로퍼티를 갖는 이터레이터 리절트(iterator result) 객체를 반환하는 것이다. 
    - 이 규약을 준수한 객체가 이터레이터이다.
  - 이터러블 프로토콜을 준수한 이터러블은 `Symbol.iterator` 메소드를 소유한다. 
    - 이 메소드를 호출하면 **이터레이터**를 반환한다.
  - 이터레이터 프로토콜을 준수한 이터레이터는 `next` 메소드를 갖는다.

  ```javascript
  // 배열은 이터러블 프로토콜을 준수한 이터러블이다.
  const array = [1, 2, 3]
  
  // Symbol.iterator 메소드는 이터레이터를 반환한다.
  const iterator = array[Symbol.iterator]()
  
  // 이터레이터 프로토콜을 준수한 이터레이터는 next 메소드를 갖는다.
  console.log('next' in iterator) // true
  ```

  - 이터레이터의 `next` 메소드를 호출하면 `value`, `done` 프로퍼티를 갖는 이터레이터 리절트 객체를 반환한다.
    - 이터레이터의 `next` 메소드는 이터러블의 각 요소를 순회하기 위한 포인터의 역할을 한다. 
    - `next` 메소드를 호출하면 이터러블을 순차적으로 한 단계씩 순회하며 이터레이터 리절트 객체를 반환한다.
    - 이터레이터 리절트 객체의 `value` 프로퍼티는 현재 순회 중인 이터러블의 값을 반환하고 `done` 프로퍼티는 이터러블의 순회 완료 여부를 반환한다.

  ```javascript
  // 배열은 이터러블 프로토콜을 준수한 이터러블이다.
  const array = [1, 2, 3]
  
  // Symbol.iterator 메소드는 이터레이터를 반환한다.
  const iterator = array[Symbol.iterator]()
  
  // 이터레이터 프로토콜을 준수한 이터레이터는 next 메소드를 갖는다.
  console.log('next' in iterator) // true
  
  // 이터레이터의 next 메소드를 호출하면 value, done 프로퍼티를 갖는 이터레이터 리절트 객체를 반환한다.
  let iteratorResult = iterator.next()
  console.log(iteratorResult) 	// {value: 1, done: false}
  
  // 순차적으로 한 단계씩 순회하며 이터레이터 리절트 객체를 반환한다.
  console.log(iterator.next()) 	// {value: 2, done: false}
  console.log(iterator.next())	// {value: 3, done: false}
  console.log(iterator.next())	// {value: undefined, done: true}
  ```



- 빌트인 이터러블
  - ECMAScript 6에서 제공하는 빌트인 이터러블은 아래와 같다.
  - Array, String, Map, Set 
  - TypedArray(Int8Array, Uint8Array, Uint8ClampedArray, Int16Array, Uint16Array, Int32Array, Uint32Array, Float32Array, Float64Array)
  - DOM data structure(NodeList, HTMLCollection), Arguments



- 이터레이션 프로토콜의 필요성

  - **데이터 소비자(Data consumer)**인 `for...of` 문, Spread 문법 등은 이터러블을 데이터 소스로 사용한다.
    - 즉, 이터러블은 **데이터 공급자(Data provider)**의 역할을 한다.
    - 만약 이처럼 다양한 데이터 소스가 각자의 순회 방식을 갖는다면 데이터 소비자는 다양한 데이터 소스의 순회 방식을 모두 지원해야 한다.
    - 이는 효율적이지 않다.
  - 다양한 데이터 소스가 이터레이션 프로토콜을 준수하도록 규정하면 데이터 소비자는 이터레이션 프로토콜만을 지원하도록 구현하면 된다.
    - 즉, 이터레이션 프로토콜은 다양한 데이터 소스가 하나의 순회 방식을 갖도록 규정하여 데이터 소비자가 효율적으로 다양한 데이터 소스를 사용할 수 있도록 데이터 소비자와 데이터 소스를 연결하는 인터페이스의 역할을 한다.

  - 이터러블을 지원하는 데이터 소비자는 내부에서 `Symbol.iterator` 메소드를 호출해 이터레이터를 생성하고 이터레리터의 `next` 메소드를 호출하여 이터러블을 순회한다. 
  - 그리고 `next` 메소드가 반환한 이터레이터 리절트 객체의 `value` 프로퍼티 값을 취득한다.



- `for...of` 문

  - 내부적으로 이터레이터의 next 메소드를 호출하여 이터러블을 순회하며 next 메소드가 반환한 이터레이터 리절트 객체의 value 프로퍼티 값을 `for...of`문의 변수에 할당한다. 
  - 그리고 이터레이터 리절트 객체의 `done` 프로퍼티 값이 false이면 이터러블의 순회를 계속하고 true이면 이터러블의 순회를 중단한다.

  ```javascript
  for (const item of [1, 2, 3]) {
    console.log(item)
  }
  
  // 내부 동작
  // 이터러블
  const iterable = [1, 2, 3]
  
  // 이터레이터
  const iterator = iterable[Symbol.iterator]()
  
  for (;;) {
    // 이터레이터의 next 메소드를 호출하여 이터러블을 순회한다.
    const res = iterator.next()
  
    // next 메소드가 반환하는 이터레이터 리절트 객체의 done 프로퍼티가 true가 될 때까지 반복한다.
    if (res.done) break
  
    console.log(res)
  }
  ```



- 커스텀 이러터블

  - 구현
    - 일반 객체는 이터러블이 아니다. 
    - 일반 객체는 Symbol.iterator 메소드를 소유하지 않는다. 
    - 즉, 일반 객체는 이터러블 프로토콜을 준수하지 않으므로 `for...of` 문으로 순회할 수 없다.
    - 하지만 일반 객체가 이터레이션 프로토콜을 준수하도록 구현하면 이터러블이 된다. 

  ```javascript
  const fibonacci = {
      // Symbol.iterator 메소드를 구현하여 이터러블 프로토콜을 준수
      [Symbol.iterator]() {
          let [pre, cur] = [0, 1]
          // 최대값
          const max = 10
  
          // Symbol.iterator 메소드는 next 메소드를 소유한 이터레이터를 반환해야 한다.
          // next 메소드는 이터레이터 리절트 객체를 반환
          return {
              // fibonacci 객체를 순회할 때마다 next 메소드가 호출된다.
              next() {
                  [pre, cur] = [cur, pre + cur]
                  // next 메소드는 done과 value 프로퍼티를 가지는 이터레이터 리절트 객체를 반환한다. 
                  return {
                      value: cur,
                      done: cur >= max
                  };
              }
          };
      }
  };
  
  // 이터러블의 최대값을 외부에서 전달할 수 없다.
  for (const num of fibonacci) {
      // for...of 내부에서 break는 가능하다.
      // if (num >= 10) break
      console.log(num) // 1 2 3 5 8
  }
  ```

  - 이터러블을 생성하는 함수
    - 위에서 구현한 fibonacci 이터러블은 외부에서 값을 전달할 방법이 없다.
    - 이터러블의 최대 순회수를 전달받아 이터러블을 반환하는 함수를 만들면 외부에서 값을 전달할 수 있다.

  ```javascript
  // 이터러블을 반환하는 함수
  const fibonacciFunc = function (max) {
    let [pre, cur] = [0, 1]
  
    return {
      // Symbol.iterator 메소드를 구현하여 이터러블 프로토콜을 준수
      [Symbol.iterator]() {
        // Symbol.iterator 메소드는 next 메소드를 소유한 이터레이터를 반환해야 한다.
        // next 메소드는 이터레이터 리절트 객체를 반환
        return {
          // fibonacci 객체를 순회할 때마다 next 메소드가 호출된다.
          next() {
            [pre, cur] = [cur, pre + cur]
            return {
              value: cur,
              done: cur >= max
            };
          }
        };
      }
    };
  };
  
  // 이터러블을 반환하는 함수에 이터러블의 최대값을 전달한다.
  for (const num of fibonacciFunc(10)) {
    console.log(num) // 1 2 3 5 8
  }
  ```

  - 이터러블이면서 이터레이션인 객체를 생성하는 함수
    - 이터레이터를 생성하려면 이터러블의 `Symbol.iterator` 메소드를 호출해야 한다. 
    - 이터러블이면서 이터레이터인 객체를 생성하면 `Symbol.iterator` 메소드를 호출하지 않아도 된다.

  ```javascript
  // 이터러블이면서 이터레이터인 객체를 반환하는 함수
  const fibonacciFunc = function (max) {
    let [pre, cur] = [0, 1]
  
    // Symbol.iterator 메소드와 next 메소드를 소유한
    // 이터러블이면서 이터레이터인 객체를 반환
    return {
      // Symbol.iterator 메소드
      [Symbol.iterator]() {
        return this
      },
      // next 메소드는 이터레이터 리절트 객체를 반환
      next() {
        [pre, cur] = [cur, pre + cur]
        return {
          value: cur,
          done: cur >= max
        };
      }
    };
  };
  
  // iter는 이터러블이면서 이터레이터이다.
  let iter = fibonacciFunc(10)
  
  // iter는 이터레이터이다.
  console.log(iter.next()) // {value: 1, done: false}
  console.log(iter.next()) // {value: 2, done: false}
  console.log(iter.next()) // {value: 3, done: false}
  console.log(iter.next()) // {value: 5, done: false}
  console.log(iter.next()) // {value: 8, done: false}
  console.log(iter.next()) // {value: 13, done: true}
  
  iter = fibonacciFunc(10);
  
  // iter는 이터러블이다.
  for (const num of iter) {
    console.log(num) // 1 2 3 5 8
  }
  ```

  - 아래의 객체는 `Symbol.iterator` 메소드와 `next` 메소드를 소유한 이터러블이면서 이터레이터이다. 
    - `Symbol.iterator` 메소드는 `this`를 반환하므로 `next` 메소드를 갖는 이터레이터를 반환한다.

  ```javascript
  {
    [Symbol.iterator]() {
      return this
    },
    next() { /***/ }
  }
  ```

  - 무한 이터러블과 지연 평가(Lazy evaluation)
    - 이터러블은 Lazy evaluation(지연 평가)를 통해 값을 생성한다.
    - Lazy evaluation은 평가 결과가 필요할 때까지 평가를 늦추는 기법이다. 
    - 아래 예시의 `fibonacciFunc` 함수는 무한 이터러블을 생성한다. 
    - 하지만 `fibonacciFunc` 함수가 생성한 무한 이터러블은 데이터를 공급하는 메커니즘을 구현한 것으로 데이터 소비자인 `for…of` 문이나 디스트럭처링 할당이 실행되기 이전까지 데이터를 생성하지는 않는다. 
    - `for…of` 문의 경우, 이터러블을 순회할 때 내부에서 이터레이터의 `next` 메소드를 호출하는데 바로 이때 데이터가 생성된다. 
    - `next` 메소드가 호출되기 이전까지는 데이터를 생성하지 않는다. 즉, 데이터가 필요할 때까지 데이터의 생성을 지연하다가 데이터가 필요한 순간 데이터를 생성한다.

  ```javascript
  // 무한 이터러블을 생성하는 함수
  const fibonacciFunc = function () {
      let [pre, cur] = [0, 1]
  
      return {
          [Symbol.iterator]() {
              return this
          },
          next() {
              [pre, cur] = [cur, pre + cur]
              // done 프로퍼티를 생략한다.
              return { value: cur }
          }
      };
  };
  
  // fibonacciFunc 함수는 무한 이터러블을 생성한다.
  for (const num of fibonacciFunc()) {
      if (num > 10000) break
      console.log(num) // 1 2 3 5 8...
  }
  
  // 무한 이터러블에서 3개만을 취득한다.
  const [f1, f2, f3] = fibonacciFunc()
  console.log(f1, f2, f3) // 1 2 3
  ```



## 제네레이터

- 제네레이터

  - 이터러블을 생성하는 함수
  - 제너레이터 함수를 사용하면 이터레이션 프로토콜을 준수해 이터러블을 생성하는 방식보다 간편하게 이터러블을 구현할 수 있다. 
  - 또한 제너레이터 함수는 비동기 처리에 유용하게 사용된다.

  ```javascript
  // 이터레이션 프로토콜을 구현하여 무한 이터러블을 생성하는 함수
  const createInfinityByIteration = function () {
    let i = 0 // 자유 변수
    return {
      [Symbol.iterator]() { return this; },
      next() {
        return { value: ++i }
      }
    };
  };
  
  for (const n of createInfinityByIteration()) {
    if (n > 5) break
    console.log(n) // 1 2 3 4 5
  }
  
  // 무한 이터러블을 생성하는 제너레이터 함수
  function* createInfinityByGenerator() {
    let i = 0
    while (true) { yield ++i; }
  }
  
  for (const n of createInfinityByGenerator()) {
    if (n > 5) break
    console.log(n) // 1 2 3 4 5
  }
  ```

  - 제너레이터 함수는 일반 함수와 같이 함수의 코드 블록을 한 번에 실행하지 않고 함수 코드 블록의 실행을 일시 중지했다가 필요한 시점에 재시작할 수 있는 특수한 함수이다.

  ```javascript
  function* counter() {
    console.log('첫번째 호출')
    yield 1                   // 첫번째 호출 시에 이 지점까지 실행된다.
    console.log('두번째 호출')
    yield 2                   // 두번째 호출 시에 이 지점까지 실행된다.
    console.log('세번째 호출')  // 세번째 호출 시에 이 지점까지 실행된다.
  }
  
  const generatorObj = counter()
  
  console.log(generatorObj.next()) // 첫번째 호출 {value: 1, done: false}
  console.log(generatorObj.next()) // 두번째 호출 {value: 2, done: false}
  console.log(generatorObj.next()) // 세번째 호출 {value: undefined, done: true}
  ```

  - 일반 함수를 호출하면 return 문으로 반환값을 리턴하지만 제너레이터 함수를 호출하면 제너레이터를 반환한다. 
    - 이 제너레이터는 이터러블(iterable)이면서 동시에 이터레이터(iterator)인 객체이다.
    - 다시 말해 제너레이터 함수가 생성한 제너레이터는 `Symbol.iterator` 메소드를 소유한 이터러블이다. 
    - 그리고 제너레이터는 `next` 메소드를 소유하며 `next` 메소드를 호출하면 `value`, `done` 프로퍼티를 갖는 이터레이터 리절트 객체를 반환하는 이터레이터이다.

  ```javascript
  function* counter() {
    for (const v of [1, 2, 3]) yield v
    // => yield* [1, 2, 3]
  }
  
  // 제너레이터 함수를 호출하면 제너레이터를 반환한다.
  let generatorObj = counter()
  
  // 제너레이터는 이터러블이다.
  console.log(Symbol.iterator in generatorObj) // true
  
  for (const i of generatorObj) {
    console.log(i) // 1 2 3
  }
  
  generatorObj = counter()
  
  // 제너레이터는 이터레이터이다.
  console.log('next' in generatorObj) // true
  
  console.log(generatorObj.next()) // {value: 1, done: false}
  console.log(generatorObj.next()) // {value: 2, done: false}
  console.log(generatorObj.next()) // {value: 3, done: false}
  console.log(generatorObj.next()) // {value: undefined, done: true}
  ```



- 제네레이터 함수 정의

  -  `function*` 키워드로 선언한다. 
  - 그리고 하나 이상의 `yield` 문을 포함한다.

  ```javascript
  // 제너레이터 함수 선언문
  function* genDecFunc() {
    yield 1
  }
  
  let generatorObj = genDecFunc()
  
  // 제너레이터 함수 표현식
  const genExpFunc = function* () {
    yield 1
  };
  
  generatorObj = genExpFunc()
  
  // 제너레이터 메소드
  const obj = {
    * generatorObjMethod() {
      yield 1
    }
  };
  
  generatorObj = obj.generatorObjMethod();
  
  // 제너레이터 클래스 메소드
  class MyClass {
    * generatorClsMethod() {
      yield 1
    }
  }
  
  const myClass = new MyClass()
  generatorObj = myClass.generatorClsMethod()
  ```



- 제네레이터 함수의 호출과 제네레이터 객체

  - 제너레이터 함수를 호출하면 제너레이터 함수의 코드 블록이 실행되는 것이 아니라 제너레이터 객체를 반환한다.
  - 제너레이터 객체는 이터러블이며 동시에 이터레이터이다. 
    - 따라서 `next` 메소드를 호출하기 위해 `Symbol.iterator` 메소드로 이터레이터를 별도 생성할 필요가 없다.
  - 제너레이터 함수가 생성한 제너레이터 객체의 `next` 메소드를 호출하면 처음 만나는 `yield` 문까지 실행되고 일시 중단(suspend)된다. 
    - 또 다시`next` 메소드를 호출하면 중단된 위치에서 다시 실행(resume)이 시작하여 다음 만나는 `yield` 문까지 실행되고 또 다시 일시 중단된다.
  - `next` 메소드는 이터레이터 리절트 객체와 같이 `value`, `done` 프로퍼티를 갖는 객체를 반환한다. 
    - `value` 프로퍼티는 `yield` 문이 반환한 값이고 `done` 프로퍼티는 제너레이터 함수 내의 모든 `yield` 문이 실행되었는지를 나타내는 boolean 타입의 값이다. 
    - 마지막 `yield` 문까지 실행된 상태에서 `next` 메소드를 호출하면 `done` 프로퍼티 값은 true가 된다.

  ```javascript
  function* counter() {
    console.log('Point 1')
    yield 1                // 첫번째 next 메소드 호출 시 여기까지 실행된다.
    console.log('Point 2')
    yield 2                // 두번째 next 메소드 호출 시 여기까지 실행된다.
    console.log('Point 3')
    yield 3                // 세번째 next 메소드 호출 시 여기까지 실행된다.
    console.log('Point 4') // 네번째 next 메소드 호출 시 여기까지 실행된다.
  }
  
  // 제너레이터 함수를 호출하면 제너레이터 객체를 반환한다.
  // 제너레이터 객체는 이터러블이며 동시에 이터레이터이다.
  // 따라서 Symbol.iterator 메소드로 이터레이터를 별도 생성할 필요가 없다
  const generatorObj = counter()
  
  // 첫번째 next 메소드 호출: 첫번째 yield 문까지 실행되고 일시 중단된다.
  console.log(generatorObj.next())
  // Point 1
  // {value: 1, done: false}
  
  // 두번째 next 메소드 호출: 두번째 yield 문까지 실행되고 일시 중단된다.
  console.log(generatorObj.next())
  // Point 2
  // {value: 2, done: false}
  
  // 세번째 next 메소드 호출: 세번째 yield 문까지 실행되고 일시 중단된다.
  console.log(generatorObj.next())
  // Point 3
  // {value: 3, done: false}
  
  // 네번째 next 메소드 호출: 제너레이터 함수 내의 모든 yield 문이 실행되면 done 프로퍼티 값은 true가 된다.
  console.log(generatorObj.next())
  // Point 4
  // {value: undefined, done: true}
  ```



### 제네레이터의 활용

- 이터러블의 구현

  - 제너레이터 함수를 사용하면 이터레이션 프로토콜을 준수해 이터러블을 생성하는 방식보다 간편하게 이터러블을 구현할 수 있다. 

  ```javascript
  // 무한 이터러블을 생성하는 제너레이터 함수
  const infiniteFibonacci = (function* () {
    let [pre, cur] = [0, 1]
  
    while (true) {
      [pre, cur] = [cur, pre + cur]
      yield cur
    }
  }())
  
  // infiniteFibonacci는 무한 이터러블이다.
  for (const num of infiniteFibonacci) {
    if (num > 10000) break
    console.log(num)
  }
  ```

  - 제너레이터 함수에 최대값을 인수를 전달

  ```javascript
  const createInfiniteFibByGen = function* (max) {
    let [prev, curr] = [0, 1]
  
    while (true) {
      [prev, curr] = [curr, prev + curr]
      if (curr >= max) return // 제너레이터 함수 종료
      yield curr
    }
  }
  
  for (const num of createInfiniteFibByGen(10000)) {
    console.log(num)
  }
  ```

  - 이터레이터의 `next` 메소드와 다르게 제너레이터 객체의 `next` 메소드에는 인수를 전달할 수도 있다. 
    - 이를 통해 제너레이터 객체에 데이터를 전달할 수 있다.

  ```javascript
  function* gen(n) {
    let res
    res = yield n    // n: 0 ⟸ gen 함수에 전달한 인수
  
    console.log(res) // res: 1 ⟸ 두번째 next 호출 시 전달한 데이터
    res = yield res
  
    console.log(res) // res: 2 ⟸ 세번째 next 호출 시 전달한 데이터
    res = yield res
  
    console.log(res) // res: 3 ⟸ 네번째 next 호출 시 전달한 데이터
    return res
  }
  const generatorObj = gen(0)
  
  // 제너레이터 함수 시작
  console.log(generatorObj.next())	// { value: 0, done: false }
  // 제너레이터 객체에 1 전달
  console.log(generatorObj.next(1))	// { value: 1, done: false }
  // 제너레이터 객체에 2 전달
  console.log(generatorObj.next(2))	// { value: 2, done: false }
  // 제너레이터 객체에 3 전달
  console.log(generatorObj.next(3)) 	// { value: 3, done: true }
  ```

  - 이터레이터의 `next` 메소드는 이터러블의 데이터를 꺼내 온다. 
    - 이에 반해 제너레이터의 `next` 메소드에 인수를 전달하면 제너레이터 객체에 데이터를 밀어 넣는다. 
    - 제너레이터의 이런 특성은 동시성 프로그래밍을 가능하게 한다.



- 비동기 처리

  - 제너레이터를 사용해 비동기 처리를 동기 처리처럼 구현할 수 있다. 
    - 다시 말해 비동기 처리 함수가 처리 결과를 반환하도록 구현할 수 있다.

  ```javascript
  const fetch = require('node-fetch')
  
  function getUser(genObj, username) {
    fetch(`https://api.github.com/users/${username}`)
      .then(res => res.json())
      // 1. 비동기처리가 완료되면 next 메소드를 통해 제너레이터 객체에 비동기 처리 결과를 전달한다.
      .then(user => genObj.next(user.name))
  }
  
  // 제너레이터 객체 생성
  const g = (function* () {
    let user
    // 2. 제너레이터 객체에 전달된 비동기 처리 결과는 user 변수에 할당된다.
    // 비동기 처리의 순서가 보장된다.
    user = yield getUser(g, 'jeresig')
    console.log(user) // John Resig
  
    user = yield getUser(g, 'ahejlsberg')
    console.log(user) // Anders Hejlsberg
  
    user = yield getUser(g, 'ungmo2')
    console.log(user) // Ungmo Lee
  }())
  
  // 제너레이터 함수 시작
  g.next()
  ```

  

## 간단한 설명

- 제네레이터 문법의 핵심 기능은 함수를 작성할 때 함수를 특정 구간에 멈춰 놓을 수도 있고, 원할 때 다시 돌아가게 할 수도 있다는 것이다.
  - 일반적인 함수는 리턴문을 만나면 함수가 종료된다.
  - 그러나 제네레이터 함수를 사용하면 함수에서 값을 순차적으로 반환할 수 있다.



- 동작 방식

  - 제네레이터가 처음 만들어지면 함수의 흐름은 멈춰 있는 상태이다.
  - `next()`가 호출되면 다음 `yield`가 있는 곳까지 호출하고 다시 함수가 멈춘다.

  ```javascript
  function* generatorFucntion(){
      console.log('안녕하세요.');
      yield 1;
      console.log('반갑습니다.');
      yield 2;
      console.log('함수 실행중입니다.')
      yield 3;
      return 4
  }
  
  const generator = generatorFucntion()
  
  console.log(generator.next())
  // 안녕하세요
  // {value:1,done:false}
  console.log(generator.next())
  // 반값습니다.
  // {value:2,done:false}
  console.log(generator.next())
  // 함수 실행중입니다.
  // {value:3,done:false}
  console.log(generator.next())
  // {value:4,done:true}
  console.log(generator.next())
  // {value:undefined,done:true}
  ```

  - `next()`에 파라미터를 넣으면 제네레이터 함수에서 `yield`를 사용하여 해당 값을 조회할 수도 있다.

  ```javascript
  function* sumGenerator(){
      let a = yield;
      let b = yield;
      yield a+b;
  }
  const sum = sumGenerator()
  sum.next(1) // {value:undefiend, done:false}
  sum.next(2) // {value:undefiend, done:false}
  sum.next()  // {value:3, done:false}
  sum.next()  // {value:undefiend, done:true}
  ```

  

  













