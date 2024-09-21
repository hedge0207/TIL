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

  - 클래스로 선언한 객체도 마찬가지로 해당 객체에 바인딩 된다.
  
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




## let, const와 블록 레벨 스코프

- `var`
  - ES5까지 변수를 선언할 수 있는 유일한 방법은 `var` 키워드를 사용하는 것이었다. 
  - `var` 키워드로 선언된 변수는 아래와 같은 특징이 있다. 이는 다른 언어와는 다른 특징으로 주의를 기울이지 않으면 심각한 문제를 일으킨다.
  - 함수 레벨 스코프
    - 함수의 코드 블록만을 스코프로 인정한다. 따라서 전역 함수 외부에서 생성한 변수는 모두 전역 변수이다. 이는 전역 변수를 남발할 가능성을 높인다.
    - for 문의 변수 선언문에서 선언한 변수를 for 문의 코드 블록 외부에서 참조할 수 있다.
  - `var` 키워드 생략 허용
    - 전역에서 `var` 키워드를 생략했을 때는 별 문제가 되지 않지만 지역에서 생략하면 문제가 된다.
    - 암묵적 전역 변수를 양산할 가능성이 크다.
  - 변수 중복 선언 허용
    - 의도하지 않은 변수값의 변경이 일어날 가능성이 크다.
  - 변수 호이스팅
    - 변수를 선언하기 이전에 참조할 수 있다.
  - ES6는 이러한 `var` 키워드의 단점을 보완하기 위해 `let`과 `const` 키워드를 도입하였다.



### let

- 블록 레벨 스코프

  - 블록 레벨 스코프를 따르지 않는 var 키워드의 특성 상, 코드 블록 내의 변수는 전역 변수이다. 
  - 그런데 이미 전역 변수 foo가 선언되어 있다. `var` 키워드를 사용하여 선언한 변수는 중복 선언이 허용되므로 아래 코드는 문법적으로 아무런 문제가 없다. 
  - 단, 코드 블록 내의 변수 foo는 전역 변수이기 때문에 전역에서 선언된 전역 변수 foo의 값 123을 새로운 값 456으로 재할당하여 덮어쓴다.

  ```javascript
  var foo = 123 // 전역 변수
  
  console.log(foo) // 123
  
  {
    var foo = 456 // 전역 변수
  }
  
  console.log(foo) // 456
  ```

  - ES6는 **블록 레벨 스코프**를 따르는 변수를 선언하기 위해 `let` 키워드를 제공한다.

  ```javascript
  let foo = 123 // 전역 변수
  
  {
    let foo = 456 // 지역 변수
    let bar = 456 // 지역 변수
  }
  
  console.log(foo) // 123
  console.log(bar) // ReferenceError: bar is not defined
  ```

  

- 변수 중복 선언 금지

  - var 키워드로는 동일한 이름을 갖는 변수를 중복해서 선언할 수 있다. 
  - 하지만, let 키워드로는 동일한 이름을 갖는 변수를 중복해서 선언할 수 없다. 
  - 변수를 중복 선언하면 문법 에러(SyntaxError)가 발생한다.

  ```javascript
  var foo = 123
  var foo = 456  // 중복 선언 허용
  
  let bar = 123
  let bar = 456  // Uncaught SyntaxError: Identifier 'bar' has already been declared
  ```



- 호이스팅

  - 자바스크립트는 ES6에서 도입된 `let`, `const`를 포함하여 모든 선언(`var`, `let`, `const`, `function`, `function*`)을 호이스팅한다. 
  - 호이스팅(Hoisting)이란, `var` 선언문이나 `function` 선언문 등을 해당 스코프의 선두로 옮긴 것처럼 동작하는 특성을 말한다.
  - 하지만 var 키워드로 선언된 변수와는 달리 let 키워드로 선언된 변수를 선언문 이전에 참조하면 참조 에러(ReferenceError)가 발생한다. 

  ```javascript
  console.log(foo) // undefined
  var foo
  
  console.log(bar) // Error: Uncaught ReferenceError: bar is not defined
  let bar
  ```

  - 이는 let 키워드로 선언된 변수는 스코프의 시작에서 변수의 선언까지 **일시적 사각지대(Temporal Dead Zone; TDZ)**에 빠지기 때문이다.
    - let 키워드로 선언된 변수는 선언 단계와 초기화 단계가 분리되어 진행된다.
    - 즉, 스코프에 변수를 등록(선언단계)하지만 초기화 단계는 변수 선언문에 도달했을 때 이루어진다. 
    - 초기화 이전에 변수에 접근하려고 하면 참조 에러(ReferenceError)가 발생한다. 
    - 이는 변수가 아직 초기화되지 않았기 때문이다. 
    - 다시 말하면 변수를 위한 메모리 공간이 아직 확보되지 않았기 때문이다. 
    - 따라서 스코프의 시작 지점부터 초기화 시작 지점까지는 변수를 참조할 수 없다. 
    - 스코프의 시작 지점부터 초기화 시작 지점까지의 구간을 일시적 사각지대(Temporal Dead Zone; TDZ)라고 부른다.

  ```javascript
  // 스코프의 선두에서 선언 단계가 실행된다.
  // 아직 변수가 초기화(메모리 공간 확보와 undefined로 초기화)되지 않았다.
  // 따라서 변수 선언문 이전에 변수를 참조할 수 없다.
  console.log(foo) // ReferenceError: foo is not defined
  
  let foo // 변수 선언문에서 초기화 단계가 실행된다.
  console.log(foo) // undefined
  
  foo = 1 // 할당문에서 할당 단계가 실행된다.
  console.log(foo) // 1
  ```

  - 지역변수의 경우
    - let으로 선언된 변수는 블록 레벨 스코프를 가지므로 코드 블록 내에서 선언된 변수 foo는 지역 변수이다. 
    - 따라서 지역 변수 foo도 해당 스코프에서 호이스팅되고 코드 블록의 선두부터 초기화가 이루어지는 지점까지 일시적 사각지대(TDZ)에 빠진다. 
    - 따라서 전역 변수 foo의 값이 출력되지 않고 참조 에러(ReferenceError)가 발생한다.

  ```javascript
  let foo = 1 // 전역 변수
  
  {
    console.log(foo) // ReferenceError: foo is not defined
    let foo = 2 // 지역 변수
  }
  ```



- 클로저

  - `var` 키워드를 사용할 경우 아래의 코드는 예상과 다르게 동작할 것이다.
    - 위 코드의 실행 결과로 0, 1, 2를 기대할 수도 있지만 결과는 3이 세 번 출력된다. 
    - 그 이유는 for 루프의 var i가 전역 변수이기 때문이다.

  ```javascript
  var funcs = []
  
  // 함수의 배열을 생성하는 for 루프의 i는 전역 변수다.
  for (var i = 0; i < 3; i++) {
    funcs.push(function () { console.log(i) })
  }
  
  // 배열에서 함수를 꺼내어 호출한다.
  for (var j = 0; j < 3; j++) {
    funcs[j]()
  }
  ```

  - `let`을 사용하여 아래와 같이 수정 가능하다.

  ```javascript
  var arr = []
  
  // 함수의 배열을 생성하는 for 루프의 i는 for 루프의 코드 블록에서만 유효한 지역 변수이면서 자유 변수이다.
  for (let i = 0; i < 3; i++) {
    arr.push(function () { console.log(i) })
  }
  
  // 배열에서 함수를 꺼내어 호출한다
  for (var j = 0; j < 3; j++) {
    console.dir(arr[j])
    arr[j]()
  }
  ```

  

- 전역 객체와 let

  - var 키워드로 선언된 변수를 전역 변수로 사용하면 전역 객체의 프로퍼티가 된다.

  ```javascript
  var foo = 123 // 전역변수
  
  console.log(window.foo) // 123
  ```

  - let 키워드로 선언된 변수를 전역 변수로 사용하는 경우, let 전역 변수는 전역 객체의 프로퍼티가 아니다. 
    - 즉, `window.foo`와 같이 접근할 수 없다. 
    - let 전역 변수는 보이지 않는 개념적인 블록 내에 존재하게 된다.

  ```javascript
  let foo = 123 // 전역변수
  
  console.log(window.foo) // undefined
  ```





### const

- `const`
  - `const`는 상수(변하지 않는 값)를 위해 사용한다. 
  - 하지만 반드시 상수만을 위해 사용하지는 않는다.



- 선언과 초기화

  - `let`은 재할당이 자유로우나 `const`는 재할당이 금지된다.

  ```javascript
  const FOO = 123
  FOO = 456 // TypeError: Assignment to constant variable.
  ```

  - `const`는 반드시 선언과 동시에 할당이 이루어져야 한다.
    - 그렇지 않으면 다음처럼 문법 에러(SyntaxError)가 발생한다.

  ```javascript
  const FOO // SyntaxError: Missing initializer in const declaration
  ```

  - `const`는 `let`과 마찬가지로 블록 레벨 스코프를 갖는다.

  ```javascript
  {
    const FOO = 10
    console.log(FOO) //10
  }
  console.log(FOO) // ReferenceError: FOO is not defined
  ```

  

- 상수
  - 상수는 가독성과 유지보수의 편의를 위해 적극적으로 사용해야 한다.
  - 네이밍이 적절한 상수로 선언하면 가독성과 유지보수성이 대폭 향상된다.



- `const`와 객체

  - const는 재할당이 금지된다. 
  - 이는 const 변수의 타입이 객체인 경우, 객체에 대한 참조를 변경하지 못한다는 것을 의미한다. 
  - 하지만 이때 객체의 프로퍼티는 보호되지 않는다. 
  - 다시 말하자면 재할당은 불가능하지만 할당된 객체의 내용(프로퍼티의 추가, 삭제, 프로퍼티 값의 변경)은 변경할 수 있다.
  - 객체의 내용이 변경되더라도 객체 타입 변수에 할당된 주소값은 변경되지 않는다. 
    - 따라서 객체 타입 변수 선언에는 const를 사용하는 것이 좋다.
    - 만약에 명시적으로 객체 타입 변수의 주소값을 변경(재할당)하여야 한다면 let을 사용한다.

  ```javascript
  const user = { name: 'Cha' }
  
  // 객체의 내용은 변경할 수 있다.
  user.name = 'Kim'
  
  console.log(user) // { name: 'Kim' }
  ```

  

- `var`, `let`, `const`
  - 변수 선언에는 기본적으로 `const`를 사용하고 `let`은 재할당이 필요한 경우에 한정해 사용하는 것이 좋다. 
  - 원시 값의 경우, 가급적 상수를 사용하는 편이 좋다. 
  - 그리고 객체를 재할당하는 경우는 생각보다 흔하지 않다.
  -  `const` 키워드를 사용하면 의도치 않은 재할당을 방지해 주기 때문에 보다 안전하다.
  - `var`, `let`, 그리고 `const`는 다음처럼 사용하는 것을 추천한다.
    - ES6를 사용한다면 `var` 키워드는 사용하지 않는다.
    - 재할당이 필요한 경우에 한정해 `let` 키워드를 사용한다. 이때 변수의 스코프는 최대한 좁게 만든다.
    - 변경이 발생하지 않는(재할당이 필요 없는 상수) 원시 값과 객체에는 `const` 키워드를 사용한다. `const` 키워드는 재할당을 금지하므로 `var`, `let` 보다 안전하다.







# 실행 컨텍스트와 JavaScript 동작 원리

> https://poiemaweb.com/js-execution-context 참고

- 실행 컨텍스트(Execution Context)

  - 실행 가능한 코드를 형상화하고 구분하는 추상적인 개념.
  - 아래와 같이 실행 가능한 코드가 되기 위해 필요한 환경이라고 할 수 있다.
    - 전역 코드: 전역 영역에 존재하는 코드
    - Eval 코드: eval 함수로 실행되는 코드
    - 함수 코드: 함수 내에 존재하는 코드
  - 스코프, 호이스팅, this, functiom, 클로져 등의 동작 원리를 담고 있는 JS의 핵심원리이다.
  - JS 엔진은 코드를 실행하기 위하여 실행에 필요한 여러가지 정보를 알고 있어야 한다.
    - 변수: 전역, 지역, 매개 변수, 객체의 프로퍼티
    - 함수 선언
    - 스코프
    - this
  - 이와 같이 실행에 필요한 정보를 형상화하고 구분하기 위해 JavaScript 엔진은 실행 컨텍스트를 물리적 객체의 형태로 관리한다.
    - 아래 코드를 실행하면 실행 컨텍스트 스택이 생성하고 소멸한다.
    - 현재 실행중인 실행 컨텍스트에서 이 실행 컨텍스트와 관련 없는 코드(예를 들면 함수)가 실행되면 새로운 실행 컨텍스트가 생성된다.
    - 이 실행 컨텍스트는 스택에 쌓이게 되고 컨트롤(제어권)이 이동한다.
    - 새롭게 쌓인 실행 컨텍스트의 실행이 끝나면 해당 실행 컨텍스트를 파기하고 직전의 실행 컨텍스트에 컨트롤을 반환한다.

  ```javascript
  var x = 'x'						// 1.{global EC}
  
  function foo () {
    var y = 'y'
  
    function bar () {
      var z = 'z'
      console.log(x + y + z)
    }
    bar()							// 3.{global EC, foo() EC, bar() EC}
    //bar() 실행 종료(4.{global EC, foo() EC})
  }
  foo()							// 2.{global EC, foo() EC}
  // foo()실행 종료(5.{global EC})
  // 전역 실행 종료(6.{})
  ```



## 실행 컨텍스트의 3가지 객체

- 실행 컨텍스트는 실행 가능한 코드를 형상화하고 구분하는 추상적인 개념이지만 물리적으로는 객체의 형태를 가지며, 아래 3가지 프로퍼티를 소유한다.



- Variable Object(VO, 변수객체)
  - 실행 컨텍스트가 생성되면 JS 엔진은 실행에 필요한 여러 정보들을 담을 객체를 생성한다. 이를 VO라 한다.
  - Variable Object는 코드가 실행될 때 엔진에 의해 참조되며 코드에서는 접근할 수 없다.
  - Variable Object는 아래의 정보를 담는 객체이다.
    - 변수
    - 매개변수와 인수 정보
    - 함수 선언(함수 표현식은 제외)
  - Variable Object는 실행 컨텍스트의 프로퍼티이기 때문에 값을 갖는데 이 값은 다른 객체를 가리킨다.
  - 그런데 전역 코드 실행시 생성되는 전역 컨텍스트의 경우와 함수를 실행할 때 생성되는 함수 컨텍스트의 경우, 가리키는 객체가 다르다.
  - 이는 전역 코드와 함수의 내용이 다르기 때문이다. 예를 들어 전역 코드에는 매개변수가 없지만 함수에는 매개변수가 있다.
  - Variable Object가 가리키는 객체는 아래와 같다.
    - 전역 컨텍스트의 경우: Variable Object는 유일하며 최상위에 위치하고 모든 전역 변수, 전역 함수 등을 포함하는 전역 객체(Global Object, GO, window)를 가리킨다. 전역  객체는 전역에 선언된 전역 변수와 전역 함수를 프로퍼티로 소유한다.
    - 함수 컨텍스트의 경우: Variable Object는 활성 객체(Actibation Object, AO)를 가리키며, 내부 함수와 지역 변수, 그리고 매개변수와 인수들의 정보를 배열의 형태로 담고 있는 객체인 `arguments object`를 프로퍼티로 갖는다.



- Scope Chain
  - 전역 객체와 중첩된 함수의 스코프의 레퍼런스를 차례로 저장하고 있는 일종의 리스트이다.
    - 다시 말해, 스코프 체인은 해당 전역 또는 함수가 참조할 수 있는 변수, 함수 선언 등의 정보를 담고 있는 전역 객체(GO) 또는 활성 객체(AO)의 리스트를 가리킨다.
    - 현재 실행 컨텍스트의 활성 객체(AO)를 선두로 하여 순차적으로 상위 컨텍스트의 활성 객체(AO)를 가리키며 마지막 리스트는 전역 객체(GO)를 가리킨다.
  - 스코프 체인은 식별자 중에서 객체(전역 객체 제외)가 아닌 식별자, 즉 변수를 검색하는 매커니즘이다.
    - 식별자 중에서 변수가 아닌 객체의 프로퍼티(메소드 포함)를 검색하는 메커니즘은 프로토타입 체인이다.
  - 엔진은 스코프 체인을 통해 렉시컬 스코프를 파악한다.
  - 함수가 중첩 상태일 때 하위 함수 내에서 상위 함수의 스코프와 전역 스코프까지 참조할 수 있는데 이것은 스코프 체인을 통해 가능하다.
    - 함수가 중첩되어 있으면 중첩될 때마다 부모 함수의 Scope가 자식 함수의 스코프 체인에 포함된다. 
    - 함수 실행중에 변수를 만나면 그 변수를 우선 현재 Scope, 즉 Activation Object에서 검색해보고, 만약 검색에 실패하면 스코프 체인에 담겨진 순서대로 그 검색을 이어가게 되는 것이다. 이것이 스코프 체인이라고 불리는 이유이다.
  - 스코프 체인은 함수의 감추어진 프로퍼티인 `[[Scope]]`로 참조할 수 있다.



- this value
  - this 프로퍼티에는 this 값이 할당된다. this에 할당되는 값은 함수 호출 패턴에 의해 결정된다.





## 실행 컨텍스트의 생성 과정

### 전역 코드로 진입

- 개요

  - 컨트롤이 실행 컨텍스트에 진입하기 이전에 유일한 전역 객체(Global Object, GO)가 생성된다. 

  - 전역 객체는 단일 사본으로 존재하며 이 객체의 프로퍼티는 코드의 어떤 곳에서도 접근할 수 있다.
  - 초기 상태의 전역 객체에는 빌트인 객체(Math, String, Array 등)와 BOM, DOM이 설정되어 있다.

  - 전역 객체가 생성된 이후, 전역 코드로 컨트롤이 진입하면 전역 실행 컨텍스트가 생성되고 실행 컨텍스트에 스택이 쌓인다.

  ```javascript
  /* 
  ------------진입 이전-------------
  전역 객체(window) 생성
  window에는 빌트인 객체와 BOM, DOM등이 설정되어 있다.
  ------------진입 이후-------------
  빈 실행 컨텍스트 스택 생성	{}
  전역 컨텍스트 생성 후 실행 컨텍스트 스택에 추가 { globalEC:{VO:None,SC:None,this:None}}
  이는 이해를 위한 예시일 뿐 실제로 위와 같이 오브젝트가 생성 되는 것은 아니다.
  */
  
  var x = 'x'
  
  function foo () {
    var y = 'y'
  
    function bar () {
      var z = 'z'
      console.log(x + y + z)
    }
    bar()
  }
  foo()
  ```

  - 그리고 이 샐행 컨텍스트를 바탕으로 아래의 처리가 실행된다.
    - 스코프 체인의 생성과 초기화
    - Variable Instantiation(변수 객체화) 실행
    - this value 결정



- 스코프 체인의 생성과 초기화

  - 전역 실행 컨텍스트가 생성된 이후 가장 먼저 스코프 체인의 생성과 초기화가 실행된다. 

  - 이때 스코프 체인은 전역 객체의 레퍼런스를 포함하는 리스트가 된다.

  - 즉 스코프 체인 리스트를 통해 전역 객체에 접근 가능해진다.

    

- 변수 객체화 실행

  - 스코프 체인의 생성과 초기화가 완료되면 변수 객체화가 실행된다.
  - 변수 객체화는 Variable Object에 프로퍼티와 값을 추가하는 것을 의미한다.
  - 전역 코드의 경우, Variable Object는 Global Object를 가리킨다.
  - 변수 객체화 진행 순서
    - (함수 코드인 경우) 매개변수가 Variable Object의 프로퍼티의 키로, 인수가 값으로 설정된다.
    - 대상 코드 내의 함수 선언(함수 표현식 제외)을 대상으로 함수명이 Variable Object의 프로퍼티의 키로, 생성된 함수 객체가 값으로 설정된다(함수 호이스팅).
    - 대상 코드 내의 변수 선언을 대상으로 하여 변수명이 Variable Object의 프로퍼티의 키로, undefined가 값으로 설정된다(변수 호이스팅).

  ```javascript
  // 아래 예시에서 전역 코드에 변수 x와 함수 foo가 선언되었다. 따라서 다음의 순서를 거치게 된다.
  // 함수 코드가 아니라 전역 코드이므로 1번은 실행되지 않는다.
  // 대상 코드 내의 함수 선언인 foo가 먼저 Variale Object의 프로퍼티 키로 함수명인 foo가, 값으로 foo 객체가 들어가게 된다.
  // 대상 코드 내의 변수 선언인 x가 Variale Object의 프로퍼티 키로 변수명인 x가, 값으로 undefined가 들어가게 된다.
  var x = 'x'
  
  function foo () {
    var y = 'y'
  
    function bar () {
      var z = 'z'
      console.log(x + y + z)
    }
    bar()
  }
  foo()
  ```

  - 함수의 선언 처리
    - 생성된 함수 객체는 `[[Scope]]` 프로퍼티를 가지게 된다.
    - `[[Scope]]` 프로퍼티는 함수 객체만이 소유하는 내부 프로퍼티(Internal Property)로서 함수 객체가 실행되는 환경을 가리킨다.
    - 따라서 현재 실행 컨텍스트의 스코프 체인이 참조하고 있는 객체를 값으로 설정한다.
    - 함수 내부의 `[[Scope]]` 프로퍼티는 자신의 실행 환경과 자신을 포함하는 외부 함수의 실행환경과 전역객체를 가리킨다.
    - 이때 자신을 포함하는 외부 함수의 실행 컨텍스트가 소멸하여도 `[[Scope]]` 프로퍼티가 가리키는 외부 함수의 실행 환경은 소멸하지 않고 참조할 수 있다. 이것이 **클로저**이다.
    - 지금까지 살펴본 실행 컨텍스트는 아직 코드가 실행되기 이전이다. 
    - 하지만 스코프 체인이 가리키는 변수 객체(VO)에 이미 함수가 등록되어 있으므로 이후 코드를 실행할 때 함수선언식 이전에 함수를 호출할 수 있게 되었다.
    - 이때 알 수 있는 것은 함수선언식의 경우, 변수 객체(VO)에 함수표현식과 동일하게 함수명을 프로퍼티로 함수 객체를 할당한다는 것이다.
    - 단, 함수선언식은 변수 객체(VO)에 함수명을 프로퍼티로 추가하고 즉시 함수 객체를 즉시 할당하지만 **함수 표현식은 일반 변수의 방식을 따른다**.
    - 따라서 함수선언식의 경우, 선언문 이전에 함수를 호출할 수 있다. 이러한 현상을 **함수 호이스팅**이라 한다.

  - 변수의 선언 처리
    - 선언 단계: 변수 객체(Variable Object)에 변수를 등록, 이 변수 객체는 스코프가 참조할 수 있는 대상이 된다.
    - 초기화 단계: 변수 객체(Variable Object)에 등록된 변수를 메모리에 할당한다. 이 단계에서 변수는 undefined로 초기화된다.
    - 할당 단계: undefined로 초기화된 변수에 실제값을 할당한다.
    - var 키워드로 선언된 변수는 선언 단계와 초기화 단계가 한번에 이루어진다.
    - 다시 말해 스코프 체인이 가리키는 변수 객체에 변수가 등록되고 변수는 undefined로 초기화된다. 
    - 따라서 변수 선언문 이전에 변수에 접근하여도 Variable Object에 변수가 존재하기 때문에 에러가 발생하지 않는다. 다만 undefined를 반환한다. 
    - 이러한 현상을 **변수 호이스팅**이라 한다.
    - 위 예시는 초기화 단계까지 진행된 것이다. 변수 할당문에 도달하면 비로소 값의 할당이 이루어진다.



- this value 결정
  - 변수 선언 처리가 끝나면 다음은 this value가 결정된다.
  - this value가 결정되기 이전에 this는 전역 객체를 가리키고 있다가 함수 호출 패턴에 의해 this에 할당되는 값이 결정된다.
  - 전역 코드의 경우, this는 전역 객체를 가리킨다.
  - 전역 컨텍스트(전역 코드)의 경우 Variable Object, 스코프 체인, this 값은 언제나 전역 객체이다.



### 전역 코드의 실행

- 이전까지는 코드 실행 환경을 갖추기 위한 사전 준비였다. 코드의 실행은 지금부터 시작된다.
  - 전역 변수에 값이 할당된다. 
  - 전역 함수의 호출이 일어난다.



- 변수 값의 할당
  - 전역 변수에 값을 할당할 때, 현재 실행 컨텍스트의 스코프 체인이 참조하고 있는  Variable Object를 선두(0번 인덱스)부터 검색을 시작한다.
  - 변수명에 해당하는 프로퍼티가 발견되면 값을 할당한다.



- 함수의 호출

  - 전역 코드의 함수가 실행되기 시작하면 실행 컨텍스트 스택에 새로운 함수 실행 컨택스트가 생성된다.

  - 함수의 실행 컨텍스트로 컨트롤이 이동하면 전역 코드와 마찬가지로 스코프 체인의 생성과 초기화, Variable Instantiation 실행, this value 결정이 순차적으로 실행된다.

  - 단, 전역 코드와 다른 점은 이번 실행되는 코드는 함수 코드라는 것이다. 따라서 위 세 과정은 전역 코드의 룰이 아닌 함수 코드의 룰이 적용된다.

  - 스코프 체인의 생성과 초기화

    - 함수 코드의 스코프 체인의 생성과 초기화는 Activation Object에 대한 레퍼런스를 스코프 체인의 선두에 설정하는 것으로 시작된다.
    - Activation Object는 우선 arguments 프로퍼티의 초기화를 실행하고 그 후, Variable Instantiation가 실행된다. 
    - Activation Object는 스펙 상의 개념으로 프로그램이 Activation Object에 직접 접근할 수 없다(Activation Object의 프로퍼티로의 접근은 가능하다).
    - 그 후, Caller(전역 컨텍스트)의 Scope Chain이 참조하고 있는 객체가 스코프 체인에 push된다.
    - 따라서, 이 경우 함수를 실행한 직후 실행 컨텍스트의 스코프 체인은 Activation Object(함수의 실행으로 만들어진 AO)과 전역 객체를 순차적으로 참조하게 된다.

  - 변수 객체화 실행

    - 함수 코드의 경우, 스코프 체인의 생성과 초기화에서 생성된 AO를 Variable Object로서 변수 객체화가 실행된다.
    - 이것을 제외하면 전역 코드의 경우와 같은 처리가 실행된다.
    - 즉, 함수 객체를 Variable Object(AO)에 바인딩한다.
    - 프로퍼티키는 내부함수명, 값은 새로 생성된 내부함수객체. 
    - 새로 생성된 내부함수객체의 [[Scope]] 프로퍼티 값은 AO와 Global Object를 참조하는 리스트이다.
    - 지역 변수를 Variable Object(AO)에 설정한다. 프로퍼티 키는 변수명, 값은 undefined.

  - this value 결정

    - 변수 선언 처리가 끝나면 다음은 this value가 결정된다. this에 할당되는 값은 함수 호출 패턴에 의해 결정된다.
    - 내부 함수의 경우, this의 value는 전역 객체이다.

    

- 내부 함수 코드의 실행

  - 실행 컨텍스트 스택에 새로운 실행 컨텍스트 생성
  - 이후는 위에서 살펴본 함수의 호출에서의 스코프 체인의 생성과 초기화, 변수 객체화 실행, this value 결정이 순차적으로 일어난다.







# 클로저

- 클로저(closure)의 개념

  - 사전지식
    - JavaScript에선 함수를 호출할 때가 아니라 함수를 어디에 선언하였는지에 따라 스코프가 결정되는데 이를 **렉시컬 스코핑**이라 한다.
    - 아래 예시에서 `inner()`가 `outer()`의 내부에 선언된 내부함수이므로 `inner()`는 자신이 속한 렉시컬 스코프(`outer()`)를 참조할 수 있다.

  ```javascript
  function outer(){
      var x = 1
      var inner = function(){
          console.log(x)
      }
      inner()
  }
  
  outer()
  ```

  - 실행 컨텍스트의 관점에서 보면 다음과 같다.
    - 내부함수 `inner()`가 호출되면 자신의 실행 컨텍스트가 실행 컨텍스트 스택에 쌓이고 변수 객체와 스코프 체인, this에 바인딩될 객체가 결정된다.
    - 이때 스코프 체인은 전역 스코프를 가리키는 전역 객체와 함수 `outer()`의 스코프를 가리키는 함수 `outer()`의 활성 객체(Activation object) 그리고 함수 자신의 스코프를 가리키는 활성 객체를 순차적으로 바인딩한다. 
    - 스코프 체인이 바인딩한 객체가 바로 렉시컬 스코프의 실체이다.
    - 내부함수 `inner()`가 자신을 포함하고 있는 외부함수 `outer()`의 변수 x에 접근할 수 있는 것, 다시 말해 상위 스코프에 접근할 수 있는 것은 렉시컬 스코프의 레퍼런스를 차례대로 저장하고 있는 실행 컨텍스트의 스코프 체인을 자바스크립트 엔진이 검색하였기에 가능한 것이다. 
    - 즉, 최초에 `inner()`함수 스코프(함수 자신의 스코프를 가리키는 활성 객체) 내에서 변수 x를 검색한다. x가 존재하지 않으므로 검색은 실패한다.
    - 다음으로 `inner()`함수를 포함하는 외부 함수 `outer()`의 스코프(함수 outerFunc의 스코프를 가리키는 함수 outerFunc의 활성 객체)에서 변수 x를 검색한다.  x가 존재하므로 검색이 성공한다.
  - 내부 함수를 외부 함수 내에서 호출하는 것이 아니라 반환하도록 변경하면 다음과 같다.
    - 아래의 경우 `outer()`는 `inner()`를 반환하고 생을 마감한다. 
    - 즉 실행 컨텍스트 스택(콜스택)에서 제거되었으므로 함수 `outer()`의 변수 x에 접근할 방법은 없어 보인다.
    - 그러나 코드를 실행하면 1을 출력한다.
    - 이처럼 자신을 포함하고 있는 외부함수보다 내부함수가 더 오래 유지되는 경우, 외부 함수 밖에서 내부 함수가 호출되더라도, 외부 함수의 지역 변수에 접근할 수 있는데 이러한 함수를 클로저라 부른다.

  ```javascript
  function outer(){
      var x = 1
      var inner = function(){
          console.log(x)
      }
      return inner
  }
  var innerFunc = outer()
  innerFunc()
  ```

  - 정의: (내부)함수와 그 함수가 선언됐을 때의 렉시컬 환경(내부 함수가 선언됐을 때의 스코프)과의 조합.
    - 자신을 포함하고 있는 외부함수보다 내부함수가 더 오래 유지되는 경우, 외부 함수 밖에서 내부 함수가 호출되더라도, 외부 함수의 지역 변수에 접근할 수 있는데 이러한 함수를 클로저라 부른다.
    - 즉, 클로저는 반환된 내부함수가 자신이 선언됐을 때의 환경(Lexical environment)인 스코프를 기억하여 자신이 선언됐을 때의 환경(스코프) 밖에서 호출되어도 그 환경(스코프)에 접근할 수 있는 함수를 말한다. 
    - 이를 조금 더 간단히 말하면 클로저는 자신이 생성될 때의 환경(Lexical environment)을 기억하는 함수라고 할 수 있다.
    - 클로저에 의해 참조되는 외부함수의 변수, 즉 `outer()`의 변수 x를 **자유변수(Free variable)**라고 부른다.
    - JavaScipt의 고유한 개념이 아니라 함수를 일급 객체로 취급하는 함수형 프로그래밍 언어에서 사용되는 중요한 특징이다.
  - 실행 컨텍스트의 관점에서 보면 다음과 같다.
    - 내부함수가 유효한 상태에서 외부함수가 종료하여 외부함수의 실행 컨텍스트가 반환되어도, 외부함수 실행 컨텍스트 내의 활성 객체는 내부함수에 의해 참조되는 한 유효하여 내부함수가 스코프 체인을 통해 참조할 수 있는 것을 의미한다.
    - 즉 외부함수가 이미 반환되었어도 외부함수 내의 변수는 이를 필요로 하는 내부함수가 하나 이상 존재하는 경우 계속 유지된다. 
    - 이때 내부함수가 외부함수에 있는 변수의 복사본이 아니라 실제 변수에 접근한다는 것에 주의하여야 한다.



## 클로저의 활용

- 클로저는 자신이 생성될 때의 환경(렉시컬 환경)을 기억해야하므로 메모리 차원에서 손해를 볼 수 있다.
  - 그러나 클로저는 JS의 강력한 기능이므로 이를 적극적으로 활용해야 한다.



- 상태 유지

  - 클로저가 가장 유용하게 사용되는 상황은 현재 상태를 기억하고 변경된 최신 상태를 유지하는 것이다.
    - 클로저는 현재 상태를 기억하고 이 상태가 변경되어도 최신 상태를 유지해야 하는 상황에 매우 유용하다. 
    - 만약 자바스크립트에 클로저라는 기능이 없다면 상태를 유지하기 위해 전역 변수를 사용할 수 밖에 없다. 전역 변수는 언제든지 누구나 접근할 수 있고 변경할 수 있기 때문에 많은 부작용을 유발해 오류의 원인이 되므로 사용을 자제해야 한다.
  - 예시
    - 클로저를 이벤트 핸들러로서 이벤트 프로퍼티에 할당한다.
    - 이벤트 프로퍼티에서 이벤트 핸들러인 클로저를 제거하지 않는 한 클로저가 기억하는 렉시컬 환경의 변수 isShow는 소멸하지 않는다. 다시 말해 현재 상태를 기억한다.
    - 버튼을 클릭하면 이벤트 프로퍼티에 할당한 이벤트 핸들러인 클로저가 호출된다. 
    - 이때 .box 요소의 표시 상태를 나타내는 변수 isShow의 값이 변경된다. 
    - 변수 isShow는 클로저에 의해 참조되고 있기 때문에 유효하며 자신의 변경된 최신 상태를 게속해서 유지한다.

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Document</title>
  </head>
  <body>
    <button id="toggle">toggle</button>
    <div id="box" style="width: 100px; height: 100px; background: red;"></div>
  
    <script>
      var box = document.querySelector('#box')
      var toggleBtn = document.querySelector('#toggle')
  	
      // 즉시 실행 함수 toggle
      var toggle = (function () {
        // box요소의 표시 상태를 나타내는 변수, 클로저를 통해 상태를 기억하고자 하는 변수.
        var isShow = false
  	  
        // 즉시 실행함수가 반환하는 함수
        // 자신이 생성됐을 때의 렉시컬 환경에 속한 변수 isShow를 기억할 수 있는 클로저다.
        return function () {
          box.style.display = isShow ? 'block' : 'none'
          isShow = !isShow
        };
      })();
  	
      // 이벤트 프로퍼티에 toggle함수의 반환값인 클로저를 할당
      toggleBtn.onclick = toggle
    </script>
  </body>
  </html>
  ```



- 전역 변수의 사용 억제

  - 변수의 값은 누군가에 의해 언제든지 변경될 수 있어 오류 발생의 근본적 원인이 될 수 있다. 
    - 상기했듯 전역 변수는 언제든지 누구나 접근할 수 있고 변경할 수 있기 때문에 많은 부작용을 유발해 오류의 원인이 되므로 사용을 자제해야 한다.
    - 상태 변경이나 가변(mutable) 데이터를 피하고 불변성(Immutability)을 지향하는 함수형 프로그래밍에서 부수 효과(Side effect)를 최대한 억제하여 오류를 피하고 프로그램의 안정성을 높이기 위해 클로저는 적극적으로 사용된다.
  - 전역 변수를 사용할 경우
    - 아래 코드는 잘 동작하지만 오류를 발생시킬 가능성을 내포하고 있는 코드다.
    - increase 함수는 호출되기 직전에 전역변수 counter의 값이 반드시 0이여야 제대로 동작한다. 
    - 하지만 변수 counter는 전역 변수이기 때문에 언제든지 누구나 접근할 수 있고 변경할 수 있다. 
    - 따라서 의도치 않게 값이 변경될 수도 있다. 
    - 만약 누군가에 의해 의도치 않게 전역 변수 counter의 값이 변경됐다면 오류가 발생할 것이다.
    - 변수 counter는 카운터를 관리하는 increase 함수가 관리하는 것이 바람직하다.

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Document</title>
  </head>
  <body>
      <p>전역 변수를 사용한 Counting</p>
      <button id="inclease">+</button>
      <p id="count">0</p>
      <script>
          var incleaseBtn = document.getElementById('inclease')
          var count = document.getElementById('count')
  
          // 카운트 상태를 유지하기 위한 전역 변수
          var counter = 0
  
          function increase() {
              return ++counter
          }
  
          incleaseBtn.onclick = function () {
              count.innerHTML = increase()
          };
      </script>
  </body>
  </html>
  ```

  - 지역 변수를 사용할 경우
    - 전역변수를 지역변수로 변경하여 의도치 않은 상태 변경은 방지했다. 
    - 하지만 increase 함수가 호출될 때마다 지역변수 counter를 0으로 초기화하기 때문에 언제나 1이 표시된다. 
    - 즉 변경된 이전 상태를 기억하지 못한다.

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Document</title>
  </head>
  <body>
      <p>지역 변수를 사용한 Counting</p>
      <button id="inclease">+</button>
      <p id="count">0</p>
      <script>
          var incleaseBtn = document.getElementById('inclease')
          var count = document.getElementById('count')
  
          function increase() {
              // 카운트 상태를 유지하기 위한 지역 변수
              var counter = 0;
              return ++counter
          }
  
          incleaseBtn.onclick = function () {
              count.innerHTML = increase()
          };
      </script>
  </body>
  </html>
  ```

  - 클로저 사용
    - 스크립트가 실행되면 즉시실행함수가 호출되고 변수 `increase`에 클로저가 할당된다.
    - 즉시실행함수는 호출된 이후 소멸되지만 즉시실행함수가 반환한 함수는 변수 `increase`에 할당되어, inclease 버튼을 클릭하면 클릭 이벤트 핸들러 내부에서 호출된다.
    - 이때 클로저인 이 함수는 자신이 선언됐을 때의 렉시컬 환경인 즉시실행함수의 스코프에 속한 지역변수 counter를 기억한다. 
    - 따라서 즉시실행함수의 변수 counter에 접근할 수 있고 변수 counter는 자신을 참조하는 함수가 소멸될 때가지 유지된다.
    - 즉시실행함수는 한번만 실행되므로 `increase`가 호출될 때마다 변수 `counter`가 재차 초기화될 일은 없을 것이다. 
    - 변수 counter는 외부에서 직접 접근할 수 없는 private 변수이므로 전역 변수를 사용했을 때와 같이 의도되지 않은 변경을 걱정할 필요가 없다.

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Document</title>
  </head>
  <body>
      <p>클로저를 사용한 Counting</p>
      <button id="inclease">+</button>
      <p id="count">0</p>
      <script>
          var incleaseBtn = document.getElementById('inclease')
          var count = document.getElementById('count')
  
          var increase = (function () {
              // 카운트 상태를 유지하기 위한 자유 변수
              var counter = 0
              
              // 클로저를 반환
              return function () {
                  return ++counter
              }
          }())
  
          incleaseBtn.onclick = function () {
              count.innerHTML = increase()
          };
      </script>
  </body>
  </html>
  ```

  - 함수형 프로그래밍에서 클로저를 활용하는 간단한 예제
    - 주의해야 할 것은 함수 `makeCounter`를 호출해 함수를 반환할 때 반환된 함수는 자신만의 독립된 렉시컬 환경을 갖는다는 것이다. 이는 함수를 호출하면 그때마다 새로운 렉시컬 환경이 생성되기 때문이다. 
    - 변수 `increaser`와 변수 `decreaser`에 할당된 함수는 각각 자신만의 독립된 렉시컬 환경을 갖기 때문에 카운트를 유지하기 위한 자유 변수 `counter`를 공유하지 않아 카운터의 증감이 연동하지 않는다. 
    - 따라서 독립된 카운터가 아니라 연동하여 증감이 가능한 카운터를 만들려면 렉시컬 환경을 공유하는 클로저를 만들어야 한다.

  ```javascript
  // 함수를 인자로 전달받고 함수를 반환하는 고차 함수
  // 이 함수가 반환하는 함수는 클로저로서 카운트 상태를 유지하기 위한 자유 변수 counter을 기억한다.
  function makeCounter(predicate) {
    // 카운트 상태를 유지하기 위한 자유 변수
    var counter = 0;
    // 클로저를 반환
    return function () {
      counter = predicate(counter)
      return counter
    }
  }
  
  // 보조 함수
  function increase(n) {
    return ++n
  }
  
  // 보조 함수
  function decrease(n) {
    return --n
  }
  
  // 함수로 함수를 생성한다.
  // makeCounter 함수는 보조 함수를 인자로 전달받아 함수를 반환한다
  const increaser = makeCounter(increase)
  console.log(increaser()) // 1
  console.log(increaser()) // 2
  
  // increaser 함수와는 별개의 독립된 렉시컬 환경을 갖기 때문에 카운터 상태가 연동하지 않는다.
  const decreaser = makeCounter(decrease)
  console.log(decreaser()) // -1
  console.log(decreaser()) // -2
  ```



- 정보의 은닉

  - 클로저의 특징을 사용해 클래스 기반 언어의 `private` 키워드를 흉내낼 수 있다.
    - 생성자 함수 `Counter`는 `increase`, `decrease` 메소드를 갖는 인스턴스를 생성한다.
    - 이 메소드들은 모두 자신이 생성됐을 때의 렉시컬 환경인 생성자 함수 `Counter`의 스코프에 속한 변수 `counter`를 기억하는 클로저이며 렉시컬 환경을 공유한다. 
    - 생성자 함수가 함수가 생성한 객체의 메소드는 객체의 프로퍼티에만 접근할 수 있는 것이 아니며, 자신이 기억하는 렉시컬 환경의 변수에도 접근할 수 있다.
    - 생성자 함수 `Counter` 내에서 선언된 변수 `cnt`가 `this`에 바인딩된 프로퍼티라면 생성자 함수 `Counter`가 생성한 인스턴스를 통해 외부에서 접근이 가능한 `public` 프로퍼티(`counter.cnt`)가 되지만, 생성자 함수 `Counter` 내에서 선언된 변수 `cnt`는 생성자 함수 `Counter` 외부에서 접근할 수 없다. 
    - 하지만 생성자 함수 `Counter`가 생성한 인스턴스의 메소드인 `increase`, `decrease`는 클로저이기 때문에 자신이 생성됐을 때의 렉시컬 환경인 생성자 함수 `Counter`의 변수 `cnt`에 접근할 수 있다.

  ```javascript
  function Counter() {
  
      // 카운트를 유지하기 위한 자유 변수
      // this에 바인딩된 프로퍼티가 아니다.
      var cnt = 0
  
      // 클로저
      this.increase = function () {
          return ++cnt
      }
  
      // 클로저
      this.decrease = function () {
          return --cnt
      }
  }
  
  const counter = new Counter()
  
  console.log(counter.increase()) // 1
  console.log(counter.decrease()) // 0
  ```



- 자주 발생하는 실수

  - 문제
    - 아래 사용된 함수는 전역 함수지 클로저가 아니다.
    - i도 전역 변수이지 자유변수가 아니다.

  ```javascript
  var arr = [];
  
  for (var i = 0; i < 5; i++) {
    arr[i] = function () {
      return i;
    };
  }	// i = 5인 상태로 반복문이 종료 
  
  for (var j = 0; j < arr.length; j++) {
    console.log(arr[j]());                // 5
  }
  ```

  - 클로저를 활용

  ```javascript
  var arr = [];
  
  for (var i = 0; i < 5; i++){
    arr[i] = (function (id) {     // 2. 매개변수 id는 자유변수가 된다.
      return function () {
        return id     // 3. id는 상위 스코프의 자유변수이므로 그 값이 유지된다.
      }
    }(i)) // 1. 즉시 실행 함수는 i를 인자로 받는다.
  }
  
  for (var j = 0; j < arr.length; j++) {
    console.log(arr[j]())
  }
  ```

  - 클로저가 아닌 `let`을 활용하는 방법도 있다.

  ```javascript
  const arr = []
  
  for (let i = 0; i < 5; i++) {
    arr[i] = function () {
      return i
    };
  }
  
  for (let i = 0; i < arr.length; i++) {
    console.log(arr[i]())
  }
  ```

  - 고차 함수를 사용하는 방법도 있다.

  ```javascript
  const arr = new Array(5).fill()
  
  arr.forEach((v, i, array) => array[i] = () => i)
  
  arr.forEach(f => console.log(f()))
  ```

  

