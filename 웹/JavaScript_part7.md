# 각종 객체

## Number 래퍼 객체

- Number 객체

  - 원시 타입 number를 다룰 때 유용한 프로퍼티와 메소드를 제공하는 레퍼(wrapper) 객체이다. 
  - 변수 또는 객체의 프로퍼티가 숫자를 값으로 가지고 있다면 Number 객체의 별도 생성없이 Number 객체의 프로퍼티와 메소드를 사용할 수 있다.
  - 이는 원시 타입으로 프로퍼티나 메소드를 호출할 때 원시 타입과 연관된 wrapper 객체로 일시적으로 변환되어 프로토타입 객체를 공유하기 때문이다.

  ```javascript
  // 원시타입 number를 담고 있는 변수 num이 Number.prototype.toFixed() 메소드를 호출할 수 있는 것은 변수 num의 값이 일시적으로 wrapper객체로 변환되었기 때문이다.
  var num = 3.5
  console.log(num.toFixed()) // 4
  ```



- Number Constructor

  - Number 객체는 `Number()` 생성자 함수를 통해 생성할 수 있다.
  - 만일 인자가 숫자로 변환될 수 없다면 `NaN`을 반환한다.

  ```javascript
  var x = new Number(1);
  var y = new Number('1');
  var z = new Number('s');
  
  console.log(x); // 1
  console.log(y); // 1
  console.log(z); // NaN
  ```

  - `Number()` 생성자 함수를 `new` 연산자를 붙이지 않아 생성자로 사용하지 않으면 Number 객체를 반환하지 않고 원시 타입 숫자를 반환한다. 
    - 이때 형 변환이 발생할 수 있다.
    - 일반적으로 숫자를 사용할 때는 원시 타입 숫자를 사용한다.

  ```javascript
  var x = Number('1')
  console.log(typeof x) // number
  ```



- Number Property

  - 정적(static) 프로퍼티로 Number 객체를 생성할 필요없이 `Number.propertyName`의 형태로 사용한다.
  - `Number.EPSILON`
    - JavaScript에서 표현할 수 있는 가장 작은 수이다. 
    - 이는 임의의 수와 그 수보다 큰 수 중 가장 작은 수와의 차이와 같다. 
    - `Number.EPSILON`은 약 2.2204460492503130808472633361816E-16 또는 2**-52이다.
    - 부동소수점 산술 연산 비교는 정확한 값을 기대하기 어렵다. 
    - 정수는 2진법으로 오차없이 저장이 가능하지만 부동소수점을 표현하는 가장 널리 쓰이는 표준인 IEEE 754는 2진법으로 변환시 무한소수가 되어 미세한 오차가 발생할 수밖에 없는 구조적 한계를 갖는다.
    - 따라서 부동소수점의 비교는 `Number.EPSILON`을 사용하여 비교 기능을 갖는 함수를 작성하여야 한다.

  ```javascript
  console.log(0.1+0.2)		// 0.30000000000000004
  console.log(0.1+0.2==0.3)	// false
  
  function isEqual(a, b){
      // Math.abs는 절댓값을 반환한다.
      // a와 b의 차이가 JavaScript에서 표현할 수 있는 가장 작은 수인 Number.EPSILON보다 작으면 같은 수로 인정할 수 있다.
      return Math.abs(a - b) < Number.EPSILON
  }
  
  
  console.log(isEqual(0.1 + 0.2, 0.3))	// true
  ```

  - `Number.MAX_VALUE`
    - 자바스크립트에서 사용 가능한 가장 큰 숫자(1.7976931348623157e+308)를 반환한다. 
    - `MAX_VALUE`보다 큰 숫자는 `Infinity`이다.
  - `Number.MAX_VALUE`
    - 자바스크립트에서 사용 가능한 가장 작은 숫자(5e-324)를 반환한다. 
    - `MIN_VALUE`는 0에 가장 가까운 양수 값이다. `MIN_VALUE`보다 작은 숫자는 0으로 변환된다.
  - `Number.POSITIVE_INFINITY`
    - 양의 무한대 `Infinity`를 반환한다.
  - `Number.NEGATIVE_INFINITY`
    - 음의 무한대 `-Infinity`를 반환한다.

  - `Number.NaN`
    - 숫자가 아님(Not-a-Number)을 나타내는 숫자값이다. 
    - Number.NaN 프로퍼티는 window.NaN 프로퍼티와 같다.



- Number Method

  - 정수 리터럴과 함께 메소드를 사용할 경우
    - 숫자 뒤의 `.`은 의미가 모호하다. 
    - 소수 구분 기호일 수도 있고 객체 프로퍼티에 접근하기 위한 마침표 표기법(Dot notation)일 수도 있다. 
    - 따라서 자바스크립트 엔진은 숫자 뒤의 `.`을 부동 소수점 숫자의 일부로 해석한다. 
    - 따라서 정수 리터럴과 함께 메소드를 사용할 경우, 숫자를 괄호로 묶거나 숫자 뒤에 공백을 한 칸 만들어야 한다.
    - 자바스크립트 숫자는 정수 부분과 소수 부분 사이에 공백을 포함할 수 없다. 따라서 숫자 뒤의 `.` 뒤에 공백이 오면 `.`을 마침표 표기법(Dot notation)으로 해석하기 때문이다.

  ```javascript
  // 방법1.
  (10).toString() // 10
  
  // 방법2.
  10 .toString()	// 10
  ```

  

  - `Number.isFinite()`
    - 매개변수에 전달된 값이 정상적인 유한수인지를 검사하여 그 결과를 Boolean으로 반환한다.
    - `Number.isFinite()`는 전역 함수 `isFinite()`와 차이가 있다.
    - 전역 함수 `isFinite()`는 인수를 숫자로 변환하여 검사를 수행하지만 `Number.isFinite()`는 인수를 변환하지 않는다. 
    - 따라서 숫자가 아닌 인수가 주어졌을 때 반환값은 언제나 false가 된다.

  ```javascript
  Number.isFinite('Hello')   // false
  Number.isFinite(0)         // true
  ```

  - `Number.isInteger()`
    - 매개변수에 전달된 값이 정수(Integer)인지 검사하여 그 결과를 Boolean으로 반환한다. 
    - 검사전에 인수를 숫자로 변환하지 않는다.

  ```javascript
  Number.isInteger(0)     //true
  Number.isInteger(0.5)   //false
  Number.isInteger('123') //false
  ```

  - `Number.isNaN()`
    - 매개변수에 전달된 값이 NaN인지를 검사하여 그 결과를 Boolean으로 반환한다.
    - `Number.isNaN()`는 전역 함수 `isNaN()`와 차이가 있다. 
    - 전역 함수 `isNaN()`는 인수를 숫자로 변환하여 검사를 수행하지만 `Number.isNaN()`는 인수를 변환하지 않는다. 
    - 따라서 숫자가 아닌 인수가 주어졌을 때 반환값은 언제나 false가 된다.

  ````javascript
  Number.isNaN(NaN)       // true
  Number.isNaN(undefined) // false
  Number.isNaN('123')     // false
  ```

  - `Number.isSafeInteger()`
    - 매개변수에 전달된 값이 안전한(safe) 정수값인지 검사하여 그 결과를 Boolean으로 반환한다. 
    - 안전한 정수값은 -(253 - 1)과 253 - 1 사이의 정수값이다. 
    - 검사전에 인수를 숫자로 변환하지 않는다.

  ```javascript
  Number.isSafeInteger(1000000000000000)  // true
  Number.isSafeInteger(10000000000000001) // false
  Number.isSafeInteger(Infinity)  		//false
  Number.isSafeInteger(-Infinity) 		//false
  ```

  - `Number.prototype.toExponential()`
    - 대상을 지수 표기법으로 변환하여 문자열로 반환한다. 
    - 지수 표기법: 매우 큰 숫자를 표기할 때 주로 사용하며, e(Exponent) 앞에 있는 숫자에 10의 n승이 곱하는 형식으로 수를 나타내는 방식이다.
    - 매개변수로 0~20 사이의 정수값을 받는데, 이는 소숫점 이하의 자릿수를 나타내며, 생략 가능하다.

  ```javascript
  var numObj = 77.1234;
  
  console.log(numObj.toExponential())   // logs 7.71234e+1
  console.log(numObj.toExponential(4))  // logs 7.7123e+1
  console.log(77 .toExponential());     // logs 7.7e+1
  ```

  - `Number.prototype.toFixed()`
    - 매개변수로 지정된 소숫점자리를 반올림하여 문자열로 반환한다.
    - 매개변수를 입력하지 않을 경우 소수점 이하를 반올림한다.

  ```javascript
  var numObj = 12.345
  
  console.log(numObj.toFixed())	// 12
  console.log(numObj.toFixed(1))	// 12.3
  console.log(numObj.toFixed(2))	// 12.35
  ```

  - `Number.prototype.toPrecision()`
    - 매개변수로 지정된 전체 자릿수까지 유효하도록 나머지 자릿수를 반올림하여 문자열로 반환한다. 
    - 지정된 전체 자릿수로 표현할 수 없는 경우 지수 표기법으로 결과를 반환한다.

  ```javascript
  var numObj = 1234.5678;
  
  console.log(numObj.toPrecision())		// 1234.5678
  console.log(numObj.toPrecision(1))		// 1e+3
  ```

  - `Number.prototype.toString()`
    - 숫자를 문자열로 변환하여 반환한다.
    - 매개변수로 진법을 나타내는 2~36 사이의 정수값을 받는다(생략 가능하다).

  ```javascript
  console.log(28 .toString())		// 28
  console.log(10 .toStrubg(2))	// 1010
  ```

  - `Number.prototype.valueOf()`
    - Number 객체의 원시 타입 값을 반환한다.

  ```javascript
  var numObj = new Number(10)
  console.log(typeof numObj) 	// object
  
  var num = numObj.valueOf()
  console.log(typeof num)		// number
  ```



## String 래퍼 객체

- String 객체

  - 원시 타입인 문자열을 다룰 때 유용한 프로퍼티와 메소드를 제공하는 레퍼(wrapper) 객체이다.
  - 변수 또는 객체 프로퍼티가 문자열을 값으로 가지고 있다면 String 객체의 별도 생성없이 String 객체의 프로퍼티와 메소드를 사용할 수 있다.
  - 이는 원시 타입으로 프로퍼티나 메소드를 호출할 때 원시 타입과 연관된 wrapper 객체로 일시적으로 변환되어 프로토타입 객체를 공유하기 때문이다.

  ```javascript
  // 원시타입 string을 담고 있는 변수 str이 String.prototype.toUpperCase() 메소드를 호출할 수 있는 것은 변수 str의 값이 일시적으로 wrapper객체로 변환되었기 때문이다.
  const str = 'Hello world!'
  console.log(str.toUpperCase()) // HELLO WORLD!
  ```



- String Constructor

  - String 객체는 String 생성자 함수를 통해 생성할 수 있다. 
  - 이때 전달된 인자는 모두 문자열로 변환된다.

  ```javascript
  var strObj = new String('Cha')
  console.log(strObj)			// [String: 'Cha']
  
  var strObj = new String(1)
  console.log(strObj)			// [String: '1']
  ```

  - new 연산자를 사용하지 않고 String 생성자 함수를 호출하면 String 객체가 아닌 문자열 리터럴을 반환한다. 
    - 이때 형 변환이 발생할 수 있다.
    - 일반적으로 문자열을 사용할 때는 원시 타입 문자열을 사용한다.

  ```javascript
  var x = String('Cha')
  
  console.log(typeof x, x) // string Cha
  ```



- String Property

  - `String.length`: 문자열 내의 문자 갯수를 반환한다.
    - String 객체는 length 프로퍼티를 소유하고 있으므로 유사 배열 객체이다.

  ```javascript
  var str = 'Hello'
  console.log(str.length) // 5
  ```



- String Method

  - String 객체의 모든 메소드는 언제나 새로운 문자열을 반환한다. 
    - 문자열은 변경 불가능(immutable)한 원시 값이기 때문이다.
  - `String.prototype.charAt()`
    - 인수로 전달한 index를 사용하여 index에 해당하는 위치의 문자를 반환한다. 
    - index는 0 ~ (문자열 길이 - 1) 사이의 정수이다. 
    - 지정한 index가 문자열의 범위(0 ~ (문자열 길이 - 1))를 벗어난 경우 빈문자열을 반환한다.

  ```javascript
  const str = 'Hello'
  
  console.log(str.charAt(0)) // H
  console.log(str.charAt(1)) // e
  console.log(str.charAt(5)) // ''
  ```

  - `String.prototype.concat()`
    - 인수로 전달한 1개 이상의 문자열과 연결하여 새로운 문자열을 반환한다.
    - concat 메소드를 사용하는 것보다는 `+`, `+=` 할당 연산자를 사용하는 것이 성능상 유리하다.

  ```javascript
  console.log('Hello '.concat('World')) // Hello World
  ```

  - `String.prototype.indexOf()`
    - 인수로 전달한 문자 또는 문자열을 대상 문자열에서 검색하여 처음 발견된 곳의 index를 반환한다. 
    - 발견하지 못한 경우 -1을 반환한다.
    - 두 번째 인수로 검색을 시작할 인덱스를 넘긴다.

  ```javascript
  const str = 'Hello World';
  
  console.log(str.indexOf('l'))  		// 2
  console.log(str.indexOf('or')) 		// 7
  console.log(str.indexOf('or' , 8)) 	// -1
  ```

  - `String.prototype.lastIndexOf()`
    - 인수로 전달한 문자 또는 문자열을 대상 문자열에서 검색하여 마지막으로 발견된 곳의 index를 반환한다. 
    - 발견하지 못한 경우 -1을 반환한다.
    - 2번째 인수(fromIndex)가 전달되면 검색 시작 위치를 fromIndex으로 이동하여 역방향으로 검색을 시작한다.

  ```javascript
  const str = 'Hello World';
  
  console.log(str.lastIndexOf('World')); // 6
  console.log(str.lastIndexOf('l'));     // 9
  console.log(str.lastIndexOf('o', 5));  // 4
  ```

  - ` String.prototype.includes()`
    - 인수로 전달한 문자열이 포함되어 있는지를 검사하고 결과를 boolean 값으로 반환한다. 
    - 두번째 인수는 옵션으로 검색할 위치를 나타내는 정수이다.

  ```javascript
  const str = 'hello world';
  
  console.log(str.includes(' '))     // true
  console.log(str.includes('wo'))    // true
  console.log(str.includes('wow'))   // false
  console.log(str.includes(''));      // true
  console.log(str.includes());        // false
  ```

  - `String.prototype.replace()`
    - 첫번째 인수로 전달한 문자열 또는 정규표현식을 대상 문자열에서 검색하여 두번째 인수로 전달한 문자열로 대체한다. 
    - 원본 문자열은 변경되지 않고 결과가 반영된 새로운 문자열을 반환한다.

  ```javascript
  const str = 'Hello world world'
  
  // 첫번째로 검색된 문자열만 대체하여 새로운 문자열을 반환한다.
  console.log(str.replace('world', 'Cha')) // Hello Cha world
  
  // 특수한 교체 패턴을 사용할 수 있다. ($& => 검색된 문자열)
  console.log(str.replace('world', '<strong>$&</strong>')) // Hello <strong>world</strong>
  
  /* 
  정규표현식
  g(Global): 문자열 내의 모든 패턴을 검색한다.
  i(Ignore case): 대소문자를 구별하지 않고 검색한다.
  */
  console.log(str.replace(/hello/gi, 'Hi')) // Hi Cha world
  
  // 두번째 인수로 치환 함수를 전달할 수 있다.
  // camelCase => snake_case
  const camelCase = 'helloWorld'
  
  // /.[A-Z]/g => 1문자와 대문자의 조합을 문자열 전체에서 검색한다.
  console.log(camelCase.replace(/.[A-Z]/g, function (match) {
    // match : oW => match[0] : o, match[1] : W
    return match[0] + '_' + match[1].toLowerCase()
  })) // hello_world
  
  // /(.)([A-Z])/g => 1문자와 대문자의 조합
  // $1 => (.)
  // $2 => ([A-Z])
  console.log(camelCase.replace(/(.)([A-Z])/g, '$1_$2').toLowerCase()) // hello_world
  
  // snake_case => camelCase
  const snakeCase = 'hello_world'
  
  // /_./g => _와 1문자의 조합을 문자열 전체에서 검색한다.
  console.log(snakeCase.replace(/_./g, function (match) {
    // match : _w => match[1] : w
    return match[1].toUpperCase()
  })) // helloWorld
  ```

  - `String.prototype.split()`
    - 첫 번째 인수로 전달한 문자열 또는 정규표현식을 대상 문자열에서 검색하여 문자열을 구분한 후 분리된 각 문자열로 이루어진 배열을 반환한다. 
    - 원본 문자열은 변경되지 않는다.
    - 인수가 없는 경우, 대상 문자열 전체를 단일 요소로 하는 배열을 반환한다.
    - 두 번째 인자로 허용할 요소의 수를  넘길 수 있다.

  ```javascript
  var str = "Hello Cha! Oh, Are you Okay?"
  console.log(str.split(' '))		// [ 'Hello', 'Cha!', 'Oh,', 'Are', 'you', 'Okay?' ]
  console.log(str.split())		// [ 'Hello Cha! Oh, Are you Okay?' ]
  console.log(str.split(''))
  /*
  [
    'H', 'e', 'l', 'l', 'o', ' ',
    'C', 'h', 'a', '!', ' ', 'O',
    'h', ',', ' ', 'A', 'r', 'e',
    ' ', 'y', 'o', 'u', ' ', 'O',
    'k', 'a', 'y', '?'
  ]
  */
  console.log(str.split(' ', 3))		// [ 'Hello', 'Cha!', 'Oh,' ]
  console.log(str.split('o'))			// [ 'Hell', ' Cha! Oh, Are y', 'u Okay?' ]
  ```

  - `String.prototype.substring()`
    - 첫번째 인수로 전달한 start 인덱스에 해당하는 문자부터 두번째 인자에 전달된 end 인덱스에 해당하는 문자의 **바로 이전 문자까지**를 모두 반환한다. 
    - 이때 첫번째 인수 < 두번째 인수의 관계가 성립된다.
    - 첫 번째 인수가 더 클 경우, 두 번째 인수와 교환된다.
    - 두 번째 인수가 생략된 경우,  해당 문자열의 끝까지 반환한다.
    - 인수가 0보다 작거나 NaN인 경우, 0으로 취급된다.
    - 인수가 문자열의 길이보다 큰 경우, 인수는 문자열의 길이로 취급된다.

  ```javascript
  const str = 'Hello World'
  
  console.log(str.substring(1, 4)) // ell
  
  // 첫번째 인수 > 두번째 인수 : 두 인수는 교환된다.
  console.log(str.substring(4, 1)) // ell
  
  // 두번째 인수가 생략된 경우 : 해당 문자열의 끝까지 반환한다.
  console.log(str.substring(4)) // o World
  
  // 인수 < 0 또는 NaN인 경우 : 0으로 취급된다.
  console.log(str.substring(-2)) // Hello World
  
  // 인수 > 문자열의 길이(str.length) : 인수는 문자열의 길이(str.length)으로 취급된다.
  console.log(str.substring(1, 12)) // ello World
  ```

  - `String.prototype.slice()`
    - String.prototype.substring과 동일하다. 
    - 단, String.prototype.slice는 음수의 인수를 전달할 수 있다.

  ```javascript
  const str = 'hello world';
  
  // 인수 < 0 또는 NaN인 경우 : 0으로 취급된다.
  console.log(str.substring(-5)) 	// 'hello world'
  // 뒤에서 5자리를 잘라내어 반환한다.
  console.log(str.slice(-5)) 		// 'world'
  ```

  - `String.prototype.toLowerCase()` / `String.prototype.toUpperCase()`
    - `String.prototype.toLowerCase()`: 대상 문자열의 모든 문자를 소문자로 변경
    - `String.prototype.toUpperCase()`: 대상 문자열의 모든 문자를 대문자로 변경

  ```javascript
  console.log('Hello World!'.toLowerCase()) // hello world!
  console.log('Hello World!'.toUpperCase()) // HELLO WORLD!
  ```

  - `String.prototype.trim()`
    - 대상 문자열 양쪽 끝에 있는 공백 문자를 제거한 문자열을 반환한다.

  ```javascript
  const str = '   foo  '
  
  console.log(str.trim()) // 'foo'
  
  // String.prototype.replace
  console.log(str.replace(/\s/g, ''))   // 'foo'
  console.log(str.replace(/^\s+/g, '')) // 'foo  '
  console.log(str.replace(/\s+$/g, '')) // '   foo'
  
  // String.prototype.{trimStart,trimEnd} : Proposal stage 3
  console.log(str.trimStart()) // 'foo  '
  console.log(str.trimEnd())   // '   foo'
  ```

  - `String.prototype.repeat()`
    - 인수로 전달한 숫자만큼 반복해 연결한 새로운 문자열을 반환한다. 
    - count가 0이면 빈 문자열을 반환하고 음수이면 RangeError를 발생시킨다.
    - 부동소수점이면 내림한다.

  ```javascript
  console.log('abc'.repeat(0))   // ''
  console.log('abc'.repeat(2.5)) // 'abcabc'
  console.log('abc'.repeat(-1))  // RangeError: Invalid count value
  ```



## Math 객체

- Math 객체
  - Math 객체는 수학 상수와 함수를 위한 프로퍼티와 메소드를 제공하는 빌트인 객체이다.
  - Math 객체는 생성자 함수가 아니다. 따라서 Math 객체는 정적(static) 프로퍼티와 메소드만을 제공한다.



- Math Property

  - `Math.PI`
    - PI 값(π ≈ 3.141592653589793)을 반환한다.

  ```javascript
  console.log(Math.PI)	// 3.141592653589793
  ```

  

- Math Method

  - `Math.abs()`
    - 인수의 절댓값을 반환한다.
    - 절댓값은 반드시 0 또는 양수여야 한다.

  ```javascript
  Math.abs(-1)       	// 1
  Math.abs('-1')     	// 1
  Math.abs('')       	// 0
  Math.abs(null)     	// 0
  Math.abs(undefined)	// NaN
  Math.abs({})       	// NaN
  Math.abs('string') 	// NaN
  ```

  - `Math.round()` / `Math.ceil()` / `Math.floor()`
    - `Math.round()`: 인수의 소수점 이하를 반올림한 정수를 반환한다.
    - `Math.ceil()`: 인수의 소수점 이하를 올림한 정수를 반환한다.
    - `Math.floor()`: 인수의 소수점 이하를 내림한 정수를 반환한다.

  ```javascript
  // round
  Math.round(-1.9); // -2
  Math.round(1);    // 1
  Math.round();     // NaN
  
  // ceil
  Math.ceil(1.6)	  // 2
  Math.ceil(-1.4)   // -1
  Math.ceil(1)	  // 1
  Math.ceil()       // NaN
  
  // floor
  Math.floor(9.1)   // 9
  Math.floor(-1.9)  // -2
  Math.floor(1)     // 1
  Math.floor()      // NaN
  ```

  - ` Math.sqrt()`
    - 인수의 제곱근을 반환한다.

  ```javascript
  Math.sqrt(4)  // 2
  Math.sqrt(-4) // NaN
  Math.sqrt()   // NaN
  ```

  - `Math.random()`
    - 임의의 부동 소수점을 반환한다.
    - 반환된 부동 소수점은 0부터 1 미만이다(즉 0은 포함되지만 1은 포함되지 않는다).

  ```javascript
  for(var i=0;i<3;i++){
      console.log(Math.random())
  }
  
  // 0.4083061090677629
  // 0.9524417917615027
  // 0.5844291517440603
  ```

  - `Math.pow()`
    - 첫번째 인수를 밑(base), 두번째 인수를 지수(exponent)로하여 거듭제곱을 반환한다.

  ```javascript
  Math.pow(3, 4)  // 81
  Math.pow(2, -1) // 0.5
  ```

  - `Math.max()` / `Math.min()` 
    - `Math.max()`: 인수 중에서 가장 큰 수를 반환한다.
    - `Math.min()` : 인수 중에서 가장 작은 수를 반환한다.

  ```javascript
  // max()
  console.log(Math.max(4,5,9))				// 9
  
  // 배열에 적용
  const arr = [4,5,9]
  const maxValue = Math.max.apply(null,arr)
  console.log(maxValue)						// 9
  
  // ES6 Spread operator
  console.log(Math.max(...arr))				// 9
  
  
  // min()
  console.log(Math.max(4,5,9))				// 4
  
  // 배열에 적용
  const arr = [4,5,9]
  const minValue = Math.min.apply(null,arr)
  console.log(maxValue)						// 4
  
  // ES6 Spread operator
  console.log(Math.min(...arr))				// 4
  ```



## Date 객체

- Date 객체
  - 날짜와 시간(년, 월, 일, 시, 분, 초, 밀리초(천분의 1초(millisecond, ms)))을 위한 메소드를 제공하는 빌트인 객체이면서 생성자 함수이다.
  - Date 생성자 함수로 생성한 Date 객체는 내부적으로 숫자값을 갖는다. 
  - 이 값은 1970년 1월 1일 00:00(UTC)을 기점으로 현재 시간까지의 밀리초를 나타낸다.
  - UTC(협정 세계시: Coordinated Universal Time)는 GMT(그리니치 평균시: Greenwich Mean Time)로 불리기도 하는데 UTC와 GMT는 초의 소숫점 단위에서만 차이가 나기 때문에 일상에서는 혼용되어 사용된다. 
    - 기술적인 표기에서는 UTC가 사용된다.
  - KST(Korea Standard Time)는 UTC/GMT에 9시간을 더한 시간이다. 즉, KST는 UTC/GMT보다 9시간이 빠르다. 
    - 예를 들어, UTC 00:00 AM은 KST 09:00 AM이다.
  - 현재의 날짜와 시간은 자바스크립트 코드가 동작한 시스템의 시계에 의해 결정된다. 
    - 시스템 시계의 설정(timezone, 시간)에 따라 서로 다른 값을 가질 수 있다.



- Date Constructor
  - Date 객체는 생성자 함수이다. 
  - Date 생성자 함수는 날짜와 시간을 가지는 인스턴스를 생성한다. 
  - 생성된 인스턴스는 기본적으로 현재 날짜와 시간을 나타내는 값을 가진다. 
  - 현재 날짜와 시간이 아닌 다른 날짜와 시간을 다루고 싶은 경우, Date 생성자 함수에 명시적으로 해당 날짜와 시간 정보를 인수로 지정한다. 



- Date 생성자 함수로 객체를 생성하는 방법

  - `new Date()`
    - 인수를 전달하지 않으면 현재 날짜와 시간을 가지는 인스턴스를 반환한다.

  ```javascript
  var date = new Date()
  console.log(date)		// 2021-01-26T11:53:18.862Z
  ```

  - `new Date(milliseconds)`
    - 인수로 숫자 타입의 밀리초를 전달하면 1970년 1월 1일 00:00(UTC)을 기점으로 인수로 전달된 밀리초만큼 경과한 날짜와 시간을 가지는 인스턴스를 반환한다.

  ```javascript
  var date = new Date(0)
  console.log(date)		// 1970-01-01T00:00:00.000Z
  ```

  - `new Date(dateString)`
    - 인수로 날짜와 시간을 나타내는 문자열을 전달하면 지정된 날짜와 시간을 가지는 인스턴스를 반환한다. 
    - 이때 인수로 전달한 문자열은 Date.parse 메소드에 의해 해석 가능한 형식이어야 한다.

  ```javascript
  var date = new Date('January 26, 2021 20:56:10')
  console.log(date)		// 2021-01-26T11:56:10.000Z
  
  var date = new Date('2021/01/26/20:56:10')
  console.log(date)		// 2021-01-26T11:56:10.000Z
  ```

  - `new Date(year, month[, day, hour, minute, second, millisecond])`

    - 인수로 년, 월, 일, 시, 분, 초, 밀리초를 의미하는 숫자를 전달하면 지정된 날짜와 시간을 가지는 인스턴스를 반환한다. 
    - 이때 년, 월은 반드시 지정하여야 한다. 
    - 지정하지 않은 옵션 정보는 0 또는 1으로 초기화된다.

    | 인수        | 내용                                   |
    | ----------- | -------------------------------------- |
    | year        | 1900년 이후의 년                       |
    | month       | 월을 나타내는 0~11까지의 정수(0 = 1월) |
    | day         | 일을 나타내는 1~31까지의 정수          |
    | hour        | 시를 나타내는 0~23까지의 정수          |
    | minute      | 분을 나타내는 0~59까지의 정수          |
    | second      | 초를 나타내는 0~59까지의 정수          |
    | millisecond | 나타내는 0 ~ 999까지의 정수            |

  ```javascript
  var date = new Date(2021, 1)
  console.log(date)		// 2021-01-31T15:00:00.000Z
  
  var date = new Date(2021, 1, 26, 21, 00, 30, 0)
  console.log(date)		// 2021-01-26T12:00:30.010Z
  
  var date = new Date('2021/1/26/21:00:30:10')
  console.log(date)		// 2021-01-26T12:00:30.010Z
  ```

  - `Date` 생성자 함수를 `new` 연산자 없이 호출
    - 인스턴스를 반환하지 않고 결과값을 문자열로 반환한다.

  ```javascript
  var date = Date()
  console.log(typeof date, date)	// string Tue Jan 26 2021 21:04:10 GMT+0900 (대한민국 표준시)
  ```

  

- Date 메소드

  - `Date.now()`
    - 1970년 1월 1일 00:00:00(UTC)을 기점으로 현재 시간까지 경과한 밀리초를 숫자로 반환한다.

  ```javascript
  var now = Date.now()
  console.log(now)	// 1611662707254
  ```

  - `Date.parse()`
    - 1970년 1월 1일 00:00:00(UTC)을 기점으로 인수로 전달된 지정 시간(new Date(dateString)의 인수와 동일한 형식)까지의 밀리초를 숫자로 반환한다.

  ```javascript
  var d = Date.parse('2021/1/26/21:00:30:10')
  console.log(d)		// 1611662430010
  
  var d = Date.parse('January 26, 2021 20:56:10')
  console.log(d)		// 1611662170000
  ```

  - `Date.UTC()`
    - 1970년 1월 1일 00:00:00(UTC)을 기점으로 인수로 전달된 지정 시간까지의 밀리초를 숫자로 반환한다.
    - `Date.UTC()` 메소드는 `new Date(year, month[, day, hour, minute, second, millisecond])`와 같은 형식의 인수를 사용해야 한다. 
    - `Date.UTC()` 메소드의 인수는 local time(KST)이 아닌 UTC로 인식된다.

  ```javascript
  var d = Date.UTC(1970, 0, 2)
  console.log(d) 		// 86400000
  ```

  - `Date.prototype.getFullYear()` / `Date.prototype.getFullMonth()` / `Date.prototype.getFullday()`  
    - `Date.prototype.getFullYear()` : 년도를 나타내는 4자리 숫자를 반환한다.
    - `Date.prototype.getFullMonth()` : 월을 나타내는 0~11의 정수를 반환한다.(0=1월)
    - `Date.prototype.getFullday()` : 일을 나타내는 1~31의 정수를 반환한다. 

  ```javascript
  var d = new Date()
  const year = d.getFullYear()
  const month = d.getMonth()
  const day = d.getDay()
  console.log(year)		// 2021
  console.log(month)		// 0
  console.log(day)		// 2
  ```

  - `Date.prototype.setFullYear()` / `Date.prototype.setMonth()` / `Date.prototype.setDate()`
    - `Date.prototype.setFullYear()`: 년도를 나타내는 4자리 숫자를 설정한다. 년도 이외 월, 일도 설정할 수 있다.
    - `Date.prototype.setMonth()`: 월을 나타내는 0 ~ 11의 정수를 설정한다. 1월은 0, 12월은 11이다. 월 이외 일도 설정할 수 있다.
    - `Date.prototype.setDate()`: 날짜(1 ~ 31)를 나타내는 정수를 설정한다.

  ```javascript
  var d = new Date()
  d.setFullYear(2016)
  console.log(d.getFullYear())	// 2016
  
  d.setMonth(3)
  console.log(d.getMonth())		// 3
  
  d.setDate(17)
  console.log(d.getDate())		// 17
  ```

  - `Date.prototype.getDay()`
    - 요일(0 ~ 6)를 나타내는 정수를 반환한다. 
    - 0은 일요일을, 6은 토요일을 나타낸다.

  ```javascript
  var d = new Date()
  console.log(d.getDay())	// 2
  ```

  - `Date.prototype.getHours()` / `Date.prototype.getMinutes()` / `Date.prototype.getSeconds()` / `Date.prototype.getMilliseconds()`
    -  `Date.prototype.getHours()`: 시간(0 ~ 23)를 나타내는 정수를 반환한다.
    - `Date.prototype.getMinutes()`: 분(0 ~ 59)를 나타내는 정수를 반환한다.
    - `Date.prototype.getSeconds()`: 초(0~59)를 나타내는 정수를 반환한다.
    - `Date.prototype.getMilliseconds()` : 밀리초(0 ~ 999)를 나타내는 정수를 반환한다.

  ```javascript
  var d = new Date()
  console.log(d.getHours())			// 21
  console.log(d.getMinutes())			// 20
  console.log(d.getSeconds())			// 55
  console.log(d.getMilliseconds())	// 1
  ```

  - `Date.prototype.setHours()` / `Date.prototype.setMinutes()` / `Date.prototype.setSeconds()` / `Date.prototype.setMilliseconds()`
    -  `Date.prototype.setHours()`: 시간(0 ~ 23)를 나타내는 정수를 설정한다. 시간 이외 분, 초, 밀리초도 설정할 수 있다.
    - `Date.prototype.setMinutes()`: 분(0 ~ 59)를 나타내는 정수를 설정한다. 분 이외 초, 밀리초도 설정할 수 있다.
    - `Date.prototype.setSeconds()`: 초(0 ~ 59)를 나타내는 정수를 설정한다. 초 이외 밀리초도 설정할 수 있다.
    - `Date.prototype.setMilliseconds()` : 밀리초(0 ~ 999)를 나타내는 정수를 설정한다.

  ```javascript
  var d = new Date()
  d.setHours(1)
  d.setMinutes(2)
  d.setSeconds(3)
  d.setMilliseconds(456)
  console.log(d.getHours())			// 1
  console.log(d.getMinutes())			// 2
  console.log(d.getSeconds())			// 3
  console.log(d.getMilliseconds())	// 456
  ```

  - `Date.prototype.getTime()` /  `Date.prototype.setTime()`
    - `Date.prototype.getTime()` : 1970년 1월 1일 00:00:00(UTC)를 기점으로 현재 시간까지 경과된 밀리초를 반환한다.
    - `Date.prototype.setTime()` : 1970년 1월 1일 00:00:00(UTC)를 기점으로 현재 시간까지 경과된 밀리초를 설정한다.

  ```javascript
  var date = new Date()
  var millise = date.getTime()
  console.log(millise)		// 1611664010372
  
  date.setTime(87895489)
  var millise = date.getTime()
  console.log(date)		// 1970-01-02T00:24:55.489Z
  console.log(millise)	// 87895489
  ```

  - `Date.prototype.getTimezoneOffset()`
    - UTC와 지정 로케일(Locale) 시간과의 차이를 분단위로 반환한다.

  ```javascript
  const today = new Date()
  const x = today.getTimezoneOffset() / 60
  
  console.log(x)	// -9
  ```

  - `Date.prototype.toDateString()` / `Date.prototype.toTimeString()`
    - `Date.prototype.toDateString()`: 사람이 읽을 수 있는 형식의 문자열로 날짜를 반환한다.
    - `Date.prototype.toTimeString()`: 사람이 읽을 수 있는 형식의 문자열로 시간을 반환한다.

  ```javascript
  const d = new Date('2021/1/26/21:30')
  console.log(d.toDateString())		// Tue Jan 26 2021
  console.log(d.toTimeString())		// 21:30:00 GMT+0900 (대한민국 표준시)
  ```