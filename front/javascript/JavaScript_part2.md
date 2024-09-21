# 함수

- 함수
  - 어떤 작업을 수행하기 위해 필요한 문들의 집합을 정의한 코드 불록.
  - 이름과 매개 변수를 가지며, 필요한 때에 호출하여 코드 블록에 담긴 문들을 일괄적으로 실행할 수 있다.
  - 함수는 선언에 의해 정의되고 호출에 의해 실행되는데 한 번만 호출할 수 있는 것이 아니라 여러번 호출할 수 있다.
  - 동일한 작업을 반복적으로 수행해야 한다면 동일한 작업을 중복해서 작성하는 것 보다 미리 정의된 함수를 재사용 하는 것이 효율적이다.



- Javascript의 함수는 1급 객체다.
  
  - 호출할 수 있다.
  
  - 무명의 리터럴로 표현이 가능하다.
  
  - 변수나 객체, 배열 등에 저장할 수 있다.
  - 다른 함수의 리턴값이 될 수 있다.
  - 다른 함수의 인자가 될 수 있다.



## 함수 정의와 함수의 특징

- 함수 정의

  - 함수 선언문을 사용하여 정의
    - `function` 키워드, 함수명, 매개변수 목록, 함수 몸체로 구성

  ```javascript
  function hello(name){
    return "Hello! "+name
  }
  
  console.log(hello("Cha"))	// Hello! Cha
  ```

  - 함수 표현식을 사용하여 정의
    - 함수의 일급 객체 특성을 이용하여 함수 리터럴 방식으로 함수를 정의하고 변수에 할당
    - 함수 표현식으로 정의한 함수는 함수명을 생략할 수 있는데 이러한 함수를 익명함수라 한다.
    - 함수 표현식에서는 함수명을 생략하는 것이 일반적이다.
    - 기명 함수의 함수명을 사용해 호출하면 에러가 발생한다.
    - 함수명은 일반적으로 재귀호출이나 자바스크립트 디버거가 해당 함수를 구분할 수 있는 식별자로 쓰인다.

  ```javascript
  // 기명 함수 표현식
  var hi = function hello(name){
    return "Hello! " + name
  }
  console.log(hi("Cha"))	// Hello! Cha
  console.log(hello("Cha"))  // ReferenceError: hello is not defined
  
  // 익명 함수 표현식
  var hi = function(name){
      return "Hello! "+name
  }
  console.log(hi("Cha"))	// Hello! Cha
  ```

  - `Function` 생성자 함수를 사용하여 정의
    - 이 방식은 일반적으로 사용하지 않는다.
    - **함수 선언문과 함수 표현식은 모두 내장 함수 `Function` 생성자 함수로 함수로 생성하는 것을 단순화 시킨 축약법이다.**

  ```javascript
  var hello = new Function('name','return "Hello! "+name')
  console.log(hello("Cha"))	// Hello! Cha
  ```
  - 함수 선언문과 함수 표현식
    - 함수 표현식의 경우 위에서 살펴본 것 처럼, 함수명이 아닌 변수명으로 호출해야 하고, 함수명으로 호출할 경우 에러가 발생한다.
    - 사실 함수 선언문도 마찬가지이다. 함수 선언문으로 함수를 선언할 경우, 자바스크립트 엔진에 의해 자동으로 함수 표현식 형태로 변경되기 때문이다.
    - 즉, 함수명으로 호출한 것 처럼 보이지만 사실은 변수명으로 호출된 것이다.
    - 결국 함수 선언문도 함수 표현식과 동일하게 함수 리터럴 방식으로 정의되는 것이다.

  ```javascript
  // 아래와 같이 함수 선언문으로 정의 된 함수는
  function hello(name){
    return "Hello! "+name
  }
  
  //자바스크립트 엔진에 의해 아래와 같이 변경된다.
  var hello = function hello(name){
      return "Hello! "+name
  }
  ```
  
  - 메서드 단축 구문
    - 메서드의 경우 아래와 같이 단축해서 선언하는 것이 가능하다.
  
  ```javascript
  // 이런 메서드 선언을
  const obj = {
      foo: function() {
          console.log("Hello!")
      }
  }
  
  //아래와 같이 단축 가능하다.
  const obj2 = {
      foo(){
          console.log("Hello!")
      }
  }
  ```
  
  
  
- 함수 호이스팅

  - 호이스팅
    - 정의: 선언문이 해당 Scope의 선두로 옮겨진 것처럼 동작하는 특성, 즉 자바스크립트는 선언문이 선언되기 이전에 참조가 가능하다.
    - 자바스크립트는 let, const를 포함하여 모든 선언(var, function, class)을 호이스팅한다.

  - 함수 선언문
    - 함수 선언문으로 선언된 함수는 자바스크립트 엔진이 스크립트가 로딩되는 시점에 바로 초기화하고 이를 VO(variable object)에 저장한다.
    - 즉, 함수 선언, 초기화, 할당이 한 번에 이루어진다. 
    - 따라서 함수 선언의 위치와 무관하게 소스 내 어느 곳에서든 호출이 가능하다.

  ```javascript
  var result = plus(2,3)
  console.log(result)		//5
  
  function plus(num1,num2){
    return num1+num2
  }
  ```

  - 함수 표현식
    - 함수 표현식은 함수 호이스팅이 아니라 변수 호이스팅이 발생한다.
    - 변수 호이스팅은 변수 생성 및 초기화와 할당이 분리되어 진행된다.
    - 호이스팅된 변수는 undefined로 초기화 되고 실제 값의 할당은 할당문에서 이루어진다.

  ```javascript
  var result = minus(3,2)			// TypeError: minus is not a function	
  // 즉 위 문장은  아래와 같다.
  // var result = undefined(3,2)
  
  var minus = function(num1,num2){
      return num1-num2
  }
  ```

  - 함수 호이스팅이 함수 호출 전 반드시 함수를 선언하여야 한다는 규칙을 무시하므로 코드의 구조를 엉성하게 만들수 있기 때문에 함수 표현식만을 사용하는 것이 권고된다.
  - 또한, 함수 선언문으로 함수를 정의하면 대규모 애플리케이션을 개발하는 경우, 인터프리터가 너무 많은 코드를 변수 객체(VO)에 저장하므로 애플리케이션의 응답속도는 현저히 떨어질 수 있으므로 주의해야 한다.



- 일급 객체

  - 정의: 생성, 대입, 연산, 인자 또는 반환값으로서의 전달 등 프로그래밍 언어의 기본적 조작을 제한 없이 사용할 수 있는 대상
  - 조건
    - 무명의 리터럴로 표현이 가능
    - 변수나 자료구조(배열, 객체 등)에 저장 가능
    - 함수의 매개변수로 전달 가능
    - 반환값으로 사용 가능

  ```javascript
  // 무명의 리터럴(아래는 함수는 함수명이 없는 무명의 리터럴이다)로 표현이 가능
  // 변수나 자료구조에 저장이 가능(변수 plus에 저장 가능)
  var plus = function(num1,num2){
      return num1+num2
  }
  
  // 함수의 매개 변수로 전달 가능
  // 반환 값으로 사용 가능
  function calculate(func){
    	return function(num1,num2){
          result = func(num1,num2)
          return result
      }
  }
  var rst = calculate(plus)
  console.log(rst(3,4))
  ```

  

- 매개 변수

  - 매개변수(인자, parameter)는 함수 내에서 변수와 동일하게 메모리 공간을 확보하며 함수에 전달한 인수는 매개변수에 할당된다.
    - 매개변수는 인수로 초기화된다.
    - 매개 변수의 갯수보다 인수를 적게 전달했을 때 인수가 전달되지 않은 매개변수는 undefined로 초기화 된다.
    - 매개 변수의 갯수보다 인수를 많이 전달한 경우, 초과된 인수는 무시된다.

  - Call-by-value
    - 원시타입 인수는 Call-by-value(값에 의한 호출)로 동작한다. 
    - 이는 함수 호출 시 원시 타입 인수를 함수에 매개 변수로 전달할 때, 매개 변수에 값을 복사하여 함수로 전달하는 방식이다.
    - 함수 내에서 매개변수를 통해 값이 변경되어도 기존의 원본 변수 값은 변경되지 않는다.

  ```javascript
  function foo(primitive){
      primitive += 3
      return primitive
  }
  
  var x = 3
  console.log(foo(x))		// 6
  console.log(x)			// 3
  ```

  - Call-by-reference
    - 객체형(참조형) 인수는 Call-by-reference(참조에 의한 호출)로 동작한다.
    - 이는 함수 호출 시 참조 타입 인수를 함수에 매개변수로 전달할 때 매개변수에 값이 복사되지 않고 객체의 참조값이 매개변수에 저장되어 함수로 전달되는 방식이다.
    - 함수 내에서 매개변수의 참조값을 이용하여 객체의 값을 변경했을 때 전달되어진 참조형의 인수값도 같이 변경된다.

  ```javascript
  function foo(objective){
      objective.name = "Lee"
      objective.smoking = false
  }
  
  var obj = {
      name:'Cha',
      smoking:true
  }
  
  console.log(obj)	// { name: 'Cha', smoking: true }
  foo(obj)
  console.log(obj)	// { name: 'Lee', smoking: false }
  ```

  - 순수함수
    - 객체형 인수는 참조값을 매개변수에 전달하기 때문에 함수 몸체에서 그 값을 변경할 경우 원본 객체가 변경되는 **부수 효과(side-effect)**가 발생한다.
    - 부수 효과를 발생시키는 함수를 **비순수 함수**라 하며 이는 복잡성을 증가시킨다.
    - 어떠한 외부 상태도 변경하지 않는 함수를 순수함수라 한다.
    - 비순수 함수를 최대한 줄이는 것은 부수 효과를 억제해 디버깅을 쉽게 만들어 준다.



- 반환값

  - 함수가 자신을 호출한 코드에게 수행한 결과를 반환할 수 있는데 이 때 반환된 값을 반환값이라 한다.
  - `return` 키워드는 함수를 호출한 코드(caller)에게 값을 반활할 때 사용한다.
    - 자바스크립트 해석기는 `return` 키워드를 만나면 함수의 실행을 중단한 후, 함수를 호출한 코드로 되돌아간다.
    - 만일 `return` 키워드 이후에 다른 구문이 존재하면 그 구문은 실행되지 않는다.
  - 함수는 배열 등을 이용하여 한 번에 여러 개의 값을 리턴할 수 있다.
    - 반환 값이 배열이므로 당연히 인덱싱도 가능하다.
  - 함수는 반환을 생략할 수 있다. 이때 함수는 암묵적으로  undefined를 반환한다.

  ```javascript
  function plusMinus(num1,num2){
    var prst = num1+num2
    var mrst = num1-num2
    return [prst,mrst]
  }
  
  console.log(plusMinus(4,1))		// [5,3]
  console.log(plusMinus(4,1)[1])	// 3
  ```



- 함수가 반환한 함수는 바로 인자를 받는 것이 가능하다.

  - 아래 예시에서 `foo` 함수는 `bar` 함수를 반환한다.
  - 그 반환값에 바로 `foo()("hello!");`와 같이 인자를 넘기면 실행이 된다.

  ```javascript
  function foo() {
    const bar = function (m) {
      console.log(m);
    };
    return bar;
  }
  
  foo()("hello!");	// hello!
  ```

  



## 함수의 객체 프로퍼티

- 함수는 객체이므로 프로퍼티를 가질 수 있다.

  - 함수는 일반 객체와는 다른 함수만의 프로퍼티를 갖는다.

  ```javascript
  function hello(name){
      return "Hello! "+name
  }
  
  hello.x = "Cha"
  console.log(hello.x)	// Hello! Cha
  
  console.dir(hello)
  
  /*
  ƒ hello(name)
  arguments: null
  caller: null
  length: 1
  name: "hello"
  prototype: {constructor: ƒ}
  __proto__: ƒ ()
  */
  ```



- arguments 프로퍼티

  - 함수 호출 시 전달된 인수들의 정보를 담고 있는 순회 가능한 유사배열객체이다.
  - **유사배열객체**: 실제 배열 객체는 아니지만 length 프로퍼티를 가진 객체를 말한다.
  - 유사배열객체는 진짜 객체는 아니므로 배열 메소드를 사용하려면 배열로 변환해야 한다.
  - 함수 내부에서 지역변수처럼 사용된다(즉 함수 외부에서는 사용할 수 없다).
  - `arguments` 객체는 매개 변수 갯수가 확정되지 않은 가변 인자 함수를 구현할 때 유용하게 사용된다.

  ```javascript
  function plus(num1,num2){
    console.log(arguments)
    return num1+num2
  }
  
  plus()			// [Arguments] {}
  plus(1)			// [Arguments] { '0': 1 }
  plus(1,2)		// [Arguments] { '0': 1, '1': 2 }
  plus(1,2,3)		// [Arguments] { '0': 1, '1': 2, '2': 3 }
  
  
  //가변 인자 함수
  function minus(){
    var bigNum = 100
    for (var i = 0;i<arguments.length;i++){
        bigNum-=arguments[i]
    }
    return bigNum
  }
  console.log(minus())			// 100
  console.log(minus(5))			// 95
  console.log(minus(10,20,30))	// 45
  
  // arguments를 진짜 배열로 변환
  function foo(){
    if (!arguments.length) return 0;
    console.log(Object.prototype.toString.call(arguments))	// [object Arguments]
    var arr = Array.prototype.slice.call(arguments)
    console.log(Object.prototype.toString.call(arr))			// [object Array]
  }
  
  foo(1,2,3,4,5)
  ```



- caller 프로퍼티

  - 자신을 호출한 함수를 의미한다.

  ```javascript
  function callerFunc(func){
      var result = func()
      return result
  }
  
  function foo(){
      return "caller: " + foo.caller
  }
  console.log(callerFunc(foo))
  /*
  caller: function callerFunc(func){
    var result = func()
    return result
  }
  */
  ```



- length 프로퍼티

  - 함수 정의 시 작성된 매개변수 갯수를 의미한다.
  - `arguments.length`의 값과는 다를 수 있으므로 주의하여야 한다. `arguments.length`는 함수 호출시 인자의 갯수이다.

  ```javascript
  function foo(){}
  function bar(x,y,z){}
  
  console.log(foo.length)		// 0
  console.log(bar.length)		// 3
  ```



- name 프로퍼티

  - 함수명을 나타낸다.
  - 기명 함수의 경우 함수명을 값으로 갖고, 익명함수의 경우 변수명을 값으로 갖는다.

  ```javascript
  var named = function foo(){}
  var anonymous = function(){}
  
  console.log(named.name)			// foo
  console.log(anonymous.name)		// anonymous
  ```



- \__proto__접근자 프로퍼티

  - 모든 객체는 [[Prototype]] 이라는 내부 슬롯이 있고, [[Prototype]] 내부 슬롯은 프로토타입 객체를 가리킨다.
  - 프로토타입 객체란 프로토타입 기반 객체 지향 프로그래밍의 근간을 이루는 객체로서, 객체간의 상속을 구현하기 위해 사용된다.
  - 즉, 프로토타입 객체는 다른 객체에 공유 프로퍼티를 제공하는 객체를 말한다.
  - \__proto__ 프로퍼티는 [[Prototype]] 내부 슬롯이 가리키는 프로토타입 객체에 접근하기 위해 사용하는 접근자 프로퍼티이다.
  - 내부 슬롯에는 직접 접근할 수 없고 간접적인 방법을 제공하는 경우에 한하여 접근할 수 있다.
  - [[Prototype]] 내부 슬롯에도 직접 접근할 수 없으며 \__proto__접근자 프로퍼티를 통해 간접적으로 프로토타입 객체에 접근할 수 있다.

  ```javascript
  // __proto__ 접근자 프로퍼티를 통해 자신의 프로토타입 객체에 접근할 수 있다.
  // 객체 리터럴로 생성한 객체의 프로토타입 객체는 Object.prototype이다.
  
  console.log({}.__proto__==Object.prototype)		// true
  ```

  - \_\_proto\__ 프로퍼티는 객체가 직접 소유하는 프로퍼티가 아니라 모든 객체의 프로토타입 객체인 `Object.prototype` 객체의 프로퍼티다. 모든 객체는 상속을 통해 \__proto__ 접근자 프로퍼티는 사용할 수  있다.
    - `Object.getOwnPropertyDescriptor(속성을 찾을 대상 객체, 설명이 검색될 속성명)`은 객체에 속성명이 존재하는 경우 주어진 속성의 속성 설명자를 반환하고 없으면 `undefined`를 반환한다. 

  ```javascript
  // 객체는 __proto__ 프로퍼티를 직접 소유하지 않는다.
  console.log(Object.getOwnPropertyDescriptor({}, '__proto__'))
  // undefined
  
  // __proto__ 프로퍼티는 모든 객체의 프로토타입 객체인 Object.prototype의 접근자 프로퍼티이다.
  console.log(Object.getOwnPropertyDescriptor(Object.prototype, '__proto__'))
  // {get: ƒ, set: ƒ, enumerable: false, configurable: true}
  
  // 모든 객체는 Object.prototype의 접근자 프로퍼티 __proto__를 상속받아 사용할 수 있다.
  console.log({}.__proto__ === Object.prototype); // true
  ```

  - 함수도 객체이므로 \__proto__ 접근자 프로퍼티를 통해 프로토타입 객체에 접근 가능하다.
    - 함수 객체의 프로토타입 객체는 `Function.prototype`이다.

  ```javascript
  console.log((function() {}).__proto__ === Function.prototype) // true
  ```



- prototype 프로퍼티(java_part4 참고)

  - 함수 객체만이 소유하는 프로퍼티
  - prototype 프로퍼티는 함수가 객체를 생성하는 생성자 함수로 사용될 때, 생성자 함수가 생성한 인스턴스의 프로토타입 객체를 가리킨다.

  ```javascript
  // 함수 객체는 prototype 프로퍼티를 소유한다.
  console.log(Object.getOwnPropertyDescriptor(function() {}, 'prototype'))
  // {value: {…}, writable: true, enumerable: false, configurable: false}
  
  // 일반 객체는 prototype 프로퍼티를 소유하지 않는다.
  console.log(Object.getOwnPropertyDescriptor({}, 'prototype'))
  // undefined
  ```






## 함수의 다양한 형태

- 생성자 함수
  - 자바스크립트의 생성자 함수는 말 그대로 객체를 생성하는 역할을 한다.
    -  정확히 말해서 Java와는 달리 클래스의 인스턴스를 만드는 것이 아니라 객체와 또 다른 객체를 연결하는 것 뿐이다.
    - 단지 `Person()` 객체(함수는 객체이므로)와 `cha` 객체를 연결해 주는 것 뿐이다.

  ```javascript
  function Person(){
      
  }
  
  var cha = new Person()
  ```

  -  Java의 생성자 함수와는 다르게 그 형식이 정해져 있는 것이 아니라 기존 함수에 new 연산자를 붙여서 호출하면 해당 함수는 생성자 함수로 동작한다.
    - `new` 연산자는 `new`를 붙인 기존 클래스와 이를 통해 생성한 객체를 연결해 주는 역할을 한다. 
    - 생성자 함수가 아닌 일반 함수에 new 연산자를 붙여 호출하면 생성자 함수처럼 동작할 수 있다. 
    - 따라서 일반적으로 생성자 함수명은 첫문자를 대문자로 기술하여 혼란을 방지하려는 노력을 한다.

  - 동작 방식은 JavaScript_part3.생성자 함수 호출시의 this참조.



- 즉시 실행 함수

  - 함수의 정의와 동시에 실행되는 함수
  - 최초 한 번만 호출되며 다시 호출할 수는 없다.
  - 이러한 특징을 이용하여 최초 한 번만 실행이 필요한 초기화 처리 등에 사용할 수 있다.
  - 즉시 실행 함수를 선언할 때는 반드시 마지막에 `;`를 붙여줘야 한다.
  - 함수 선언문은 자바스크립트 엔진에 의해 함수 몸체를 닫는 중괄호 뒤에 ;가 자동 추가된다.
    - 따라서 즉시 실행 함수는 소괄호로 감싸줘야 한다.
    - 감싸지 않을 경우: `function(){};();`(`SyntaxError: Unexpected token (` 발생)
    - 감쌀 경우: `(function(){}());`

  ```javascript
  // 즉시 실행 함수는 소괄호로 감싸준다.
  // 기명 즉시 실행 함수
  (function hello(){
    console.log("기명 즉시 실행 함수 실행")		// 기명 즉시 실행 함수 실행
    return "Hello!"
  }());
  
  // 익명 즉시 실행 함수
  (function(){
    console.log("익명 즉시 실행 함수 실행")		// 익명 즉시 실행 함수 실행
    return "Hi!"
  }());
  ```

  - 자바스크립트의 가장 큰 문제점 중 하나는 파일이 분리되어 있어도 글로벌 스코프가 하나이며, 글로벌 스코프에 선언된 변수나 함수는 코드 내의 어디서든지 접근이 가능하다는 것이다.
    - 따라서 다른 스크립트 파일 내에서 동일한 이름으로 명명된 변수나 함수가 같은 스코프 내에 존재할 경우 원치 않는 결과를 가져올 수 있다.
    - 즉시 실행 함수 내에 처리 로직을 모아 두면, 혹시 있을 수도 있는 변수명 또는 함수명의 충돌을 방지할 수 있어, 이를 위한 목적으로 즉시실행함수를 사용하기도 한다(함수 내부의 변수는 함수 내부에서만 효력을 가지므로).
    - 특히 jQuery와 같은 라이브러리의 경우, 코드를 즉시 실행 함수 내에 정의해 두면 라이브러리의 변수들이 독립된 영역 내에 있게 되므로 여러 라이브러리들은 동시에 사용하더라도 변수명 충돌과 같은 문제를 방지할 수 있다.

  ```javascript
  (function () {
    var foo = 1;
    console.log(foo);		// 1
  }());
  
  var foo = 10;
  console.log(foo);		// 10
  ```



- 내부 함수

  - 함수 내부에 정의된 함수
  - 내부함수는 부모 함수의 변수에 접근할 수 있지만 부모 함수는 자식 함수의 변수에 접근할 수 없다.

  ```javascript
  function parent(pra){
      var parentValue = pra
      function child(){
          var childValue = "Cha"
          console.log("parentValue: "+parentValue)	// parentValue1: Ha
          console.log("childValue: "+ childValue)		// childValue1: Cha
      }
      child()
      console.log("parentValue: "+parentValue)		// parentValue2: Ha
      console.log("childValue: "+ childValue)			// ReferenceError: childValue is not defined
  }
  
  parent("Ha")
  ```

  - 내부함수는 부모함수의 외부에서 접근할 수 없다.

  ```javascript
  function hello(){
      var hi = function(){
          console.log("Hello!, Hi!")
      }
      hi()
  }
  
  hello()		// Hello!, Hi!
  hi()		// ReferenceError: hi is not defined
  ```

  

- 재귀 함수

  - 자기 자신을 호출하는 함수
  - 탈출 조건을 반드시 만들어야 한다. 탈출 조건이 없는 경우, 함수가 무한 호출되어 stackoverflow 에러가 발생한다. 
  - 대부분의 재귀 함수는 for나 while 문으로 구현이 가능하다. 
  - 반복문보다 재귀 함수를 통해 보다 직관적으로 이해하기 쉬운 구현이 가능한 경우에만 한정적으로 적용하는 것이 바람직하다.

  ```javascript
  // 피보나치 수열을 구하는 예제
  function fibonacci(n) {
    if (n < 2) return n
    return fibonacci(n - 1) + fibonacci(n - 2)
  }
  
  console.log(fibonacci(6)) // 8
  
  
  // 팩토리얼을 구하는 예제
  function factorial(n) {
    if (n < 2) return 1
    return factorial(n - 1) * n
  }
  
  console.log(factorial(3)) // 6
  ```

  

- 콜백 함수

  - 함수를 명시적으로 호출하는 방식이 아니라 특정 이벤트가 발생했을 때 시스템에 의해 호출되는 함수
  - 예시1. click이라는 이벤트에 의해 실행되는 콜백 함수
  
  ```html
  <html>
  <body>
    <button id="myButton">Click me</button>
    <script>
      var button = document.getElementById('myButton');
      button.addEventListener('click', function() {
        console.log('button clicked!');
      });
    </script>
  </body>
  </html>
  ```
  
  - 예시2. 함수의 인자로 넘겨져 해당 함수가 실행됨으로써 실행 되는 콜백 함수
  
  ```javascript
  function first(a,b,callback){
      let v=a*b;
      callback(v);
  }
  function callback(a){
      console.log(a);
  }
  ```
  
    - 자바스크립트의 함수는 일급 객체이므로 변수와 유사하게 사용될 수 있다.
      - 콜백 함수는 매개변수롤 통해 전달될 수 있다.
      - 전달 받은 함수의 내부에서 어느 특정 시점에 실행된다.
  
  ```javascript
  // 첫 매개변수로 함수가 전달되며, 두 번째 매개변수에 전달된 시간이 경과하면 매개변수로 전달된 콜백 함수가 호출된다.
  setTimeout(function () {
      console.log('1초 뒤 출력됩니다.');
  }, 1000);
  ```
  
    - 콜백 함수는 주로 비동기식 처리 모델에 사용된다.
      - 비동기식 처리 모델: 처리가 종료하면 호출될 함수(콜백 함수)를 미리 매개변수에 전달하고 처리가 종료되면 콜백함수를 호출하는 것
      - 콜백 함수는 콜백 큐에 들어 있다가 해당 이벤트가 발생하면 호출된다.
      - 콜백 함수는 클로저이므로 콜백 큐에 단독으로 존재하다가 호출되어도 콜백함수를 전달받은 함수의 변수에 접근할 수 있다.
    - 동기식 처리 모델에 사용되지 못한다는 말은 아니다.
      - 아래의 코드도 명시적으로 호출하지 않고 `foo` 함수가 실행되면서 시스템에 의해 호출되었으므로 콜백 함수를 사용한 것이다.
      - 또한 비동기적이 아닌 동기적으로 사용되었다.
  
  ```javascript
  function foo(f){
      f()
  }
  console.log("Cha!")				
  foo(()=>console.log("Hello!"))	
  console.log("Have a nice day!")
  // Cha!
  // Hello!
  // Have a nice day!
  ```
  
    - 아래는 비동기적으로 동작하는 함수의 예시이다.
  
  ```javascript
  function foo(f){
      setTimeout(f,1000)
  }
  console.log("Cha!")
  foo(()=>console.log("Hello!"))
  console.log("Have a nice day!")
  // Cha!
  // Have a nice day!
  // Hello!
  ```

  





# 프로토타입

> https://poiemaweb.com/js-prototype 

> https://medium.com/@bluesh55/javascript-prototype-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0-f8e67c286b67 

- 자바스크립트는 Java, C++ 같은 클래스 기반 객체 지향 언어와 달리 프로토타입 기반 객체 지행 언어다.
  - 따라서 자바스크립트의 동작 원리를 이해하기 위해서는 프로토 타입의 개념을 잘 이해하고 있어야 한다.
  - 클래스 기반 객체 지향 언어는 객체 생성 이전에 클래스를 정의하고 이를 통해 객체를 생성한다.
  - 프로토타입 기반 객체 지향 언어는 클래스 없이도 객체를 생성할 수 있다.



- 사전지식
  - JavaScript의 모든 객체는 결국 함수를 통해 생성된다.
    - 객체 리터럴 방식은 결국 `Object()` 생성자 함수를 축약한 방식이다.
    - 객체인 함수와 배열을 생성하는 `Function()`,`Array()`도 함수이다. 
    - 따라서 결국 모든 객체는 함수를 통해 생성된다.
  - 생성자 함수가 정의될 때 2가지 일이 발생한다.
    - 해당 함수에 Constructor(생성자) 자격 부여(`new` 를 통해 객체를 만들어 낼 수있게 된다).
    - 해당 함수의 프로토타입 객체가 생성되고 함수와 연결된다. 이 객체의 constructor 프로퍼티는 생성자 함수를 가리키게 된다.
  - 모든 함수는 결국 함수 생성자를 통해 생성된다.



- 프로토타입(Prototype)

  - 자바스크립트의 모든 객체는 자신의 부모 역할을 담당하는 객체와 연결되어 있다.
  - 객체 지향의 상속 개념과 같이 부모 객체의 프로퍼티 또는 메서드를 상속 받아 사용할 수 있게 한다.
  - 이러한 부모 객체를 프로토타입 객체 또는 프로토타입이라 한다.
  - 프로토타입은 생성자 함수에 의해 생성된 각각의 객체에 공유 프로퍼티를 제공하기 위해 사용한다.
  - 객체를 생성할 때 프로토타입이 결정된다.
    - 결정된 프로토타입은 다른 임의의 객체로 변경 가능하다.
    - 즉, 부모 객체인 프로토타입을 동적으로 변경할 수 있다는 것을 의미한다.
    - 이러한 특징을 활용하여 객체의 상속을 구현할 수 있다.

  ```javascript
  var person = {
      name:'Cha',
      age:28
  }
  
  // person에는 hasOwnProperty를 정의해 준 적이 없지만 아래 문장은 동작한다.
  console.log(person.hasOwnProperty('name'))	//true
  ```



- [[Prototype]]

  - 자바스크립트의 모든 객체는 [[Prototype]]라는 인터널 슬롯을 가진다.
  - [[Prototype]]의 값은 `null` 또는  프로토타입 객체(부모 객체)이며, 상속을 구현하는데 사용된다.
  - `__proto__` 접근자 프로퍼티로 접근이 가능하다.
    - `__proto__` 프로퍼티에 접근하면 내부적으로 `Object.getPrototypeOf`가 호출되어 프로토타입 객체(부모 객체)를 반환한다.
  - [[Prototype]] 객체의 데이터 프로퍼티는 get 엑세스를 위해 상속되어 자식 객체의 프로퍼티처럼 사용할 수 있다.
  - 하지만 set 엑세스는 허용되지 않는다.

  ```javascript
  var person = {
      name:'Cha',
      age:28
  }
  
  // person 객체는 __proto__ 프로퍼티로 자신의 부모 객체(포로토타입)인 Object.prototype를 가리키고 있다.
  console.log(person.__proto__ === Object.prototype)	//true
  ```



- [[Prototype]]과 prototype 프로퍼티의 차이

  - 자바스크립트의 모든 객체는 [[Prototype]]라는 인터널 슬롯을 가지며 상속을 위해 사용된다.
    - 함수도 객체이므로 [[Prototype]] 인터널 슬롯을 갖는다.
    - 그런데 함수 객체는 일반 객체와는 달리 prototype 프로퍼티도 소유하게 된다.
  - [[Prototype]]
    - `__proto__` 프로퍼티로 접근한다.
    - 함수를 포함한 모든 객체가 가지고 있는 인터널 슬롯이다.
    - 객체의 입장에서 자신의 부모 역할을 하는 프로토타입 객체를 가리키며 함수 객체의 경우 `Function.prototype`을 가리킨다.
  - prototype 프로퍼티
    - 함수 객체만 가지고 있는 프로퍼티이다.
    - 함수 객체가 생성자로 사용될 때 이 함수를 통해 생성될 객체의 부모 역할을 하는 객체(프로토타입)를 가리킨다.

  ```javascript
  function Person(name) {
    this.name = name;
  }
  
  var cha = new Person('Cha');
  
  // [[Prototype]]: __proto__ 접근자 프로퍼티에 접근하며, 함수 객체의 경우 Function.prototype을 가리킨다.
  console.log(Person.__proto__ === Function.prototype)	// true
  
  // prototype 프로퍼티: prototype 프로퍼티로 접근하며, Person 함수로 생성된 객체의 부모 객체를 가리킨다.
  console.log(Person.prototype === cha.__proto__)			// true
  
  // 둘은 다르다!!
  console.log(Person.prototype === Person.prototype)     // true
  console.log(Person.__proto__ === Function.prototype)   // true
  
  
  /*
  위 예시에서 객체인 cha는 prototype 프로퍼티를 가지고 있지 않다.
  따라서 자신의 부모 객체(프로토타입)을 확인하기 위해서는 __proto__ 프로퍼티에 접근해야 한다.
  반면에 Person은 함수이므로 prototype 프로퍼티를 가지고 있다.
  따라서 Person은 prototype 프로퍼티에 접근하여 자신을 통해 생성될 객체의 부모 역할을 하는 객체를 확인할 수 있다.
  cha는 Person을 통해 생성된 객체이므로 Peson의 prototype 프로퍼티로 접근한 값과 cha의 __proto__ 프로퍼티로 접근한 값은 같을 수 밖에 없다.
  */
  ```

  

- constructor 프로퍼티

  - **프로토타입 객체**는 constructor 프로퍼티를 갖는다. 이 construtor 프로퍼티는 객체의 입장에서 자신을 생성한 객체를 가리킨다.
    - 오직 프로토타입 객체만이 constructor 프로퍼티를 갖는다.
  - 아래 예시에서 `Person()`은 생성자 함수(객체)이고, `cha`는 생성자 함수에 의해 생성된 객체이다.
    - `cha` 입장에서 자신을 생성한 객체는 `Person()` 생성자 함수이다.
    - `cha`객체는 프로토타입 객체는 아니므로 constructor 프로퍼티를 갖지 않는다.
  - 본래 프로토타입 객체가 아닌 객체는 constructor 프로퍼티를 갖지 않는다. 그러나 아래 예제에서는 `cha.constructor===Person`이 `true`를 반환하는데 이는 어떻게 된 것일까?
    - `Person()` 생성자 함수가 생성될 때, constructor를 `Person()` 생성자 함수로 갖는 `Person.prototype` 객체도 함께 생성된다.
  - `Person.prototype` 객체는 앞으로 `Person()` 생성자 함수로 생성되는 모든 객체의 프로토타입이 될 객체이다.
    - `cha` 객체는 `Person()` 생성자 함수로 생성된 객체이다.
    - 따라서 `cha` 객체의 프로토타입 객체는 `Person.prototype`객체이다.
    - `cha` 객체는 프로토타입 객체가 아니므로 constructor 프로퍼티가 존재하지 않는다.
    - `Person.prototype` 객체는 constructor로 `Person()` 생성자 함수를 가리킨다.
    - `cha.constructor`는 프로토타입 체인에 따라 부모 객체인 `Person.prototype`의 constructor인 `Person()` 생성자 함수를 가리키게 된다.
  
  ```javascript
  function Person(name){
      this.name = name
  }
  
  var cha = new Person('Cha')
  
  // Person() 생성자 함수에 의해 생성된 프로토타입 객체를 생성한 객체는 Person() 생성자 함수이다.
  console.log(Person.prototype.constructor === Person)
  // Person() 생성자 함수를 생성한 객체는 Function() 생성자 함수이다.
  console.log(Person.constructor === Function)
  // cha 객체를 생성한 객체는 Person() 생성자 함수이다.
  console.log(cha.constructor === Person)
  ```







## 프로토타입 체인

- Prototype chain

  - 특정 객체의 프로퍼티나 메서드에 접근하려고 할 때 해당 객체에 접근하려는 프로퍼티나 메서드가 없다면 [[Prototype]]이 가리키는 링크를 따라 자신의 부모 역할을 하는 프로토타입 객체의 프로퍼티나 메서드를 차례로 검색하는데 이를 프로토타입 체인이라 한다.

  ```javascript
  var person = {
      name:'Cha',
      age:28
  }
  
  // person에는 hasOwnProperty를 정의해 준 적이 없지만 person 객체의  [[Prototype]]이 가리키는 링크를 따라 person의 부모 역할을 하는 프로토타입 객체의 메서드를 호출하였기에 에러가 발생하지 않는다.
  console.log(person.hasOwnProperty('name'))	//true
  ```



- 객체 리터럴 방식으로 생성된 객체의 프로토타입 체인

  - 객체 리터럴 방식으로 생성된 객체는 내장 함수인 `Object()` 생성자 함수로 객체를 생성하는 것을 단순화시킨 것이다.
    - `Object()` 생성자 함수는 함수 객체이므로 prototype 프로퍼티가 있다.
  - 결국 객체 리터럴을 사용하여 객체를 생성한 경우, 그 객체의 프로토타입 객체는 `Object.prototype`이다.

  ```javascript
  var cha = {
      name:"Cha",
      age:28
  }
  
  console.log(Function.prototype.__proto__ === Object.prototype)	// true
  console.log(Object.__proto__ === Function.prototype)			// true
  console.log(Object.prototype.constructor === Object)			// true
  console.log(cha.__proto__ === Object.prototype)					// true
  ```
  
  - 상세설명(`.__proto__`와 `.protytype`은 다르다는 것을 염두에 둬야 한다.)
    - 함수를 생성하는 생성자 함수 `Funcion()`은 생성 되는 순간, 앞으로 `Function()` 생성자 함수로 생성될 모든 함수들의 프로토타입이 될 `Function.prototype`이 함께 생성된다.
    - `Function.prototype`은 프로토타입 객체이므로 모든 객체의 부모 객체인 `Object.prototype`을 프로토타입으로 갖는다.
    - `Object()` 생성자 함수는 `Function()` 생성자 함수로 생성된 것이므로 `Function()` 생성자 함수가 생성될 때 함께 생성된 `Function.prototype`을 프로퍼티로 갖는다.
    - `Object.prototype`은 `Object()` 생성자 함수가 생성됨으로 인해 생성된 것이므로 `Object()`를 constructor로 갖는다.
    - `cha` 객체는  `Object()` 생성자 함수로 생성된 것이므로 프로토타입으로 `Object.prototype`을 갖는다.



- 생성자 함수로 생성된 객체의 프로토타입 체인

  - 생성자 함수로 객체를 생성하기 위해서는 우선 생성자 함수를 정의하여야 한다.
  - 함수를 정의하는 3가지 방식 모두 결국은 `Function()` 생성자 함수로 함수를 생성하는 것을 단순화 시킨 것이다.
    - 따라서 어떠한 방식으로 함수 객체를 생성하여도 모든 함수 객체의 prototype 객체는 Function.prototype이다. 
    - 생성자 함수도 함수 객체이므로 생성자 함수의 prototype 객체는 Function.prototype이다.

  ```javascript
  function Person(name){
      this.name = name
  }
  
  var cha = new Person('Cha')
  
  console.log(Function.prototype.__proto__ === Object.prototype) // true
  console.log(Person.prototype.constructor === Person)           // true
  console.log(Person.__proto__ === Function.prototype)           // true
  console.log(cha.__proto__ === Person.prototype)                // true
  console.log(Person.prototype.__proto__ === Object.prototype)   // true
  ```

  - 상세 설명(`.__proto__`와 `.protytype`은 다르다는 것을 염두에 둬야 한다.)
    - 함수를 생성하는 생성자 함수 `Funcion()`은 생성 되는 순간, 앞으로 `Function()` 생성자 함수로 생성될 모든 함수들의 프로토타입이 될 `Function.prototype`이 함께 생성된다.
    - `Function.prototype`은 프로토타입 객체이므로 모든 객체의 부모 객체인 `Object.prototype`을 프로토타입으로 갖는다.
    - `Person()` 생성자 함수는 `Function()` 생성자 함수를 통해 생성되는 순간 `Person`생성자 함수로 생성될 모든 객체들의 프로토타입이 될 `Person.prototype`이 함께 생성되고 `Person.prototype`는 `Person()`이 생성되면서 생성되었으므로 consturctor는 Person을 가리킨다.
    - `Person()` 생성자 함수는 `Function()` 생성자 함수를 통해 생성되었으므로 `Person()` 생성자함수의 프로토타입은 `Function.prototype`이 된다.
    - `cha` 객체는 `Person()` 생성자 함수를 통해 생성되었으므로 `cha` 객체의 프로토타입은 `Person.prototype`이 된다.
    - `Person()`생성자 함수는 프로토타입 프로퍼티로 `Person.prototype`을 가지고,  `Person.prototype`은 프로퍼티로 `Object.prototype`을 가진다.




- 프로토타입 체인의 종점(End of prototype chain)
  - 객체 리터럴 방식이나 생성자 함수 방식 모두 결국은 모든 객체의 부모 객체인 Object.prototype 객체에서 프로토타입 체인이 끝나게 된다.
  - 이 때문에 **Object.prototype**객체를 **프로토타입 체인의 종점(End of prototype chain)**이라 한다.



- 프로토타입 객체의 확장

  - 프로토타입 객체도 객체이므로 일반 객체와 같이 프로퍼티를 추가/삭제할 수 있다.
  - 그리고 이렇게 추가/삭제 된 프로퍼티는 즉시 프로토타입 체인에 반영된다.
    - 아래 예시에서 `cha` 객체가 생성될 때에는 `Person()` 생성자 함수에 `work()`라는 함수가 없었다.
    - 그러나 추가하자마자 별도의 수정 없이 `cha` 객체에서도 `work()` 메서드를 사용 가능하다.

  ```javascript
  function Person(name) {
      this.name = name
  }
  
  var cha = new Person('Cha')
  
  Person.prototype.work = function(){
      console.log("Working")
  }
  
  cha.work()
  ```

  

- 원시 타입의 확장

  - 자바스크립트에서 원시 타입을 제외한 모든 것은 객체이다.
  - 원시 타입은 객체가 아니므로 프로퍼티나 메서드를 가질 수 없다.
  - 그러나 원시 타입으로 프로퍼티나 메서드를 호출할 때 원시 타입과 연관된 객체로 일시적으로 변환되어 프로토타입 객체를 공유하게 된다.

  ```javascript
  // 원시 타입 문자열
  var str = 'test'
  console.log(typeof str)              		// string
  console.log(str.constructor === String)     // true            
  
  // String() 생성자 함수로 생성한 문자열 객체
  var strObj = new String('test')
  console.log(typeof strObj)         			// object        
  console.log(strObj.constructor === String)	// true
  
  // 메서드를 사용 가능하다.
  console.log(str.toUpperCase())				// TEST
  console.log(strObj.toUpperCase())			// TEST
  ```

  - 원시타입은 객체가 아니므로 프로퍼티나 메서드를 직접 추가할 수 없다.

  ```javascript
  var str = 'test';
  
  // 에러가 발생하지는 않는다.
  str.someMethod = function () {
    console.log('Add method')
  };
  
  str.someMethod()  // Uncaught TypeError: str.someMethod is not a function
  ```

  - 그러나 String 객체의 프로토타입 객체 `String.prototype`에 메서드를 추가하면 원시 타입, 객체 모두 메서드를 사용할 수 있다.
    - `Number.prototype` 등 다른 객체의 프로토타입 객에 역시 마찬가지다.
    - 자바스크립트는 표준 내장 객체의 프로토타입 객체에 개발자가 정의한 메서드의 추가를 허용한다.

  ```javascript
  var str = 'test';
  
  String.prototype.someMethod = function () {
    return 'Add method'
  };
  
  console.log(str.someMethod())	// Add method
  
  // 원시 타입으로 프로퍼티나 메서드를 호출할 때 원시 타입과 연관된 객체로 일시적으로 변환되어 프로토타입 객체를 공유하게 된다.
  console.log(str.__proto__ === String.prototype);                 // true
  console.log(String.prototype.__proto__  === Object.prototype);   // true
  console.log(String.prototype.constructor === String);            // true
  console.log(String.__proto__ === Function.prototype);            // true
  console.log(Function.prototype.__proto__  === Object.prototype); // true
  ```

  

- 프로토타입 객체의 변경

  - 객체를 생성할 때 프로토타입이 결정된다.
  - 결정된 프로토타입 객체는 다른 임의의 객체로 변경할 수 있다.
  - 이러한 특징을 활용하여 객체의 상속을 구현할 수 있다.
  - 주의점
    - 프로토타입 객체 변경 시점 이전에 생성된 객체는 기존 프로토타입 객체를 [[Prototype]]에 바인딩한다.
    - 프로토타입 객체 변경 시점 이후에 생성된 객체는 변경된 프로토타입 객체를 [[Prototype]]에 바인딩한다.

  ```javascript
  function Person(name) {
      this.name = name;
    }
    
  var cha = new Person('Cha');
  
  // 프로토타입 객체의 변경
  Person.prototype = { age: 28 };
  
  var kim = new Person('Kim');
  
  console.log(cha.gender); // undefined
  console.log(kim.gender); // male
  
  // 프로토타입 객체가 변경되기 이전에는 Person()생성자 함수로 생성된 객체의 constructor는 Person() 생성자 함수를 가리킨다.
  console.log(cha.constructor); // [Function: Person]
  // 프로토타입 객체가 일반 객체 { age : 24 }로 변경되면서 Person.prototype.constructor 프로퍼티도 삭제된다.
  // 따라서 kim.constructor의 값은 프로토타입 체인에 의해 Object.prototype.constructor 즉 Object() 생성자 함수가 된다.
  console.log(kim.constructor); // [Function: Object]
  ```



- 프로토타입 체인 동작 조건

  - 객체의 프로퍼티를 참조하는 경우, 해당 객체에 참조하려는 프로퍼티가 없으면 프로토타입 체인이 동작한다.
  - 객체의 프로퍼티에 값을 할당하는 경우에는 프로토타입 체인이 동작하지 않는다.
    - 객체에 해당 프로퍼티가 있는 경우에는 값을 재할당하고
    - 해당 프로퍼티가 없는 경우에는 해당 객체에 프로퍼티를 동적으로 추가하기 때문이다.
  - 예시 설명
    - 아래에서 `cha`, `kim` 객체에는 `age`라는 참조하려는 프로퍼티가 존재하지 않는다.
    - `age`는 `Person.prototype` 객체에만 존재한다.
    - 따라서  `cha`, `kim`객체는 프로토타입 체인에 따라 `age`프로퍼티에 접근할 수 있다.
    - 그런데 `cha` 객체에 `age` 프로퍼티를 할당하면 더 이상 `cha` 객체는 프로토타입 체인을 따라기지 않는다.

  ```javascript
  function Person(name) {
      this.name = name
  }
  
  Person.prototype.age = 28
  
  var cha = new Person('Cha')
  var kim = new Person('Kim')
  
  
  console.log(cha.age)	// 28
  console.log(kim.age)	// 28
  
  // cha 객체에 age 프로퍼티가 없으면 프로퍼티 동적 추가
  // cha 객체에 age 프로퍼티가 있으면 해당 프로퍼티에 값 할당
  cha.age = 20
  
  // 이제 cha 객체에 age라는 프로퍼티가 생겼으므로, 즉 참조하려는 프로퍼티가 있으므로, 프로토타입 체인이 동작하지 않는다.
  console.log(cha.age)	// 20
  console.log(kim.age)	// 28
  ```
