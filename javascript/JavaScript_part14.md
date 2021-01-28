# ECMAScript

## Symbol

- 심볼
  - ES6에서 새롭게 추가된 7번째 타입으로 변경 불가능한 원시 타입의 값.
  - 주로 이름의 충돌 위험이 없는 유일한 객체의 프로퍼티 키(property key)를 만들기 위해 사용한다.



- 심볼 생성

  - `Symbol()` 함수로 생성한다. 
    - `Symbol()` 함수는 호출될 때마다 Symbol 값을 생성한다. 
    - 이때 생성된 Symbol은 객체가 아니라 변경 불가능한 원시 타입의 값이다.

  ```javascript
  // 심볼 mySymbol은 이름의 충돌 위험이 없는 유일한 프로퍼티 키
  let mySymbol = Symbol()
  
  console.log(mySymbol)        // Symbol()
  console.log(typeof mySymbol) // symbol
  ```

  - Symbol() 함수는 String, Number, Boolean과 같이 래퍼 객체를 생성하는 생성자 함수와는 달리 `new` 연산자를 사용하지 않는다.

  ```javascript
  new Symbol() 	// TypeError: Symbol is not a constructor
  ```

  - Symbol() 함수에는 문자열을 인자로 전달할 수 있다. 
    - 이 문자열은 Symbol 생성에 어떠한 영향을 주지 않으며 다만 생성된 Symbol에 대한 설명(description)으로 디버깅 용도로만 사용된다.

  ```javascript
  let symbolWithDesc = Symbol('ungmo2')
  
  console.log(symbolWithDesc) 					 // Symbol(ungmo2)
  console.log(symbolWithDesc === Symbol('ungmo2')) // false
  ```

  

- 심볼의 사용

  - 객체의 프로퍼티 키는 빈 문자열을 포함하는 모든 문자열로 만들 수 있다.
  - Symbol 값도 객체의 프로퍼티 키로 사용할 수 있다. 
    - Symbol 값은 유일한 값이므로 Symbol 값을 키로 갖는 프로퍼티는 다른 어떠한 프로퍼티와도 충돌하지 않는다.

  ```javascript
  const obj = {}
  
  const mySymbol = Symbol('mySymbol')
  obj[mySymbol] = 123
  
  console.log(obj) 			// { [Symbol(mySymbol)]: 123 }
  console.log(obj[mySymbol]) 	// 123
  ```



- 심볼 객체

  - Symbol() 함수로 Symbol 값을 생성할 수 있었다. 
    - 이것은 Symbol이 함수 객체라는 의미이다.
  - Symbol 객체는 프로퍼티와 메소드를 가지고 있다. 
    - Symbol 객체의 프로퍼티 중에 length와 prototype을 제외한 프로퍼티를 `Well-Known Symbol`이라 부른다.
  - `Symbol.iterator`
    - `Well-Known Symbol`은 자바스크립트 엔진에 상수로 존재하며 자바스크립트 엔진은 `Well-Known Symbol`을 참조하여 일정한 처리를 한다. 
    - 예를 들어 어떤 객체가 `Symbol.iterator`를 프로퍼티 key로 사용한 메소드 가지고 있으면, 자바스크립트 엔진은 이 객체가 이터레이션 프로토콜을 따르는 것으로 간주하고 이터레이터로 동작하도록 한다.
    - `Symbol.iterator`를 프로퍼티 key로 사용하여 메소드를 구현하고 있는 빌트인 객체(빌트인 이터러블)는 다음과 같다.
    - Array, String, Map, Set, DOM data structures, arguments
    - 위 객체들은 이터레이션 프로토콜을 준수하고 있으며 이터러이터를 반환한다.

  ```javascript
  // 이터러블
  // Symbol.iterator를 프로퍼티 key로 사용한 메소드를 구현하여야 한다.
  // 배열에는 Array.prototype[Symbol.iterator] 메소드가 구현되어 있다.
  const iterable = ['a', 'b', 'c']
  
  // 이터레이터
  // 이터러블의 Symbol.iterator를 프로퍼티 key로 사용한 메소드는 이터레이터를 반환한다.
  const iterator = iterable[Symbol.iterator]()
  
  // 이터레이터는 순회 가능한 자료 구조인 이터러블의 요소를 탐색하기 위한 포인터로서 value, done 프로퍼티를 갖는 객체를 반환하는 next() 함수를 메소드로 갖는 객체이다. 이터레이터의 next() 메소드를 통해 이터러블 객체를 순회할 수 있다.
  console.log(iterator.next()) 	// { value: 'a', done: false }
  console.log(iterator.next()) 	// { value: 'b', done: false }
  console.log(iterator.next()) 	// { value: 'c', done: false }
  console.log(iterator.next()) 	// { value: undefined, done: true }
  ```

  - `Symbol.for`
    - 인자로 전달받은 문자열을 키로 사용하여 Symbol 값들이 저장되어 있는 전역 Symbol 레지스트리에서 해당 키와 일치하는 저장된 Symbol 값을 검색한다. 
    - 이때 검색에 성공하면 검색된 Symbol 값을 반환하고, 검색에 실패하면 새로운 Symbol 값을 생성하여 해당 키로 전역 Symbol 레지스트리에 저장한 후, Symbol 값을 반환한다.
    - Symbol 함수는 매번 다른 Symbol 값을 생성하는 것에 반해, `Symbol.for` 메소드는 하나의 Symbol을 생성하여 여러 모듈이 키를 통해 같은 Symbol을 공유할 수 있다.
    - `Symbol.for` 메소드를 통해 생성된 Symbol 값은 반드시 키를 갖는다. 이에 반해 Symbol 함수를 통해 생성된 Symbol 값은 키가 없다.

  ```javascript
  // 전역 Symbol 레지스트리에 foo라는 키로 저장된 Symbol이 없으면 새로운 Symbol 생성
  const s1 = Symbol.for('foo')
  // 전역 Symbol 레지스트리에 foo라는 키로 저장된 Symbol이 있으면 해당 Symbol을 반환
  const s2 = Symbol.for('foo')
  
  console.log(s1 === s2) // true
  
  
  const shareSymbol = Symbol.for('myKey')
  const key1 = Symbol.keyFor(shareSymbol)
  console.log(key1) // myKey
  
  const unsharedSymbol = Symbol('myKey')
  const key2 = Symbol.keyFor(unsharedSymbol)
  console.log(key2) // undefined
  ```





## 객체리터럴 프로퍼티 기능 확장

- 프로퍼티 축약 표현

  - 객체 리터럴의 프로퍼티는 프로퍼티 이름과 프로퍼티 값으로 구성된다. 
    - 프로퍼티의 값은 변수에 할당된 값일 수도 있다.

  ```javascript
  var a = 1
  var b = 2
  var obj = {
      a:a,
      b:b
  }
  console.log(obj)	// { a: 1, b: 2 }
  ```

  - ES6에서는 프로퍼티 값으로 변수를 사용하는 경우, 프로퍼티 이름을 생략(Property shorthand)할 수 있다. 
    - 이때 프로퍼티 이름은 변수의 이름으로 자동 생성된다.

  ```javascript
  var a = 1
  var b = 2
  var obj = {
      a,
      b
  }
  console.log(obj)	// { a: 1, b: 2 }
  ```

  

- 프로퍼티 키 동적 생성

  - 문자열 또는 문자열로 변환 가능한 값을 반환하는 표현식을 사용해 프로퍼티 키를 동적으로 생성할 수 있다. 
  - 단, 프로퍼티 키로 사용할 표현식을 대괄호([…])로 묶어야 한다. 
  - 이를 **계산된 프로퍼티 이름(Computed property name)**이라 한다.
  - ES5에서 프로퍼티 키를 동적으로 생성하려면 객체 리터럴 외부에서 대괄호([…]) 표기법을 사용해야 한다.

  ```javascript
  var obj = {}
  var str = 'str'
  var cnt = 0
  
  obj['a'] = cnt
  obj[str+'-'+ ++cnt] = cnt
  obj[123] = '일이삼'
  console.log(obj)	// { '123': '일이삼', a: 0, 'str-1': 1 }
  ```

  - ES6에서는 객체 리터럴 내부에서도 프로퍼티 키를 동적으로 생성할 수 있다.

  ```javascript
  var str = 'str'
  var cnt = 0
  
  var obj = {
      ['a']: cnt,
      [str+'-'+ ++cnt]: cnt,
      [123]: '일이삼'
  }
  console.log(obj)    // { '123': '일이삼', a: 0, 'str-1': 1 }
  ```

  

- 메소드 축약 표현

  - ES5에서 메소드를 선언하려면 프로퍼티 값으로 함수 선언식을 할당한다.

  ```javascript
  var obj = {
    name: 'Cha',
    sayHi: function() {
      console.log('Hi! ' + this.name);
    }
  }
  
  obj.sayHi() // Hi! Cha
  ```

  - ES6에서는 메소드를 선언할 때, `function` 키워드를 생략한 축약 표현을 사용할 수 있다.

  ```javascript
  const obj = {
    name: 'Cha',
    // 메소드 축약 표현
    sayHi() {
      console.log('Hi! ' + this.name)
    }
  }
  
  obj.sayHi() // Hi! Cha
  ```



- `__proto__` 프로퍼티에 의한 상속

  - ES5에서 객체 리터럴을 상속하기 위해서는 `Object.create()` 함수를 사용한다. 이를 프로토타입 패턴 상속이라 한다.

  ```javascript
  var parent = {
    name: 'parent',
    sayHi: function() {
      console.log('Hi! ' + this.name)
    }
  }
  
  // 프로토타입 패턴 상속
  var child = Object.create(parent)
  child.name = 'child'
  
  parent.sayHi() // Hi! parent
  child.sayHi()  // Hi! child
  ```

  - ES6에서는 객체 리터럴 내부에서 `__proto__` 프로퍼티를 직접 설정할 수 있다. 
    - 이것은 객체 리터럴에 의해 생성된 객체의 `__proto__` 프로퍼티에 다른 객체를 직접 바인딩하여 상속을 표현할 수 있음을 의미한다.

  ```javascript
  const parent = {
    name: 'parent'
    sayHi() {
      console.log('Hi! ' + this.name)
    }
  }
  
  const child = {
    // child 객체의 프로토타입 객체에 parent 객체를 바인딩하여 상속을 구현한다.
    __proto__: parent,
    name: 'child'
  }
  
  parent.sayHi() // Hi! parent
  child.sayHi()  // Hi! child
  ```





## 디스트럭처링

- 디스트럭처링(Destructuring)
  - 구조화된 배열 또는 객체를 Destructuring(비구조화, 파괴)하여 개별적인 변수에 할당하는 것이다. 
  - 배열 또는 객체 리터럴에서 필요한 값만을 추출하여 변수에 할당하거나 반환할 때 유용하다.



- 배열 디스트렁처링

  - ES5에서 배열의 각 요소를 배열로부터 디스트럭처링하여 변수에 할당하기 위한 방법은 아래와 같다.

  ```javascript
  var arr = [1, 2, 3]
  
  var a = arr[0]
  var b = arr[1]
  var c = arr[2]
  
  console.log(a, b, c) // 1 2 3
  ```

  - ES6의 배열 디스트럭처링은 배열의 각 요소를 배열로부터 추출하여 변수 리스트에 할당한다. 
    - 이때 추출/할당 기준은 **배열의 인덱스**이다.
    - 배열 디스트럭처링을 위해서는 할당 연산자 왼쪽에 배열 형태의 변수 리스트가 필요하다.

  ```javascript
  const arr = [1, 2, 3]
  
  // 배열의 인덱스를 기준으로 배열로부터 요소를 추출하여 변수에 할당
  // 변수 a, b, c 선언되고 arr(initializer(초기화자))가 Destructuring(비구조화, 파괴)되어 할당된다.
  const [a, b, c] = arr
  
  // 디스트럭처링을 사용할 때는 반드시 initializer(초기화자)를 할당해야 한다.
  const [a, b, c] 	// SyntaxError: Missing initializer in destructuring declaration
  
  console.log(a, b, c) // 1 2 3
  
  
  let x, y, z;
  [x, y, z] = [1, 2, 3];
  
  // 위의 구문과 동치이다.
  let [x, y, z] = [1, 2, 3];
  ```

  - 기본값을 주는 것이 가능하다.
    - 단, 기본 값을 준 변수의 인덱스에 해당하는 값이 있을 경우 기본값은 무시된다.

  ```javascript
  // 기본값
  var [x, y, z = 5] = [1, 2]
  console.log(x, y, z)    // 1 2 3
  
  // 기본값이 무시된다.
  var [x, y, z = 5] = [1, 2, 3]
  console.log(x, y, z)    // 1 2 5
  ```

  - 개수가 맞지 않을 경우

  ```javascript
  // 넘칠 경우
  var [x, y, z] = [1,2,3,4]
  console.log(x,y,z)  // 1 2 3
  
  // 모자랄 경우
  var [x, y, z] = [1,2]
  console.log(x,y,z)  // 1 2 undefined
  ```

  - Spread 문법을 사용 가능하다.

  ```javascript
  [x, ...y] = [1, 2, 3]
  console.log(x, y) 	// 1 [ 2, 3 ]
  ```

  

- 객체 디스트럭처링

  - 객체의 각 프로퍼티를 객체로부터 디스트럭처링하여 변수에 할당하기 위해서는 프로퍼티 이름(키)을 사용해야 한다.

  ```javascript
  var obj = { firstName: 'GilDong', lastName: 'Hong' }
  
  var firstName = obj.firstName
  var lastName  = obj.lastName
  
  console.log(firstName, lastName) // GilDong Hong
  ```

  - ES6의 객체 디스트럭처링은 객체의 각 프로퍼티를 객체로부터 추출하여 변수 리스트에 할당한다. 
    - 이때 할당 기준은 **프로퍼티 이름(키)**이다.

  ```javascript
  var obj = { firstName: 'GilDong', lastName: 'Hong' };
  
  // 프로퍼티 키를 기준으로 디스트럭처링 할당이 이루어진다. 순서는 의미가 없다.
  // 변수 lastName, firstName가 선언되고 obj(initializer(초기화자))가 Destructuring(비구조화, 파괴)되어 할당된다.
  var { lastName, firstName } = obj
  
  console.log(firstName, lastName) // GilDong Hong
  ```

  - 키와 값을 함께 디스트럭처링 하는 것도 가능하다.

  ```javascript
  const { prop1: p1, prop2: p2 } = { prop1: 'a', prop2: 'b' }
  console.log(p1, p2) // 'a' 'b'
  console.log({ prop1: p1, prop2: p2 }) // { prop1: 'a', prop2: 'b' }
  
  // 축약형
  const { prop1, prop2 } = { prop1: 'a', prop2: 'b' }
  console.log({ prop1, prop2 }) // { prop1: 'a', prop2: 'b' }
  ```

  - 기본값을 주는 것도 가능하다.
    - 배열과 마찬가지로 해당하는 키가 있으면 기본값이 무시된다.

  ```javascript
  const { prop1, prop2, prop3 = 'c' } = { prop1: 'a', prop2: 'b' }
  console.log({ prop1, prop2, prop3 }) 	// { prop1: 'a', prop2: 'b', prop3: 'c' }
  
  // 기본값 무시
  const { prop1, prop2, prop3 = 'c' } = { prop1: 'a', prop2: 'b', prop3: 'd' }
  console.log({ prop1, prop2, prop3 }) 
  ```

  - 중첩 객체에서의 활용

  ```javascript
  const person = {
    name: 'Lee',
    address: {
      zipCode: '03068',
      city: 'Seoul'
    }
  }
  
  const { address: { city } } = person
  console.log(city) // 'Seoul'
  ```

  - 매개변수로도 사용 가능하다.

  ```javascript
  const todos = [
      { id: 1, content: 'HTML', completed: true },
      { id: 2, content: 'CSS', completed: false },
      { id: 3, content: 'JS', completed: false }
  ]
  
  // filter 메소드의 콜백 함수는 대상 배열(todos)을 순회하며 첫 번째 인자로 대상 배열의 요소를 받는다.  
  // todos 배열의 요소인 객체로부터 completed 프로퍼티만을 추출한다.
  // var { completed } = { id: 1, content: 'HTML', completed: true }
  // var { completed } = { id: 2, content: 'CSS', completed: false }
  // var { completed } = { id: 3, content: 'JS', completed: false }
  const completedTodos = todos.filter(function({ completed }) {
      console.log(completed)
      console.log({completed})
      return completed
  })
  console.log(completedTodos) // [ { id: 1, content: 'HTML', completed: true } ]
  ```





## etc

- 매개변수 기본값

  - 함수를 호출할 때는 매개변수의 개수만큼 인수를 전달하는 것이 일반적이지만 그렇지 않은 경우에도 에러가 발생하지는 않는다.
  - 함수는 매개변수의 개수와 인수의 개수를 체크하지 않는다. 
  - 인수가 부족한 경우, 매개변수의 값은 undefined이다.

  ```javascript
  function foo(a,b){
      console.log(a,b)	// 1 undefined
  }
  
  foo(1)
  ```

  - 따라서 매개변수에 적절한 인수가 전달되었는지 함수 내부에서 확인할 필요가 있다.

  ```javascript
  function foo(a, b) {
    // 매개변수의 값이 falsy value인 경우, 기본값을 할당한다.
    a = a || 0
    b = b || 0
  
    console.log(a,b)		// 1 0
  }
  
  foo(1)
  ```

  - ES6에서는 매개변수 기본값을 사용하여 함수 내에서 수행하던 인수 체크 및 초기화를 간소화할 수 있다. 
    - 매개변수 기본값은 매개변수에 인수를 전달하지 않았을 경우에만 유효하다.
    - 매개변수 기본값은 함수 정의 시 선언한 매개변수 개수를 나타내는 함수 객체의 `length` 프로퍼티와 `arguments` 객체에 영향을 주지 않는다.

  ```javascript
  function foo(a, b = 0) {
    console.log(arguments)
  }
  
  console.log(foo.length) // 1
  
  sum(1)    // Arguments { '0': 1 }
  sum(1, 2) // Arguments { '0': 1, '1': 2 }
  ```



- Rest 파라미터

  - Rest 파라미터(Rest Parameter, 나머지 매개변수)는 매개변수 이름 앞에 세개의 점 `...`을 붙여서 정의한 매개변수를 의미한다. 
  - Rest 파라미터는 함수에 전달된 인수들의 목록을 배열로 전달받는다.

  ```javascript
  function foo(...rest) {
    console.log(Array.isArray(rest)) // true
    console.log(rest) // [ 1, 2, 3, 4, 5 ]
  }
  
  foo(1, 2, 3, 4, 5)
  ```

  - 함수에 전달된 인수들은 순차적으로 파라미터와 Rest 파라미터에 할당된다.
    - Rest 파라미터는 이름 그대로 먼저 선언된 파라미터에 할당된 인수를 제외한 나머지 인수들이 모두 배열에 담겨 할당된다. 
    - 따라서 Rest 파라미터는 반드시 마지막 파라미터이어야 한다.

  ```javascript
  function foo(a,b,...rest){
      console.log(a,b,rest)	// 1 2 [ 3, 4, 5 ]
  }
  foo(1,2,3,4,5)
  ```

  - Rest 파라미터는 함수 정의 시 선언한 매개변수 개수를 나타내는 함수 객체의 length 프로퍼티에 영향을 주지 않는다.

  ```javascript
  function foo(...rest){}
  console.log(foo.length) // 0
  ```



- arguments와 rest 파라미터
  - arguments
    - ES5에서는 인자의 개수를 사전에 알 수 없는 가변 인자 함수의 경우, arguments 객체를 통해 인수를 확인한다. 
    - arguments 객체는 함수 호출 시 전달된 인수(argument)들의 정보를 담고 있는 순회가능한(iterable) 유사 배열 객체(array-like object)이며 함수 내부에서 지역 변수처럼 사용할 수 있다.
    - arguments 프로퍼티는 현재 일부 브라우저에서 지원하고 있지만 ES3부터 표준에서 deprecated 되었다. 
    - `Function.arguments`와 같은 사용 방법은 권장되지 않으며, 함수 내부에서 지역변수처럼 사용할 수 있는 arguments 객체를 참조하도록 한다.
    - arguments 객체는 유사 배열 객체이므로 배열 메소드를 사용하려면 `Function.prototype.call`을 사용해야 하는 번거로움이 있다.
  - rest 파라미터
    - 가변 인자의 목록을 **배열**로 전달받을 수 있다. 
    - 이를 통해 유사 배열인 arguments 객체를 배열로 변환하는 번거로움을 피할 수 있다.
    - 또한 ES6의 화살표 함수에는 함수 객체의 arguments 프로퍼티가 없다.
    - 따라서 화살표 함수로 가변 인자 함수를 구현해야 할 때는 반드시 rest 파라미터를 사용해야 한다.



- Spread 문법

  - 대상을 개별 요소로 분리한다.
  - 대상은 이터러블이어야 한다.
    - 배열, 문자열, `Map`, `Set` 등은 이터러블이므로 가능하다.
    - 일반 객체는 이터러블이 아니므로 불가능하다.

  ```javascript
  console.log(...[1,2,3])	// 1 2 3
  console.log(...'Cha')	// C h a
  ```

  - 함수의 인수로 사용하는 경우
    - 배열을 분해하여 배열의 각 요소를 파라미터에 전달하고 싶은 경우, `Function.prototype.apply`를 사용하는 것이 일반적이다.
    - ES6의 Spread 문법(…)을 사용한 배열을 인수로 함수에 전달하면 배열의 요소를 분해하여 순차적으로 파라미터에 할당한다.

  ```javascript
  // apply 사용
  function foo(a,b,c){
      console.log(a,b,c)	// 1 2 3
  }
  
  const arr = [1,2,3]
  foo.apply(null,arr)
  
  // Spread 문법 사용
  foo(...arr)
  ```

  - Rest 파라미터는 결국 Spread 문법을 사용한 것이다.
    - Spread 문법은 rest 파라미터와 달리 마지막 인수일 필요는 없다.

  ```javascript
  function foo(a,b,c,d,e){
      console.log(a,b,c,d,e)	// 1 2 3 4 5
  }
  
  foo(1,...[2,3],...[4,5])
  ```

  - 배열에서 사용하는 경우
    - `concat` 메소드 대신 사용이 가능하다.
    - `push` 메소드 대신 사용이 가능하다.
    - `splice` 메소드 대신 사용이 가능하다.
    - `slice` 메소드 대신 사용이 가능하다.

  ```javascript
  // concat
  var arr = [1,2,3]
  console.log(arr.concat([4,5,6]))    // [ 1, 2, 3, 4, 5, 6 ]
  
  // Spread
  console.log([...arr,4,5,6])         // [ 1, 2, 3, 4, 5, 6 ]
  
  
  // push
  var arr1 = [1,2,3]
  var arr2 = [4,5,6]
  Array.prototype.push.apply(arr1,arr2)
  console.log(arr1)       // [ 1, 2, 3, 4, 5, 6 ]
  
  // Spread
  var arr3 = [1,2,3]
  var arr4 = [4,5,6]
  arr3.push(...arr4)
  console.log(arr3)       // [ 1, 2, 3, 4, 5, 6 ]
  
  
  //splice
  var arr1 = [1, 2, 3, 6]
  var arr2 = [4, 5]
  /*
  apply 메소드의 2번째 인자는 배열. 이것은 개별 인자로 splice 메소드에 전달된다.
  [3, 0].concat(arr2) → [3, 0, 4, 5]
  arr1.splice(3, 0, 4, 5) → arr1[3]부터 0개의 요소를 제거하고 그자리(arr1[3])에 새로운 요소(4, 5)를 추가한다.
  */
  Array.prototype.splice.apply(arr1, [3, 0].concat(arr2))
  
  console.log(arr1) // [ 1, 2, 3, 4, 5, 6 ]
  
  // Spread
  var arr3 = [1, 2, 3, 6]
  var arr4 = [4, 5]
  // ...arr2는 [4, 5]을 개별 요소로 분리한다
  arr3.splice(3, 0, ...arr4) // == arr1.splice(3, 0, 4, 5);
  console.log(arr3) // [ 1, 2, 3, 4, 5, 6 ]
  
  
  // copy
  var arr  = [1, 2, 3]
  var copy = arr.slice()
  console.log(copy) // [ 1, 2, 3 ]
  // copy를 변경한다.
  copy.push(4)
  console.log(copy) // [ 1, 2, 3, 4 ]
  // arr은 변경되지 않는다.
  console.log(arr)  // [ 1, 2, 3 ]
  
  // Spread
  var arr = [1, 2, 3]
  // ...arr은 [1, 2, 3]을 개별 요소로 분리한다
  var copy = [...arr]
  console.log(copy) // [ 1, 2, 3 ]
  // copy를 변경한다.
  copy.push(4)
  console.log(copy) // [ 1, 2, 3, 4 ]
  // arr은 변경되지 않는다.
  console.log(arr)  // [ 1, 2, 3 ]
  ```

  - 유사 배열 객체를 배열로 손쉽게 변환할 수 있다.

  ```javascript
  const htmlCollection = document.getElementsByTagName('li')
  
  // 유사 배열인 HTMLCollection을 배열로 변환한다.
  const newArray = [...htmlCollection] // Spread 문법
  ```

  

  

  