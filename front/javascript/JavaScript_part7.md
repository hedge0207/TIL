

# 프로미스

- 프로미스
  - 자바스크립트는 비동기 처리를 위한 하나의 패턴으로 콜백 함수를 사용한다. 
    - 하지만 전통적인 콜백 패턴은 콜백 헬로 인해 가독성이 나쁘고 비동기 처리 중 발생한 에러의 처리가 곤란하며 여러 개의 비동기 처리를 한번에 처리하는 데도 한계가 있다.
  - ES6에서는 비동기 처리를 위한 또 다른 패턴으로 프로미스(Promise)를 도입했다. 
    - 프로미스는 비동기 작업을 위한 JS 객체이다.
    - 프로미스는 전통적인 콜백 패턴이 가진 단점을 보완하며 비동기 처리 시점을 명확하게 표현할 수 있다는 장점이 있다.





## 콜백 패턴의 단점

### 콜백 헬(Callback Hell)

- 비동기 처리를 위해 콜백 패턴을 사용하면 처리 순서를 보장하기 위해 여러 개의 콜백 함수가 네스팅(nesting, 중첩)되어 복잡도가 높아지는 것.

  - 콜백 헬은 가독성을 나쁘게 하며 실수를 유발하는 원인이 된다.

  ```javascript
  // 출처: https://velog.io/@yujo/JS%EC%BD%9C%EB%B0%B1-%EC%A7%80%EC%98%A5%EA%B3%BC-%EB%B9%84%EB%8F%99%EA%B8%B0-%EC%A0%9C%EC%96%B4
  setTimeout(
      (name) => {
          let coffeeList = name;
          console.log(coffeeList);
          setTimeout(
              (name) => {
                  coffeeList += ', ' + name;
                  console.log(coffeeList);
                  setTimeout(
                      (name) => {
                          coffeeList += ', ' + name;
                          console.log(coffeeList);
                          setTimeout(
                              (name) => {
                                  coffeeList += ', ' + name;
                                  console.log(coffeeList);
                              },
                              500,
                              'Latte',
                          );
                      },
                      500,
                      'Mocha',
                  );
              },
              500,
              'Americano',
          );
      },
      500,
      'Espresso',
  );
  ```



- 발생 이유

  - 비동기 처리 모델은 실행 완료를 기다리지 않고 즉시 다음 태스크를 실행한다. 
    - 따라서 비동기 함수(비동기를 처리하는 함수) 내에서 처리 결과를 반환(또는 전역 변수에의 할당)하면 기대한 대로 동작하지 않는다.

  ```html
  <!DOCTYPE html>
  <html>
      <body>
          <script>
              // 비동기 함수
              function get(url) {
                  // XMLHttpRequest 객체 생성
                  const xhr = new XMLHttpRequest()
  
                  // 서버 응답 시 호출될 이벤트 핸들러
                  xhr.onreadystatechange = function () {
                      // 서버 응답 완료가 아니면 무시
                      if (xhr.readyState !== XMLHttpRequest.DONE) return
  
                      if (xhr.status === 200) { // 정상 응답
                          console.log(xhr.response)
                          // 비동기 함수의 결과에 대한 처리는 반환할 수 없다.
                          return xhr.response //@
                      } else { // 비정상 응답
                          console.log('Error: ' + xhr.status)
                      }
                  };
  
                  // 비동기 방식으로 Request 오픈
                  xhr.open('GET', url)
                  // Request 전송
                  xhr.send()
              }
  
              // 비동기 함수 내의 readystatechange 이벤트 핸들러에서 처리 결과를 반환(@)하면 순서가 보장되지 않는다.
              const res = get('http://jsonplaceholder.typicode.com/posts/1')
              console.log(res)	// undefined #
          </script>
      </body>
  </html>
  ```

  - 예시의 비동기 함수 내의 `onreadystatechange` 이벤트 핸들러에서 처리 결과를 반환(`@`)하면 순서가 보장되지 않는다. 
    - 즉, `#`에서 `get` 함수가 반환한 값을 참조할 수 없다.
    - `get` 함수가 호출되면 `get` 함수의 실행 컨텍스트가 생성되고 호출 스택(Call stack,실행 컨텍스트 스택)에서 실행된다. 
    - `get` 함수가 반환하는 `xhr.response`는 `onreadystatechange` 이벤트 핸들러가 반환한다. 
    - `readystatechange` 이벤트는 발생하는 시점을 명확히 알 수 없지만 반드시 `get` 함수가 종료한 이후 발생한다.
    - `get` 함수의 마지막 문인 `xhr.send()`가 실행되어야 request를 전송하고, request를 전송해야 `readystatechange` 이벤트가 발생할 수 있기 때문이다.
    - `get` 함수가 종료하면 곧바로 `console.log`(`#`)가 호출되어 호출 스택에 들어가 실행된다. `console.log`가 호출되기 직전에 `readystatechange` 이벤트가 이미 발생했다하더라도 이벤트 핸들러는 `console.log`보다 먼저 실행되지 않는다.
    - `readystatechange` 이벤트의 이벤트 핸들러는 이벤트가 발생하면 즉시 실행되는 것이 아니다.
    - 이벤트가 발생하면 일단 태스크 큐( 혹은 Event Queue)로 들어가고, 호출 스택이 비면 그때 이벤트 루프에 의해 호출 스택으로 들어가 실행된다. 
    - `console.log` 호출 시점 이전에 `readystatechange` 이벤트가 이미 발생했다하더라도 `get` 함수가 종료하면 곧바로 `console.log`가 호출되어 호출 스택에 들어가기 때문에 `readystatechange` 이벤트의 이벤트 핸들러는 `console.log`가 종료되어 호출 스택에서 빠진 이후 실행된다. 
    - 만약 `get` 함수 이후에 `console.log`가 100번 호출된다면 `readystatechange` 이벤트의 이벤트 핸들러는 모든 `console.log`가 종료한 이후에나 실행된다.
    - 때문에 `get` 함수의 반환 결과를 가지고 후속 처리를 할 수 없다. 
    - 즉, 비동기 함수의 처리 결과를 반환하는 경우, 순서가 보장되지 않기 때문에 그 반환 결과를 가지고 후속 처리를 할 수 없다. 
    - 즉, 비동기 함수의 처리 결과에 대한 처리는 비동기 함수의 콜백 함수 내에서 처리해야 한다. 이로 인해 콜백 헬이 발생한다.







### 예외 처리의 한계

- 콜백 방식의 비동기 처리가 갖는 문제점 중에서 가장 심각한 것은 에러 처리가 곤란하다는 것이다. 

  ```javascript
  // 콜백 함수를 사용하지 않을 때
  try {
      throw new Error('Error!')
  } catch (e) {
      console.log('에러를 캐치한다.')	// 에러를 캐치한다.
      console.log(e)					// Error: Error!
  }
  
  // 콜백 함수 사용
  try {
    setTimeout(() => { throw new Error('Error!') }, 1000)
  } catch (e) {
    console.log('에러를 캐치하지 못한다.')
    console.log(e)
  }
  ```

  - `try` 블록 내에서 `setTimeout` 함수가 실행되면 1초 후에 콜백 함수가 실행되고 이 콜백 함수는 예외를 발생시킨다. 
  - 하지만 이 예외는 `catch` 블록에서 캐치되지 않는다.
    - 비동기 처리 함수의 콜백 함수는 해당 이벤트(timer 함수의 tick 이벤트, XMLHttpRequest의 readystatechange 이벤트 등)가 발생하면 태스트 큐(Task queue)로 이동한 후 호출 스택이 비어졌을 때, 호출 스택으로 이동되어 실행된다. 
    - `setTimeout` 함수는 비동기 함수이므로 콜백 함수가 실행될 때까지 기다리지 않고 즉시 종료되어 호출 스택에서 제거된다. 
    - 이후 tick 이벤트가 발생하면 `setTimeout` 함수의 콜백 함수는 태스트 큐로 이동한 후 호출 스택이 비어졌을 때 호출 스택으로 이동되어 실행된다. 
    -  `setTimeout` 함수의 콜백 함수를 호출한 것은 `setTimeout` 함수가 아니라 tick 이벤트이다.
    - 예외(exception)는 호출자(caller) 방향으로 전파된다. 
    - `setTimeout` 함수의 콜백 함수의 호출자(caller)는  tick 이벤트이므로 tick에 예외가 전파된다.
    - 따라서 `setTimeout` 함수의 콜백 함수 내에서 발생시킨 에러는 catch 블록에서 캐치되지 않아 프로세스는 종료된다.



## 프로미스 생성

- 프로미스는 `Promise` 생성자 함수를 통해 인스턴스화한다. 

  - `Promise` 생성자 함수는 비동기 작업을 수행할 콜백 함수를 인자로 전달받는다.
    - 이 콜백 함수는 executor라 불리는 `resolve`와 `reject` 콜백 함수 쌍을 인자로 전달받는다.
    - `resolve`: 기능을 정상적으로 수행하면 호출되어 최종 데이터를 전달하는 콜백함수.
    - `reject`: 기능을 수행하다 문제가 생기면 호출되는 콜백함수.
  - 새로운 프로미스 객체가 생성되면 프로미스 코드 블록이 자동으로 실행된다.

  ```javascript
  // Promise 객체의 생성
  const promise = new Promise((resolve, reject) => {
    // 비동기 작업을 수행한다.
  
    if (/* 비동기 작업 수행 성공 */) {
      resolve('result')
    }
    else { /* 비동기 작업 수행 실패 */
      reject('failure reason')
    }
  })
  ```



- 비동기 처리가 성공(fulfilled)하였는지 또는 실패(rejected)하였는지 등의 상태(state) 정보.

  | 상태      | 의미                                       | 구현                                               |
  | --------- | ------------------------------------------ | -------------------------------------------------- |
  | pending   | 비동기 처리가 아직 수행되지 않은 상태      | resolve 또는 reject 함수가 아직 호출되지 않은 상태 |
  | fulfilled | 비동기 처리가 수행된 상태 (성공)           | resolve 함수가 호출된 상태                         |
  | rejected  | 비동기 처리가 수행된 상태 (실패)           | reject 함수가 호출된 상태                          |
  | settled   | 비동기 처리가 수행된 상태 (성공 또는 실패) | resolve 또는 reject 함수가 호출된 상태             |



- Promise 생성자 함수가 인자로 전달받은 콜백 함수는 내부에서 비동기 처리 작업을 수행한다. 

  - 비동기 처리가 성공하면 콜백 함수의 인자로 전달받은 resolve 함수를 호출한다. 이때 프로미스는 ‘fulfilled’ 상태가 된다. 
  - 비동기 처리가 실패하면 reject 함수를 호출한다. 이때 프로미스는 ‘rejected’ 상태가 된다.

  ```javascript
  const promiseAjax = (method, url, payload) => {
      // 비동기 함수 내에서 Promise 객체를 생성
      return new Promise((resolve, reject) => {
          // 내부에서 비동기 처리를 구현
          const xhr = new XMLHttpRequest()
          xhr.open(method, url)
          xhr.setRequestHeader('Content-type', 'application/json');
          xhr.send(JSON.stringify(payload))
  
          xhr.onreadystatechange = function () {
              // 서버 응답 완료가 아니면 무시
              if (xhr.readyState !== XMLHttpRequest.DONE) return
  
              if (xhr.status >= 200 && xhr.status < 400) {
                  // resolve 메소드를 호출하면서 처리 결과를 전달
                  resolve(xhr.response) // Success!
              } else {
                  // reject 메소드를 호출하면서 에러 메시지를 전달
                  reject(new Error(xhr.status)) // Failed...
              }
          };
      });
  };
  ```

  

## 프로미스의 후속 메소드

- Promise로 구현된 비동기 함수는 Promise 객체를 반환하여야 한다. 
  - Promise로 구현된 비동기 함수를 호출하는 측(promise consumer)에서는 Promise 객체의 후속 처리 메소드(`then`, `catch`, `finally`)를 통해 비동기 처리 결과 또는 에러 메시지를 전달받아 처리한다. 
  - Promise 객체는 상태를 갖는다고 하였다. 이 상태에 따라 후속 처리 메소드를 체이닝 방식으로 호출한다.



- Promise의 후속 처리 메소드

  - `then`
    - then 메소드는 두 개의 콜백 함수를 인자로 전달 받는다. 
    - 첫 번째 콜백 함수는 성공(프로미스에서 `fulfilled`,`resolve` 함수가 호출된 상태) 시 호출되고 두 번째 함수는 실패(프로미스에서 `rejected`, `reject` 함수가 호출된 상태) 시 호출된다.
    - `then` 메소드는 Promise 또는 값을 반환한다. 반환 값을 따로 설정하지 않을 경우에는 프로미스 객체를, 설정하면 설정한 값을 반환한다.
  - `catch`
    - 프로미스에서 `rejected`, `reject` 함수가 호출되었거나 `then` 메소드에서 에러가 발생하면 호출된다. 
    - `catch` 메소드는 Promise를 반환한다.
  - 예시1, 2번 처럼 따로 따로 써야 하는 것은 아니다. 
    - 예시 3번 처럼 쓰는 것이 가능하다.
    - `then`, `catch`는 자신이 반환 받은 프로미스 객체(예시의 경우 `promise3`)를 다시 반환한다(프로미스 체이닝).
    - 결국 아래 코드에서 `promise3.then(value=>{console.log("then",value)}).catch(error=>{console.log("catch",error)})`의 `catch`는 `promise3.catch(error=>{console.log("catch",error)})`와 같다.
  - `finally`
    - 성공, 실패 여부와 무관하게 무조건 실행

  ```javascript
  // 예시1
  const promise1 = new Promise((resolve,reject)=>{
      setTimeout(()=>{
          resolve('Hi!!')
      },1000)
  })
  
  // value에는 resolve에서 넘긴 값이 담긴다.
  promise1.then(value=>{
      console.log(value) // Hi!!
  })
  
  
  // 예시2
  const promise2 = new Promise((resolve,reject)=>{
      setTimeout(()=>{
          reject('Hi!!')
      },1000)
  })
  
  promise2
    // then은 reject를 받지 못한다.
    .then(value=>{
        console.log("then",value)	// (node:20360) UnhandledPromiseRejectionWarning: Hi!!
    })
  
  
  // 예시3
  const promise3 = new Promise((resolve,reject)=>{
      setTimeout(()=>{
          reject('Hi!!')
      },1000)
  })
  
  promise3
    .then(value=>{
        console.log("then",value)
    })
    .catch(error=>{
        console.log("catch",error)  // Hi!!
    })
  ```



## 프로미스 체이닝

- 콜백 헬 해결
  - 비동기 함수의 처리 결과를 가지고 다른 비동기 함수를 호출해야 하는 경우, 함수의 호출이 중첩(nesting)이 되어 복잡도가 높아지는 콜백 헬이 발생한다. 
  - 프로미스는 후속 처리 메소드를 체이닝(chainning)하여 여러 개의 프로미스를 연결하여 사용할 수 있다. 
  - 이로써 콜백 헬을 해결한다.



- Promise 객체를 반환한 비동기 함수는 프로미스 후속 처리 메소드인 `then`이나 `catch` 메소드를 사용할 수 있다. 

  - 따라서 `then` 메소드가 Promise 객체를 반환하도록 하면(`then` 메소드는 기본적으로 Promise를 반환) 여러 개의 프로미스를 연결하여 사용할 수 있다.

  ```javascript
  const getHen = () => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>resolve('Chicken'),1000)
  })
  
  const getEgg = hen => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>resolve(`${hen} => Egg`),1000)
  })
  
  const cook = egg => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>resolve(`${egg} => Meal`),1000)
  })
  
  // 아래와 같이 받아온 값을 다른 함수로 바로 넘길 때에는 축약이 가능하다.
  getHen()
    .then(hen => getEgg(hen))	// getEgg 프로미스 객체를 반환
    // .then(getEgg) 으로 축약 가능
    .then(egg => cook(egg))	// cook 프로미스 객체를 반환
    // .then(cook) 으로 축약 가능
    .then(meal => console.log(meal))
    // .then(console.log) 로 축약 가능
  ```

  - `then` 메소드는 프로미스 객체 외에도 값을 반환할 수 있다.

  ```javascript
  const fetchNumber = new Promise((resolve,reject)=>{
      setTimeout(() => resolve(1),1000)
  })
  
  fetchNumber
    .then(num => num*2)	// 값을 반환
    .then(num => num*3)	// 값을 반환
    .then(num => {		// 프로미스 객체를 반환
      return new Promise((resolve,reject)=>{
          setTimeout(()=>resolve(num+1),1000)
      })
  })
  .then(num => console.log(num))
  ```

  

## 프로미스의 에러 처리

- 비동기 처리 결과에 대한 후속 처리는 Promise 객체가 제공하는 후속 처리 메서드`then`, `catch`, `finally`를 사용하여 수행한다. 



- 비동기 처리 시에 발생한 에러는 `then` 메서드의 두 번째 콜백 함수로 처리할 수 있다.

  - 단, `then` 메서드의 두 번째 콜백 함수는 첫 번째 콜백 함수에서 발생한 에러를 캐치하지 못하고 코드가 복잡해져서 가독성이 좋지 않다.
  - 따라서 에러 처리는 `then` 메서드에서 하지 말고 `catch` 메서드를 사용하는 것을 권장한다.

  ```javascript
  // 예시(위에서 정의 한 `promiseAjax` 사용)
  
  // 부적절한 URL이 지정되었기 때문에 에러가 발생한다.
  const wrongUrl = 'https://jsonplaceholder.typicode.com/XXX/1'
  
  promiseAjax(wrongUrl)
    .then(res => console.log(res), err => console.error(err))
  
  
  // 두 번째 콜백 함수는 첫 번째 콜백 함수에서 발생한 에러를 캐치하지 못한다.
  promiseAjax('https://jsonplaceholder.typicode.com/todos/1')
    .then(res => console.xxx(res), err => console.error(err))
  ```

  

- Promise 객체의 후속 처리 메서드 `catch`를 사용해서 처리할 수도 있다.

  - `catch` 메서드를 호출하면 내부적으로 `then(undefined, onRejected)`을 호출한다.
  - `catch` 메서드를 모든 `then` 메서드를 호출한 이후에 호출하면, 비동기 처리에서 발생한 에러(reject 함수가 호출된 상태)뿐만 아니라 `then` 메서드 내부에서 발생한 에러까지 모두 캐치할 수 있다.

  ```javascript
  // 예시(위에서 정의 한 `promiseAjax` 사용)
  
  // 부적절한 URL이 지정되었기 때문에 에러가 발생한다.
  const wrongUrl = 'https://jsonplaceholder.typicode.com/XXX/1'
  
  promiseAjax(wrongUrl)
    .then(res => console.log(res))
    .catch(err => console.error(err)) // Error: 404
  
  
  //위 예시는 결국 아래와 같다.
  const wrongUrl = 'https://jsonplaceholder.typicode.com/XXX/1'
  
  promiseAjax(wrongUrl)
    .then(res => console.log(res))
    .then(undefined, err => console.error(err)) // Error: 404
  
  
  // then 메서드 내부에서 발생한 에러까지 모두 캐치할 수 있다.
  promiseAjax('https://jsonplaceholder.typicode.com/todos/1')
    .then(res => console.xxx(res))
    .catch(err => console.error(err)) // TypeError: console.xxx is not a function
  ```

  

- 특정 시점에 예외 처리

  - `catch`를 사용하여 에러가 발생했을 때 다른 값을 넘겨주는 것도 가능하다.

  ```javascript
  const getHen = () => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>resolve('Chicken'),1000)
  })
  
  const getEgg = hen => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>reject(new Error('error가 발생')),1000)
  })
  
  const cook = egg => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>resolve(`${egg} => Meal`),1000)
  })
  
  getHen()
    .then(getEgg)
    .then(cook)
    .then(console.log)
    .catch(console.log)	// Error: error가 발생
  
  
  // 만일 에러가 발생했을 때 다른 값을 넘겨주고 싶다면 다음과 같이 하면 된다.
  const getHen = () => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>resolve('Chicken'),1000)
  })
  
  const getEgg = hen => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>reject(new Error('error가 발생')),1000)
  })
  
  const cook = egg => new Promise((resolve,rejecjt)=>{
      setTimeout(()=>resolve(`${egg} => Meal`),1000)
  })
  
  getHen()
    .then(getEgg)
    .catch(error => {
      return 'Bread'
    })
    .then(cook)
    .then(console.log)	// Bread => Meal
  ```

  

## 프로미스의 정적 메소드

- `Promise.resolve` / `Promise.reject`

  - 존재하는 값을 Promise로 래핑하기 위해 사용한다.
  - 정적 메소드 `Promise.resolve` 는 인자로 전달된 값을 resolve하는 Promise를 생성한다.

  ```javascript
  // 위와 아래는 동일하게 동작한다.
  var resolvedPromise = Promise.resolve([1, 2, 3])
  resolvedPromise.then(console.log) // [ 1, 2, 3 ]
  
  var resolvedPromise = new Promise(resolve => resolve([1, 2, 3]))
  resolvedPromise.then(console.log) // [ 1, 2, 3 ]
  ```

  - `Promise.reject` 메소드는 인자로 전달된 값을 reject하는 프로미스를 생성한다.

  ```javascript
  // 위와 아래는 동일하게 동작한다.
  const rejectedPromise = Promise.reject(new Error('Error!'))
  rejectedPromise.catch(console.log) // Error: Error!
  
  const rejectedPromise = new Promise((resolve, reject) => reject(new Error('Error!')))
  rejectedPromise.catch(console.log) // Error: Error!
  ```



- `Promise.all`

  - `Promise.all` 메소드는 프로미스가 담겨 있는 배열 등의 이터러블을 인자로 전달 받는다. 
  - 그리고 전달받은 모든 프로미스를 병렬로 처리하고 그 처리 결과를 resolve하는 새로운 프로미스를 반환한다.
  - 예시
    - 첫번째 프로미스는 3초 후에 1을 resolve하여 처리 결과를 반환한다.
    - 두번째 프로미스는 2초 후에 2을 resolve하여 처리 결과를 반환한다.
    - 세번째 프로미스는 1초 후에 3을 resolve하여 처리 결과를 반환한다.

  ```javascript
  Promise.all([
    new Promise(resolve => setTimeout(() => resolve(1), 3000)),
    new Promise(resolve => setTimeout(() => resolve(2), 2000)),
    new Promise(resolve => setTimeout(() => resolve(3), 1000))
  ]).then(console.log) 	// [ 1, 2, 3 ]
    .catch(console.log)
  ```

  - `Promise.all` 메소드는 전달받은 모든 프로미스를 병렬로 처리한다.
    - 이때 모든 프로미스의 처리가 종료될 때까지 기다린 후 모든 처리 결과를 resolve 또는 reject한다.
    - 모든 프로미스의 처리가 성공하면 각각의 프로미스가 resolve한 처리 결과를 배열에 담아 resolve하는 새로운 프로미스를 반환한다. 
    - 이때 첫번째 프로미스가 가장 나중에 처리되어도 `Promise.all` 메소드가 반환하는 프로미스는 첫번째 프로미스가 resolve한 처리 결과부터 차례대로 배열에 담아 그 배열을 resolve하는 새로운 프로미스를 반환한다. 
    - 즉, **처리 순서가 보장된다.**
    - 프로미스의 처리가 하나라도 실패하면 가장 먼저 실패한 프로미스가 reject한 에러를 reject하는 새로운 프로미스를 즉시 반환한다.

  ```javascript
  Promise.all([
    new Promise((resolve, reject) => setTimeout(() => reject(new Error('Error 1!')), 3000)),
    new Promise((resolve, reject) => setTimeout(() => reject(new Error('Error 2!')), 2000)),
    new Promise((resolve, reject) => setTimeout(() => reject(new Error('Error 3!')), 1000))
  ]).then(console.log)
    .catch(console.log) // Error: Error 3!
  ```

  - `Promise.all` 메소드는 전달 받은 이터러블의 요소가 프로미스가 아닌 경우, `Promise.resolve` 메소드를 통해 프로미스로 래핑된다.

  ```javascript
  Promise.all([
    1, // => Promise.resolve(1)
    2, // => Promise.resolve(2)
    3  // => Promise.resolve(3)
  ]).then(console.log) // [1, 2, 3]
    .catch(console.log)
  ```



- `Promise.race`

  - 프로미스가 담겨 있는 배열 등의 이터러블을 인자로 전달 받는다. 
  - 모든 프로미스를 병렬 처리하는 것이 아니라 가장 먼저 처리된 프로미스가 resolve한 처리 결과를 resolve하는 새로운 프로미스를 반환한다.

  ```javascript
  Promise.race([
    new Promise(resolve => setTimeout(() => resolve(1), 3000)), // 1
    new Promise(resolve => setTimeout(() => resolve(2), 2000)), // 2
    new Promise(resolve => setTimeout(() => resolve(3), 1000))  // 3
  ]).then(console.log) // 3
    .catch(console.log)
  ```

  - 에러가 발생한 경우는 `Promise.all` 메소드와 동일하게 처리된다. 
    - 즉, `Promise.race` 메소드에 전달된 프로미스 처리가 하나라도 실패하면 가장 먼저 실패한 프로미스가 reject한 에러를 reject하는 새로운 프로미스를 즉시 반환한다.

  ```javascript
  Promise.race([
    new Promise((resolve, reject) => setTimeout(() => reject(new Error('Error 1!')), 3000)),
    new Promise((resolve, reject) => setTimeout(() => reject(new Error('Error 2!')), 2000)),
    new Promise((resolve, reject) => setTimeout(() => reject(new Error('Error 3!')), 1000))
  ]).then(console.log)
    .catch(console.log) // Error: Error 3!
  ```





# async&await

- async와 await
  - 프로미스를 보다 간편하게 사용할 수 있게 해준다.
  - 프로미스가 동기적으로 수행되는 것 처럼 보이게 해준다.
  - 기존 프로미스 사용 방식의 syntactic sugar다.
  - 모든 프로미스에 적용해야 하는 것은 아니고 적용하기 적합한 프로미스가 존재한다.



- async

  - 프로미스는 강력한 기능이지만 코드상으로 복잡해 보일 수 있다는 단점이 있다.
  - async를 사용하면 보다 간편하게 프로미스를 작성 가능하다.
  - 아래와 같이 `async` 키워드를 함수 앞에 붙여주면 된다.
    - 코드 블록이 자동으로 프로미스로 변경된다.

  ```javascript
  // 기존의 프로미스 사용
  function fetchUser(){
      return new Promise((resolve,reject)=>{
          resolve('Cha')
      })
  }
  
  const user = fetchUser()
  user.then(console.log)
  
  
  // 함수 앞에 async 키워드를 붙여준다.
  async function fetchUser(){
      return "Cha"
  }
  
  const user = fetchUser()
  user.then(console.log)
  ```



- 프로미스를 사용해도 콜백 헬이 발생할 수 있다.

  - async를 사용하면 보다 간편하게 코드를 작성 가능하다.

  ```javascript
  function getFruits(){
      return getApple()
      .then(apple => {
          return getBanana()
          .then(banana => `${apple} + ${banana}`)
      })
  }
  getFruits().then(console.log)
  
  
  // async를 활용하면 아래와 같이 작성 가능하다.
  async function getFruits(){
      const apple = await getApple()
      const banana = await getBanana()
      return `${apple} + ${banana}`
  }
  getFruits().then(console.log)
  ```

  

- await 사용하기

  - `await` 키워드는 `async` 키워드가 붙은 함수 내부에서만 사용이 가능하다.
  - `await` 키워드를 만나면 해당 작업이 완료될 때 까지 아래 작업이 진행되지 않는다. 즉, 동기적으로 동작하게 된다.

  ```javascript
  function delay(ms){
      // 정해진 시간이 지나면 resolve를 호출
      return new Promise(resolve => setTimeout(resolve,ms))
  }
  
  async function getApple(){
      // await 키워드가 붙은 작업이 끝날 때 까지 아래의 작업을 수행하지 않는다.
      await delay(3000)
      return 'Apple'
  }
  
  async function getBanana(){
      await delay(3000)
      return 'Banana'
  }
  
  // 만일 위 코드를 async와 await 없이 작성하면 아래와 같다.
  function getBanana(){
      return delay(3000)
      .then(()=>'Banana')
  } 
  ```

  

- 예외처리는 `try`, `catch`를 활용한다.

  ```javascript
  async function getApple(){
      await delay(3000)
      throw 'error'	// 에러를 발생시킨다.
      return 'Apple'
  }
  
  async function getBanana(){
      await delay(3000)
      return 'Banana'
  }
  
  async function getFruits(){
      let apple
      let banana
      try{
          apple = await getApple()
          banana = await getBanana()
      } catch{
          apple = 'error apple'
          banana = 'error banana'
      }
      return `${apple} + ${banana}`
  }
  
  getFruits().then(console.log)	// error apple + error banana
  ```



- 병렬 처리하기

  - `await`을 사용하면 병렬 처리가 불가능해진다.
  - 아래 코드에서 `getApple`이 실행되고 3초 후에 `getBanana`가 실행되는데 꼭 apple을 받아야 banana를 받을 수 있는 것은 아니므로 이는 비효율적이다.
  - 프로미스가 생성되는 순간 프로미스 내부의 코드 블록이 실행된다는 점을 이용하면 된다.

  ```javascript
  function delay(ms){
      return new Promise(resolve => setTimeout(resolve,ms))
  }
  
  async function getApple(){
      await delay(3000)
      return 'Apple'
  }
  
  async function getBanana(){
      await delay(3000)
      return 'Banana'
  }
  
  async function getFruits(){
      // applePromise, bananaPromise를 생성
      // 생성과 동시에 내부의 코드 블록이 실행된다.
      // 따라서 병렬적 처리가 가능해진다.
      const applePromise = getApple()
      const bananaPromise = getBanana()
      const apple = await applePromise
      const banana = await bananaPromise
      return `${apple} + ${banana}`
  }
  
  getFruits().then(console.log)
  ```

  - `Promise.all()`을 활용
    - 위에서 살펴본 방법 보다 훨씬 깔끔하기에 이 방법을 많이 쓴다.
    - `Promise.all()`에 프로미스 배열을 전달하면, 모든 프로미스들이 병렬적으로 수행되고, 모든 프로미스들이 완료될 때까지 기다린다.

  ```javascript
  function delay(ms){
      return new Promise(resolve => setTimeout(resolve,ms))
  }
  
  async function getApple(){
      await delay(3000)
      return 'Apple'
  }
  
  async function getBanana(){
      await delay(3000)
      return 'Banana'
  }
  
  function getFruits(){
  	return Promise.all([getApple(),getBanana()])
      .then(fruits => fruits.join(' + '))
  }
  
  getFruits().then(console.log)
  ```

  - `Promise.race()`
    - 병렬 처리를 할 때 가장 먼저 완료된 프로미스만을 받아 오기 위해 사용한다.

  ```javascript
  function delay(ms){
      return new Promise(resolve => setTimeout(resolve,ms))
  }
  
  async function getApple(){
      await delay(3000)		// 3초
      return 'Apple'
  }
  
  async function getBanana(){
      await delay(1000)		// 1초
      return 'Banana'
  }
  
  function getFastestFruit(){
  	return Promise.race([getApple(),getBanana()])
  }
  
  getFastestFruit().then(console.log)	// banana
  ```

  

# 예외처리

- 예외
  - 프로그램 실행 중 발생하는 런타임 오류
  - 예외가 발생하지 않도록 하는 것도 중요하지만, 발생한 예외를 처리하는 것도 중요하다.



- 예외 발생시키기

  - `throw` 키워드를 사용하면 예외를 발생시킬 수 있다.
  - 표현식에는 예외 코드를 나타내는 숫자나 오류 메시지를 담고 있는 문자열, Error 객체 등이 올 수있다.

  ```javascript
  throw 표현식
  ```

  

- 예외 처리하기

  - `try`: 기본적으로 맨 먼저 실행되는 블록이며, 여기서 발생한 예외는 `catch` 블록에서 처리될 수 있다.
  - `catch`: `try` 블록에서 발생한 예외 코드나 Error 객체를 인수로 전달받아 그 처리가 이루어지는 블록이다.
    - 옵션으로, 반드시 사용하지 않아도 된다.
  - `finally`: `try` 블록에서 예외가 발생하건 안 하건 맨 마지막에 무조건 실행되는 블록이다.
    - 옵션으로, 반드시 사용하지 않아도 된다.
    - `break`, `return `등이 `try` 혹은 `catch` 문에 있어도 실행 된다.

  ```javascript
  try {
      // 여기서 에러가 나면 에러가 난 시점에 코드의 흐름이 catch로 넘어간다.
      throw new Error("억지로 발생시킨 에러!!")
      console.log('에러 발생 이후의 코드는 실행되지 않는다.')
  } catch (e) {
      console.log(`에러가 발생했습니다: ${e.name}: ${e.message}`) // 에러가 발생했습니다: Error: 억지로 발생시킨 에러!!
  } finally {
      console.log("그래도 finally는 실행이 된다.")    // 그래도 finally는 실행이 된다.
  }
  ```



- 예외의 전파

  - 예외는 호출 스택(call stack)을 따라 전파된다.
    - 아래 예시에서 예외가 발생한 것은 `c` 함수지만 `a` 함수까지 전파되어 `catch`문에 걸리게 된다.

  ```javascript
  try {
      a()
     	console.log("이 줄은 실행이 안됩니다!")
  } catch(e) {
      console.log(e)              // 에러 발생!!
      console.log('에러 복구!!')  // 에러 복구!!
  }
    
  function a() {
      b()
  }
    
  function b() {
      c()
  }
    
  function c() {
      throw '에러 발생!!';
  }
  ```

  - 예외를 `try`, `catch`로 감싸면 전파되지 않는다.

  ```javascript
  try {
      a()
     	console.log("이 줄은 실행 됩니다!") // 이 줄은 실행 됩니다!
  } catch(e) {
      console.log('에러 발생 X!!!')
      console.log(e)
  }
    
  function a() {
      b()
  }
    
  function b() {
      c()
  }
    
  function c() {
      try{
          throw '에러 발생!!'
      } catch(e) {
          console.log(e)	// 에러 발생!!
      }
  }
  ```



- 비동기식 코드에서의 예외 처리

  - 비동기식으로 작동하는 콜백의 내부에서 발생한 에러는 콜백 바깥에 있는 `try` 블록으로 잡아낼 수 없다.
    - 상기했듯 JS에서는 예외를 전파한다.
    - `throw new Error('Error!')`를 실행시킨 것은 `setTimeout()` 함수가 아니라 "1초가 지났다."는 `time event`다.
    - `setTimeout()`으로 예외가 전파되지 않고 `time event`로 예외가 전파된다.
    - 결국 `setTimeout()`에서는 예외가 발생하지 않으므로 `catch`문에 걸리지도 않는다.

  ```javascript
  try {
      setTimeout(() => { throw new Error('Error!') }, 1000)	// 에러 자체는 발생하지만
  } catch (e) {
      console.log('에러를 캐치하지 못한다.')		// catch문에 잡히지는 않는다.
      console.log(e)
  }
  ```

  - 따라서 아래와 같이 비동기식 코드 내부에 작성해야 한다.

  ```javascript
  setTimeout(() => {
      try {
          throw new Error('Error 발생!')
      } catch (e) {
          console.log("이제 걸린다!")	// 이제 걸린다!
          console.log(e)
      }
  },1000)
  ```



# 클래스

- 클래스
  - 자바스크립트는 **프로토타입 기반(prototype-based)** 객체지향 언어다. 
    - 프로토타입 기반 프로그래밍은 클래스가 필요없는(class-free) 객체지향 프로그래밍 스타일로 프로토타입 체인과 클로저 등으로 객체 지향 언어의 상속, 캡슐화(정보 은닉) 등의 개념을 구현할 수 있다.
    - ES5에서는 생성자 함수와 프로토타입, 클로저를 사용하여 객체 지향 프로그래밍을 구현하였다.
    - 하지만 클래스 기반 언어에 익숙한 프로그래머들은 프로토타입 기반 프로그래밍 방식이 혼란스러울 수 있으며 자바스크립트를 어렵게 느끼게하는 하나의 장벽처럼 인식되었다.
  - ES6의 클래스
    - ES6의 클래스는 기존 프로토타입 기반 객체지향 프로그래밍보다 클래스 기반 언어에 익숙한 프로그래머가 보다 빠르게 학습할 수 있는 단순명료한 새로운 문법을 제시하고 있다. 
    - 그렇다고 ES6의 클래스가 기존의 프로토타입 기반 객체지향 모델을 폐지하고 새로운 객체지향 모델을 제공하는 것은 아니다. 
    - 사실 **클래스도 함수**이며 기존 프로토타입 기반 패턴의 문법적 설탕(Syntactic sugar)이라고 볼 수 있다. 
    - 다만, 클래스와 생성자 함수가 정확히 동일하게 동작하지는 않는다. 클래스가 보다 엄격하다. 
    - 따라서 클래스를 프로토타입 기반 패턴의 문법적 설탕이라고 인정하지 않는 견해도 일리가 있다.



- 클래스 정의

  - ES6 클래스는 `class` 키워드를 사용하여 정의한다.
  - 클래스 이름은 성성자 함수와 마찬가지로 파스칼 케이스를 사용하는 것이 일반적이다. 
    - 파스칼 케이스를 사용하지 않아도 에러가 발생하지는 않는다.

  ```javascript
  class Person {
      // 반드시 constructor라고 작성해야 한다.
      constructor(name){
          this._name = name
      }
      
      sayHi(){
          console.log(`Hi! ${this._name}!`)
      }
  }
  
  const cha = new Person('Cha')
  cha.sayHi()     // Hi! Cha!
  console.log(cha instanceof Person)  // true
  ```

  - 클래스는 선언문 이전에 참조할 수 없다.
    - 하지만 호이스팅이 발생하지 않는 것은 아니다. 
    - 클래스는 var 키워드로 선언한 변수처럼 호이스팅되지 않고 let, const 키워드로 선언한 변수처럼 호이스팅된다. 
    - 따라서 클래스 선언문 이전에 일시적 사각지대(Temporal Dead Zone; TDZ)에 빠지기 때문에 호이스팅이 발생하지 않는 것처럼 동작한다.

  ```javascript
  var Foo = ''
  
  {
    // 호이스팅이 발생하지 않는다면 ''가 출력되어야 한다.
    console.log(Foo)	// // ReferenceError: Cannot access 'Foo' before initialization
    class Foo {}
  }
  ```

  - 일반적이지는 않지만, 표현식으로도 클래스를 정의할 수 있다. 
    - 함수와 마찬가지로 클래스는 이름을 가질 수도 갖지 않을 수도 있다. 
    - 이때 클래스가 할당된 변수를 사용해 클래스를 생성하지 않고 기명 클래스의 클래스 이름을 사용해 클래스를 생성하면 에러가 발생한다. 
    - 이는 함수와 마찬가지로 클래스 표현식에서 사용한 클래스 이름은 외부 코드에서 접근 불가능하기 때문이다.

  ```javascript
  // 클래스명 MyClass는 함수 표현식과 동일하게 클래스 몸체 내부에서만 유효한 식별자이다.
  const Foo = class MyClass {}
  
  const foo = new Foo()
  console.log(foo)  // MyClass {}
  
  new MyClass() // ReferenceError: MyClass is not defined
  ```

  

- 인스턴스 생성

  - 마치 생성자 함수 같이, `new` 연산자와 함께 클래스 이름을 호출하면 클래스의 인스턴스가 생성된다.
    - 아래 코드에서 `new` 연산자와 함께 호출한 `Foo`는 클래스의 이름이 아니라 constructor(생성자)이다. 
    - 표현식이 아닌 선언식으로 정의한 클래스의 이름은 constructor와 동일하다.

  ```javascript
  class Foo {}
  
  const foo = new Foo()
  console.log(foo instanceof Foo)	// true
  ```

  - `new` 연산자를 사용하지 않고 constructor를 호출하면 타입 에러(TypeError)가 발생한다. 
    - constructor는 `new` 연산자 없이 호출할 수 없다.

  ```javascript
  class Foo {}
  
  const foo = Foo() // TypeError: Class constructor Foo cannot be invoked without 'new'
  ```

  

- constructor

  - 인스턴스를 생성하고 클래스 필드를 초기화하기 위한 특수한 메소드이다.
  - 클래스 필드
    - 클래스 내부의 캡슐화된 변수를 말한다. 
    - 데이터 멤버 또는 멤버 변수라고도 부른다. 
    - 클래스 필드는 인스턴스의 프로퍼티 또는 정적 프로퍼티가 될 수 있다. 
    - 쉽게 말해, 자바스크립트의 생성자 함수에서 `this`에 추가한 프로퍼티를 클래스 기반 객체지향 언어에서는 클래스 필드라고 부른다.

  ```javascript
  // 클래스 선언문
  class Person {
    // constructor(생성자). 이름을 바꿀 수 없다.
    constructor(name) {
      // this는 클래스가 생성할 인스턴스를 가리킨다.
      // _name은 클래스 필드이다.
      this._name = name
    }
  }
  ```

  - constructor는 클래스 내에 한 개만 존재할 수 있다. 
    - 만약 클래스가 2개 이상의 constructor를 포함하면 문법 에러(SyntaxError)가 발생한다. 
    - 인스턴스를 생성할 때 `new` 연산자와 함께 호출한 것이 바로 constructor이며 constructor의 파라미터에 전달한 값은 클래스 필드에 할당한다.
  - constructor는 생략할 수 있다. 
    - constructor를 생략하면 클래스에 `constructor() {}`를 포함한 것과 동일하게 동작한다. 
    - 즉, 빈 객체를 생성한다. 
    - 따라서 인스턴스에 프로퍼티를 추가하려면 인스턴스를 생성한 이후, 프로퍼티를 동적으로 추가해야 한다.

  ```javascript
  class Foo { }
  
  const foo = new Foo()
  console.log(foo) // Foo {}
  
  // 프로퍼티 동적 할당 및 초기화
  foo.num = 1
  console.log(foo) // Foo&nbsp;{ num: 1 }
  ```

  - constructor는 인스턴스의 생성과 동시에 클래스 필드의 생성과 초기화를 실행한다. 
    - 따라서 클래스 필드를 초기화해야 한다면 constructor를 생략해서는 안된다.

  

- 클래스 필드

  - 클래스 몸체(class body)에는 메소드만 선언할 수 있다. 
  - 클래스 바디에 클래스 필드(멤버 변수)를 선언하면 문법 에러(SyntaxError)가 발생한다.

  ```javascript
  class Foo {
    name = '' // SyntaxError
  
    constructor() {}
  }
  ```

  - 클래스 필드의 선언과 초기화는 반드시 constructor 내부에서 실시한다.

  ```javascript
  class Foo {
    constructor(name = '') {
      this.name = name // 클래스 필드의 선언과 초기화
    }
  }
  const foo = new Foo('Cha')
  console.log(foo) // Foo { name: 'Cha' }
  ```

  - constructor 내부에서 선언한 클래스 필드는 클래스가 생성할 인스턴스를 가리키는 this에 바인딩한다.
    - 이로써 클래스 필드는 클래스가 생성할 인스턴스의 프로퍼티가 되며, 클래스의 인스턴스를 통해 클래스 외부에서 언제나 참조할 수 있다. 
    - 즉, 언제나 `public`이다.
    - ES6의 클래스는 다른 객체지향 언어처럼 private, public, protected 키워드와 같은 접근 제한자(access modifier)를 지원하지 않는다.
    - 현재 접근 제한자 지원과 관련된 논의가 진행 중이다.

  ```javascript
  class Foo {
      constructor(name = '') {
          this.name = name // public 클래스 필드
      }
  }
  
  const foo = new Foo('Cha')
  // 클래스 외부에서 참조할 수 있다.
  console.log(foo.name) // Cha
  ```

  

- getter, setter

  - getter와 setter는 클래스에서 새롭게 도입된 기능이 아니다. getter와 setter는 접근자 프로퍼티(accessor property)이다.
  - getter
    - 클래스 필드에 접근할 때마다 클래스 필드의 값을 조작하는 행위가 필요할 때 사용한다.
    - 메소드 이름 앞에 `get` 키워드를 사용해 정의한다.
    - 이때 메소드 이름은 클래스 필드 이름처럼 사용된다. 
    - 다시 말해 getter는 호출하는 것이 아니라 프로퍼티처럼 참조하는 형식으로 사용하며 참조 시에 메소드가 호출된다. 

  ```javascript
  class Foo {
      constructor(arr = []) {
          this._arr = arr
      }
  
      // getter: get 키워드 뒤에 오는 메소드 이름 firstElem은 클래스 필드 이름처럼 사용된다.
      get firstElem() {
          // getter는 반드시 무언가를 반환해야 한다.
          return this._arr.length ? this._arr[0] : null
      }
  }
  
  const foo = new Foo([1, 2])
  // 필드 firstElem에 접근하면 getter가 호출된다.
  console.log(foo.firstElem) // 1
  ```

  - setter
    - setter는 클래스 필드에 값을 할당할 때마다 클래스 필드의 값을 조작하는 행위가 필요할 때 사용한다.
    - 메소드 이름 앞에 `set` 키워드를 사용해 정의한다. 
    - 이때 메소드 이름은 클래스 필드 이름처럼 사용된다. 
    - 다시 말해 setter는 호출하는 것이 아니라 프로퍼티처럼 값을 할당하는 형식으로 사용하며 할당 시에 메소드가 호출된다.

  ```javascript
  class Foo {
      constructor(arr = []) {
          this._arr = arr
      }
  
      // getter: get 키워드 뒤에 오는 메소드 이름 firstElem은 클래스 필드 이름처럼 사용된다.
      get firstElem() {
          // getter는 반드시 무언가를 반환하여야 한다.
          return this._arr.length ? this._arr[0] : null
      }
  
      // setter: set 키워드 뒤에 오는 메소드 이름 firstElem은 클래스 필드 이름처럼 사용된다.
      set firstElem(elem) {
          // ...this._arr은 this._arr를 개별 요소로 분리한다
          this._arr = [elem, ...this._arr]
      }
  }
  
  const foo = new Foo([1, 2])
  
  // 클래스 필드 lastElem에 값을 할당하면 setter가 호출된다.
  foo.firstElem = 100
  
  console.log(foo.firstElem) // 100
  ```

  

- 정적 메소드

  - 클래스의 정적(static) 메소드를 정의할 때 `static` 키워드를 사용한다. 
    - 정적 메소드는 클래스의 인스턴스가 아닌 클래스 이름으로 호출한다.
    - 따라서 클래스의 인스턴스를 생성하지 않아도 호출할 수 있다.

  ```javascript
  class Foo {
      constructor(prop) {
          this.prop = prop
      }
  
      static staticMethod() {
  
          // 정적 메소드는 this를 사용할 수 없다.
          // 정적 메소드 내부에서 this는 클래스의 인스턴스가 아닌 클래스 자신을 가리킨다.
          return 'staticMethod';
      }
  
      prototypeMethod() {
          return this.prop;
      }
  }
  
  // 정적 메소드는 클래스 이름으로 호출한다.
  console.log(Foo.staticMethod())	// staticMethod
  
  const foo = new Foo(1)
  // 정적 메소드는 인스턴스로 호출할 수 없다.
  console.log(foo.staticMethod()) // Uncaught TypeError: foo.staticMethod is not a function
  ```

  - 클래스의 정적 메소드 용도
    - 클래스의 정적 메소드는 인스턴스로 호출할 수 없다.
    - 이것은 정적 메소드는 this를 사용할 수 없다는 것을 의미한다. 
    - 일반 메소드에서 this는 클래스의 인스턴스를 가리키며, 메소드 내부에서 this를 사용한다는 것은 클래스의 인스턴스의 생성을 전제로 하는 것이다.
    - 메소드 내부에서 this를 사용할 필요가 없는 메소드는 정적 메소드로 만들 수 있다.
    - 애플리케이션 전역에서 사용할 유틸리티(utility) 함수를 생성할 때 주로 사용한다.
  - 정적 메소드를 인스턴스로 호출할 수 없는 이유

    - 사실 클래스도 함수이고 기존 prototype 기반 패턴의 Syntactic sugar일 뿐이다.
    - 함수 객체는 prototype 프로퍼티를 갖는데, 일반 객체는 prototype 프로퍼티를 가지지 않는다.
    - 함수 객체만이 가지고 있는 prototype 프로퍼티는 함수 객체가 생성자로 사용될 때, 이 함수를 통해 생성된 객체의 부모 역할을 하는 프로토타입 객체를 가리킨다. 
    - 그리고 생성자 함수의 prototype 프로퍼티가 가리키는 프로토타입 객체가 가지고 있는 constructor 프로퍼티는 생성자 함수를 가리킨다.
    - 정적 메소드는 생성자 함수의 메소드(함수는 객체이므로 메소드를 가질 수 있다.)이고, 일반 메소드는 프로토타입 객체의 메소드이다. 
    - 인스턴스는 프로토타입 객체와 프로토타입 체인이 연결되어 있지만, 생성자 함수와는 연결되어 있지 않다.
    - 따라서 정적 메소드는 인스턴스에서 호출할 수 없다.

  ```javascript
  var Foo = (function () {
      // 생성자 함수
      function Foo(prop) {
          this.prop = prop
      }
  	
      // 정적 메소드
      Foo.staticMethod = function () {
          return 'staticMethod'
      }
  	
      // 일반 메소드
      Foo.prototype.prototypeMethod = function () {
          return this.prop
      }
  
      return Foo
  }())
  
  var foo = new Foo(1)
  console.log(foo.prototypeMethod()) 	// 123
  console.log(Foo.staticMethod()) 	// staticMethod
  console.log(foo.staticMethod()) 	// Uncaught TypeError: foo.staticMethod is not a function
  ```

  

  

- 클래스 상속

  - `extends` 키워드
    - 부모 클래스(base class)를 상속받는 자식 클래스(sub class)를 정의할 때 사용한다. 
  - `super` 키워드
    - 부모 클래스를 참조 하거나, 부모 클래스의 constructor를 호출할 때 사용한다.
    - `super`가 메소드로 사용될 때, 그리고 객체로 사용될 때 다르게 동작한다.
    - `super` 메소드는 자식 class의 constructor 내부에서 부모 클래스의 constructor(super-constructor)를 호출한다. 
    - 즉, 부모 클래스의 인스턴스를 생성한다. 
    - 자식 클래스의 constructor에서 `super()`를 호출하지 않으면 `this`에 대한 참조 에러(ReferenceError)가 발생한다.
    - 즉, `super` 메소드를 호출하기 이전에는 `this`를 참조할 수 없음을 의미한다.
    - `super` 키워드는 부모 클래스(Base Class)에 대한 참조다. 부모 클래스의 필드 또는 메소드를 참조하기 위해 사용한다.
  - 오버라이딩과 오버로딩
    - 오버라이딩: 상위 클래스가 가지고 있는 메소드를 하위 클래스가 재정의하여 사용하는 방식.
    - 오버로딩: 매개변수의 타입 또는 갯수가 다른, 같은 이름의 메소드를 구현하고 매개변수에 의해 메소드를 구별하여 호출하는 방식. 
    - 자바스크립트는 오버로딩을 지원하지 않지만 arguments 객체를 사용하여 구현할 수는 있다.

  ```javascript
  // 부모 클래스
  class Circle {
      
      constructor(radius) {
          this.radius = radius // 반지름
      }
  
      // 원의 지름
      getDiameter() {
          return 2 * this.radius
      }
  
      // 원의 둘레
      getPerimeter() {
          return 2 * Math.PI * this.radius
      }
  
      // 원의 넓이
      getArea() {
          return Math.PI * Math.pow(this.radius, 2)
      }
  }
  
  // 자식 클래스
  class Cylinder extends Circle {
      
      constructor(radius, height) {
          // super 메소드는 부모 클래스의 constructor를 호출하면서 인수를 전달한다.
          super(radius)
          this.height = height
      }
  
      // 원통의 넓이: 부모 클래스의 getArea 메소드를 오버라이딩하였다.
      getArea() {
          // (원통의 높이 * 원의 둘레) + (2 * 원의 넓이)
          // super 키워드는 부모 클래스(Base Class)에 대한 참조에 사용된다.
          return (this.height * super.getPerimeter()) + (2 * super.getArea())
      }
  
      // 원통의 부피
      getVolume() {
          // super 키워드는 부모 클래스(Base Class)에 대한 참조에 사용된다.
          return super.getArea() * this.height
      }
  }
  
  // 반지름이 2, 높이가 10인 원통
  const cylinder = new Cylinder(2, 10)
  
  // 원의 지름
  console.log(cylinder.getDiameter())  // 4
  // 원의 둘레
  console.log(cylinder.getPerimeter()) // 12.566370614359172
  // 원통의 넓이
  console.log(cylinder.getArea())      // 150.79644737231007
  // 원통의 부피
  console.log(cylinder.getVolume())    // 125.66370614359172
  
  // cylinder는 Cylinder 클래스의 인스턴스이다.
  console.log(cylinder instanceof Cylinder) // true
  // cylinder는 Circle 클래스의 인스턴스이다.
  console.log(cylinder instanceof Circle)   // true
  
  
  console.log(cylinder.__proto__ === Cylinder.prototype) // true
  console.log(Cylinder.prototype.__proto__ === Circle.prototype) // true
  console.log(Circle.prototype.__proto__ === Object.prototype) // true
  ```

  - ` static` 메소드와 `prototype` 메소드의 상속
    - 프로토타입 체인에 의해 부모 클래스의 정적 메소드도 상속이 된다.
    - 자식 클래스의 정적 메소드 내부에서도 `super` 키워드를 사용하여 부모 클래스의 정적 메소드를 호출할 수 있다.
    - 하지만 자식 클래스의 일반 메소드(프로토타입 메소드) 내부에서는 `super` 키워드를 사용하여 부모 클래스의 정적 메소드를 호출할 수 없다.

  ```javascript
  class Parent {
      static staticMethod() {
          return 'Hello'
      }
  }
  
  class Child extends Parent {
      static staticMethod() {
          return `${super.staticMethod()} wolrd`;
      }
  
      prototypeMethod() {
          return `${super.staticMethod()} wolrd`
      }
  }
  
  console.log(Parent.staticMethod()) 			// 'Hello'
  console.log(Child.staticMethod())  			// 'Hello wolrd'
  console.log(new Child().prototypeMethod())	// TypeError: (intermediate value).staticMethod is not a function
  ```

  



# 모듈

- 모듈
  - 애플리케이션을 구성하는 개별적 요소로서 재사용 가능한 코드 조각을 말한다. 
  - 모듈은 세부 사항을 캡슐화하고 공개가 필요한 API만을 외부에 노출한다.
  - 일반적으로 모듈은 파일 단위로 분리되어 있으며 애플리케이션은 필요에 따라 명시적으로 모듈을 로드하여 재사용한다. 
    - 즉, 모듈은 애플리케이션에 분리되어 개별적으로 존재하다가 애플리케이션의 로드에 의해 비로소 애플리케이션의 일원이 된다. 
  - 모듈은 기능별로 분리되어 작성되므로 코드의 단위를 명확히 분리하여 애플리케이션을 구성할 수 있으며 재사용성이 좋아서 개발 효율성과 유지보수성을 높일 수 있다.



- JS의 모듈

  - JS에는 본래 모듈 기능이 없었다.
    - 클라이언트 사이드 자바스크립트는 script 태그를 사용하여 외부의 스크립트 파일을 가져올 수는 있지만, 파일마다 독립적인 파일 스코프를 갖지 않고 하나의 전역 객체(Global Object)를 공유한다. 
    - 즉, 자바스크립트 파일을 여러 개의 파일로 분리하여 script 태그로 로드하여도 분리된 자바스크립트 파일들이 결국 하나의 자바스크립트 파일 내에 있는 것처럼 하나의 전역 객체를 공유한다. 
    - 따라서 분리된 자바스크립트 파일들이 하나의 전역을 갖게 되어 전역 변수가 중복되는 등의 문제가 발생할 수 있다. 
    - 이것으로는 모듈화를 구현할 수 없다.
    - JS를 클라이언트 사이드에 국한하지 않고 범용적으로 사용하고자 하는 움직임이 생기면서 모듈 기능은 반드시 해결해야 하는 핵심 과제가 되었다.
    - 이런 상황에서 제안된 것이 **CommonJS**와 **AMD(Asynchronous Module Definition)**이다.
    - 결국, 자바스크립트의 모듈화는 크게 CommonJS와 AMD 진영으로 나뉘게 되었고 브라우저에서 모듈을 사용하기 위해서는 CommonJS 또는 AMD를 구현한 모듈 로더 라이브러리를 사용해야 하는 상황이 되었다.
    - 서버 사이드 자바스크립트 런타임 환경인 Node.js는 모듈 시스템의 사실상 표준(de facto standard)인 CommonJS를 채택하였고 독자적인 진화를 거쳐 현재는 CommonJS 사양과 100% 동일하지는 않지만 기본적으로 CommonJS 방식을 따르고 있다. 
    - 즉, Node.js에서는 표준은 아니지만 모듈이 지원된다. 따라서 Node.js 환경에서는 모듈 별로 독립적인 스코프, 즉 모듈 스코프를 갖는다.
  - ES6에서는 클라이언트 사이드 자바스크립트에서도 동작하는 모듈 기능을 추가하였다.
    - script 태그에 `type="module"` 어트리뷰트를 추가하면 로드된 자바스크립트 파일은 모듈로서 동작한다. 
    - ES6 모듈의 파일 확장자는 모듈임을 명확히 하기 위해 mjs를 사용하도록 권장한다.

  ```html
  <script type="module" src="lib.mjs"></script>
  <script type="module" src="app.mjs"></script>
  ```

  - 단, 아래와 같은 이유로 아직까지는 브라우저가 지원하는 ES6 모듈 기능보다는 Webpack 등의 모듈 번들러를 사용하는 것이 일반적이다.
    - IE를 포함한 구형 브라우저는 ES6 모듈을 지원하지 않는다.
    - 브라우저의 ES6 모듈 기능을 사용하더라도 트랜스파일링이나 번들링이 필요하다.
    - 아직 지원하지 않는 기능(Bare import 등)이 있다.
    - 점차 해결되고는 있지만 아직 몇가지 이슈가 있다.



- 모듈 스코프

  - ES6 모듈 기능을 사용하지 않으면 분리된 자바스크립트 파일에 독자적인 스코프를 갖지 않고 하나의 전역을 공유한다.
    - 아래 예시의 HTML에서 2개의 자바스크립트 파일을 로드하면 로드된 자바스크립트는 하나의 전역을 공유한다.
    - 로드된 2개의 자바스크립트 파일은 하나의 전역 객체를 공유하며 하나의 전역 스코프를 갖는다. 
    - 따라서 foo.js에서 선언한 변수 x와 bar.js에서 선언한 변수 x는 중복 선언되며 의도치 않게 변수 `x`의 값이 덮어 써진다.

  ```javascript
  // foo.js
  
  var x = 'foo'
  
  // 변수 x는 전역 변수이다.
  console.log(window.x) // foo
  ```

  ```javascript
  // bar.js
  // foo.js에서 선언한 전역 변수 x와 중복된 선언이다.
  var x = 'bar'
  
  // 변수 x는 전역 변수이다.
  // foo.js에서 선언한 전역 변수 x의 값이 재할당되었다.
  console.log(window.x) // bar
  ```

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <script src="foo.js"></script>
    <script src="bar.js"></script>
  </body>
  </html>
  ```

  - ES6 모듈은 파일 자체의 스코프를 제공한다. 
    - 즉, ES6 모듈은 독자적인 **모듈 스코프**를 갖는다. 
    - 따라서, 모듈 내에서 `var` 키워드로 선언한 변수는 더 이상 전역 변수가 아니며 `window` 객체의 프로퍼티도 아니다.
    - 모듈 내에서 선언한 변수는 모듈 외부에서 참조할 수 없다. 스코프가 다르기 때문이다.

  ```javascript
  // foo.mjs
  var x = 'foo'
  
  console.log(x) // foo
  // 변수 x는 전역 변수가 아니며 window 객체의 프로퍼티도 아니다.
  console.log(window.x) // undefined
  ```

  ```javascript
  // bar.mjs
  // 변수 x는 foo.mjs에서 선언한 변수 x와 스코프가 다른 변수이다.
  var x = 'bar'
  
  console.log(x) // bar
  // 변수 x는 전역 변수가 아니며 window 객체의 프로퍼티도 아니다.
  console.log(window.x) // undefined
  ```

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <script type="module" src="foo.mjs"></script>
    <script type="module" src="bar.mjs"></script>
  </body>
  </html>
  ```



- `export` 키워드

  - 모듈은 독자적인 모듈 스코프를 갖기 때문에 모듈 안에 선언한 모든 식별자는 기본적으로 해당 모듈 내부에서만 참조할 수 있다. 
  - 만약 모듈 안에 선언한 식별자를 외부에 공개하여 다른 모듈들이 참조할 수 있게 하고 싶다면 `export` 키워드를 사용한다. 
  - 선언된 변수, 함수, 클래스 모두 export할 수 있다.
  - 모듈을 공개하려면 선언문 앞에 `export` 키워드를 사용한다. 여러 개를 export할 수 있는데 이때 각각의 export는 이름으로 구별할 수 있다.

  ```javascript
  // lib.mjs
  // 변수의 공개
  export const a = 'Hello!'
  
  // 함수의 공개
  export function foo() {
    console.log("Hello!")
  }
  
  // 클래스의 공개
  export class Person {
    constructor(name) {
      this.name = name;
    }
  }
  ```

  - 선언문 앞에 매번 `export` 키워드를 붙이는 것이 싫다면 export 대상을 모아 하나의 객체로 구성하여 한번에 export할 수도 있다.

  ```javascript
  // lib.mjs
  const a = 'Hello!'
  
  function foo() {
    console.log("Hello!")
  }
  
  class Person {
    constructor(name) {
      this.name = name
    }
  }
  
  // 변수, 함수 클래스를 하나의 객체로 구성하여 공개
  export { a, foo, Person }
  ```



- `import` 키워드

  - 모듈에서 공개(export)한 대상을 로드하려면 `import` 키워드를 사용한다.
  - 모듈이 export한 식별자로 import하며 ES6 모듈의 파일 확장자를 생략할 수 없다.

  ```javascript
  // app.mjs
  // 같은 폴더 내의 lib.mjs 모듈을 로드.
  // lib.mjs 모듈이 export한 식별자로 import한다.
  // ES6 모듈의 파일 확장자를 생략할 수 없다.
  import { a, foo, Person } from './lib.mjs';
  
  console.log(a)  // Hello!
  foo()	 		// Hello!
  console.log(new Person('Cha')) // Person { name: 'Cha' }
  ```

  - 모듈이 export한 식별자를 각각 지정하지 않고 하나의 이름으로 한꺼번에 import할 수도 있다. 
    - 이때 import되는 식별자는 as 뒤에 지정한 이름의 객체에 프로퍼티로 할당된다.

  ```javascript
  // app.mjs
  import * as lib from './lib.mjs'
  
  console.log(lib.a)  // Hello!
  lib.foo()	 		// Hello!
  lib.console.log(new lib.Person('Cha')) // Person { name: 'Cha' }
  ```

  - 이름을 변경하여 import할 수도 있다.

  ```javascript
  import { a as ab, foo as f, Person as P } from './lib.mjs';
  
  console.log(ab)  // Hello!
  f()				 // Hello!
  console.log(new P('Cha')) // Person { name: 'Cha' }
  ```

  - 모듈에서 하나만을 export할 때는 `default` 키워드를 사용할 수 있다.
    - 다만, `default`를 사용하는 경우, `var`, `let`, `const`는 사용할 수 없다.

  ```javascript
  // lib.mjs
  export default function () {
    console.log("Hello!")
  }
  
  // var, let, const 사용 불가
  export default () => {}			// O
  
  export default const foo = () => {} // => SyntaxError: Unexpected token 'const'
  ```

  - `default` 키워드와 함께 export한 모듈은 `{}` 없이 임의의 이름으로 import한다.

  ```javascript
  // app.mjs
  import someFunction from './lib.mjs';
  
  someFunction // Hello!
  ```

