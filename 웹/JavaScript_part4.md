# this

- 자바스크립트 함수는 호출될 때, 매개변수로 전달되는 인자값 외에 `arguments` 객체와 `this`를 암묵적으로 전달 받는다.



- JS에서의 this

  - Java에서의 this는 인스턴스 자신(python의 self)을 가리키는 참조 변수다.
    - this가 객체 자신에 대한 참조 값을 가지고 있다는 뜻이다.
    - 주로 매개변수와 객체 자신이 가지고 있는 멤버변수명이 같을 경우 이를 구분하기 위해 사용된다.

  - 그러나 JS의 경우 this에 바인딩 되는 객체는 한 가지가 아니라 해당 함수 호출 방식에 따라 this에 바인딩 되는 객체가 달라진다.
    - 다시 말해 함수를 선언할 때 this에 바인딩할 객체가 정적으로 결정되는 것이 아니다.
    - 함수를 호출할 때 함수가 어떻게 호출되었는지에 따라 this에 바인딩할 객체가 동적으로 결정된다.
  - JS의 함수 호출 방식은 다음과 같다.
    - 함수 호출
    - 메소드 호출
    - 생성자 함수 호출
    - apply/call/bind 호출

  ```javascript
  var foo = function () {
    console.dir(this);
  };
  
  // 1. 함수 호출
  // 사실 아래의 호출 방식은 window.foo()와 같다.
  // 글로벌 영역에 선언한 함수는 전역객체의 프로퍼티로 접근할 수 있는 전역 변수의 메서드다.
  foo() // window
  
  
  // 2. 메소드 호출
  var obj = { foo: foo }
  obj.foo() // obj
  
  // 3. 생성자 함수 호출
  var instance = new foo() // instance
  
  // 4. apply/call/bind 호출
  var bar = { name: 'bar' }
  foo.call(bar)   // bar
  foo.apply(bar)  // bar
  foo.bind(bar)() // bar
  ```

## 함수 호출시의 this

- `this`는 전역객체(`window`)에 바인딩 된다.

  - 전역객체는 모든 객체의 유일한 최상위 객체를 의미하며 일반적으로 브라우저에서는 `window`, Server-side(Node.js)에서는 `global` 객체를 의미한다.

  ```javascript
  // 브라우저 콘솔에서 입력할 경우
  this === window // true
  
  // Terminal에서 입력할 경우
  this === global // true
  ```

  - 전역객체(`window`)는 전역 스코프를 갖는 전역변수를 프로퍼티로 소유한다. 글로벌 영역에 선언한 함수는 전역객체의 프로퍼티로 접근할 수 있는 전역 변수의 메서드다.

  ```javascript
  var gv = 'global'
  
  console.log(gv)			// global
  console.log(window.gv)	// global
  
  function foo() {
    console.log('호출됨!!')
  }
  foo()			// 호출됨!!
  window.foo()	// 호출됨!!
  ```



- 내부함수는 일반 함수, 메소드, 콜백함수 어디에서 선언되었든 this는 외부함수가 아닌 전역객체를 바인딩한다.

  - 이것은 설계 단계의 결험으로 메소드가 내부함수를 사용하여 자신의 작업을 돕게 할 수 없게 된다.
  - 내부함수의 this가 전역변수를 참조하는 것을 회피하는 방법이 있다.

  ```javascript
  // 내부함수
  function foo(){
      console.log("foo's this:",this)			// foo's this: window {...}
      function bar(){
          console.log("bar's this:", this)	// bar's this: window {...}
      }
      bar()
  }
  foo()
  
  
  // 메소드의 내부 함수
  var obj = {
      foo:function(){
          console.log("foo's this:",this)		// foo's this: obj
          function bar(){
              console.log("bar's this:",this)	// bar's this: window {...}
          }
          bar()
      }
  }
  obj.foo()
  
  
  // 콜백 함수
  var obj = {
    foo: function() {
      setTimeout(function() {
        console.log(this)  // window {...}
      }, 100)
    }
  }
  obj.foo()
  ```



- 내부함수의 this가 전역변수를 참조하는 것을 회피하는 방법

  - 외부함수에서 this를 다른 변수에 저장한 후 사용하는 방법

  ```javascript
  // 내부함수의 this가 전역객체를 참조하는 것을 피하는 방법
  var obj = {
    foo: function() {
      var that = this;  // this === obj
  
      console.log("foo's this: ",  this);  // foo's this: obj
      function bar() {
        console.log("bar's this: ",  this); // bar's this: window
  
        console.log("bar's that: ",  that); // bar's that: obj
      }
      bar();
    }
  };
  
  obj.foo();
  ```

  - this를 명시적으로 바인딩할 수 있는 `apply`, `call`, `bind` 메소드를 사용하는 방법

  ```javascript
  var obj = {
    foo: function() {
      console.log("foo's this: ",  this)  // obj
      function bar(a, b) {
        console.log("bar's this: ",  this) // obj
        console.log("bar's arguments: ", arguments)
      }
      bar.apply(obj, [1, 2])
      bar.call(obj, 1, 2)
      bar.bind(obj)(1, 2)
    }
  }
  
  obj.foo()
  ```

## 메소드 호출 시의 this

- 메소드 내부의 this는 해당 메소드를 소유한 객체, 즉 해당 메소드를 호출한 객체에 바인딩된다.

  ```javascript
  var obj = {
      name: 'Cha',
      sayName: function() {
        console.log(this.name)
      }
  }
  
  obj.sayName();
  ```



- 프로토타입 객체 메소드 내부에서 사용된 this도 일반 메소드 방식과 마찬가지로 해당 메소드를 호출한 객체에 바인딩된다.

  ```javascript
  function Person(name) {
      this.name = name
  }
    
  Person.prototype.getName = function() {
      console.log(this.name)
  }
    
  var cha = new Person('Cha')
  cha.getName()
  ```

## 생성자 함수 호출시의 this

- 생성자 함수 동작 방식

  - 빈 객체 생성 및 `this` 바인딩
    - 생성자 함수의 코드가 실행되기 전 빈 객체가 생성된다.
    - 이 빈 객체가 생성자 함수가 새로 생성하는 객체이다. 이후 생성자 함수에서 사용되는 **this는 이 빈 객체를 가리킨다. **
    - 그리고 생성된 빈 객체는 생성자 함수의 prototype 프로퍼티가 가리키는 객체를 자신의 프로토타입 객체로 설정한다.
  - this를 통한 프로퍼티 생성
    - 생성된 빈 객체에 this를 사용하여 동적으로 프로퍼티나 메소드를 생성할 수 있다.
    - this는 새로 생성된 객체를 가리키므로 this를 통해 생성한 프로퍼티와 메소드는 새로 생성된 객체에 추가된다.
  - 생성된 객체 반환
    - 반환문이 없는 경우,  this에 바인딩된 새로 생성한 객체가 반환된다. 명시적으로 this를 반환하여도 결과는 같다.
    - 반환문이 this가 아닌 다른 객체를 명시적으로 반환하는 경우, this가 아닌 해당 객체가 반환된다. 이때 this를 반환하지 않은 함수는 생성자 함수로서의 역할을 수행하지 못한다. 따라서 생성자 함수는 반환문을 명시적으로 사용하지 않는다.

  ```javascript
  function Person(name) {
    // 즉 아래 코드는 `Person으로 생성된 빈 객체`.name = name과 같다.
    this.name = name
  }
  
  var cha = new Person('Cha')
  console.log(cha.name)
  ```



- 생성자 함수에 new 연산자를 붙이지 않고 호출할 경우

  - 일반함수와 생성자 함수에 특별한 형식적 차이는 없으며 함수에 new 연산자를 붙여서 호출하면 해당 함수는 생성자 함수로 동작한다.
  - 그러나 객체 생성 목적으로 작성한 생성자 함수를 new 없이 호출하거나 일반함수에 new를 붙여 호출하면 오류가 발생할 수 있다. 일반함수와 생성자 함수의 호출 시 this 바인딩 방식이 다르기 때문이다.
  - 일반 함수를 호출하면 this는 전역객체에 바인딩되지만 new 연산자와 함께 생성자 함수를 호출하면 this는 생성자 함수가 암묵적으로 생성한 빈 객체에 바인딩된다.

  ```javascript
  function Person(name) {
    // new없이 호출하는 경우, 전역객체에 name 프로퍼티를 추가
    this.name = name
  }
  
  // 일반 함수로서 호출되었기 때문에 객체를 암묵적으로 생성하여 반환하지 않는다.
  // 일반 함수의 this는 전역객체를 가리킨다.
  var cha = Person('Cha')
  
  // 객체를 암묵적으로 생성하여 반환하지 않으므로 undefined가 출력된다.
  console.log(cha) 		 // undefined
  console.log(window.name) // Cha
  ```

  - Scope-Safe Constructor
    - 생성자 함수를 `new` 키워드 없이 호출하였을 경우 위처럼 원하는대로 동작하지 않는다.
    - 위와 같은 일을 방지하기 위해 Scope-Safe Constructor 패턴을 사용한다.
    - `arguments.callee`는 현재 사용중인 함수를 나타낸다.

  ```javascript
  // arguments.callee
  function foo(){
      console.log(arguments.callee)	// [Function: foo]
  }
  foo()
  
  // 아래와 같이 재귀함수도 구현 가능하다.
  function bar(){
      arguments.callee()
  }
  foo()
  
  
  function foo(name) {
      // 생성자 함수가 new 연산자와 함께 호출되면 함수의 선두에서 빈객체를 생성하고 this에 바인딩한다.
  
      /*
      this가 호출된 함수(이 경우엔 foo)의 인스턴스가 아니면 new 연산자를 사용하지 않은 것이므로
      이 경우 new와 함께 생성자 함수를 호출하여 인스턴스를 반환한다.
      arguments.callee는 호출된 함수의 이름을 나타낸다.
      이 예제의 경우 foo로 표기하여도 문제없이 동작하지만 특정함수의 이름과 의존성을 없애기 위해서 arguments.callee를 사용하는 것이 좋다.
      */
      if (!(this instanceof arguments.callee)) {
          return new arguments.callee(name)
      }
  
      // 프로퍼티 생성과 값의 할당
      this.name = name
  }
  
  var a = new foo('Cha')
  var b = foo('Kim')
  
  console.log(a.name)	// Cha
  console.log(b.name)	// Kim
  ```

## apply/call/bind 호출

- this를 특정 객체에 명시적으로 바인딩하는 방법
  - this에 바인딩될 객체는 함수 호출 패턴에 의해 결정된다.
  - 이는 JavaScript 엔진이 수행하는 것이다.
  - 이러한 JavaScript의 암묵적 this 바인딩 이외의 this를 특정 객체에 명시적으로 바인딩하는 방법도 제공된다.
  - 이것을 가능하게 하는 것이 `Function.prototype.apply`, `Function.prototype.call` 메소드이다.
  - 이 메소드들은 모든 함수 객체의 프로토타입 객체인 `Function.prototype` 객체의 메소드이다.



- `apply()`

  - `apply()`메소드를 호출하는 주체는 함수이며  `apply()` 메소드는 this를 특정 객체에 바인딩할 뿐 본질적인 기능은 함수 호출이다.
  - `func.apply(thisArg,[argsArray])`
    - `func`: `apply()` 메소드를 호출하는 함수
    - `thisArg`: 함수 내부의 this에 바인딩할 객체
    - `argsArray`: 함수에 전달할 argument의 배열, 필수 값은 아니다.

  ```javascript
  var Person = function (name) {
      this.name = name
      // foo.name = name
  };
  
  var foo = {}
  
  
  Person.apply(foo, ['Cha'])
  
  console.log(foo) // { name: 'Cha' }
  ```

  - `apply()` 메소드의 대표적인 용도는 arguments 객체와 같은 유사 배열 객체에 배열 메소드를 사용하는 경우이다.
    - 아래 코드는 `Array.prototype.slice()` 메소드를 this는 arguments 객체로 바인딩해서 호출하라는 뜻이다.
    - 메소드 내부의 this는 해당 메소드를 소유한 객체, 즉 해당 메소드를 호출한 객체에 바인딩된다.
    - `Array.prototype.slice()` 메소드를 arguments 객체 자신의 메소드인 것처럼 `arguments.slice()`와 같은 형태로 호출하라는 것이다.

  ```javascript
  function convertArgsToArray() {
      console.log(arguments);
    
      // arguments 객체를 배열로 변환
      // slice: 배열의 특정 부분에 대한 복사본을 생성한다.
      var arr = Array.prototype.slice.apply(arguments)
    
      console.log(arr)
      return arr
  }
  
  convertArgsToArray(1, 2, 3)
  ```



- `call()`

  - `apply()`와 기능은 같지만 `apply()`의 두 번째 인자에서 배열 형태로 넘긴 것을 각각 하나의 인자로 넘긴다.

  ```javascript
  var Person = function (name) {
      this.name = name
  };
  
  var foo = {}
  
  
  Person.apply(foo, ['Cha'])
  Person.call(foo,'Cha')
  ```

  

- `apply()`와 `call()` 메소드는 콜백 함수의 this를 위해서 사용되기도 한다.

  - 콜백함수를 호출하는 외부 함수 내부의 this와 콜백함수 내부의 this가 상이하기 때문에 문맥상 문제가 발생한다.

  ```javascript
  function Person(name) {
      this.name = name
  }
    
  Person.prototype.foo = function(callback) {
      if(typeof callback == 'function') {
          // 콜백함수 내부의 this
          // foo를 호출한 것은 p라는 Person 객체이므로 this는 이 p를 가리키게 된다.
          console.log(this)   // Person { name: 'Lee' }
          callback()
      }
  }
  
  function bar() {
      // 콜백함수를 호출하는 외부 함수 내부의 this
      console.log(this)       // window
  }
  
  var p = new Person('Lee')
  p.foo(bar)
  ```

  - 따라서 콜백함수 내부의 this를 콜백함수를 호출하는 함수 내부의 this와 일치시켜 주어야 한다.

  ```javascript
  function Person(name) {
      this.name = name
  }
  
  Person.prototype.foo = function (callback) {
      if (typeof callback == 'function') {
          console.log(this)    // Person { name: 'Lee' }
          callback.call(this)
      }
  };
    
  function bar() {
      console.log(this)       // Person { name: 'Lee' }
      console.log(this.name)
  }
    
    var p = new Person('Lee')
    p.foo(bar)    // Lee
  ```

  - ES5에 추가된 `Function.prototype.bind`를 사용하는 방법도 있다.
    -  `Function.prototype.bind`는 함수에 인자로 전달한 this가 바인딩된 새로운 함수를 리턴한다.

  ```javascript
  function Person(name) {
      this.name = name
  }
  
  Person.prototype.foo = function (callback) {
      if (typeof callback == 'function') {
          console.log(this)
          // this가 바인딩된 새로운 함수를 호출
          callback.bind(this)();
      }
  };
  
  function bar() {
      console.log(this)
      console.log(this.name)
  }
    
    var p = new Person('Lee')
    p.foo(bar);  // Lee
  ```

  



# 스코프

- 스코프
  - 참조 대상 식별자를 찾아내기 위한 규칙
    - 식별자(identifier): 변수, 함수의 이름과 같이 어떤 대상을 다른 대상과 구분하여 식별할 수 있는 유일한 이름
    - 식별자는 자신이 어디에서 선언됐는지에 따라 자신이 유효한(다른 코드에서 자신을 참조할 수 있는) 범위를 갖는다.
  - 자바스크립트를 포함한 프로그래밍 언어의 기본적인 개념
  - 스코프가 없다면 모든 식별자의 이름은 유일해야 할 것이다.



- 스코프의 구분
  - 전역 스코프: 코드 어디에서든 참조 가능
  - 지역 스코프: 함수 코드 블록이 만든 스코프로, 함수 자신과 하위 함수에서만 참조 가능



- 자바스크립트 스코프의 특징

  - **C-family 언어들**은 **블록 레벨 스코프**를 따른다.
    - 코드 블록 내에서 유효한 스코프를 의미한다.
  - **JavaScript**는 **함수 레벨 스코프**를 따른다.
    - 함수 코드 블록 내에서 선언된 변수는 함수 코드 블록 내에서만 유효하고 함수 외부에서는 유효하지 않다는 것이다.
    - 단, ECMAScript6에서 도입된 let, const를 사용하면 블록 레벨 스코프를 사용할 수 있다.

  ```javascript
  var x = 1
  var foo = function(){
      var x = 2
      console.log(x)		// 2
  }
  foo()
  console.log(x)			// 1
  
  
  // let과 const를 사용
  var x = 0
  {
      var x = 1
      console.log(x)	// 1
  }
  console.log(x)		// 1
  
  let y = 0
  {
      let y = 1
      console.log(y)	// 1
  }
  console.log(y)		// 0
  
  const z = 0
  {
      const z = 1
      console.log(z)	// 1
  }
  console.log(z)		// 0
  ```



- 함수 레벨 스코프(Function-level-scope)

  - 비 블록 레벨 스코프(Non block-level-scope)
    - 아래와 같이 블록 레벨 스코프를 사용하지 않고 함수 블록 스코프를 사용한다.
    - 따라서 함수 밖에서 선언된 변수는 코드 블록 내에서 선언되었다 할지라도 모두 전역 스코프를 갖게 된다.

  ```javascript
  if (true){
      var x = 1
  }
  console.log(x)	// 1
  ```

  - 함수 내에서 선언된 매개변수와 변수는 함수 외부에서는 유효하지 않다.

  ```javascript
  var x = 'global'
  
  function foo() {
    var x = 'local'
    console.log(x)
  }
  
  foo()          // local
  console.log(x) // global
  ```

  - 함수 외부에서 선언된 변수는 함수 내부에서 유효하다.

  ```javascript
  // 외부에서 선언한 변수의 참조와 변경
  var x = 0
  
  function foo(){
      console.log(x)	// 0
      x = 10
  }
  foo()
  console.log(x)		// 10
  ```

  - 내부함수는 자신을 포함하고 있는 외부함수의 변수에 접근하고 변경 수 있다.

  ```javascript
  // 내부 함수
  function foo() {
    var x = 0
    function bar() {
      console.log(x)	// 0
      x = 10
      console.log(x)	// 10
    }
    bar()
    console.log(x)	// 10
  }
  
  foo()
  ```

  - 중첩된 스코프는 가장 인접한 지역을 우선하여 참조한다.

  ```javascript
  var x = 0
  function foo(){
      var x = 10
      function bar(){
          var x = 20
          function fao(){
              console.log(x)	// 20
          }
          fao()
      }
      bar()
  }
  
  foo()
  ```

  - 재선언과 재할당은 다르다.

  ```javascript
  var x = 10
  
  function foo(){
    var x = 100
    console.log(x)	// 100
  
    function bar(){
      x = 1000
      console.log(x)	// 1000
    }
  
    bar()
  }
  foo()
  console.log(x)		// 10
  ```



- 전역 스코프

  - 전역에 변수를 선언하면 이 변수는 어디서든지 참조할 수 있는 전역 스코프를 갖는 전역 변수가 된다.
  - var 키워드로 선언한 전역변수는 전역 객체 `window`의 프로퍼티다.
  - 전역 변수의 사용은 변수 이름이 중복될 수 있고, 의도치 않은 재할당에 의한 상태 변화로 코드를 예측하기 어렵게 만드므로 사용을 자제해야 한다.

  ```javascript
  var global = 'global'
  
  function foo() {
    var local = 'local'
    console.log(global)	// global
    console.log(local)	// local
  }
  foo()
  
  console.log(global)		// global
  console.log(local)		// local
  ```

  - 전역 변수 사용을 최소화 하는 방법 중 하나는 다음과 같이 전역 변수 객체를 만들어 사용하는 것이다.

  ```javascript
  var GLOBALVALUE = {}
  
  GLOBALVALUE.person = {
      name:'Cha',
      age:28
  }
  
  GLOBALVALUE.value = 'globla'
  
  console.log(GLOBALVALUE.person.name)  // Cha
  console.log(GLOBALVALUE.value)		  // global
  ```

  - 다음과 같이 즉시 실행 함수를 사용하는 방법도 있다.
    - 이 방법을 사용하면 전역변수를 만들지 않으므로 라이브러리 등에 자주 사용된다.
    - 즉시 실행되고 그 후 전역에서 바로 사라진다.

  ```javascript
  (function () {
    	var GLOBALVALUE = {}
  
      GLOBALVALUE.person = {
          name:'Cha',
          age:28
      }
      GLOBALVALUE.value = 'globla'
  
      console.log(GLOBALVALUE.person.name)  // Cha
      console.log(GLOBALVALUE.value)		  // global
  }());
  
  console.log(GLOBALVALUE.person.name)  // ReferenceError: GLOBALVALUE is not defined
  console.log(GLOBALVALUE.value)		  // ReferenceError: GLOBALVALUE is not defined
  ```

  

- 렉시컬 스코프

  - 상위 스코프 결정 방식에는 두 가지가 있다.
    - 동적 스코프: 함수를 어디서 호출하였는지에 따라 상위 스코프를 결정하는 방식
    - 렉시컬 스코프: 함수를 어디서 선언하였는지에 따라 상위 스코프를 결정하는 방식
  - 자바스크립트를 비롯한 대부분의 프로그래밍 언어는 렉시컬 스코프를 따른다.
  - 따라서 함수를 선언한 시점에 상위 스코프가 결정된다.
    - 아래 예에서 `bar()`는 전역에 선언되었고 상위 스코프는 전역 스코프이다.
    - 따라서 아래 예제는 1을 2번 출력한다. 
  - 함수를 어디서 호출하였는지는 스코프 결정에 아무런 의미를 주지 않는다.

  ```javascript
  var x = 1
  
  function foo() {
    var x = 10
    bar()
  }
  
  function bar() {
    console.log(x)
  }
  
  foo()   // 1
  bar()   // 1
  ```



- 암묵적 전역

  - 선언하지 않은 식별자에 값을 할당했을 때 해당 식별자가 전역 변수처럼 동작하는 것.
  - 전역변수처럼 동작하게 되는 과정
    - 아래 예시에서 `foo()` 함수가 호출되면 JS 엔진은 변수x를 찾아야 변수 x에 값을 할당할 수 있기에 먼저 변수 x가 어디서 선언되었는지 스코프 체인으로 검색하기 시작한다.
    - JS엔진은 먼저 `foo()`함수의 스코프에서 x의 선언을 검색한다. `foo()` 함수의 스코프에는 x의 선언이 없으므로 검색에 실패한다.
    - JS엔진은 다음으로 foo 함수 컨텍스트의 상위 스코프(아래 예제의 경우, 전역 스코프)에서 변수 x의 선언을 검색한다. 전역 스코프에도 변수 x의 선언이 존재하지 않기 때문에 검색에 실패한다.
    - `foo()` 함수의 스코프와 전역 스코프 어디에서도 변수 x의 선언을 찾을 수 없으므로  ReferenceError가 발생할 것 같지만 JS 엔진은 `x=20`을 `window.x=20`으로 해석하여 프로퍼티를 동적 생성한다.
    - 결국 x는 전역 객체(`window`)의 프로퍼티가 되어 마치 전역 변수처럼 동작한다.
  - 하지만 이 경우 변수 선언 없이 단지 전역 객체의 프로퍼티로 추가되었을 뿐이므로 진짜 변수가 된 것은 아니다.
    - 따라서 호이스팅이 발생하지 않는다.
    - 또한 변수가 아니라 단순히 프로퍼티이므로 delete 연산자로 삭제할 수 있다.
    - 본래 전역 변수는 프로퍼티이지만 변수이므로 delete 연산자로 삭제할 수 없다.

  ```javascript
  function foo(){
      x = 20
      // 에러가 발생하지 않을 뿐 아니라
      console.log(x)	// 20
  }
  foo()
  //전역 변수처럼 동작한다.
  console.log(x)		// 20
  
  
  //호이스팅이 발생하지는 않는다.
  console.log(y)		// ReferenceError: y is not defined
  
  function bar(){
      y = 20
      console.log(y)
  }
  bar()
  console.log(y)
  
  
  
  // delete를 통핸 삭제
  var a = 10
  function tmp(){
      b = 20
  }
  
  tmp()
  
  console.log(window.a)	// 10
  console.log(window.b)	// 20
  
  delete a
  delete b
  
  console.log(window.a)	// 10
  console.log(window.b)	// undefined
  ```

  



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

  
