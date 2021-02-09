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
  
  const { address: { city } } = person;
  console.log(city); // 'Seoul'
  const { address: qwe } = person;
console.log(qwe)	// { zipCode: '03068', city: 'Seoul' }
  ```

  - 매개변수로도 사용 가능하다.
  
  ```javascript
  const obj = {
    name: "Cha",
    age: 28,
  };
  
  function foo({ age }) {
    console.log(age);
  }
  
  foo(obj);	// 28
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





# Device Orientation

- Device Orientation

  - HTML5가 제공하는 기능으로 중력과의 관계에서 디바이스의 물리적 방향의 변화를 감지할 수 있다. 
  - 이것을 이용하면 모바일 디바이스를 회전시켰을 때 이벤트를 감지하여 적절히 화면을 변화 시킬 수 있다.
  - 디바이스의 방향 정보를 다루는 자바스크립트 이벤트는 두가지가 있다.
    - `DeviceOrientationEvent` 가속도계(accelerometer)가 기기의 방향의 변화를 감지했을 때 발생한다.
    - `DeviceMotionEvent` 가속도에 변화가 일어났을 때 발생한다.
  - 현재 사파리를 제외한 대부분의 브라우저에서 사용할 수 있다.
  - 하지만 오래된 브라우저를 사용하는 사용자를 위해 브라우저의 이벤트 지원 여부를 먼저 확인할 필요가 있다.

  ```javascript
  if (window.DeviceOrientationEvent) {
    console.log(Our browser supports DeviceOrientation)
  } else {
    console.log("Sorry, your browser doesn't support Device Orientation")
  }
  ```

  

- `DeviceOrientationEvent`

  - 디바이스의 방향 변화는 3개의 각도( alpha, beta, gamma )를 사용하여 측정된다. 
  - `deviceorientation` 이벤트에 리스너를 등록하면 리스너 함수가 주기적으로 호출되어 업데이트된 방향 데이터를 제공한다. 
  - `deviceorientation` 이벤트는 다음 4가지의 값을 가진다.
    - DeviceOrientationEvent.absolute: 지구좌표계(Earth coordinate system)을 사용하는 지에 대한 boolean 값이다. 일반적인 경우 사용하지 않는다.
    - DeviceOrientationEvent.alpha: 0도부터 360도까지 범위의 z축을 중심으로 디바이스의 움직임을 나타낸다.
    - DeviceOrientationEvent.beta: -180도부터 180도(모바일 사파리: -90도~90도)까지 범위의 x축을 중심으로 디바이스의 움직임을 나타낸다. 이는 디바이스의 앞뒤 움직임을 나타낸다.
    - DeviceOrientationEvent.gamma: -90도부터 90도(모바일 사파리: -180도~180도)까지 범위의 y축을 중심으로 디바이스의 움직임을 나타낸다. 이는 디바이스의 좌우 움직임을 나타낸다.

  ```javascript
  window.addEventListener('deviceorientation', handleOrientation, false)
  
  function handleOrientation(event) {
      var absolute = event.absolute;
      var alpha    = event.alpha;
      var beta     = event.beta;
      var gamma    = event.gamma;
      // Do stuff with the new orientation data
  }
  ```

  



# REST API

- REST(Representational State Transfer)
  - HTTP/1.0과 1.1의 스펙 작성에 참여하였고, 아파치 HTTP 서버 프로젝트의 공동설립자인 로이 필딩 (Roy Fielding)의 2000년 논문에서 처음 소개되었다.
  - 발표 당시의 웹이 HTTP의 설계 상 우수성을 제대로 사용하지 못하고 있는 상황을 보고 웹의 장점을 최대한 활용할 수 있는 아키텍쳐로서 REST를 소개하였고 이는 HTTP 프로토콜을 의도에 맞게 디자인하도록 유도하고 있다.
  - REST의 기본 원칙을 성실히 지킨 서비스 디자인을 “RESTful”이라고 표현한다.



- REST API 중심 규칙

  - 가장 중요한 기본적인 규칙 두 가지는 **URI는 자원을 표현하는 데에 집중**하고 **행위에 대한 정의는 HTTP Method를 통해 해야 한다**는 것이다.

  - URI는 정보의 자원을 표현해야 한다.

    - 리소스명은 동사보다는 명사를 사용한다. 
    - URI는 자원을 표현하는데 중점을 두어야 한다. 
    - get 같은 행위에 대한 표현이 들어가서는 안된다.

    ```
    # bad
    GET /getTodos/1		// 행위 표현이 들어갔다.
    GET /todos/show/1   // 행위 표현이 들어갔다.
    
    
    # good
    GET /todos/1
    ```

  - 자원에 대한 행위는 HTTP Method로 표현한다.

    ```
    # bad
    GET /todos/delete/1
    
    # good
    DELETE /todos/1
    ```

    

- HTTP Method

  - 주로 5가지의 Method를 사용하여 CRUD를 구현한다.

  | Method | Action         | 역할                    | 페이로드(데이터) |
  | ------ | -------------- | ----------------------- | ---------------- |
  | GET    | index/retrieve | 모든/특정 리소스를 조회 | X                |
  | POST   | create         | 리소스를 생성           | O                |
  | PUT    | replace        | 리소스의 전체를 교체    | O                |
  | PATCH  | modify         | 리소스의 일부를 수정    | O                |
  | DELETE | delete         | 모든/특정 리소스를 삭제 | X                |

  

- REST API의 구성

  - 자원(Resource), 행위(Verb), 표현(Representations)의 3가지 요소로 구성된다.
  - REST는 자체 표현 구조(Self-descriptiveness)로 구성되어 REST API만으로 요청을 이해할 수 있다.

  | 구성 요소       | 내용                    | 표현 방법             |
  | --------------- | ----------------------- | --------------------- |
  | Resource        | 자원                    | HTTP URI              |
  | Verb            | 자원에 대한 행위        | HTTP Method           |
  | Representations | 자원에 대한 행위의 내용 | HTTP Message Pay Load |

  



# SPA

- SPA(Single Page Application)
  - 단일 페이지 애플리케이션(Single Page Application, SPA)는 모던 웹의 패러다임이다. 
  - SPA는 기본적으로 단일 페이지로 구성되며 기존의 서버 사이드 렌더링과 비교할 때, 배포가 간단하며 네이티브 앱과 유사한 사용자 경험을 제공할 수 있다는 장점이 있다.
  - link tag를 사용하는 전통적인 웹 방식은 새로운 페이지 요청 시마다 정적 리소스가 다운로드되고 전체 페이지를 다시 렌더링하는 방식을 사용하므로 새로고침이 발생되어 사용성이 좋지 않다. 그리고 변경이 필요없는 부분를 포함하여 전체 페이지를 갱신하므로 비효율적이다.
  - SPA는 기본적으로 웹 애플리케이션에 필요한 모든 정적 리소스를 최초에 한번 다운로드한다. 이후 새로운 페이지 요청 시, 페이지 갱신에 필요한 데이터만을 전달받아 페이지를 갱신하므로 전체적인 트래픽을 감소할 수 있고, 전체 페이지를 다시 렌더링하지 않고 변경되는 부분만을 갱신하므로 새로고침이 발생하지 않아 네이티브 앱과 유사한 사용자 경험을 제공할 수 있다.
  - 모바일의 사용이 증가하고 있는 현 시점에 트래픽의 감소와 속도, 사용성, 반응성의 향상은 매우 중요한 이슈이다. SPA의 핵심 가치는 **사용자 경험(UX) 향상**에 있으며 부가적으로 애플리케이션 속도의 향상도 기대할 수 있어서 모바일 퍼스트(Mobile First) 전략에 부합한다.
  - 모든 소프트웨어 아키텍처에는 trade-off가 존재하며 모든 애플리케이션에 적합한 은탄환(Silver bullet)은 없듯이 SPA 또한 구조적인 단점을 가지고 있다. 대표적인 단점은 아래와 같다.
    - SPA는 웹 애플리케이션에 필요한 모든 정적 리소스를 최초에 한번 다운로드하기 때문에 초기 구동 속도가 상대적으로 느리다. 하지만 SPA는 웹페이지보다는 애플리케이션에 적합한 기술이므로 트래픽의 감소와 속도, 사용성, 반응성의 향상 등의 장점을 생각한다면 결정적인 단점이라고 할 수는 없다.
    - SPA는 서버 렌더링 방식이 아닌 자바스크립트 기반 비동기 모델(클라이언트 렌더링 방식)이다. 따라서 SEO(검색엔진 최적화)는 언제나 단점으로 부각되어 왔던 이슈이다. 하지만 SPA는 정보의 제공을 위한 웹페이지보다는 애플리케이션에 적합한 기술이므로 SEO 이슈는 심각한 문제로 볼 수 없다. Angular 또는 React 등의 SPA 프레임워크는 서버 렌더링을 지원하는 SEO 대응 기술이 이미 존재하고 있어 SEO 대응이 필요한 페이지에 대해서는 선별적 SEO 대응이 가능하다.



- Routing
  - 라우팅이란 출발지에서 목적지까지의 경로를 결정하는 기능이다. 
    - 애플리케이션의 라우팅은 사용자가 태스크를 수행하기 위해 어떤 화면(view)에서 다른 화면으로 화면을 전환하는 내비게이션을 관리하기 위한 기능을 의미한다.
    - 일반적으로 사용자자 요청한 URL 또는 이벤트를 해석하고 새로운 페이지로 전환하기 위한 데이터를 취득하기 위해 서버에 필요 데이터를 요청하고 화면을 전환하는 위한 일련의 행위를 말한다.
  - 브라우저가 화면을 전환하는 경우는 아래와 같다.
    - 브라우저의 주소창에 URL을 입력하면 해당 페이지로 이동한다.
    - 웹페이지의 링크를 클릭하면 해당 페이지로 이동한다.
    - 브라우저의 뒤로가기 또는 앞으로가기 버튼을 클릭하면 사용자가 방문한 웹페이지의 기록(history)의 뒤 또는 앞으로 이동한다.
  - AJAX 요청에 의해 서버로부터 데이터를 응답받아 화면을 생성하는 경우, 브라우저의 주소창의 URL은 변경되지 않는다. 
    - 이는 사용자의 방문 history를 관리할 수 없음을 의미하며, SEO(검색엔진 최적화) 이슈의 발생 원인이기도 하다. 
    - history 관리를 위해서는 각 페이지는 브라우저의 주소창에서 구별할 수 있는 유일한 URL을 소유하여야 한다.



- 전통적 링크 방식

  -  link tag로 동작하는 기본적인 웹페이지의 동작 방식이다.
  -  link tag(`<a href="service.html">Service</a>` 등)을 클릭하면 href 어트리뷰트의 값인 리소스의 경로가 URL의 path에 추가되어 주소창에 나타나고 해당 리소스를 서버에 요청된다.
  -  이때 서버는 html로 화면을 표시하는데 부족함이 없는 완전한 리소스를 클라이언트에 응답한다. 
  -  이를 **서버 렌더링**이라 한다. 브라우저는 서버가 응답한 html을 수신하고 렌더링한다. 
  -  이때 이전 페이지에서 수신된 html로 전환하는 과정에서 전체 페이지를 다시 렌더링하게 되므로 새로고침이 발생한다.
  -  이 방식은 JavaScript가 필요없이 응답된 html만으로 렌더링이 가능하며 각 페이지마다 고유의 URL이 존재하므로 history 관리 및 SEO 대응에 아무런 문제가 없다. 
  -  하지만 중복된 리소스를 요청마다 수신해야 하며, 전체 페이지를 다시 렌더링하는 과정에서 새로고침이 발생하여 사용성이 좋지 않은 단점이 있다.

  ```html
  <!DOCTYPE html>
  <html>
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <meta http-equiv="X-UA-Compatible" content="ie=edge">
          <title>Link</title>
          <link rel="stylesheet" href="css/style.css">
      </head>
      <body>
          <nav>
              <ul>
                  <li><a href="/">Home</a></li>
                  <li><a href="service.html">Service</a></li>
                  <li><a href="about.html">About</a></li>
              </ul>
          </nav>
          <section>
              <h1>Home</h1>
              <p>This is main page</p>
          </section>
      </body>
  </html>
  ```

  

- AJAX

  > JS 코드는 https://poiemaweb.com/js-spa 참고

  - 전통적 링크 방식의 단점을 보완하기 위해 등장한 것이 AJAX(Asynchronous JavaScript and XML)이다. 
  - AJAX는 자바스크립트를 이용해서 비동기적(Asynchronous)으로 서버와 브라우저가 데이터를 교환할 수 있는 통신 방식을 의미한다.
  - 서버로부터 웹페이지가 반환되면 화면 전체를 새로 렌더링해야 하는데 페이지 일부만을 갱신하고도 동일한 효과를 볼 수 있도록 하는 것이 AJAX이다.
  - 예제를 살펴보면 link tag(`<a id="home">Home</a>` 등)에 href 어트리뷰트를 사용하지 않는다. 그리고 웹페이지의 내용이 일부 비어있는 것을 알 수 있다.
  - 내비게이션이 클릭되면 link tag의 기본 동작을 prevent하고 AJAX을 사용하여 서버에 필요한 리소스를 요청한다. 요청된 리소스가 응답되면 클라이언트에서 웹페이지에 그 내용을 갈아끼워 html을 완성한다.
  - 이를 통해 불필요한 리소스 중복 요청을 방지할 수 있다. 또한 페이지 전체를 새로 렌더링할 필요가 없고 갱신이 필요한 일부만 로드하여 갱신하면 되므로 빠른 퍼포먼스와 부드러운 화면 표시 효과를 기대할 수 있으므로 새로고침이 없는 보다 향상된 사용자 경험을 구현할 수 있다는 장점이 있다.
  - AJAX는 URL을 변경시키지 않으므로 주소창의 주소가 변경되지 않는다. 
    - 이는 브라우저의 뒤로가기, 앞으로가기 등의 **history 관리가 동작하지 않음을 의미한다.** 
    - 물론 코드 상의 history.back(), history.go(n) 등도 동작하지 않는다. 
  - 새로고침을 클릭하면 주소창의 주소가 변경되지 않기 때문에 언제나 첫페이지가 다시 로딩된다. 
  - 하나의 주소로 동작하는 AJAX 방식은 **SEO 이슈**에서도 자유로울 수 없다.

  ```html
  <!DOCTYPE html>
  <html>
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <meta http-equiv="X-UA-Compatible" content="ie=edge">
          <title>AJAX</title>
          <link rel="stylesheet" href="css/style.css">
          <script src="js/index.js" defer></script>
      </head>
      <body>
          <nav>
              <ul id="navigation">
                  <li><a id="home">Home</a></li>
                  <li><a id="service">Service</a></li>
                  <li><a id="about">About</a></li>
              </ul>
          </nav>
          <div class="app-root">Loading..</div>
      </body>
  </html>
  ```



- Hash 방식

  > JS 코드는 https://poiemaweb.com/js-spa 참고

  - AJAX 방식은 불필요한 리소스 중복 요청을 방지할 수 있고, 새로고침이 없는 사용자 경험을 구현할 수 있다는 장점이 있지만 history 관리가 되지 않는 단점이 있다. 이를 보완한 방법이 Hash 방식이다.
  - Hash 방식은 URI의 fragment identifier(#service)의 고유 기능인 앵커(anchor)를 사용한다. 
    - fragment identifier는 hash mark 또는 hash라고 부르기도 한다.
  - 위 예제를 살펴보면 link tag(`<a href="#service">Service</a>` 등)의 href 어트리뷰트에 hash를 사용하고 있다.
    - 즉, 내비게이션이 클릭되면 hash가 추가된 URI가 주소창에 표시된다. 
    - 단, URL이 동일한 상태에서 hash가 변경되면 브라우저는 서버에 어떠한 요청도 하지 않는다. 
    - 즉, hash는 변경되어도 서버에 새로운 요청을 보내지 않으며 따라서 페이지가 갱신되지 않는다.
    - hash는 요청을 위한 것이 아니라 fragment identifier(#service)의 고유 기능인 앵커(anchor)로 웹페이지 내부에서 이동을 위한 것이기 때문이다.
  - 또한 hash 방식은 서버에 새로운 요청을 보내지 않으며 따라서 페이지가 갱신되지 않지만 페이지마다 고유의 논리적 URL이 존재하므로 history 관리에 아무런 문제가 없다.
  - hash 방식은 uri의 hash가 변경하면 발생하는 이벤트인 hashchange 이벤트를 사용하여 hash의 변경을 감지하여 필요한 AJAX 요청을 수행한다.
  - hash 방식의 단점 
    - uri에 불필요한 `#`이 들어간다는 것이다. 일반적으로 hash 방식을 사용할 때 `#!`을 사용하기도 하는데 이를 해시뱅(Hash-bang)이라고 부른다.
    - hash 방식은 과도기적 기술이다.
    - SEO 이슈

  ```html
  <!DOCTYPE html>
  <html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>SPA</title>
    <link rel="stylesheet" href="css/style.css">
    <script src="js/index.js" defer></script>
  </head>
  <body>
    <nav>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="#service">Service</a></li>
        <li><a href="#about">About</a></li>
      </ul>
    </nav>
    <div class="app-root">Loading...</div>
  </body>
  </html>
  ```



- PJAX 방식

  > JS 코드는 https://poiemaweb.com/js-spa 참고

  - hash 방식의 가장 큰 단점은 SEO 이슈이다. 이를 보완한 방법이 HTML5의 Histroy API인 `pushState`와 `popstate` 이벤트를 사용한 PJAX 방식이다. 
  - pushState와 popstate은 IE 10 이상에서 동작한다.
  - 예시를 살펴보면 link tag(`<a href="/service">Service</a>` 등)의 href 어트리뷰트에 path를 사용하고 있다. 
  - 내비게이션이 클릭되면 path가 추가된 URI가 서버로 요청된다. 
  - PJAX 방식은 내비게이션 클릭 이벤트를 캐치하고 `preventDefault`를 사용하여 서버로의 요청을 방지한다. 
  - 이후, href 어트리뷰트에 path을 사용하여 AJAX 요청을 하는 방식이다.
    - 이때 AJAX 요청은 주소창의 URL을 변경시키지 않아 history 관리가 불가능하다. 
    - 이때 사용하는 것이 `pushState` 메서드이다. 
    - `pushState` 메서드는 주소창의 URL을 변경하고 URL을 history entry로 추가하지만 요청하지는 않는다.

  - PJAX 방식은 서버에 새로운 요청을 보내지 않으며 따라서 페이지가 갱신되지 않는다. 
  - 하지만 페이지마다 고유의 URL이 존재하므로 history 관리에 아무런 문제가 없다. 또한 hash를 사용하지 않으므로 SEO에도 문제가 없다.

  ```html
  <!DOCTYPE html>
  <html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>PJAX</title>
    <link rel="stylesheet" href="css/style.css">
    <script src="js/index.js" defer></script>
  </head>
  <body>
    <nav>
      <ul id="navigation">
        <li><a href="/">Home</a></li>
        <li><a href="/service">Service</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </nav>
    <div class="app-root">Loading...</div>
  </body>
  </html>
  ```

  

- 결론

  - 모든 소프트웨어 아키텍처에는 trade-off가 존재한다. 
  - SPA 또한 모든 애플리케이션에 적합한 은탄환(Silver bullet)은 아니다. 
  - 애플리케이션의 상황을 고려하여 적절한 방법을 선택할 필요가 있다.

  | 구분             | History 관리 | SEO 대응 | 사용자 경험 | 서버 렌더링 | 구현 난이도 | IE 대응 |
  | ---------------- | ------------ | -------- | ----------- | ----------- | ----------- | ------- |
  | 전통적 링크 방식 | O            | O        | X           | O           | 간단        |         |
  | AJAX 방식        | X            | X        | O           | X           | 보통        | 7 이상  |
  | Hash 방식        | O            | X        | O           | X           | 보통        | 8 이상  |
  | PJAX 방식        | O            | O        | O           | △           | 복잡        | 10 이상 |

