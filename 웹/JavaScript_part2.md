# 연산자

## 할당 연산자

- 할다 연산자

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


  - "+","-":양수, 음수 변경 및 표현, 단, "+"는 음수를 양수로 변경하지 않는다.
  - 숫자 형 문자열의 경우 숫자로 자동 형변환된다.
  - "++","--": 증가 연산자와 감소 연산자. 피연산자 앞에 오는지 뒤에 오는지에 따라 효과가 달라진다.

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

  

- 논리 연산자(단축평가가 적용 된다)

  ```javascript
  //and 는 &&로 표현
  console.log(true && false)
  //or 는 ||로 표현
  console.log(true || false)
  //not 은 !로 표현
  console.log(!true)
  //true, false값이 아닌 값 앞에 !를 붙이면 해당 값은 true, false값 중 하나가 된다.
  console.log("A") //A
  console.log(!"A") //false, 본래 비어있지 않은 문자열은 true값이므로 부정은 false가 된다
  console.log(!!"A") //true, false의 부정이므로 true가 된다.
  //즉 !!는 boolean 타입이 아닌 값을 boolean 타입으로 바꿔주는 역할을 한다고 보면 된다.
  
  //단축평가
  console.log(1 && false)
  console.log(0 && false)
  console.log(0 || false)
  console.log(1 || false)
  
  
  out
  false
  true
  false
  
  false
  0
  false
  1
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

  - for in

  ```js
  const fruits = {
      'apple':2,
      'banana':10,
      'tomato':10,
      'watermelon':2,
  }
  
  //어차피 문자열이 올 것을 알고 있으므로 아래와 같이 문자열 안에 쓰지 않아도 된다.
  const fruits = {
      apple:2,
      banana:10,
      tomato:10,
      watermelon:2,
  }
  
  for (const fruit in fruits){
      console.log(fruit,fruits[fruit])
  }
  
  out
  apple 2
  banana 10
  tomato 10
  watermelon 2
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

  

​    

# 함수

- Javascript의 객체는 1급 객체다.
  - 변수에 저장할 수 있다.
  - 함수의 리턴값이 될 수 있다.
  - 함수의 인자가 될 수 있다.

```javascript
// 함수의 선언식
// 인자 없이
function f(){
    return 10
}
console.log(f())

out
10

//인자가 있을 때
function f(a){
    return 10+a
}
console.log(f(3))

out
13

//디폴트값 설정
function f(a=3){
    return 10+a
}
console.log(f())

out
13



//함수의 표현식
//익명함수(파이썬의 lamda와 유사), 주로 한 번 쓰고 쓰지 않을 함수를 지정할때 사용
const bar = function(a,b){ //함수의 이름이 존재X
    return a+b
}
console.log(bar(10,20))  //변수로 함수를 실행시킨다.

out
30


//함수명을 지정
const bar1 = function bar2(a,b){  
    //꼭 함수명을 변수명과 동일하게 할 필요는 없으나 일반적으로 동일하게 한다.		
    return a+b
}
console.log(bar1(10,20))  //bar2로는 실행시킬 수 없다.

out
30


//화살표 함수
//화살표 함수는 함수의 선언식 & 표현식과 문법적으로 차이가 있고, 내부 동작도 다르다.
//this를 사용할 경우에 차이가 존재한다.
const ssum = (a,b) => {
    return a+b
}
console.log(ssum(10,20))

out
30

//매개변수가 1개일 경우 괄호를 안쓰는 것도 가능하다(그러나 괄호를 쓰는 것이 권장된다).
const pprint = a => {
    return a
}

// 중괄호 안에 들어가는 내용이 한 줄이면 중괄호 없이 가능하다
const pprint = a => return a



// 함수의 인자의 개수가 부족하거나 넘치거나 없어도 에러가 발생하지 않는다.
function wrong(a,b){
    console.log(a,b)
}

wrong()
wrong(1)
wrong(1,2,3)

out
undefined undefined  //입력을 안하면 에러가 아닌 undefined를 출력
1 undefined //모자라면 받은 것만 출력
1 2         //넘치면 필요한 만큼만 받는다.




// rest parameter라는 python의 *args와 유사한 기능이 존재
// *의 역할을 ...이 한다.
function restOperator1(...numbers){
    console.log(numbers)
}

restOperator1(1,2,3,4,5)

out
[1,2,3,4,5]

function restOperator2(a,b,...numbers){
    console.log(a,b,numbers)
}

restOperator2(1,2,3,4,5)

out
1 2 [3,4,5]



//spead operator
function spreadOperator(a,b,c){
    console.log(a,b,c)
}

let numbers = [1,2,3]

spreadOperator(numbers[0],numbers[1],numbers[2])
spreadOperator(...numbers) //spreadOperator 위와 정확히 동일한 코드이다.
//귀찮게 인덱스로 접근해서 넣어주지 않아도 ...을 쓰면 알아서 배열의 요소를 흩뿌려준다.

out
1 2 3
1 2 3
```






# 자료구조

- Array(파이썬의 리스트): 파이썬과 마찬가지로 동적(배열 크기가 정해져 있지 않음)으로 배열의 추가와 삭제가 가능

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



- 오브젝트(파이썬의 딕셔너리)
  - 객체의 값은 이름과 값의 쌍(`{이름:값}`)으로 이루어져 있으며 이 쌍을 property라고 부른다.
  - property는 어떠한 데이터 타입이라도 가능하다.
  - property 값이 함수일 경우, 일반 함수와 구분하기 위해 method라 부른다.

```js
  const me = {
     name : '홍길동',  //오브젝트 안에서는 따옴표를 쓰지 않아도 된다.
     'phone number':'01012345678',  //그러나 이처럼 띄어쓰기 등을 쓰고자 하면 따옴표 써야 한다.
     electronics:{
          phone:'galaxy s8',
        	laptop:'samsung notebook 11',
        	keyboards:['happyhacking','logitech']
    	}
    }
  console.log(me.name)
  console.log(me.electronics.keyboards[0])
  console.log(me.height) //설정하지 않은 키를 입력하면
    
  out
  홍길동
  happyhacking
  undefined  //undefined가 출력
    
  console.log(Object.keys(me))    //키만 배열로 반환
  console.log(Object.values(me))  //value만 배열로 반환
  console.log(Object.entries(me)) //key,value를 array에 넣어서 반환
    
  out
  ["name", "phone number", "electronics"]
  ["홍길동", "01012345678", {phone: "galaxy s8", laptop: "samsung notebook 11", keyboar...}]
  [["name", "홍길동"], ["phone number", "01012345678"], ["electronics", {…}]]
    
    
    
  //오브젝트 리터럴
  //키와 밸류가 같을 경우 하나만 적으면 된다.
  const a = 1
  const b = 2
  const c = 3
    
  const abc = {
      'a':a,
      'b':b,
      'c':c,
  }
  //위와 같이 쓰지 않고 아래와 같이 쓰는 것이 가능
  const abc = {
      a,
      b,
      c,
  }
  console.log(abc.a)
    
  out
  1
  
  
//메소드
  var Person = {
    // Person이라는 객체 내부에 위치한 sayHello라는 method
      sayHello: function(){
          console.log('Hello!')
      }
  }
```

  

- JSON과 object의 치환

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





# 예외처리

- try, catch, finally를 사용하여 예외처리

  ```js
  try {
  //정상이라면 이 코드는 아무런 문제없이 블록의 시작부터 끝까지 실행됨.
  
  } catch(error) {
  //이 블록 내부의 문장들은 오직 try 블록에서 예외가 발생할 경우에만 실행된다.
  
  } finally(){
  //try 블록에서 일어난 일에 관계없이 무조건 실행될 코드가 위치한다.
  }
  ```

- throw는사용자 지정 에러를 지정하여 예외를 발생시킬 수 있게 해준다.





# 정규표현식

> https://poiemaweb.com/js-regexp

- 닉네임, 비밀번호 검증을 위한 정규표현식이 존재





# 기타

- 현재 페이지의 url을 가져오는 방법
  - 현재 페이지의 url 전체 가져오기: `document.location.href` 또는 `document.URL`
  - 현재 페이지 url의 쿼리문만 가져오기: `document.location.href.split("?")`