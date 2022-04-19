# IndexedDB 개요

> https://developer.mozilla.org/ko/docs/Web/API/IndexedDB_API

- 정의: Indexed Database API, WebSimpleDB 등의 이름으로도 불리는데, 색인(index)이 포함된 JSON 객체가 모여있는 트랜잭셔널 로컬 데이터베이스를 위해 W3C 가 권고한 웹 브라우저 표준 인터페이스의 하나 
- 특징
  - 웹 스토리지 보다도 큰 저장 공간을 제공한다.
  - 많은 양의 구조화된 데이터를 저장하기에 적합하다.
  - SQL을 사용하는 관계형 데이터베이스(RDBMS)와 같이 트랜잭션을 사용하는 데이터베이스 시스템이다.
  - 그러나 IndexedDB는 RDBMS의 고정컬럼 테이블 대신 JavaScript 기반의 객체지향 데이터베이스이다.
  - key-value의 쌍으로 존재한다. key로 색인 된 객체를 저장하고 검색이 가능하다.
  - 모두 문자열로 저장하는 스토리지와 다르게 IndexedDB 는 javascript에서 사용하는 모든 타입의 데이터를 저장 가능하다.
  - 비동기적으로 동작한다.
  - 트랜잭션 데이터베이스 모델을 기반으로 만들어 졌다.





# 사용해보기

> https://developer.mozilla.org/ko/docs/Web/API/IndexedDB_API/Using_IndexedDB#Indexed_DB_%EC%9D%98_%EC%8B%A4%ED%97%98%EC%A0%81%EC%9D%B8_%EB%B2%84%EC%A0%84%EC%9D%84_%EC%82%AC%EC%9A%A9%ED%95%B4%EB%B3%B4%EA%B8%B0 
>
> https://romeoh.tistory.com/entry/indexed-db 

## IndexedDB를 사용 가능한지 체크하기

- 아래 코드를 통해 IndexedDB를 사용 가능한지 알아볼 수 있다.

  ```javascript
  if (!window.indexedDB) {
      window.alert("Your browser doesn't support a stable version of IndexedDB. Such and such feature will not be available.")
  } else {
      console.log("Your browser support a stable version of IndexedDB")
  }
  ```





## 데이터베이스 생성하기

- 아래 코드를 통해 DB를 생성한다.

  - `open()`: DB를 생성하는 함수
    - 첫 번째 인자로 데이터베이스의 이름을 받는다(직접 지정해주면 된다).
    - 두 번째 인자로 데이터베이스의 버전을 받는다. 버전 번호의 타입은 unsigned long long으로 매우 큰 정수도 입력 가능하며 부동소수점은 사용할 수 없다.
    - open() 함수의 결과는 IDBDatabase 객체의 인스턴스이다.
  - 결과에 따라 제어할 함수를 만든다.

  ```javascript
  var db;
  var request = window.indexedDB.open("MyTestDatabase")
  
  //open() 함수가 성공할 경우 실행되는 함수, success 이벤트가 request를 target으로 발생한다.
  request.onerror = function(event){
      alert("Database error: " + event.target.errorCode);
  }
  //open() 함수에 문제가 있을 경우 발생하는 함수, request에서 발생
  request.onsuccess = function(event){
      db = request.result
      console.log(db)
  }
  ```



- 새로운 DB가 생성되거나 기존 데이터베이스의 버전을 높일 때 실행될 함수를 만든다.

  - `.onupgradeneeded`: 새로운 DB가 생성되거나 기존 데이터베이스의 버전이 높아질 때 트리거 된다.
    - `request.result`(즉, 아래의 예제의 db)에 설정된 onversionchange 이벤트 핸들러에 IDBVersionChangeEvent 객체가 전달된다.
    - 데이터 베이스의 버전이 높아질 경우 높아진 버전의 데이터 베이스에 필요한 객체 저장소를 만들어야 한다.
    - 이 경우(데이터 베이스의 버전을 높일 경우) 이전 버전의 데이터베이스에 있는 객체 저장소가 이미 있으므로, 이전 버전의 객체 저장소를 다시 만들 필요가 없다.
    - 새로운 객체 저장소를 만들거나 더 이상 필요하지 않은 이전 버전의 객체 저장소만 삭제하면 된다.
    - 기존 객체 저장소를 변경(예, keyPath를 변경) 해아 하는 경우, 이전 객체 저장소를 삭제하고 새 옵션으로 다시 만들어야 한다.
    - 이것은 객체 저장소의 정보를 삭제하므로 주의해야 한다.
    - 이미 존재하는 이름으로 객체 저장소를 만들려고 하면 (또는 존재하지 않는 객체 저장소를 삭제하려고 하면) 오류가 발생 한다.
  - `createObjectStore()` 함수는 객체 저장소를 생성한다.
    - 첫 번째 인자로 저장소 이름(직접 지정해주면 된다)을 받는다.
    - 두 번째 인자로 `unique`, `keyPath`, `autoIncrement`등의 속성이 포함된 객체를 받는다.
    - 하나의 데이터 베이스 안에는 여러 개의 객체 저장소가 존재할 수 있다(테이블 같은 것이라고 생각하면 된다).

  ```javascript
  request.onupgradeneeded = function(event){
      //IDBDatabase interface를 저장
      var db = event.target.result;
  
      //데이터 베이스를 위한 objectStore(객체 저장소)를 생성
      var objectStore = db.createObjectStore("name", { keyPath: "myKey" });
  }
  ```





## 데이터 추가, 조회, 수정, 삭제하기

- 객체 저장소에 접근하기

  - `transaction()` 함수를 사용하여 트랜잭션을 확장한다.
    - 첫 번째 인자는 확장될 객체 저장소의 목록으로 모든 객체 저장소의 트랜잭션을 확장하고자 한다면 빈 배열을 넘기면 된다.
    - 두 번째 인자는 readonly, readwrite, versionchange 중 하나를 넘기면 된다(아무것도 넘기지 않을 경우 readonly가 기본값으로 설정된다). 
  - 트랜젝션에서 `objectStore()` 함수를 통해 원하는 객체 저장소에 접근하면 된다.
    - 인자로 접근하려는 객체저장소의 이름을 넘긴다.

  ```javascript
  //indexedDB에 저장할 고객 데이터의 예시, 실제로 아래 list를 넣는 것이 아니다. 예시일 뿐이다.
  const customerData = [
      { ssn: "444-44-4444", name: "Bill", age: 35, email: "bill@company.com" },
      { ssn: "555-55-5555", name: "Donna", age: 32, email: "donna@home.org" }
  ];
  
  var db;
  
  var request = window.indexedDB.open("MyTestDatabase",2)
  
  
  request.onerror = function(event){
      alert("Database error: " + event.target.errorCode);
  }
  
  request.onsuccess = function(event){
      db = request.result
      console.log(db)
  }
  
  request.onupgradeneeded = function(event){
      var db = event.target.result;
  
      //ssn은 유일한 값임이 보장되므로 keyPath로 사용한다.
      var objectStore = db.createObjectStore("customers", { keyPath: "ssn" });
      console.log(objectStore)
  
      //고객을 이름으로 찾기 위해 인덱스를 생성한다. 이름은 겹칠 수 있으므로 unique 인덱스를 사용하지 않는다.
      objectStore.createIndex("name", "name", { unique: false });
  
      //고객을 이메일로 찾기 위한 인덱스를 생성한다. 이메일은 겹칠 수 없으므로 unique 인덱스를 사용한다.
      objectStore.createIndex("email", "email", { unique: true });
  
      //데이터가 객체 저장소에 들어가기 전에 객체 저장소가 미리 생성되어 있도록 하기 위해 transaction.oncomplete를 사용한다.
      objectStore.transaction.oncomplete = function(event){
  
          // 사용할 객체 저장소에 접근하기
          var customerObjectStore = db.transaction(["customers"],"readwrite").objectStore("customers")
  
      }
  }
  ```




- 데이터 추가

  - `add()`함수를 사용

  ```javascript
  //indexedDB에 저장할 고객 데이터의 예시, 실제로 아래 list를 넣는 것이 아니다. 예시일 뿐이다.
  const customerData = [
      { ssn: "444-44-4444", name: "Bill", age: 35, email: "bill@company.com" },
      { ssn: "555-55-5555", name: "Donna", age: 32, email: "donna@home.org" }
  ];
  
  var db;
  
  var request = window.indexedDB.open("MyTestDatabase",2)
  
  
  request.onerror = function(event){
      alert("Database error: " + event.target.errorCode);
  }
  
  request.onsuccess = function(event){
      db = request.result
      console.log(db)
  }
  
  request.onupgradeneeded = function(event){
      var db = event.target.result;
  
      var objectStore = db.createObjectStore("customers", { keyPath: "ssn" });
      console.log(objectStore)
  
      objectStore.createIndex("name", "name", { unique: false });
  
      objectStore.createIndex("email", "email", { unique: true });
  
      objectStore.transaction.oncomplete = function(event){
  
          var customerObjectStore = db.transaction(["customers"],"readwrite").objectStore("customers")
          
          //데이터 추가
          customerData.forEach(function(customer){
              customerObjectStore.add(customer)
          })
  
          // 위 과정을 풀어서 쓰면 다음과 같다.
          // 추가뿐 아니라 조회, 수정, 삭제 모두 아래와 같이 풀어 쓰거나 위 처럼 축약해서 쓸 수 있다.
          // var transaction = db.transaction(["customers"], "readwrite")
  
          // transaction.oncomplete = function(evt) {
          //     alert("All done!");
          // };
  
          // transaction.onerror = function(evt) {
          //     alert("error!!")
          // };
  
          // var objectStore = transaction.objectStore("customers");
          // for (var i in customerData) {
          //     var request = objectStore.add(customerData[i]);
          //     request.onsuccess = function(event) {
          //     };
          // }
  
      }
  }
  ```



- 데이터 조회

  - 아래 소개한 방법들 외에 더 구체적으로 조회하는 방법이 존재하는데 이는 아래 링크 참조

  > https://developer.mozilla.org/ko/docs/Web/API/IndexedDB_API/Using_IndexedDB#Indexed_DB_%EC%9D%98_%EC%8B%A4%ED%97%98%EC%A0%81%EC%9D%B8_%EB%B2%84%EC%A0%84%EC%9D%84_%EC%82%AC%EC%9A%A9%ED%95%B4%EB%B3%B4%EA%B8%B0

  ```javascript
  const customerData = [
      { ssn: "444-44-4444", name: "Bill", age: 35, email: "bill@company.com" },
      { ssn: "555-55-5555", name: "Donna", age: 32, email: "donna@home.org" }
  ];
  
  var db;
  
  var request = window.indexedDB.open("MyTestDatabase",2)
  
  
  request.onerror = function(event){
      alert("Database error: " + event.target.errorCode);
  }
  
  request.onsuccess = function(event){
      db = request.result
      console.log(db)
  }
  
  request.onupgradeneeded = function(event){
      var db = event.target.result;
  
      var objectStore = db.createObjectStore("customers", { keyPath: "ssn" });
      console.log(objectStore)
  
      objectStore.createIndex("name", "name", { unique: false });
  
      objectStore.createIndex("email", "email", { unique: true });
  
      objectStore.transaction.oncomplete = function(event){
  
          //데이터를 넣고
          var customerObjectStore = db.transaction(["customers"],"readwrite").objectStore("customers")
          customerData.forEach(function(customer){
              customerObjectStore.add(customer)
          })
  
          // 단일 데이터 조회(get을 사용하여 key로 조회하기)
          var transaction = db.transaction(["customers"])  //2번째 인자를 넘기지 않으면 readonly가 기본값이다.
          var objectStore = transaction.objectStore("customers")
          var request = objectStore.get("555-55-5555")  //key를 통해 조회 한다.
  
          request.onsuccess = function(event){
              console.log("Name for SSN 555-55-5555: " + request.result.name)
          }
  
          // 단일 데이터 조회(get을 사용하여 index로 조회하기)
          var index = objectStore.index("name");
  
          index.get("Donna").onsuccess = function(event) {
              alert("Donna's SSN is " + event.target.result.ssn);
          };
  
          // 모든 데이터 조회(openCursor 사용)
          var objectStore = db.transaction("customers").objectStore("customers")
          // openCursor 메서드는 첫 번째 인자로 얼마나 조회할 것인지를 받고, 두 번째 인자로 오름 차순으로 할지 내림 차순으로 할지를 정할 수 있다.
          objectStore.openCursor().onsuccess = function(event) {
              var cursor = event.target.result;
              if (cursor) {
                  alert("Name for SSN " + cursor.key + " is " + cursor.value.name);
                  cursor.continue();
              }
              else {
                  alert("No more entries!");
              }
          };
  
          // 모든 데이터 조회(gettAll 사용)
          //getAll은 IndexedDB의 표준은 아니다.
          objectStore.getAll().onsuccess = function(event) {
              alert("Got all customers: " + event.target.result);
          };
  
      }
  }
  
  ```



- 데이터 수정

  - `put()` 함수를 사용

  ```javascript
  const customerData = [
      { ssn: "444-44-4444", name: "Bill", age: 35, email: "bill@company.com" },
      { ssn: "555-55-5555", name: "Donna", age: 32, email: "donna@home.org" }
  ];
  
  var db;
  
  var request = window.indexedDB.open("MyTestDatabase",2)
  
  
  request.onerror = function(event){
      alert("Database error: " + event.target.errorCode);
  }
  
  request.onsuccess = function(event){
      db = request.result
      console.log(db)
  }
  
  request.onupgradeneeded = function(event){
      var db = event.target.result;
  
      var objectStore = db.createObjectStore("customers", { keyPath: "ssn" });
      console.log(objectStore)
  
      objectStore.createIndex("name", "name", { unique: false });
  
      objectStore.createIndex("email", "email", { unique: true });
  
      objectStore.transaction.oncomplete = function(event){
  
          //데이터를 넣고
          var customerObjectStore = db.transaction(["customers"],"readwrite").objectStore("customers")
          customerData.forEach(function(customer){
              customerObjectStore.add(customer)
          })
  
          //데이터 수정
          var objectStore = db.transaction(["customers"], "readwrite").objectStore("customers");
          var request = objectStore.get("555-55-5555");
          request.onerror = function(event) {
              console.log("Error!!! when get data from objectStore")
          };
  
          request.onsuccess = function(event) {
              // 수정하고자 하는 값을 data에 넣는다.
              var data = event.target.result;
  
              // 수정한다.
              data.age = 152;
  
              // 수정된 객체를 다시 객체 저장소에 넣는다.
              var requestUpdate = objectStore.put(data);
              requestUpdate.onerror = function(event) {
                  console.log("Error!!! when put data to objectStore")
              };
              requestUpdate.onsuccess = function(event) {
                  console.log("data is successfully updated!!!")
              };
          };
  
      }
  }
  ```






- 데이터 삭제

  - `delete()` 함수를 사용

  ```javascript
  const customerData = [
      { ssn: "444-44-4444", name: "Bill", age: 35, email: "bill@company.com" },
      { ssn: "555-55-5555", name: "Donna", age: 32, email: "donna@home.org" }
  ];
  
  var db;
  
  var request = window.indexedDB.open("MyTestDatabase",2)
  
  
  request.onerror = function(event){
      alert("Database error: " + event.target.errorCode);
  }
  
  request.onsuccess = function(event){
      db = request.result
      console.log(db)
  }
  
  request.onupgradeneeded = function(event){
      var db = event.target.result;
      var objectStore = db.createObjectStore("customers", { keyPath: "ssn" });
  
      objectStore.createIndex("name", "name", { unique: false });
  
      objectStore.createIndex("email", "email", { unique: true });
  
      objectStore.transaction.oncomplete = function(event){
  
          //데이터를 넣고
          var customerObjectStore = db.transaction(["customers"],"readwrite").objectStore("customers")
          customerData.forEach(function(customer){
              customerObjectStore.add(customer)
          })
  
          //데이터 삭제
          var request = db.transaction(["customers"], "readwrite").objectStore("customers").delete("444-44-4444")
  
          request.onsuccess = function(event){
              console.log("지워졌습니다!!")
          }
  
          request.onerror = function(event){
              console.log("지우지 못했습니다....")
          }
  
      }
  }
  ```





## 활용

> https://github.com/hedge0207/web/blob/master/indexeddb/07_practice.html 에 활용한 코드를 업로드 하였음
>
> https://romeoh.tistory.com/entry/indexed-db를 참고하여 작성함