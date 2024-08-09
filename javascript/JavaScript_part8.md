# 정규표현식

- 정규표현식(Regular Expression)

  - 문자열에서 특정 내용을 찾거나 대체 또는 발췌하는데 사용한다.
  - 반복문과 조건문을 사용한 복잡한 코드도 정규표현식을 이용하면 매우 간단하게 표현할 수 있다. 
  - 하지만 정규표현식은 주석이나 공백을 허용하지 않고 여러가지 기호를 혼합하여 사용하기 때문에 가독성이 좋지 않다는 문제가 있다.
  - 정규표현식은 리터럴 표기법으로 생성할 수 있다. 정규 표현식 리터럴은 아래와 같이 표현한다.

  ```javascript
  /패턴/플래그
  ```

  - 정규표현식을 사용하는 자바스크립트 메소드는 `RegExp.prototype.exec`, `RegExp.prototype.test`, `String.prototype.match`, `String.prototype.replace`, `String.prototype.search`, `String.prototype.split` 등이 있다.



- 플래그

  - 플래그는 옵션이므로 선택적으로 사용한다. 
  - 플래그를 사용하지 않은 경우 문자열 내 검색 매칭 대상이 1개 이상이더라도 첫번째 매칭한 대상만을 검색하고 종료한다.

  - 종류
    - `i`(Ignore Case): 대소문자를 구별하지 않고 검색
    - `g`(Global): 문자열 내의 모든 패턴을 검색
    - `m`(Multi Line): 문자열의 행이 바뀌더라도 검색을 계속한다.

  ```javascript
  const targetStr = 'Bibbidi Bobbidi Boo'
  
  // 문자열 bi를 대소문자를 구별하여 한번만 검색한다.
  var regexr = /bi/
  
  console.log(regexr.exec(targetStr))		// [ 'bi', index: 3, input: 'Bibbidi Bobbidi Boo', groups: undefined ]
  
  // 문자열 bi를 대소문자를 구별하지 않고 대상 문자열 끝까지 검색한다.
  var regexr = /bi/ig;
  
  console.log(targetStr.match(regexr))		// [ 'Bi', 'bi', 'bi' ]
  console.log(targetStr.match(regexr).length) // 3
  ```



- 패턴

  - 검색하고 싶은 문자열을 지정한다. 
    - 이때 문자열의 따옴표는 생략한다. 
    - 따옴표를 포함하면 따옴표까지도 검색한다. 
    - 또한 패턴은 특별한 의미를 가지는 메타문자(Metacharacter) 또는 기호로 표현할 수 있다. 

  - `.`은 임의의 문자 한 개를 의미한다.

  ```javascript
  var targetStr = 'Bibbidi Bobbidi Boo'
  
  // 임의의 문자 5개
  var regexr = /...../
  console.log(targetStr.match(regexr))	// [ 'Bibbi', index: 0, input: 'Bibbidi Bobbidi Boo', groups: undefined ]
  
  // 임의의 문자 5개를 반복하여 검색
  var regexr = /...../g
  console.log(targetStr.match(regexr))	// [ 'Bibbi', 'di Bo', 'bbidi' ]
  
  // .과 g를 동시에 지정하여 모든 문자를 선택
  var regexr = /./g
  console.log(targetStr.match(regexr))
  /*
  [
    'B', 'i', 'b', 'b', 'i',
    'd', 'i', ' ', 'B', 'o',
    'b', 'b', 'i', 'd', 'i',
    ' ', 'B', 'o', 'o'
  ]
  */
  ```

  - 문자 또는 문자열을 지정하면 일치하는 문자 또는 문자열을 추출한다.

  ```javascript
  var targetStr = 'Bibbidi Bobbidi Boo'
  var regexr = /bi/
  console.log(targetStr.match(regexr))	// [ 'bi', index: 3, input: 'Bibbidi Bobbidi Boo', groups: undefined ]
  ```

  - 앞선 패턴을 반복하려면 앞선 패턴 뒤에 `+`를 붙인다.

  ```javascript
  var targetStr = 'bibibibididi'
  var regexr = /bi+/g
  console.log(targetStr.match(regexr))	// [ 'bi', 'bi', 'bi', 'bi' ]
  ```

  - `|`는 or의 의미를 가진다.

  ```javascript
  var targetStr = 'Bibbidi'
  var regexr = /bi|di/g
  console.log(targetStr.match(regexr))    // [ 'bi', 'di' ]
  ```

  - `[]`내의 문자는 or로 동작한다.

  ```javascript
  var targetStr = 'Bibbidi'
  // b|i|d
  var regexr = /[bid]/g
  console.log(targetStr.match(regexr))    // [ 'i', 'b', 'b', 'i', 'd', 'i' ]
  ```

  - 범위를 지정하려면 `[]`  내에 `-`를 사용한다.

  ```javascript
  // 대문자
  var targetStr = 'Bi Boo Doo'
  var regexr = /[A-Z]+/g
  console.log(targetStr.match(regexr))    // [ 'B', 'B', 'D' ]
  
  // 대소문자
  // /[A-Z]+/gi와 동일
  var regexr = /[A-Za-z]+/g;
  console.log(targetStr.match(regexr));   // [ 'Bi', 'Boo', 'Doo' ]
  
  // 숫자
  var targetStr = 'abcd 1234578000000000'
  var regexr = /[0-9]+/g
  console.log(targetStr.match(regexr))	// [ '1234578000000000' ]
  ```

  - `\d`는 숫자를 의미하고, `\D`는 숫자가 아닌 문자를 의미한다.

  ```javascript
  var targetStr = 'abcd 1234578000000000'
  var regexr = /[\d]+/g
  console.log(targetStr.match(regexr))	// [ '1234578000000000' ]
  
  var targetStr = 'abcd 1234578000000000'
  var regexr = /[\D]+/g
  console.log(targetStr.match(regexr))	// [ 'abcd ' ]
  ```

  - `\w`는 알파벳과 숫자를 의미하고, `\W`는 숫자와 알파벳이 아닌 문자를 의미한다.

  ```javascript
  var targetStr = 'abcd 1234578000000000'
  var regexr = /[\w]+/g
  console.log(targetStr.match(regexr))    // [ 'abcd', '1234578000000000' ]
  
  var targetStr = 'abcd 1234578000000000'
  var regexr = /[\W]+/g
  console.log(targetStr.match(regexr))    // [ ' ' ]
  ```



- 자주 사용하는 정규표현식

  - 특정 단어로 시작하는지 검사
    - `^ `: 문자열의 처음을 의미한다.

  ```javascript
  var url = 'http://example.com'
  
  // 'http'로 시작하는지 검사
  var regexr = /^http/
  
  console.log(regexr.test(url)) // true
  ```

  - 특정 단어로 끝나는지 검사
    - `$`: 문자열의 끝을 의미한다.

  ```javascript
  var fileName = 'index.js'
  var regexr = /js$/
  console.log(regexr.test(fileName)) // true
  ```

  - 숫자인지 검사
    - `[^]`: 부정을 의미한다.

  ```javascript
  var targetStr = '12345'
  var regexr = /^\d/
  console.log(regexr.test(targetStr))	// true
  ```

  - 하나 이상의 공백으로 시작하는지 검사
    - `\s`: 여러 가지 공백 문자(탭, 스페이스 등, `\t\r\n\b\f`)

  ```javascript
  const targetStr = ' Hi!'
  
  // 1개 이상의 공백으로 시작하는지 검사
  const regexr = /^[\s]+/
  
  console.log(regexr.test(targetStr)) // true
  ```



- JavaScript 정규표현식

  - ` RegExp Constructor`
    - 자바스크립트은 정규표현식을 위해 RegExp 객체를 지원한다. 
    - RegExp 객체를 생성하기 위해서는 리터럴 방식과 RegExp 생성자 함수를 사용할 수 있다. 
    - 일반적인 방법은 리터럴 방식이다.

  ```javascript
  // 플래그는 생략 가능
  new RegExp(패턴[, 플래그])
  ```

  - `RegExp Method`
    - ` RegExp.prototype.exec()`: 문자열을 검색하여 매칭 결과를 반환한다. 반환값은 배열 또는 null이다. `g` 플래그를 지정하여도 첫번째 메칭 결과만을 반환한다.
    - `RegExp.prototype.test()`: 문자열을 검색하여 매칭 결과를 반환한다. 반환값은 true 또는 false이다.



# 배열

- 배열
  - 1개의 변수에 여러 개의 값을 순차적으로 저장할 때 사용한다. 
  - 대부분의 프로그래밍 언어에서 배열의 요소들은 모두 같은 데이터 타입이어야 하지만, JS의 배열은 어떤 데이터 타입의 조합이라도 포함할 수 있다.
  - 자바스크립트의 배열은 객체이며 유용한 내장 메소드를 포함하고 있다.
  - 배열은 Array 생성자로 생성된 Array 타입의 객체이며 프로토타입 객체는 Array.prototype이다.



- 배열 생성

  - 배열 리터럴
    - 0개 이상의 값을 쉼표로 구분하여 대괄호(`[]`)로 묶는다. 
    - 배열 리터럴은 객체 리터럴과 달리 프로퍼티명이 없고 각 요소의 값만이 존재한다. 
    - 배열은 요소에 접근하기 위해 대괄호 표기법만을 사용하며 대괄호 내에 접근하고자 하는 요소의 인덱스를 넣어준다. 인덱스는 0부터 시작한다.
    - 존재하지 않는 요소에 접근하면 `undefined`를 반환한다.

  ```javascript
  var emptyArr = []
  console.log(emptyArr[0])	// undefined
  
  var arr = [1,2,3,4,5]
  console.log(arr[1])         // 2
  console.log(typeof arr)     // object
  console.log(arr.length)     // 5
  ```

  - `Array()` 생성자 함수
    - 일반적으로 배열 리터럴 방식으로 생성하지만 배열 리터럴 방식도 결국 `Array()` 생성자 함수로 배열을 생성하는 것을 단순화시킨 것이다.
    - `Array()` 생성자 함수는 `Array.prototype.constructor` 프로퍼티로 접근할 수 있다.
    - Array() 생성자 함수는 매개변수의 갯수에 따라 다르게 동작한다.
    - 매개변수가 1개이고 숫자인 경우 매개변수로 전달된 숫자를 length 값으로 가지는 빈 배열을 생성한다.
    - 그 외의 경우 매개변수로 전달된 값들을 요소로 가지는 배열을 생성한다.

  ```javascript
  var arr = new Array(3)
  console.log(arr)            // [ <3 empty items> ]
  console.log(arr.length)     // 3
  
  var arr = new Array(1,2,3)
  console.log(arr)            // [ 1, 2, 3 ]
  ```

  

- 배열 요소 추가와 삭제

  - 배열 요소 추가
    - 순서에 맞게 값을 할당할 필요는 없고 인덱스를 사용하여 필요한 위치에 값을 할당한다. 
    - 배열의 길이(length)는 마지막 인덱스를 기준으로 산정된다.
    - 값이 할당되지 않은 인덱스 위치의 요소는 생성되지 않는다.
    - 단, 존재하지 않는 요소를 참조하면 undefined가 반환된다.

  ```javascript
  var arr = []
  arr[1] = 1
  arr[2] = 2
  console.log(arr[4])     // undefined
  console.log(arr[0])     // undefined
  console.log(arr)        // [ <1 empty item>, 1, 2 ]
  ```

  - 배열 요소의 삭제
    - 배열은 객체이기 때문에 배열의 요소를 삭제하기 위해 `delete` 연산자를 사용할 수 있다.
    - 이때 length에는 변함이 없다. 
    - 해당 요소를 완전히 삭제하여 length에도 반영되게 하기 위해서는 `Array.prototype.splice(시작 인덱스, 삭제할 요소 수)` 메소드를 사용한다.

  ```javascript
  var arr = [1,2,3,4]
  
  delete arr[0]
  console.log(arr)		// [ <1 empty item>, 2, 3, 4 ]
  
  arr.splice(0,1)
  console.log(arr)		// [ 2, 3, 4 ]
  ```



- 배열의 순회

  - 객체의 프로퍼티를 순회할 때 `for…in` 문을 사용한다. 배열 역시 객체이므로 `for…in` 문을 사용할 수 있다.
  - 그러나 배열은 객체이기 때문에 프로퍼티를 가질 수 있다. `for…in` 문을 사용하면 배열 요소뿐만 아니라 불필요한 프로퍼티까지 출력될 수 있고 요소들의 순서를 보장하지 않으므로 배열을 순회하는데 적합하지 않다.
  - 따라서 배열의 순회에는 `forEach` 메소드, `for` 문, `for…of` 문을 사용하는 것이 좋다.

  ```javascript
  var arr = [1,2,3]
  arr.x = -10
  console.log(arr)                // [ 1, 2, 3, x: -10 ]
  
  for (const key in arr){
      console.log(key,arr[key])
  }
  /*
  0 1
  1 2
  2 3
  x -10   // 불필요한 프로퍼티까지 출력
  */
  
  arr.forEach((item,index) => console.log(index,item))
  /*
  0 1
  1 2
  2 3
  */
  
  for (let i = 0; i < arr.length; i++) {
    console.log(i, arr[i]);
  }
  /*
  0 1
  1 2
  2 3
  */
  
  for (const item of arr) {
    console.log(item);
  }
  /*
  1
  2
  3
  */
  ```



- Array Property

  - `Array.length`
    - 요소의 개수(배열의 길이)를 나타낸다. 
    - 배열 인덱스는 32bit 양의 정수로 처리된다. 따라서 length 프로퍼티의 값은 양의 정수이며 232 - 1(4,294,967,296 - 1) 미만이다.
    - 현재 length 프로퍼티 값보다 더 큰 인덱스로 요소를 추가하면 새로운 요소를 추가할 수 있도록 자동으로 length 프로퍼티의 값이 늘어난다. 
    - length 프로퍼티의 값은 가장 큰 인덱스에 1을 더한 것과 같다.
    - length 프로퍼티의 값은 명시적으로 변경할 수 있다. 
    - 만약 length 프로퍼티의 값을 현재보다 작게 변경하면 변경된 length 프로퍼티의 값보다 크거나 같은 인덱스에 해당하는 요소는 모두 삭제된다.
    - 주의할 것은 배열 요소의 개수와 length 프로퍼티의 값이 반드시 일치하지는 않는다는 것이다.

  ```javascript
  var arr = [0,1,2,3,4]
  console.log(arr.length)	// 5
  
  // 배열 길이의 명시적 변경
  arr.length = 2
  console.log(arr) // [ 0, 1 ]
  ```

  - 희소배열
    - 배열 요소의 개수와 length 프로퍼티의 값이 일치하지 않는 배열을 **희소 배열**(sparse array)이라 한다.
    - 희소 배열은 배열의 요소가 연속적이지 않은 배열을 의미한다. 
    - 희소 배열이 아닌 일반 배열은 배열의 요소 개수와 length 프로퍼티의 값이 언제나 일치하지만 희소 배열은 배열의 요소 개수보다 length 프로퍼티의 값이 언제나 크다. 
    - 희소 배열은 일반 배열보다 느리며 메모리를 낭비한다.



- Array Method

  - `Array.isArray()`
    - 주어진 인수가 배열이면 true, 배열이 아니면 false를 반환한다.

  ```javascript
  Array.isArray([])				// true
  Array.isArray([1, 2,3])			// true
  Array.isArray(new Array())		// true
  Array.isArray(1)				// false
  Array.isArray('Array')			// false
  ```

  - `Array.from()`
    - 유사 배열 객체(array-like object) 또는 이터러블 객체(iterable object)를 변환하여 새로운 배열을 생성한다.
    - 두 번째 매개변수에 배열의 모든 요소에 대해 호출할 함수를 전달할 수 있다.

  ```javascript
  // 이터러블 객체 문자열을 배열로 변환
  const arr1 = Array.from('Hello')
  console.log(strArray) // [ 'H', 'e', 'l', 'l', 'o' ]
  
  // 유사 배열 객체를 배열로 변환
  const arr2 = Array.from({ length: 2, 0: 'a', 1: 'b' })
  console.log(arr2)	// [ 'a', 'b' ]
  
  const arr3 = Array.from({ length: 3 }, function(v,i){return i+=3})
  console.log(arr3)   // [ 3, 4, 5 ]
  ```

  - `Array.of()`
    - 전달된 인수를 요소로 갖는 배열을 생성한다.
    - `Array.of`는 `Array()` 생성자 함수와 다르게 전달된 인수가 1개이고 숫자이더라도 인수를 요소로 갖는 배열을 생성한다.

  ```javascript
  var arr1 = Array.of(1)
  console.log(arr)		// [ 1 ]
  
  var arr2 = Array.of(1,2,3)
  console.log(arr)		// [ 1, 2, 3 ]
  
  var arr3 = Array.of('Hello!')
  console.log(arr3)		// [ 'Hello!' ]
  ```

  - `Array.prototype.indexOf()`
    - 원본 배열에서 인수로 전달된 요소를 검색하여 인덱스를 반환한다.
    - 중복되는 요소가 있는 경우, 첫번째 인덱스를 반환한다.
    - 해당하는 요소가 없는 경우, -1을 반환한다.
    - 두 번째 인수로 검색을 시작할 인덱스를 받는다.

  ```javascript
  var arr = [0,1,2,2]
  console.log(arr.indexOf(2))		// 2
  console.log(arr.indexOf(3))		// -1
  console.log(arr.indexOf(2,3))	// 3
  ```

  - `Array.prototype.includes()`
    - 원본 배열에서 인수로 전달된 요소를 검색하여 존재 여부를 boolean 값으로 반환한다.

  ```javascript
  var arr = [1,2]
  console.log(arr.includes(1))	// true
  console.log(arr.includes(3))	// false
  ```

  - `Array.prototype.concat()`
    - 인수로 전달된 값들을 원본 배열의 마지막 요소로 추가한 새로운 배열을 반환한다.
    - 인수로 전달한 값이 배열인 경우 배열을 해체하여 새로운 배열의 요소로 추가한다.
    - 원본 배열은 변경되지 않는다.

  ```javascript
  var arr1 = [0,1]
  var arr2 = [2,3]
  result = arr1.concat(arr2)
  console.log(result)		// [ 0, 1, 2, 3 ]
  
  result = arr1.concat(11)
  console.log(result)		// [ 0, 1, 11 ]
  
  result = arr1.concat(arr2,100)
  console.log(result)		// [ 0, 1, 2, 3, 100 ]
  ```

  - `Array.prototype.join()`
    - 원본 배열의 모든 요소를 문자열로 변환한 후, 인수로 전달받은 값, 즉 구분자(separator)로 연결한 문자열을 반환한다. 
    - 구분자(separator)는 생략 가능하며 기본 구분자는 `,`이다.
    - 원본 배열은 변경되지 않는다.

  ```javascript
  var arr = [1,2,3]
  var result = arr.join()
  console.log(result)		// 1,2,3
  
  result = arr.join('')
  console.log(result)		// 123
  ```

  - `Array.prototype.push()`
    - 인수로 전달받은 모든 값을 원본 배열의 마지막에 요소로 추가하고 변경된 length 값을 반환한다. 
    - 원본 배열을 직접 변경한다.
    - push 메소드는 원본 배열을 직접 변경하지만 concat 메소드는 원본 배열을 변경하지 않고 새로운 배열을 반환한다.
    - 인수로 전달받은 값이 배열인 경우, push 메소드는 배열을 그대로 원본 배열의 마지막 요소로 추가하지만 concat 메소드는 배열을 해체하여 새로운 배열의 마지막 요소로 추가한다.
    - push 메소드는 성능면에서 좋지 않다.

  ```javascript
  var arr = [1,2]
  var result = arr.push(7,8,9)
  console.log(result)		// 5
  console.log(arr)		// [ 1, 2, 7, 8, 9 ]
  
  result = arr.push([7,8,9])
  console.log(arr)		// [ 1, 2, 7, 8, 9, [ 7, 8, 9 ] ]
  
  // arr.push(3)와 동일한 처리를 한다. 이 방법이 push 메소드보다 빠르다.
  arr[arr.length] = 3
  ```

  - `Array.prototype.pop()`
    - 원본 배열에서 마지막 요소를 제거하고 제거한 요소를 반환한다. 
    - 원본 배열이 빈 배열이면 `undefined`를 반환한다.
    - 원본 배열을 직접 변경한다.

  ```javascript
  var arr = [0]
  var result = arr.pop()
  console.log(result) // 0
  
  result = arr.pop()
  console.log(result) // undefined
  
  console.log(arr)    // []
  ```

  - `Array.prototype.shift()`
    - 배열에서 첫요소를 제거하고 제거한 요소를 반환한다. 
    - 만약 빈 배열일 경우 `undefined`를 반환한다. 
    - 대상 배열 자체를 변경한다.

  ```javascript
  var arr = [0,1]
  console.log(arr.shift())	// 0
  console.log(arr.shift())	// 1
  console.log(arr.shift())	// undefined
  console.log(arr)			// []
  ```

  - `Array.prototype.reverse()`
    - 배열 요소의 순서를 반대로 변경한다. 반환값은 변경된 배열이다.
    - 원본 배열이 변경된다.

  ```javascript
  const arr = ['a', 'b', 'c']
  const rra = a.reverse()
  console.log(arr)	// [ 'c', 'b', 'a' ]
  console.log(rra)	// [ 'c', 'b', 'a' ]
  ```

  - `Array.prototype.slice()`
    - 인자로 지정된 배열의 부분을 복사하여 반환한다. 
    - 원본 배열은 변경되지 않는다.
    - 첫 번째 매개 변수로 복사를 시작할 값을 나타낸다. 음수일 경우 배열의 끝에서의 인덱스를 나타낸다.
    - 두 번째 매개 변수로 복사를 끝낼 값을 나타낸다. 옵션이며 기본값은 length 값이다.
    - 매개변수를 입력하지 않으면 원본 배열의 각 요소를 얕은 복사(shallow copy)하여 반환한다.

  ```javascript
  var arr = ['x','y','z']
  console.log(arr.slice())	// [ 'x', 'y', 'z' ]
  console.log(arr.slice(1,2))	// [ 'y' ]
  console.log(arr.slice(-2))	// [ 'y', 'z' ]
  ```

  - `Array.prototype.splice()`
    - 기존의 배열의 요소를 제거하고 그 위치에 새로운 요소를 추가한다. 
    - 배열 중간에 새로운 요소를 추가할 때도 사용된다.
    - 원본 배열이 변경된다.
    - 첫 번째 매개 변수로 시작 위치를 받는다.
    - 두 번째 매개 변수로 시작 위치부터 제거할 요소의 수를 받는다(옵션). 입력하지 않으면 시작 위치부터  전부 삭제된다.
    - 세 번째 매개 변수로 삭제한 위치에 추가될 요소를 받는다(옵션).

  ```javascript
  var arr1 = [1,2,3,4,5]
  console.log(arr1.splice(1,3))       // [ 2, 3, 4 ]
  console.log(arr1)                   // [ 1, 5 ]
  
  var arr2 = [1,2,3,4,5,6,7,8,9]
  console.log(arr2.splice(2))         // [ 3, 4, 5, 6, 7, 8, 9 ]
  console.log(arr2)                   // [ 1, 2 ]
  
  var arr3 = [1,2,3,4]
  console.log(arr3.splice(0,2,13))    // [ 1, 2 ]
  console.log(arr3)                   // [ 13, 3, 4 ]
  
  var arr4 = [1,2,3,5]
  arr4.splice(3,0,4)
  console.log(arr)					// [ 1, 2, 3, 4, 5 ]
  ```

  



## JS의 배열은 배열이 아니다.

- 밀집 배열
  - 일반적으로 배열이라는 자료 구조의 개념은 동일한 크기의 메모리 공간이 빈틈없이 연속적으로 나열된 자료 구조를 말한다. 
  - 즉, 배열의 요소는 하나의 타입으로 통일되어 있으며 서로 연속적으로 인접해 있다. 이러한 배열을 **밀집 배열(dense array)**이라 한다.
  - 이처럼 배열의 요소는 동일한 크기를 갖으며 빈틈없이 연속적으로 이어져 있으므로 인덱스를 통해 단 한번의 연산으로 임의의 요소에 접근(임의 접근(random access), 시간 복잡도 O(1))할 수 있다. 이는 매우 효율적이며 고속으로 동작한다.
  - 하지만 정렬되지 않은 배열에서 특정한 값을 탐색하는 경우, 모든 배열 요소를 처음부터 값을 발견할 때까지 차례대로 탐색(선형 탐색(linear search), 시간 복잡도 O(n))해야 한다.
  - 또한 배열에 요소를 삽입하거나 삭제하는 경우, 배열 요소를 연속적으로 유지하기 위해 요소를 이동시켜야 하는 단점도 있다.



- 희소 배열

  - JS의 배열은 지금까지 살펴본 일반적인 의미의 배열과 다르다. 
  - 즉, 배열의 요소를 위한 각각의 메모리 공간은 동일한 크기를 갖지 않아도 되며 연속적으로 이어져 있지 않을 수도 있다. 
  - 배열의 요소가 연속적으로 이어져 있지 않는 배열을 **희소 배열(sparse array)**이라 한다.
  - 이처럼 JS의 배열은 일반적인 배열의 동작을 흉내낸 특수한 객체이다. 
  - JS 배열은 해시 테이블로 구현된 객체이므로 인덱스로 배열 요소에 접근하는 경우, 일반적인 배열보다 성능적인 면에서 느릴 수 밖에 없는 구조적인 단점을 갖는다. 
    - 인덱스로 배열 요소에 접근할 때 일반적인 배열보다 느릴 수 밖에 없는 구조적인 단점을 보완하기 위해 대부분의 모던 자바스크립트 엔진은 배열을 일반 객체와 구별하여 보다 배열처럼 동작하도록 최적화하여 구현하였다.
  - 하지만 특정 요소를 탐색하거나 요소를 삽입 또는 삭제하는 경우에는 일반적인 배열보다 빠른 성능을 기대할 수 있다.
  - 아래 예시처럼 JS 배열은 인덱스를 프로퍼티 키로 갖으며 length 프로퍼티를 갖는 특수한 객체이다.
    - JS 배열의 요소는 사실 프로퍼티 값이다. 
    - JS에서 사용할 수 있는 모든 값은 객체의 프로퍼티 값이 될 수 있으므로 어떤 타입의 값이라도 배열의 요소가 될 수 있다.

  ```javascript
  console.log(Object.getOwnPropertyDescriptors([1, 2, 3]))
  /*
  {
    '0': { value: 1, writable: true, enumerable: true, configurable: true },
    '1': { value: 2, writable: true, enumerable: true, configurable: true },
    '2': { value: 3, writable: true, enumerable: true, configurable: true },
    length: { value: 3, writable: true, enumerable: false, configurable: false }
  }
  */
  ```





## 배열 고차 함수

- 고차 함수(Higher order function)
  - 함수를 인자로 전달받거나 함수를 결과로 반환하는 함수를 말한다.
    - 다시 말해, 고차 함수는 인자로 받은 함수를 필요한 시점에 호출하거나 클로저를 생성하여 반환한다.
    - JS의 함수는 일급 객체이므로 값처럼 인자로 전달할 수 있으며 반환할 수도 있다.
  - 고차 함수는 외부 상태 변경이나 가변(mutable) 데이터를 피하고 **불변성(Immutability)을 지향**하는 함수형 프로그래밍에 기반을 두고 있다.
  - 함수형 프로그래밍
    - 순수 함수(Pure function)와 보조 함수의 조합을 통해 로직 내에 존재하는 조건문과 반복문을 제거하여 복잡성을 해결하고 변수의 사용을 억제하여 상태 변경을 피하려는 프로그래밍 패러다임.
    - 조건문이나 반복문은 로직의 흐름을 이해하기 어렵게 하여 가독성을 해치고, 변수의 값은 누군가에 의해 언제든지 변경될 수 있어 오류 발생의 근본적 원인이 될 수 있기 때문이다.
    - 함수형 프로그래밍은 결국 순수 함수를 통해 **부수 효과(Side effect)를 최대한 억제**하여 오류를 피하고 프로그램의 안정성을 높이려는 노력의 한 방법이라고 할 수 있다.
  - JS는 고차 함수를 다수 지원하고 있다. 특히 Array 객체는 매우 유용한 고차 함수를 제공한다.



- `Array.prototype.sort()`

  - 배열의 요소를 적절하게 정렬한다. 
  - 원본 배열을 직접 변경하며 정렬된 배열을 반환한다.

  ```javascript
  var arr1 = [3,5,4,1,2]
  arr1.sort()
  console.log(arr1)       // [ 1, 2, 3, 4, 5 ]
  
  var arr2 = ['a','c','d','e','b']
  arr3.sort()
  console.log(arr3)       // [ 'a', 'b', 'c', 'd', 'e' ]
  ```

  - 기본 정렬 순서는 문자열 Unicode 코드 포인트 순서에 따른다. 
    - 배열의 요소가 숫자타입이라 할지라도 배열의 요소를 일시적으로 문자열로 변환하여 정렬한다.
    - 이러한 경우, sort 메소드의 인자로 정렬 순서를 정의하는 비교 함수를 인수로 전달한다.

  ```javascript
  var arr = [4,5,10,2,100,1]
  arr.sort()
  console.log(arr)    // [ 1, 10, 100, 2, 4, 5 ]
  
  // 숫자 배열 오름차순 정렬
  // 비교 함수의 반환값이 0보다 작은 경우, a를 우선하여 정렬한다.
  var arr = [4,5,10,2,100,1]
  arr.sort(function (a, b) { return a - b; })
  console.log(arr)    // [ 1, 2, 4, 5, 10, 100 ]
  ```

  - 객체를 요소로 갖는 배열의 정렬

  ```javascript
  var todoList = [
      {id:3, content: 'JavaScript'},
      {id:1, content: 'React'},
      {id:2, content: 'Spring'}
  ]
  
  function compare(k){
      return function(a,b){
          // 프로퍼티 값이 문자열인 경우, - 산술 연산으로 비교하면 NaN이 나오므로 비교 연산을 사용.
          return a[k] > b[k] ? 1 : (a[k] < b[k] ? -1 : 0)
      }
  }
  
  // id를 기준으로 정렬
  todoList.sort(compare('id'));
  console.log(todoList);
  /*
  [
    { id: 1, content: 'React' },
    { id: 2, content: 'Spring' },
    { id: 3, content: 'JavaScript' }
  ]
  */
  
  // content를 기준으로 정렬
  todoList.sort(compare('content'));
  console.log(todoList);
  /*
  [
    { id: 3, content: 'JavaScript' },
    { id: 1, content: 'React' },
    { id: 2, content: 'Spring' }
  ]
  */
  ```

  

- `Array.prototype.forEach()`

  - `forEach` 메소드는 for 문 대신 사용할 수 있다.
    - `forEach` 메소드는 for 문과는 달리 **break 문을 사용할 수 없다.** 다시 말해, 배열의 모든 요소를 순회하며 중간에 순회를 중단할 수 없다.
    - forEach 메소드는 for 문에 비해 성능이 좋지는 않다. 하지만 for 문보다 가독성이 좋으므로 적극 사용을 권장한다.
  - 배열을 순회하며 배열의 각 요소에 대하여 인자로 주어진 콜백함수를 실행한다. 반환값은 `undefined`이다.
  - IE 9 이상에서 정상 동작한다.

  ```javascript
  // for문으로 순회
  var arr = [7,8,9]
  for (let i = 0; i<arr.length; i++){
      console.log(arr[i])
  }
  
  // forEach 메소드로 순회
  arr.forEach(function(i){
      console.log(i)
  })
  
  // 둘 다 결과는 같다.
  /*
  7
  8
  9
  */
  ```

  - 콜백 함수의 매개변수를 통해 배열 요소의 값, 요소 인덱스, `forEach` 메소드를 호출한 배열, 즉 `this`를 전달 받을 수 있다.

  ```javascript
  var arr = [3,6,9,12,15]
  
  arr.forEach(function(item,index,self){
      console.log(`arr[${index}] = ${item}`)
      if(index===4){
          console.log(self)
      }
  })
  /*
  arr[0] = 3
  arr[1] = 6
  arr[2] = 9
  arr[3] = 12
  arr[4] = 15
  [ 3, 6, 9, 12, 15 ]
  */
  ```

  - `forEach` 메소드는 원본 배열(`this`)을 변경하지 않는다. 하지만 콜백 함수는 원본 배열(`this`)을 변경할 수는 있다.

  ```javascript
  var arr = [2,4,6,8]
  
  arr.forEach(function(item,index,self){
      self[index] += 2
  })
  console.log(arr)	// [ 4, 6, 8, 10 ]
  ```

  - `forEach` 메소드에 두번째 인자로 `this`를 전달할 수 있다.
    - 화살표 함수를 사용하면 `this`를 생략해도 동일한 동작을 한다.

  ```javascript
  function Square() {
    this.array = []
  }
  
  Square.prototype.multiply = function (arr) {
    arr.forEach(function (item) {
      // this를 인수로 전달하지 않으면 this === window
      this.array.push(item * item)
    }, this)
  }
  
  const square = new Square()
  square.multiply([2,3,4])
  console.log(square.array) // [ 4, 9, 16 ]
  

  // 화살표 함수 사용
  Square.prototype.multiply = function (arr) {
    arr.forEach(item => this.array.push(item * item))
  }
  ```
  
  

- `Array.prototype.map()`

  - 배열을 순회하며 각 요소에 대하여 인자로 주어진 콜백 함수의 반환값(결과값)으로 새로운 배열을 생성하여 반환한다.
  - 이때 원본 배열은 변경되지 않는다.
  - `forEach` 메소드는 배열을 순회하며 요소 값을 참조하여 무언가를 하기 위한 함수이며, `map` 메소드는 배열을 순회하며 요소 값을 다른 값으로 맵핑하기 위한 함수이다.
  - 콜백 함수의 매개변수를 통해 배열 요소의 값, 요소 인덱스, `map` 메소드를 호출한 배열, 즉 `this`를 전달 받을 수 있다.
  - IE 9 이상에서 정상 동작한다.

  ```javascript
  var arr = [1,2,3,4]
  var result = arr.map(function(itme){
      // 반환값이 새로운 배열의 요소가 된다. 반환값이 없으면 새로운 배열은 비어 있다.
      return itme += 3
  })
  console.log(arr)		// [ 1, 2, 3, 4 ]
  console.log(result)		// [ 4, 5, 6, 7 ]
  ```

  - `map` 메소드에 두번째 인자로 `this`를 전달할 수 있다.
    - 화살표 함수를 사용하면 `this`를 생략해도 동일한 동작을 한다.

  ```javascript
  function Name(name) {
      this.lastName = name
  }
  
  Name.prototype.fullName = function (arr) {
      // 콜백함수의 인자로 배열 요소의 값, 요소 인덱스, map 메소드를 호출한 배열, 즉 this를 전달할 수 있다.
      return arr.map(function (fisrtName) {
          // x는 배열 요소의 값이다.
          return this.lastName + fisrtName // 2번째 인자 this를 전달하지 않으면 this === window
      }, this)
  }
  
  const nm = new Name('Cha')
  const fullNameArr = nm.fullName(['jong', 'Jun'])
  console.log(fullNameArr)	// [ 'Chajong', 'ChaJun' ]
  ```

  

- `Array.prototype.filter()`

  - `filter` 메소드를 사용하면 if 문을 대체할 수 있다.
  - 배열을 순회하며 각 요소에 대하여 인자로 주어진 콜백함수의 실행 결과가 true인 배열 요소의 값만을 추출한 새로운 배열을 반환한다.
  - 배열에서 특정 케이스만 필터링 조건으로 추출하여 새로운 배열을 만들고 싶을 때 사용한다. 이때 원본 배열은 변경되지 않는다.
  - 콜백 함수의 매개변수를 통해 배열 요소의 값, 요소 인덱스, `filter` 메소드를 호출한 배열, 즉 `this`를 전달 받을 수 있다.
  - IE 9 이상에서 정상 동작한다.

  ```javascript
  var oddNum = [1,2,3,4,5,6].filter(function(item,index,self){
      // item % 2가 1, 즉 참이면 반환한다.
      return item % 2
  })
  console.log(oddNum)	// [ 1, 3, 5 ]
  ```

  

- `Array.prototype.reduce()`

  - 배열을 순회하며 각 요소에 대하여 이전의 콜백함수 실행 반환값을 전달하여 콜백함수를 실행하고 그 결과를 반환한다. 
  - 원본 배열은 변경되지 않는다.
  - IE 9 이상에서 정상 동작한다.

  ```javascript
  var arr = [1, 2, 3, 4, 5]
  
  var sum = arr.reduce(function(previousValue, currentValue, currentIndex, self){
      return previousValue + currentValue
  })
  
  console.log(sum)	// 15
  
  // 최대값 구하기
  const max = arr.reduce(function (pre, cur) {
    return pre > cur ? pre : cur
  })
  
  console.log(max)	// 5
  ```

  - 두번째 인수로 초기값을 전달할 수 있다. 이 값은 콜백 함수에 최초로 전달된다.

  ```javascript
  var sum = [1, 2, 3, 4, 5].reduce(function (pre, cur) {
    return pre + cur;
  }, 10)
  
  console.log(sum)	// 25
  ```

  - 객체에서의 활용
    - 객체의 프로퍼티 값을 합산하는 경우에는 반드시 초기값을 전달해야 한다.

  ```javascript
  var products = [
      { id: 1, price: 100 },
      { id: 2, price: 200 },
      { id: 3, price: 300 }
  ]
    
  // price를 합산
  var priceSum = products.reduce(function (pre, cur) {
      console.log(pre.price, cur.price)
      // 숫자값이 두번째 콜백 함수 호출의 인수로 전달된다.
      // 따라서, 숫자값인 pre에는 price라는 프로퍼티가 존재하지 않으므로 undefined가 된다.
      return pre.price + cur.price
  })
  /*
  15
  100 200
  undefined 300
  */
  
  
  // 초기값 전달
  var products = [
    { id: 1, price: 100 },
    { id: 2, price: 200 },
    { id: 3, price: 300 }
  ]
  
  var priceSum = products.reduce(function (pre, cur) {
      console.log(pre, cur.price)
    	return pre + cur.price
  }, 0)
  
  console.log(priceSum) // 600
  ```

  - 빈 배열을 호출하면 에러가 발생한다.
    - 초기값을 전달하면 에러를 회피할 수 있다.
    - `reduce`를 호출할 때는 **언제나 초기값을 전달하는 것이 보다 안전하다.**

  ```javascript
  const sum = [].reduce(function (pre, cur) {
    console.log(pre, cur)
    return pre + cur
  })
  // TypeError: Reduce of empty array with no initial value
  
  
  // 초기값 전달
  const sum = [].reduce(function (pre, cur) {
    console.log(pre, cur)
    return pre + cur
  }, 0)
  
  console.log(sum) // 0
  ```

  

- `Array.prototype.some()`

  - 배열 내 일부 요소가 콜백 함수의 테스트를 통과하는지 확인하여 그 결과를 boolean으로 반환한다. 
    - 하나라도 통과하면 true를, 모두 통과하지 않으면 false를 반환한다.
  - IE 9 이상에서 정상 동작한다.
  - 콜백함수의 매개변수를 통해 배열 요소의 값, 요소 인덱스, 메소드를 호출한 배열, 즉 `this`를 전달 받을 수 있다.
  -  두번째 인자로` this`를 전달할 수 있다.

  ```javascript
  // 하나라도 일치하면 true를, 모두 일치하지 않으면 false를 반환한다.
  res = [3,6,9].some(function (item) {
    return item < 5
  })
  console.log(res) // true
  
  
  // 배열 내 요소 중 특정 값이 1개 이상 존재하는지 확인
  res = ['a', 'b', 'c'].some(function (item) {
    return item === 'a'
  })
  console.log(res) // true
  ```

  

- `Array.prototype.every()`

  - 배열 내 모든 요소가 콜백함수의 테스트를 통과하는지 확인하여 그 결과를 boolean으로 반환한다. 
    - 모두 통과하면 true를, 하나라도 통과하지 않으면 false를 반환한다.
  - IE 9 이상에서 정상 동작한다.
  - 콜백함수의 매개변수를 통해 배열 요소의 값, 요소 인덱스, 메소드를 호출한 배열, 즉 `this`를 전달 받을 수 있다.
  - 두번째 인자로 `this`를 전달할 수 있다.

  ```javascript
  let res = [11, 12, 13, 14, 9].every(function (item) {
    return item > 10
  })
  console.log(res) // false
  
  res = [11, 12, 13, 14, 15].every(function (item) {
    return item > 10
  })
  console.log(res) // true
  ```

  

- `Array.prototype.find()`

  - 배열을 순회하며 각 요소에 대하여 인자로 주어진 **콜백함수를 실행하여 그 결과가 참인 첫번째 요소를 반환한다.** 
    - 콜백함수의 실행 결과가 참인 요소가 존재하지 않는다면 `undefined`를 반환한다.
    - `filter`는 **콜백함수의 실행 결과가 true인 배열 요소의 값만을 추출한 새로운 배열을 반환한다.** 따라서 `filter`의 반환값은 언제나 배열이다. 
    - 하지만 `find`는 **콜백함수를 실행하여 그 결과가 참인 첫번째 요소를 반환**하므로 `find`의 결과값은 해당 요소값이다.
  - Internet Explorer에서는 지원하지 않는다.
  - 콜백함수의 매개변수를 통해 배열 요소의 값, 요소 인덱스, 메소드를 호출한 배열, 즉 this를 전달 받을 수 있다.

  ```javascript
  var arr = [1,2,3,4,5]
  var res = arr.find(function(item){
      return item===3
  })
  console.log(res)	// 3
  ```

  

- `Array.prototype.findIndex()`

  - 배열을 순회하며 각 요소에 대하여 인자로 주어진 **콜백함수를 실행하여 그 결과가 참인 첫번째 요소의 인덱스를 반환한다.** 
    - 콜백함수의 실행 결과가 참인 요소가 존재하지 않는다면 -1을 반환한다.

  - Internet Explorer에서는 지원하지 않는다.
  - 콜백함수의 매개변수를 통해 배열 요소의 값, 요소 인덱스, 메소드를 호출한 배열, 즉 this를 전달 받을 수 있다.

  ```javascript
  var arr = [1,2,3,4,5]
  var res = arr.findIndex(function(item){
      return item===3
  })
  console.log(res)	// 2
  ```







# DOM

- DOM(Document Object Model)
  - 텍스트 파일로 만들어져 있는 웹 문서를 브라우저에 렌더링하려면 웹 문서를 브라우저가 이해할 수 있는 구조로 메모리에 올려야 한다. 
  - 브라우저의 렌더링 엔진은 웹 문서 로드 후, 파싱하여 웹 문서를 브라우저가 이해할 수 있는 구조로 구성하여 메모리에 적재하는데 이를 **DOM**이라 한다. 
    - 즉 모든 요소와 요소의 어트리뷰트, 텍스트를 각각의 객체로 만들고 이들 객체를 부자 관계를 표현할 수 있는 트리 구조로 구성한 것이 DOM이다. 
  - 이 DOM은 자바스크립트를 통해 동적으로 변경할 수 있으며 변경된 DOM은 렌더링에 반영된다.
    - 이러한 웹 문서의 동적 변경을 위해 DOM은 프로그래밍 언어가 자신에 접근하고 수정할 수 있는 방법을 제공하는데 일반적으로 프로퍼티와 메소드를 갖는 자바스크립트 객체로 제공된다. 
    - 이를 **DOM API**(Application Programming Interface)라고 부른다. 
    - 달리 말하면 정적인 웹페이지에 접근하여 동적으로 웹페이지를 변경하기 위한 유일한 방법은 메모리 상에 존재하는 DOM을 변경하는 것이고, 이때 필요한 것이 DOM에 접근하고 변경하는 프로퍼티와 메소드의 집합인 DOM API이다.
  - DOM은 HTML, ECMAScript에서 정의한 표준이 아닌 별개의 W3C의 공식 표준이며 플랫폼/프로그래밍 언어 중립적이다. 
  - DOM은 다음 두 가지 기능을 담당한다.
    - HTML 문서에 대한 모델 구성: 브라우저는 HTML 문서를 로드한 후 해당 문서에 대한 모델을 메모리에 생성한다. 이때 모델은 객체의 트리로 구성되는데 이것을 **DOM tree**라 한다.
    - HTML 문서 내의 각 요소에 접근 / 수정: DOM은 모델 내의 각 객체에 접근하고 수정할 수 있는 프로퍼티와 메소드를 제공한다. DOM이 수정되면 브라우저를 통해 사용자가 보게 될 내용 또한 변경된다.



## DOM tree

- DOM tree

  - 브라우저가 HTML 문서를 로드한 후 파싱하여 생성하는 모델을 의미한다. 

  - 객체의 트리로 구조화되어 있기 때문에 DOM tree라 부른다.

  - DOM 트리를 크롬 브라우저에서 확인하려면 개발자도구(Developer Tools)의 Elements 를 선택한 후 오른쪽의 properties을 선택하면 된다.

  - DOM을 통해 웹페이지를 조작(manipulate)하기 위해서는 다음과 같은 수순이 필요하다.

    - 조작하고자하는 요소를 선택 또는 탐색한다.
    - 선택된 요소의 콘텐츠 또는 어트리뷰트를 조작한다.

    - 자바스크립트는 이것에 필요한 수단(API)을 제공한다.



- DOM tree의 종류
  - 문서 노드(Document Node)
    - 트리의 최상위에 존재하며 각각 요소, 어트리뷰트, 텍스트 노드에 접근하려면 문서 노드를 통해야 한다. 
    - 즉, DOM tree에 접근하기 위한 시작점(entry point)이다.
  - 요소 노드(Element Node)
    - 요소 노드는 HTML 요소를 표현한다. 
    - HTML 요소는 중첩에 의해 부자 관계를 가지며 이 부자 관계를 통해 정보를 구조화한다. 
    - 따라서 요소 노드는 문서의 구조를 서술한다고 말 할 수 있다. 
    - 어트리뷰트, 텍스트 노드에 접근하려면 먼저 요소 노드를 찾아 접근해야 한다. 
    - 모든 요소 노드는 요소별 특성을 표현하기 위해 HTMLElement 객체를 상속한 객체로 구성된다.
  - 어트리뷰트 노드(Attribute Node)
    - 어트리뷰트 노드는 HTML 요소의 어트리뷰트를 표현한다. 
    - 어트리뷰트 노드는 해당 어트리뷰트가 지정된 요소의 자식이 아니라 해당 요소의 일부로 표현된다. 
    - 따라서 해당 요소 노드를 찾아 접근하면 어트리뷰트를 참조, 수정할 수 있다.
  - 텍스트 노드(Text Node)
    - 텍스트 노드는 HTML 요소의 텍스트를 표현한다. 
    - 텍스트 노드는 요소 노드의 자식이며 자신의 자식 노드를 가질 수 없다. 
    - 즉, 텍스트 노드는 DOM tree의 최종단이다.



## DOM Query

- 예시로 사용되는 HTML 코드

  ```html
  <!DOCTYPE html>
  <html>
      <head>
          <style>
              .red  { color: #ff0000; }
              .blue { color: #0000ff; }
          </style>
      </head>
      <body>
          <div>
              <h1>Cities</h1>
              <ul>
                  <li id="one" class="red">Seoul</li>
                  <li id="two" class="red">Daejeon</li>
                  <li id="three" class="red">Daegu</li>
                  <li id="four">Busan</li>
              </ul>
          </div>
          <script>
              // id로 하나의 요소를 선택한다.
              const elem = document.getElementById('one')
              // 클래스 어트리뷰트의 값을 변경한다.
              elem.className = 'blue'
              console.log(elem)
              console.log(elem.__proto__)				// HTMLLIElement
              console.log(elem.__proto__.__proto__)	// HTMLElement
              console.log(elem.__proto__.__proto__.__proto__)		// Element
              console.log(elem.__proto__.__proto__.__proto__.__proto__)	// Node
              
          </script>
      </body>
  </html>
  ```

  

### 하나의 요소 노드 선택(DOM Query)

- `document.getElementById(id)`

  - id 어트리뷰트 값으로 요소 노드를 한 개 선택한다. 복수개가 선택된 경우, 첫 번째 요소만 반환한다.
  - HTMLElement를 상속받은 객체를 반환한다.

  - 모든 브라우저에서 동작한다.

  ```javascript
  // id로 하나의 요소를 선택한다.
  const elem = document.getElementById('one')
  // 클래스 어트리뷰트의 값을 변경한다.
  elem.className = 'blue'
  console.log(elem)
  console.log(elem.__proto__)				// HTMLLIElement
  console.log(elem.__proto__.__proto__)	// HTMLElement
  console.log(elem.__proto__.__proto__.__proto__)		// Element
  console.log(elem.__proto__.__proto__.__proto__.__proto__)	// Node
  ```



- `document.querySelector(cssSelector)`

  - CSS 셀렉터를 사용하여 요소 노드를 한 개 선택한다. 복수개가 선택된 경우, 첫번째 요소만 반환한다.
  - HTMLElement를 상속받은 객체를 반환한다.
  - IE8 이상의 브라우저에서 동작

  ```javascript
  const elem = document.querySelector('li.red')
  
  elem.className = 'blue';
  ```





### 여러 개의 요소 노드 선택(DOM Query)

- `document.getElementsByCalssName(class)`

  - class 어트리뷰트 값으로 요소 노드를 모두 선택한다. 공백으로 구분하여 여러 개의 class를 지정할 수 있다.
  - HTMLCollection을 반환한다.
    - HTMLCollection은 **유사배열(array-like object)**이다. 
    - HTMLCollection은 **실시간(live)으로 Node의 상태 변경을 반영한다.**
  - IE9 이상의 브라우저에서 동작한다.

  ```javascript
  // HTMLCollection을 반환한다. HTMLCollection은 live하다.
  const elems = document.getElementsByClassName('red')
  
  for (let i = 0; i < elems.length; i++) {
    // 클래스 어트리뷰트의 값을 변경한다.
    elems[i].className = 'blue'
  }
  ```

  - 위 예제를 실행해보면 두 번째 요소만 클래스 변경이 되지 않는데 그 이유는 다음과 같다.
    - `elems.length`는 3이므로 3번의 반복이 실행된다.
    - `i`가 0일 때, `elems`의 첫 번째 요소(`li#one.red`)의 class 어트리뷰트 값이 className 프로퍼티에 의해 blue로 변경된다.
    - 이 때 `elems`는 실시간으로 Node의 상태 변경을 반영하는  HTMLCollection 객체이다.
    - elems의 첫 요소는 `li#one.red`에서 `li#one.blue`로 변경되었으므로 `getElementsByClassName` 메소드의 인자로 지정한 선택 조건(red)과 더이상 부합하지 않게 되어 반환값에서 실시간으로 제거된다.
    - i가 1일때, `elems`에서 첫째 요소는 제거되었으므로 `elems[1]`은 3번째 요소(`li#three.red`)가 된다. `li#three.red`의 class 어트리뷰트 값이 blue로 변경되고 마찬가지로 HTMLCollection에서 제외된다.
    - i가 2일때, HTMLCollection의 1,3번째 요소가 실시간으로 제거되었으므로 2번째 요소(`li#two.red`)만 남았다. 이때 `elems.length`는 1이므로 for 문의 조건식 `i < elems.length`가 false로 평가되어 반복을 종료한다. 따라서 `elems`에 남아 있는 2번째 li 요소(`li#two.red`)의 class 값은 변경되지 않는다.
  - HTMLCollection는 실시간으로 Node의 상태 변경을 반영하기 때문에 loop가 필요한 경우 주의가 필요하다. 아래와 같은 방법으로 회피할 수 있다.
    - 반복문을 역방향으로 돌린다.
    - while 반복문을 사용한다. 이때 elems에 요소가 남아 있지 않을 때까지 무한반복하기 위해 index는 0으로 고정시킨다.
    - **HTMLCollection을 배열로 변경한다(권장)**.
    - `querySelectorAll`메소드를 사용하여 HTMLCollection(live)이 아닌 NodeList(non-live를 반환하게 한다.

  ```javascript
  // 반복문을 역방향으로
  const elems = document.getElementsByClassName('red')
  
  for (let i = elems.length - 1; i >= 0; i--) {
    elems[i].className = 'blue'
  }
  
  
  // while 반복문을 사용
  const elems = document.getElementsByClassName('red');
  
  let i = 0
  while (elems.length > i) { 	// elems에 요소가 남아 있지 않을 때까지 무한반복, elems.length가 0이 되면 반복이 종료된다.
    elems[i].className = 'blue'
  }
  
  
  // HTMLCollection을 배열로 변경
  const elems = document.getElementsByClassName('red')
  console.log([...elems]) // [li#one.red, li#two.red, li#three.red]
  [...elems].forEach(elem => elem.className = 'blue');
  
  
  // querySelectorAll 메소드를 사용
  const elems = document.querySelectorAll('.red')
  [...elems].forEach(elem => elem.className = 'blue')
  ```

  

- `document.getElementsByTagName(tagName)`

  - 태그명으로 요소 노드를 모두 선택한다.
  - HTMLCollection을 반환한다.
  - 모든 브라우저에서 동작한다.

  ```javascript
  const elems = document.getElementsByTagName('li')
  
  [...elems].forEach(elem => elem.className = 'blue')
  ```

  

- `document.querySelectorAll(selector)`

  - 지정된 CSS 선택자를 사용하여 요소 노드를 모두 선택한다.
  - NodeList를 반환한다.
    - 실시간(live)으로 Node의 상태 변경을 반영하지 않는다.
  - IE8 이상의 브라우저에서 동작

  ```javascript
  const elems = document.querySelectorAll('li.red');
  
  [...elems].forEach(elem => elem.className = 'blue');
  ```

  



### DOM Traversing(탐색)

- `parentNode`

  - 부모 노드를 탐색한다.
  - HTMLElement를 상속받은 객체를 반환한다.
  - 모든 브라우저에서 동작한다.

  ```javascript
  const elem = document.querySelector('#two')
  
  elem.parentNode.className = 'blue'
  ```



- `firstChild`, `lastChild`

  - 자식 노드를 탐색한다.
  - HTMLElement를 상속받은 객체를 반환한다.
  - IE9 이상의 브라우저에서 동작한다.

  ```javascript
  const elem = document.querySelector('ul')
  
  elem.firstChild.className = 'blue'
  elem.lastChild.className = 'blue'
  ```

  - 위 예제는 제대로 동작하지 않는데 그 이유는 다음과 같다.
    - IE를 제외한 대부분의 브라우저들은 요소 사이의 공백 또는 줄바꿈 문자를 텍스트 노드로 취급한다.
    - 이것을 회피하기 위해서는 아래와 같이 HTML의 공백을 제거하거나 `jQuery: .prev()`와 `jQuery: .next()`를 사용한다.
    - 또는 `firstElementChild`, `lastElementChild`를 사용할 수도 있다. 이 두가지 프로퍼티는 모든 IE9 이상에서 정상 동작한다.

  ```html
  <ul><li
    id='one' class='red'>Seoul</li><li
    id='two' class='red'>Daejeon</li><li
    id='three' class='red'>Daegu</li><li
    id='four'>Busan</li></ul>
  ```

  ```javascript
  const elem = document.querySelector('ul')
  
  elem.firstElementChild.className = 'blue'
  elem.lastElementChild.className = 'blue'
  ```



- `hasChildNodes()`

  - 자식 노드가 있는지 확인한다. 
  - Boolean 값을 반환한다.
  - 모든 브라우저에서 동작한다.

  ```javascript
  const hasChild = document.hasChildNodes('ul')
  console.log(hasChild)   // true
  ```



- `childNodes`, `children`

  - `childNodes`
    - 자식 노드의 컬렉션을 반환한다. 텍스트 요소를 포함한 모든 자식 요소를 반환한다.
    - NodeList를 반환한다.
    - IE9 이상의 브라우저에서 동작한다.
  - `children`
    - 자식 노드의 컬렉션을 반환한다. 자식 요소 중에서 Element type 요소만을 반환한다.
    - HTMLCollection을 반환한다.
    - IE9 이상의 브라우저에서 동작한다.

  ```javascript
  const elem = document.querySelector('ul');
  
  if (elem.hasChildNodes()) {
    console.log(elem.childNodes);
    // 텍스트 요소를 포함한 모든 자식 요소를 반환한다.
    // NodeList(9) [text, li#one.red, text, li#two.red, text, li#three.red, text, li#four, text]
  
    console.log(elem.children);
    // 자식 요소 중에서 Element type 요소만을 반환한다.
    // HTMLCollection(4) [li#one.red, li#two.red, li#three.red, li#four, one: li#one.red, two: li#two.red, three: li#three.red, four: li#four]
    [...elem.children].forEach(el => console.log(el.nodeType)) // 1
  }
  ```

  

- `previousSibling`, `nextSibling` / `previousElementSibling`, `nextElementsSibling`

  - `previousSibling`, `nextSibling`
    - 형제 노드를 탐색한다. **text node를 포함한 모든 형제 노드를 탐색한다.**
    - HTMLElement를 상속받은 객체를 반환한다.
    - 모든 브라우저에서 동작한다.
  - `previousElementSibling`, `nextElementsSibling`
    - 형제 노드를 탐색한다. **형제 노드 중에서 Element type 요소만을 탐색한다.**
    - HTMLElement를 상속받은 객체를 반환한다.
    - IE9 이상의 브라우저에서 동작한다.

  ```javascript
  const elem = document.querySelector('ul')
  
  elem.firstElementChild.nextElementSibling.className = 'blue'
  elem.firstElementChild.nextElementSibling.previousElementSibling.className = 'blue'
  ```

  

## DOM Manipulation

- 텍스트 노드에 접근 및 수정

  - 요소의 텍스트는 텍스트 노드에 저장되어 있다. 텍스트 노드에 접근하려면 아래와 같은 수순이 필요하다.
    - 해당 텍스트 노드의 부모 노드를 선택한다. 텍스트 노드는 요소 노드의 자식이다.
    - `firstChild` 프로퍼티를 사용하여 텍스트 노드를 탐색한다.
    - 텍스트 노드의 유일한 프로퍼티(`nodeValue`)를 이용하여 텍스트를 취득한다.
    - `nodeValue`를 이용하여 텍스트를 수정한다.
  - `nodeValue`
    - 노드의 값을 반환한다.
    - 텍스트 노드의 경우는 문자열, 요소 노드의 경우 null 반환한다.
    - IE6 이상의 브라우저에서 동작한다.
  - `nodeName`, `nodeType`을 통해 노드의 정보를 취득할 수 있다.

  ```javascript
  const one = document.getElementById('one')
  
  // nodeName, nodeType을 통해 노드의 정보를 취득할 수 있다.
  console.log(one.nodeName) // LI
  console.log(one.nodeType) // 1: Element node
  
  // firstChild 프로퍼티를 사용하여 텍스트 노드를 탐색한다.
  const textNode = one.firstChild
  
  console.log(textNode.nodeName) // #text
  console.log(textNode.nodeType) // 3: Text node
  
  // nodeValue 프로퍼티를 사용하여 노드의 값을 취득한다.
  console.log(textNode.nodeValue) // Seoul
  
  // nodeValue 프로퍼티를 이용하여 텍스트를 수정한다.
  textNode.nodeValue = 'Ulsan'
  ```

  

- 어트리뷰트 노드에 접근 및 수정

  - `className`
    - class 어트리뷰트의 값을 취득 또는 변경한다. 
    - `className` 프로퍼티에 값을 할당하는 경우, class 어트리뷰트가 존재하지 않으면 class 어트리뷰트를 생성하고 지정된 값을 설정한다. 
    - class 어트리뷰트의 값이 여러 개일 경우, 공백으로 구분된 문자열이 반환되므로 String 메소드 `split(' ')`를 사용하여 배열로 변경하여 사용한다.
    - 모든 브라우저에서 동작한다.
  - `classList`
    - `add`, `remove`, `item`, `toggle`, `contains`, `replace` 메소드를 제공한다.
    - IE10 이상의 브라우저에서 동작한다.

  ```javascript
  const elems = document.querySelectorAll('li')
  
  // className
  [...elems].forEach(elem => {
    // class 어트리뷰트 값을 취득하여 확인
    if (elem.className === 'red') {
      // class 어트리뷰트 값을 변경한다.
      elem.className = 'blue'
    }
  })
  
  // classList
  [...elems].forEach(elem => {
    // class 어트리뷰트 값 확인
    if (elem.classList.contains('blue')) {
      // class 어트리뷰트 값 변경한다.
      elem.classList.replace('blue', 'red')
    }
  })
  ```

  - `id`
    - id 어트리뷰트의 값을 취득 또는 변경한다. 
    - id 프로퍼티에 값을 할당하는 경우, id 어트리뷰트가 존재하지 않으면 id 어트리뷰트를 생성하고 지정된 값을 설정한다.
    - 모든 브라우저에서 동작한다.

  ```javascript
  // h1 태그 요소 중 첫번째 요소를 취득
  const heading = document.querySelector('h1')
  
  console.dir(heading) // HTMLHeadingElement: h1
  console.log(heading.firstChild.nodeValue) // Cities
  
  // id 어트리뷰트의 값을 변경.
  // id 어트리뷰트가 존재하지 않으면 id 어트리뷰트를 생성하고 지정된 값을 설정
  heading.id = 'heading';
  console.log(heading.id); // heading
  ```

  - `hasAttribute(attribute)`
    - 지정한 어트리뷰트를 가지고 있는지 검사한다.
    - Boolean 값을 반환한다.
    - IE8 이상의 브라우저에서 동작한다.
  - `getAttribute(attribute)`
    - 어트리뷰트의 값을 취득한다.
    - 문자열을 반환한다.
    - 모든 브라우저에서 동작한다.
  - `setAttribute(attribute)`
    - 어트리뷰트와 어트리뷰트 값을 설정한다.
    - undefined를 반환한다.
    - 모든 브라우저에서 동작한다.
  - `removeAttribute(attribute)`
    - 지정한 어트리뷰트를 제거한다.
    - undefined를 반환한다.
    - 모든 브라우저에서 동작한다.

  ```html
  <!DOCTYPE html>
  <html>
      <body>
          <input type="text">
          <script>
              const input = document.querySelector('input[type=text]')
  
              // value 어트리뷰트가 존재하지 않으면
              if (!input.hasAttribute('value')) {
                  // value 어트리뷰트를 추가하고 값으로 'hello!'를 설정
                  input.setAttribute('value', 'hello!')
              }
  
              // value 어트리뷰트 값을 취득
              console.log(input.getAttribute('value')) // hello!
  
              // value 어트리뷰트를 제거
              input.removeAttribute('value')
  
              // value 어트리뷰트의 존재를 확인
              console.log(input.hasAttribute('value')) // false
          </script>
      </body>
  </html>
  ```

  

- HTML 콘텐츠 조작

  - 마크업이 포함된 콘텐츠를 추가하는 행위는 크로스 스크립팅 공격(XSS: Cross-Site Scripting Attacks)에 취약하므로 주의가 필요하다.
    - 스크립트 태그를 추가하여 자바스크립트가 실행되도록 할 수 있고(최신 브라우저는 막아놨다).
    - 에러 이벤트를 발생시켜 스크립트가 실행되도록 할 수 있다.
  - `textContent`
    - 요소의 텍스트 콘텐츠를 취득 또는 변경한다. 이때 마크업은 무시된다. 
    - textContent를 통해 요소에 새로운 텍스트를 할당하면 텍스트를 변경할 수 있다. 
    - 이때 순수한 텍스트만 지정해야 하며 마크업을 포함시키면 문자열로 인식되어 그대로 출력된다.
    - IE9 이상의 브라우저에서 동작한다.

  ```javascript
  // 요소의 텍스트 컨텐츠 취득
  const ul = document.querySelector('ul')
  console.log(ul.textContent)
  /*
  Seoul
  Daejeon
  Daegu
  Busan
  */
  
  
  // 요소의 텍스트 컨텐츠 변경
  const oneLi = document.querySelector('#one')
  oneLi.textContent = 'Yangpyung'
  console.log(oneLi.textContent)		// Yangpyung
  
  // 마크업을 포함
  oneLi.textContent = '<h1>Yangpyung</H1>'
  console.log(oneLi.textContent)		// <h1>Yangpyung</H1>
  ```

  - `innerText`
    - innerText 프로퍼티를 사용하여도 요소의 텍스트 콘텐츠에만 접근할 수 있다. 하지만 아래의 이유로 사용하지 않는 것이 좋다.
    - 비표준이다.
    - CSS에 순종적이다. 예를 들어 CSS에 의해 비표시(visibility: hidden;)로 지정되어 있다면 텍스트가 반환되지 않는다.
    - CSS를 고려해야 하므로 textContent 프로퍼티보다 느리다.

  - `innerHTML`
    - 해당 요소의 모든 자식 요소를 포함하는 모든 콘텐츠를 하나의 문자열로 취득할 수 있다. 
    - 이 문자열은 마크업을 포함한다.
    - innerHTML 프로퍼티를 사용하여 마크업이 포함된 새로운 콘텐츠를 지정하면 새로운 요소를 DOM에 추가할 수 있다.
    - 그러나 마크업이 포함된 콘텐츠를 추가하는 것은 크로스 스크립팅 공격(XSS: Cross-Site Scripting Attacks)에 취약하다.

  ```javascript
  const one = document.getElementById('one')
  
  // 마크업이 포함된 콘텐츠 취득
  console.log(one.innerHTML) // Seoul
  
  // 마크업이 포함된 콘텐츠 변경
  one.innerHTML = '<h1>Yangpyung</h1>'
  
  // 마크업이 포함된 콘텐츠 취득
  console.log(one.innerHTML)	// <h1>Yangpyung</h1>
  ```

  

- DOM 조작 방식

  - innerHTML 프로퍼티를 사용하지 않고 새로운 콘텐츠를 추가할 수 있는 방법은 DOM을 직접 조작하는 것이다. 
  - 한 개의 요소를 추가하는 경우 사용한다. 
  - 이 방법은 다음의 수순에 따라 진행한다.
    - 요소 노드 생성: `createElement()` 메소드를 사용하여 새로운 요소 노드를 생성한다. `createElement()` 메소드의 인자로 태그 이름을 전달한다.
    - 텍스트 노드 생성: `createTextNode()` 메소드를 사용하여 새로운 텍스트 노드를 생성한다. 경우에 따라 생략될 수 있지만 생략하는 경우, 콘텐츠가 비어 있는 요소가 된다.
    - 생성된 요소를 DOM에 추가: `appendChild()` 메소드를 사용하여 생성된 노드를 DOM tree에 추가한다. 또는 `removeChild()` 메소드를 사용하여 DOM tree에서 노드를 삭제할 수도 있다.

  - `createElement(tagName)`
    - 태그이름을 인자로 전달하여 요소를 생성한다.
    - HTMLElement를 상속받은 객체를 반환한다.
    - 모든 브라우저에서 동작한다.
  - `createTextNode(text)`
    - 텍스트를 인자로 전달하여 텍스트 노드를 생성한다.
    - Text 객체를 반환한다.
    - 모든 브라우저에서 동작한다.
  - `appendChild(Node)`
    - 인자로 전달한 노드를 마지막 자식 요소로 DOM 트리에 추가한다.
    - 추가한 노드를 반환한다.
    - 모든 브라우저에서 동작한다.
  - `removeChild(Node)`
    - 인자로 전달한 노드를 DOM 트리에 제거한다.
    - 제거한 노드를 반환한다.
    - 모든 브라우저에서 동작한다.

  ```javascript
  // 태그이름을 인자로 전달하여 요소를 생성
  const newElem = document.createElement('li')
  
  // 텍스트 노드를 생성
  const newText = document.createTextNode('GoYang')
  
  // 텍스트 노드를 newElem 자식으로 DOM 트리에 추가
  newElem.appendChild(newText)
  
  const container = document.querySelector('ul')
  
  // newElem을 container의 자식으로 DOM 트리에 추가. 마지막 요소로 추가된다.
  container.appendChild(newElem)
  
  const removeElem = document.getElementById('one')
  
  // container의 자식인 removeElem 요소를 DOM 트리에 제거한다.
  container.removeChild(removeElem)
  ```

  

- `insertAdjacentHTML(position, string)`

  - 인자로 전달한 텍스트를 HTML로 파싱하고 그 결과로 생성된 노드를 DOM 트리의 지정된 위치에 삽입한다. 
  - 첫번째 인자는 삽입 위치, 두번째 인자는 삽입할 요소를 표현한 문자열이다. 첫번째 인자로 올 수 있는 값은 아래와 같다.
    - ‘beforebegin’
    - ‘afterbegin’
    - ‘beforeend’
    - ‘afterend’

  ```html
  <!--beforebegin-->
  <h1>
      <!--afterbegin-->
      Hello!
      <!--beforeend-->
  </h1>
  <!--afterend-->
  ```

  - 모든 브라우저에서 동작한다.

  ```javascript
  const one = document.getElementById('one')
  // 마크업이 포함된 요소 추가
  one.insertAdjacentHTML('afterend', '<li>Pyeongchang</li>')
  ```

  

- `innerHTML` 대 DOM 조작 방식 대 `insertAdjacentHTML()`

  - `innerHTML`
    - DOM 조작 방식에 비해 빠르고 간편하다.
    - 간편하게 문자열로 정의한 여러 요소를 DOM에 추가할 수 있다.
    - 콘텐츠를 취득할 수 있다.
    - XSS공격에 취약점이 있기 때문에 사용자로 부터 입력받은 콘텐츠(untrusted data: 댓글, 사용자 이름 등)를 추가할 때 주의하여야 한다.
    - 해당 요소의 내용을 덮어 쓴다. 즉, HTML을 다시 파싱한다. 이것은 비효율적이다.
  - DOM 조작 방식
    - 특정 노드 한 개(노드, 텍스트, 데이터 등)를 DOM에 추가할 때 적합하다.
    - innerHTML보다 느리고 더 많은 코드가 필요하다.
  - `insertAdjacentHTML()`
    - 간편하게 문자열로 정의된 여러 요소를 DOM에 추가할 수 있다.
    - 삽입되는 위치를 선정할 수 있다.
    - XSS공격에 취약점이 있기 때문에 사용자로 부터 입력받은 콘텐츠(untrusted data: 댓글, 사용자 이름 등)를 추가할 때 주의하여야 한다.
  - 결론
    - `nnerHTML`과 `insertAdjacentHTML()`은 크로스 스크립팅 공격(XSS)에 취약하다. 
    - 따라서 untrusted data의 경우, 주의하여야 한다. 
    - 텍스트를 추가 또는 변경시에는 `textContent`, 새로운 요소의 추가 또는 삭제시에는 DOM 조작 방식을 사용하도록 한다.



## Style

- stlye 프로퍼티

  - style 프로퍼티를 사용하면 inline 스타일 선언을 생성한다. 
  - 특정 요소에 inline 스타일을 지정하는 경우 사용한다.

  ```javascript
  const four = document.getElementById('four')
  
  // inline 스타일 선언을 생성
  four.style.color = 'blue';
  
  // font-size와 같이 '-'으로 구분되는 프로퍼티는 카멜케이스로 변환하여 사용한다.
  four.style.fontSize = '2em';
  ```

  - style 프로퍼티의 값을 취득하려면 `window.getComputedStyle`을 사용한다. 
    - `window.getComputedStyle` 메소드는 인자로 주어진 요소의 모든 CSS 프로퍼티 값을 반환한다.

  ```html
  <!DOCTYPE html>
  <html>
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <meta http-equiv="X-UA-Compatible" content="ie=edge">
          <title>style 프로퍼티 값 취득</title>
          <style>
              .box {
                  width: 100px;
                  height: 50px;
                  background-color: red;
                  border: 1px solid black;
              }
          </style>
      </head>
      <body>
          <div class="box"></div>
          <script>
              const box = document.querySelector('.box');
              
              /*
              요소에 적용된 CSS 프로퍼티를 반환한다.
              @param {HTTPElement} elem - 대상 요소 노드.
              @param {string} prop - 대상 CSS 프로퍼티.
              @returns {string} CSS 프로퍼티의 값.
              */
              function getStyle(elem, prop) {
                  return window.getComputedStyle(elem, null).getPropertyValue(prop);
              }
  
              const width = getStyle(box, 'width');
              const height = getStyle(box, 'height');
              const backgroundColor = getStyle(box, 'background-color');
              const border = getStyle(box, 'border');
  
              console.log('width: ' + width)		// width: 100px
              console.log('height: ' + height)	// height: 50px
              console.log('backgroundColor: ' + backgroundColor)	// backgroundColor: rgb(255, 0, 0)
              console.log('border: ' + border)	// border: 1px solid rgb(0, 0, 0)
          </script>
      </body>
  </html>
  ```

