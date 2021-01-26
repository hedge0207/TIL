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