

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
