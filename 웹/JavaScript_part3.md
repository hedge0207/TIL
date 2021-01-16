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