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



-  논리 연산자

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
```
  
- for in
    - 객체의 문자열 키(key)를 순회하기 위한 문법.
    - 배열에는 사용하지 않는 것이 좋다.
    - 배열은 순서를 보장하는 데이터 구조이지만 for in은 객체에 사용할 것을 염두했기에 순서를 보장하지 않기 때문이다.
  
  ```js
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

```js
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
    - 키: 빈 문자열을 포함하는 모든 문자열 또는  symbol 값
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



