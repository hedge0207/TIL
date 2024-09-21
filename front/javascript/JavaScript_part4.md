# JavaScript 객체 지향 프로그래밍

- 객체 지향 프로그래밍
  - 명확한 정의가 존재하지 않는다.
  - 실세계에 존재하고 있는 객체를 소프트웨어 세계에서 표현하기 위해 객체의 핵심적인 개념 또는 기능만을 추출하는 추상화를 통해 모델링하려는 프로그래밍 패러다임
  - 다시 말해, 우리가 주변의 실세계에서 사물을 인지하는 방식을 프로그래밍에 접목하려는 사상을 의미한다.
  - 객체지향 프로그래밍은 함수들의 집합 혹은 단순한 컴퓨터의 명령어들의 목록이라는 전통적인 절차지향 프로그래밍과는 다른, 관계성있는 객체들의 집합이라는 관점으로 접근하는 소프트웨어 디자인으로 볼 수 있다.
  - 각 객체는 별도의 역할이나 책임을 갖는 작은 독립적인 기계 또는 부품으로 볼 수 있다.
  - 객체지향 프로그래밍은 보다 유연하고 유지보수하기 쉬우며 확장성 측면에서서도 유리한 프로그래밍을 하도록 의도되었고, 대규모 소프트웨어 개발에 널리 사용되고 있다.



- 클래스 기반 대 프로토타입 기반

  - 클래스 기반 언어
    - Java, C++, C#, Python, PHP, Ruby등
    - 클래스로 객체의 자료구조와 기능을 정의하고 생성자를 통해 인스턴스를 생성한다.
    - 클래스란 같은 종류의 집단에 속하는 속성(attribute)과 행위(behavior)를 정의한 것으로 객체지향 프로그램의 기본적인 사용자 정의 데이터형(user define data type)이라고 할 수 있다.
    - 결국 클래스는 객체 생성에 사용되는 패턴 혹은 청사진(blueprint)일 뿐이며 new 연산자를 통한 인스턴스화 과정이 필요하다.
    - 모든 인스턴스는 오직 클래스에서 정의된 범위 내에서만 작동하며 런타임에 그 구조를 변경할 수 없다. 
    - 이러한 특성은 정확성, 안정성, 예측성 측면에서 클래스 기반 언어가 프로토타입 기반 언어보다 좀 더 나은 결과를 보장한다.

  ```java
  // Java로 구현된 클래스
  class Person {
        private String name;
        // 생성자 함수
        public Person(String name) {
          this.name = name;
        }
  
        public String getName() {
          return this.name;
        }
  
        public void setName(String name) {
          this.name = name;
        }
  
        public static void main(String[] args) {
          Person cha = new Person("Cha");
  
          String name= cha.getName();
          System.out.println(name); // Cha
        }
  }
  ```
  - 프로토타입 기반 언어
    - JS는 멀티-패러다임 언어로 명령형(imperative), 함수형(functional), 프로토타입 기반(prototype-based) 객체지향 언어다.
    - 간혹 클래스가 없어서 객체지향이 아니라고 생각하는 사람들도 있으나 프로토타입 기반의 객체지향 언어다.
    - JS에는클래스 개념이 없고 별도의 객체 생성 방법이 존재한다.
    - JS는 이미 생성된 인스턴스의 자료구조와 기능을 동적으로 변경할 수 있다는 특징이 있다. 
    - 객체 지향의 상속, 캡슐화(정보 은닉) 등의 개념은 프로토타입 체인과 클로저 등으로 구현할 수 있다.
    - ECMAScript 6에서 새롭게 클래스가 도입되었다. ES6의 Class는 기존 prototype 기반 객체지향 프로그래밍보다 Class 기반 언어에 익숙한 프로그래머가 보다 빠르게 학습할 수 있는 단순하고 깨끗한 새로운 문법을 제시하고 있다. ES6의 Class가 새로운 객체지향 모델을 제공하는 것이 아니며 Class도 사실 함수이고 기존 prototype 기반 패턴의 Syntactic sugar이다.

  ```javascript
  // 객체 리터럴
  var obj1 = {}
  obj1.name = 'Cha'
  
  // Object() 생성자 함수
  var obj2 = new Object();
  obj2.name = 'Cha'
  
  // 생성자 함수
  function Obj() {}
  var obj3 = new Obj()
  obj3.name = 'Cha'
  ```

  

- 생성자 함수와 인스턴스의 생성

  - JS는 생성자 함수와 `new` 연산자를 통해 인스턴스를 생성할 수 있다.
  - 이 때 생성자 함수는 클래스이자 생성자의 역할을 한다.
  - 여러 개의 인스턴스를 생성할 경우 문제가 발생한다.
    - 아래 예시에서 생성된 인스턴스들은 모두 `setName`, `getName`이 중복되어 생성된다. 즉, 각 인스턴스가 내용이 동일한 메소드를 각자 소유한다.
    - 이는 메모리 낭비인데 생성되는 인스턴스가 많아지거나 메소드가 크거나 많다면 낭비도 심해지게 된다.
  - 프로토타입이 이같은 문제를 해결해준다.

  ```javascript
  function Person(name) {
    // 프로퍼티
    this.name = name;
  
    // 메소드
    this.setName = function (name) {
      this.name = name;
    };
  
    // 메소드
    this.getName = function () {
      return this.name;
    };
  }
  
  var cha  = new Person('Cha');
  var kim = new Person('Kim');
  var lee = new Person('Lee');
  ```



- 프로토타입 체인과 메소드의 정의
  - 모든 객체는 프로토타입이라는 다른 객체를 가리키는 내부 링크를 가지고 있다.
  - 즉, 프로토타입을 통해 직접 객체를 연결할 수 있는데 이를 프로토타입 체인이라 한다.
  - 프로토타입을 이용하여 생성자 함수 내부의 메소드를 생성자 함수의 prototype 프로퍼티가 가리키는 프로토타입 객체로 이동시키면 생성자 함수에 의해 생성된 모든 인스턴스는 프로토타입 체인을 통해 프로토타입 객체의 메소드를 참조할 수 있다.
  
  ```javascript
  function Person(name) {
    this.name = name
  }
  
  // 프로토타입 객체에 메소드 정의
  Person.prototype.setName = function (name) {
    this.name = name
  }
  
  // 프로토타입 객체에 메소드 정의
  Person.prototype.getName = function () {
    return this.name
  }
  
  var me  = new Person('Cha')
  var you = new Person('Kim')
  var him = new Person('Lee')
  
  console.log(Person.prototype) // Person { setName: [Function], getName: [Function] }
  
  console.log(me)  // Person { name: 'Cha' }
  console.log(you) // Person { name: 'Kim' }
  console.log(him) // Person { name: 'Lee' }
  ```
  
  - 더글라스 크락포드가 제안한 프로토타입 객체에 메소드를 추가하는 방식
    - 모든 생성자는 함수이고 모든 함수의 프로토타입은 `Function.prototype`이다.
    - 따라서 모든 생성자 함수는 `Function.prototype`에 접근할 수 있다.
  
  ```javascript
  // Function.prototype에 method라는 메소드를 생성하는 프로퍼티를 추가.
  // name에는 메서드 이름, func에는 메서드의 몸체를 넣으면 된다. 
  Function.prototype.method = function (name, func) {
    // this는 생성자 함수를 가리키게 된다.
    if (!this.prototype[name]) {
      this.prototype[name] = func
    }
  }
  
  // 생성자 함수
  function Person(name) {
    this.name = name
  }
  
  // Function.prototype의 method 메소드를 활용하여 생성자함수 Person의 프로토타입에 메소드 setName을 추가.
  Person.method('setName', function (name) {
    this.name = name
  })
  
  // Function.prototype의 method 메소드를 활용하여 생성자함수 Person의 프로토타입에 메소드 getName을 추가.
  Person.method('getName', function () {
    return this.name
  })
  
  var me  = new Person('Cha')
  var you = new Person('Kim')
  var him = new Person('Lee')
  
  console.log(Person.prototype) // Person { setName: [Function], getName: [Function] }
  
  console.log(me)  // Person { name: 'Cha' }
  console.log(you) // Person { name: 'Kim' }
  console.log(him) // Person { name: 'Lee' }
  ```



## 상속

- 상속(inheritance)
  - 상속은 코드 재사용의 관점에서 매우 유용하다. 코드 재사용은 개발 비용을 현저히 줄일 수 있는 잠재력이 있기 때문에 매우 중요하다. 
  - 새롭게 정의할 클래스가 기존에 있는 클래스와 매우 유사하다면, 상속을 통해 다른 점만 구현하면 된다. 
  - 클래스 기반 언어에서 객체는 클래스의 인스턴스이며 클래스는 다른 클래스로 상속될 수 있다. 
  - 자바스크립트는 기본적으로 프로토타입을 통해 상속을 구현한다. 이것은 프로토타입을 통해 객체가 다른 객체로 직접 상속된다는 의미이다. 
  - 자바스크립트의 상속 구현 방식은 크게 두 가지로 구분할 수 있다. 
    - 클래스 기반 언어의 상속 방식을 흉내 내는 것(의사 클래스 패턴 상속, Pseudo-classical Inheritance) .
    - 프로토타입으로 상속을 구현하는 것(프로토타입 패턴 상속, Prototypal Inheritance).





### 의사 클래스 패턴 상속

- 방식

  - 자식 생성자 함수의 prototype 프로퍼티를 부모 생성자 함수의 인스턴스로 교체하여 상속을 구현한다. 
  - 부모와 자식 모두 생성자 함수를 정의하여야 한다.
- `new` 연산자를 사용한다는 것이 핵심이다.
    - 생성자 함수는 정의되는 순간 해당 함수에 constructor 자격이 부여되고, `new` 키워드를 통해 새로운 객체를 만들어 낼 수 있게 된다.
    - 또한 해당 함수의 프로토타입 객체가 생성되고 함수와 연결된다. 이 객체의 constructor 프로퍼티는 생성자 함수를 가리키게 된다.
    
  ```javascript
  var Parent = (function () {
      // 생성자 함수 정의
      function ParentConstructor(name) {
          this.name = name
      }
  
      // 메소드
      ParentConstructor.prototype.sayHi = function () {
          console.log('Hi! ' + this.name)
      }
  
      // 생성자를 반환한다.
      return ParentConstructor;
  }())
  
  // 자식 생성자 함수
  var Child = (function () {
      // 생성자 함수 정의
      function ChildConstructor(name) {
          this.name = name
      }
  
      // 자식 생성자 함수의 프로토타입 객체를 부모 생성자 함수의 인스턴스로 교체.
      ChildConstructor.prototype = new Parent()
  
      // 메소드 오버라이드
      ChildConstructor.prototype.sayHi = function () {
          console.log('안녕하세요! ' + this.name)
      }
  
      // sayBye 메소드는 Parent 생성자함수의 인스턴스에 위치된다
      ChildConstructor.prototype.sayBye = function () {
          console.log('안녕히가세요! ' + this.name)
      }
  
      // 생성자를 반환한다.
      return ChildConstructor
  }())
  
  var child = new Child('Cha')
  console.log(child)  // ParentConstructor { name: 'Cha' }
  
  console.log(Child.prototype) 
  // ParentConstructor { name: undefined, sayHi: [Function (anonymous)], sayBye: [Function (anonymous)] }
  
  child.sayHi()  // 안녕하세요! Cha
  child.sayBye() // 안녕히가세요! Cha
  
  console.log(child instanceof Parent) // true
  console.log(child instanceof Child)  // true
  ```



- 문제점

  - `new` 연산자를 통해 인스턴스를 생성한다.
    - JS의 프로토타입 본질에 모순되는 것이다.
    - 프로토타입 본성에 맞게 객체에서 다른 객체로 직접 상속하는 방법을 갖는 대신 생성자 함수와 new 연산자를 통해 객체를 생성하는 불필요한 간접적인 단계가 있다. 
    - 클래스와 비슷하게 보이는 일부 복잡한 구문은 프로토타입 메커니즘을 명확히 나타내지 못하게 한다.
    - 또한 생성자 함수의 사용에는 심각한 위험이 존재한다. 
    - 만약 생성자 함수를 호출할 때 new 연산자를 포함하는 것을 잊게 되면 this는 새로운 객체와 바인딩되지 않고 전역객체에 바인딩된다(new 연산자와 함께 호출된 생성자 함수 내부의 this는 새로 생성된 객체를 참조한다).
    - 이런 문제점을 경감시키기 위해 파스칼 표시법(첫글자를 대문자 표기)으로 생성자 함수 이름을 표기하는 방법을 사용하지만, 더 나은 대안은 new 연산자의 사용을 피하는 것이다.
  - 생성자 링크의 파괴
    - 위 예에서 `child` 객체의 프로토타입 객체는 `Parent` 생성자 함수가 생성한 `new Parent()` 객체이다. 
    - 프로토타입 객체는 내부 프로퍼티로 constructor를 가지며 이는 생성자 함수를 가리킨다. 
    - 그러나 `child` 객체의 프로토타입 객체인 `new Parent()`객체는 본래 프로토타입 객체가 아니었으므로 constructor가 없다.
    -  `child` 객체의 프로토타입 객체인 `new Parent()` 객체는 constructor가 없기 때문에 프로토타입 체인에 의해  `new Parent()` 객체의 프로토타입 객체인  `Parent.prototype`의 constructor를 참조하게 된다.
    - 즉, `child` 객체를 생성한 것은 `Child` 생성자 함수이지만 `child.constructor`의 출력 결과는 `Child` 생성자 함수가 아닌 `Parent` 생성자 함수를 나타낸다.
- 따라서 의사 클래스 패턴 상속은 프로토타입 객체를 인스턴스로 교체하는 과정에서 constructor의 연결이 깨지게 된다. 
  
  - 객체 리터럴
    - 생성자 함수를 사용하기 때문에 객체 리터럴 패턴으로 생성한 객체의 상속에는 적합하지 않다.
    - 객체 리터럴 패턴으로 생성한 객체의 생성자 함수는 `Object()`이고 이를 변경할 방법이 없기 때문이다.



### 프로토타입 패턴 상속

- 방식

  - `Object.create` 함수를 사용하여 객체에서 다른 객체로 직접 상속을 구현
    - `Object.create` 함수는 매개변수에 프로토타입으로 설정할 객체 또는 인스턴스를 전달하고 이를 상속하는 새로운 객체를 생성한다.
    - IE9 이상에서 정상적으로 동작한다. 따라서 크로스 브라우징에 주의하여야 한다.
  - 프로토타입 패턴 상속은 개념적으로 의사 클래스 패턴 상속보다 더 간단하다. 
  - 또한 의사 클래스 패턴의 단점인 `new` 연산자가 필요없다.
  - 생성자 링크도 파괴되지 않는다.

  ```javascript
  // 부모 생성자 함수
  var Parent = (function () {
    // 생성자 정의
    function Parent(name) {
      this.name = name
    }
  
    // method
    Parent.prototype.sayHi = function () {
      console.log('Hi! ' + this.name)
    };
  
    // 생성자를 반환
    return Parent
  }())
  
  // create 함수의 인수는 프로토타입이다.
  var child = Object.create(Parent.prototype)
  child.name = 'child'
  
  child.sayHi()  // Hi! child
  
  console.log(child instanceof Parent) // true
  ```

  - 객체리터럴에도 사용할 수 있다.

  ```javascript
  var parent = {
    name: 'parent',
    sayHi: function() {
      console.log('Hi! ' + this.name)
    }
  }
  
  // create 함수의 인자는 객체이다.
  var child = Object.create(parent)
  child.name = 'child'
  
  // var child = Object.create(parent, {name: {value: 'child'}});
  
  parent.sayHi() // Hi! parent
  child.sayHi()  // Hi! child
  
  console.log(parent.isPrototypeOf(child)) // true
  ```

  - `Object.create` 함수의 **폴리필**(Polyfill: 특정 기능이 지원되지 않는 브라우저를 위해 사용할 수 있는 코드 조각이나 플러그인)을 살펴보면 상속의 핵심을 이해할 수 있다.
    - 비어있는 생성자 함수 F를 생성.
    - 생성자 함수 F의 prototype 프로퍼티에 매개변수로 전달받은 객체를 할당.
    - 생성자 함수 F를 생성자로 하여 새로운 객채를 생성하고 반환

  ```javascript
  // Object.create 함수의 폴리필
  if (!Object.create) {
    Object.create = function (o) {
      function F() {}
      F.prototype = o;
      return new F();
    };
  }
  ```



## 캡슐화와 모듈 패턴

- 캡슐화

  - 캡슐화는 관련있는 멤버 변수와 메소드를 클래스와 같은 하나의 틀 안에 담고 외부에 공개될 필요가 없는 정보는 숨기는 것을 말하며 다른 말로 정보 은닉(information hiding)이라고 한다.
  - 이것은 클래스 외부에는 제한된 접근 권한을 제공하며 원하지 않는 외부의 접근에 대해 내부를 보호하는 작용을 한다. 이렇게 함으로써 이들 부분이 프로그램의 다른 부분들에 영향을 미치지 않고 변경될 수 있다.
  - 예시
    - JS는 함수 레벨 스코프를 제공하므로 함수 내의 변수는 외부에서 참조할 수 없다. 따라서 `Person()` 내의 `name`은 private 변수가 된다.
    - 만약 this를 사용하면 public 멤버가 된다(단, `new` 키워드로 `Person` 객체를 생성하지 않으면 this는 생성된 객체가 아닌 전역 객체에 연결된다).
    - public 메소드 `getName`, `setName`은 클로저로서 private 변수(자유 변수)에 접근할 수 있다. 이것이 기본적인 정보 은닉 방법이다.

  ```javascript
  var Person = function(arg) {
      var name = arg ? arg : ''
  
      this.getName = function() {
          return name
      };
  
      this.setName = function(arg) {
          name = arg
      };
  }
  // 외부에서는 접근이 불가능
  console.log(name)    // ReferenceError: name is not defined
  
  var me = new Person('Lee')
  
  var myName = me.getName()
  
  console.log(myName)	// Lee
  
  me.setName('Kim')
  myName = me.getName()
  
  console.log(myName)	// Kim
  ```



- 모듈 패턴

  - 모듈: 전체 어플리케이션의 일부를 독립된 코드로 분리하여 만들어 놓은 것.
  - 캡슐화를 위한 패턴의 하나로 public한 메서드를 통해서만 private 변수에 접근할 수 있게 하는 방식이다.
    - `return` 이하는 public 으로 접근할 수 있는 부분을 구현하고, 위쪽으로는 private 한 영역을 구현한다. 
  - 위 예시를 아래와 같이 변경하면 모듈 패턴이 된다.
  - `person` 함수는 객체를 반환한다. 이 객체 내의 메소드 `getName`, `setName`은 클로저로서 private 변수 `name`에 접근할 수 있다.

  ```javascript
  var person = function(arg) {
      var name = arg ? arg : '';
  
      return {
          getName: function() {
              return name;
          },
          setName: function(arg) {
              name = arg;
          }
      }
  }
  
  console.log(name)		// ReferenceError: name is not defined
  var me = person('Lee')
  
  var myName = me.getName()
  
  console.log(myName)
  
  me.setName('Kim')
  myName = me.getName()
  
  console.log(myName)
  ```



- 모듈 패턴의 주의점

  - private 멤버가 객체나 배열일 경우, 반환된 해당 멤버의 변경이 가능하다.
    - 객체를 반환하는 경우 반환값은 얕은 복사(shallow copy)로 private 멤버의 참조값을 반환하게 된다.
    - 따라서 외부에서도 private 멤버의 값을 변경할 수 있다.
    - 이를 회피하기 위해서는 객체를 그대로 반환하지 않고 반환해야 할 객체의 정보를 새로운 객체에 담아 반환해야 한다. 
    - 반드시 객체 전체가 그대로 반환되어야 하는 경우에는 깊은 복사(deep copy)로 복사본을 만들어 반환한다.

  ```javascript
  var person = function (personInfo) {
      // private 멤버, personInfo에는 객체가 담겨 있다.
      var info = personInfo
  	
      // 객체를 반환
      return {
          getPersonInfo: function() {
              return info
          }
      }
  }
  
  var me = person({ name: 'Lee', gender: 'male' })
  
  var myInfo = me.getPersonInfo()
  console.log(myInfo)  // myInfo:  { name: 'Lee', gender: 'male' }
  
  myInfo.name = 'Kim'
  
  myInfo = me.getPersonInfo()
  console.log(myInfo)  // myInfo:  { name: 'Kim', gender: 'male' }
  ```

  - 반환된 객체는 함수 객체의 프로퍼티에 접근할 수 없다.
    - 이는 상속을 구현할 수 없음을 의미한다.
    - 앞에서 살펴본 모듈 패턴은 생성자 함수가 아니며 단순히 메소드를 담은 객체를 반환한다. 
    - 반환된 객체는 객체 리터럴 방식으로 생성된 객체로 함수 person의 프로토타입에 접근할 수 없다.
    - 반환된 객체가 함수 person의 프로토타입에 접근할 수 없다는 것은 person을 부모 객체로 상속할 수 없다는 것을 의미한다.
    - 함수 person을 부모 객체로 상속할 수 없다는 것은 함수 person이 반환하는 객체에 모든 메소드를 포함시켜야한다는 것을 의미한다.
    - 이 문제를 해결하기 위해서는 객체를 반환하는 것이 아닌 함수를 반환해야 한다.

  ```javascript
  var person = function(arg) {
      var name = arg ? arg : ''
  
      return {
          getName: function() {
              return name
          },
          setName: function(arg) {
              name = arg
          }
      }
  }
  
  var me = person('Lee')
  console.log(me.__proto__ === person.prototype) // false
  // 객체 리터럴 방식으로 생성된 객체와 동일하다
  console.log(me.__proto__ === Object.prototype) // true
  
  
  
  // 상속을 구현하기 위해 함수를 반환하는 방식
  var Person = function() {
    var name
  
    var F = function(arg) { name = arg ? arg : ''; }
  
    F.prototype = {
      getName: function() {
        return name
      },
      setName: function(arg) {
        name = arg
      }
    }
    return F
  }()
  
  var me = new Person('Lee')
  
  console.log(me.__proto__ === Person.prototype)	// True
  
  console.log(me.getName())	// Lee
  me.setName('Kim')
  console.log(me.getName())	// Kim
  ```








#  빌트인 객체

- 자바스크립트의 객체는 크게 아래의 3가지로 분류할 수 있다.
  - 네이티브 객체(Native objects 또는 Built-in objects 또는 Global Objects)
  - 호스트 객체(Host object)
  - 사용자 정의 객체(User-defined object)



- 네이티브 객체

  - ECMAScript 명세에 정의된 객체를 말하며, 애플리케이션 전역의 공통 기능을 제공한다. 
  - 애플리케이션의 환경과 관계없이 언제나 사용할 수 있다.
  - Object, String, Number, Function, Array, RegExp, Date, Math와 같은 객체 생성에 관계가 있는 함수 객체와 메소드로 구성된다.
  - 네이티브 객체를 Global Objects라고 부르기도 하는데 이것은 전역 객체(Global Object)와 다른 의미로 사용되므로 혼동에 주의하여야 한다.
  - Object
    - `Object()` 생성자 함수는 객체를 생성한다.
    - 만일 생성자 인수값이 null 이거나 undefiend이면 빈 객체를 반환한다.
    - 그 외의 경우 함수의 인수값에 따라 강제 형변환된 객체가 반환된다. 이때 반환된 객체의 [[Prototype]] 프로퍼티에 바인딩된 객체는 Object.prototype이 아니다.

  ```javascript
  var a = new Object()
  console.log(typeof a + ': ', a)				// object:  {}
  
  var b = new Object(undefined)
  console.log(typeof b + ': ', b)				// object:  {}
  
  var c = new Object(null)
  console.log(typeof c + ': ', c)				// object:  {}
  
  
  var obj = new Object('String')
  console.log(typeof obj + ': ', obj)			// object:  [String: 'String']
  
  var strObj = new String('String')
  console.log(typeof strObj + ': ', strObj)	// object:  [String: 'String']
  
  // Number 객체를 반환한다
  // var obj = new Number(123);과 동치이다
  var obj = new Object(123)
  console.log(typeof obj + ': ', obj)			// object:  [Number: 123]
  
  var numObj = new Number(123)
  console.log(typeof numObj + ': ', numObj)	// object:  [Number: 123]
  
  // Boolean 객체를 반환한다.
  // var obj = new Boolean(true);과 동치이다
  var obj = new Object(true)
  console.log(typeof obj + ': ', obj)			// object:  [Boolean: true]
  
  var boolObj = new Boolean(123)
  console.log(typeof boolObj + ': ', boolObj)	// object:  [Boolean: true]
  ```

  - Function
    - JS의 모든 함수는 Function 객체이다. 
    - 다른 모든 객체들처럼 Function 객체는 `new` 연산자을 사용해 생성할 수 있다.

  - Boolean
    - Boolean 객체는 원시 타입 boolean을 위한 래퍼(wrapper) 객체이다. 
    - Boolean 생성자 함수로 Boolean 객체를 생성할 수 있다.
    - Boolean 객체와 원시 타입 boolean을 혼동하기 쉽다. Boolean 객체는 true/false를 포함하고 있는 객체이다.

  ```javascript
   Numberconsole.log(typeof true)			// boolean
  console.log(typeof Boolean(1))		// boolean
  console.log(typeof new Boolean(1))	// object
  ```

  - Error
    - Error 생성자는 error 객체를 생성한다. error 객체의 인스턴스는 런타임 에러가 발생하였을 때 throw된다.
  - 이 밖에도 Number, Math, Date, String, RegExp, Array, Symbol 등의 네이티브 객체가 존재한다.
  - 원시타입과 래퍼 객체(Wrapper Object)
    - 앞서 살펴본 바와 같이 각 네이티브 객체는 각자의 프로퍼티와 메소드를 가진다. 
    - 정적(static) 프로퍼티, 메소드는 해당 인스턴스를 생성하지 않아도 사용할 수 있고 prototype에 속해있는 메소드는 해당 prototype을 상속받은 인스턴스가 있어야만 사용할 수 있다.
    - 그런데 원시 타입 값에 대해 표준 빌트인 객체의 메소드를 호출하면 정상적으로 작동한다.
    - 이는 원시 타입 값에 대해 표준 빌트인 객체의 메소드를 호출할 때, 원시 타입 값은 연관된 객체(Wrapper 객체)로 일시 변환 되기 때문이다.
    - 메소드 호출이 종료되면 객체로 변환된 원시 타입 값은 다시 원시 타입 값으로 복귀한다.
    - 프로토타입에서 원시 타입의 확장 참고

  ```javascript
  // 본래 toUpperCase()는 String 객체의 메서드이다.
  var str = new String("hello! world!")
  console.log(str.toUpperCase())		// HELLO WORLD!
  
  // 그러나 String 객체가 아닌 원시타입 string에도 사용이 가능하다.
  var str = 'Hello world!'
  var res = str.toUpperCase()
  console.log(res) 					// HELLO WORLD!
  
  var num = 1.5
  console.log(num.toFixed()) 			// 2
  ```



- 호스트 객체

  - 정의: 브라우저 환경에서 제공하는 window, XmlHttpRequest, HTMLElement 등의 DOM 노드 객체와 같이 호스트 환경에 정의된 객체 
    - 예를 들어 브라우저에서 동작하는 환경과 브라우저 외부에서 동작하는 환경의 자바스크립트(Node.js)는 다른 호스트 객체를 사용할 수 있다.
    - 브라우저에서 동작하는 환경의 호스트 객체는 전역 객체인 window, BOM(Browser Object Model)과 DOM(Document Object Model) 및 XMLHttpRequest 객체 등을 제공한다.

  - 전역 객체(Global Object)
    - 모든 객체의 최상위 객체.
    - 일반적으로 브라우저에서는 window, 서버에서는 global을 의미한다.
  - BOM(Browser Object Model)
    - 브라우저 탭 또는 브라우저 창의 모델을 생성.
    - 최상위 객체는 window 객체로 현재 브라우저 창 또는 탭을 표현하는 객체이다.
    - 이 객체의 자식 객체들은 브라우저의 다른 기능들을 표현한다.
    - 이 객체들은 Standard Built-in Objects가 구성된 후에 구성된다.
  - DOM(Document Object Model)
    - 문서 객체 모델은 현재 웹페이지의 모델을 생성한다. 
    - 최상위 객체는 document 객체로 전체 문서를 표현한다. 
    - 또한 이 객체의 자식 객체들은 문서의 다른 요소들을 표현한다. 
    - 이 객체들 역시 Standard Built-in Objects가 구성된 후에 구성된다.





# 전역 객체

- 전역 객체(Global Onject)
  - 모든 객체의 유일한 최상위 객체
  - 일반적으로 브라우저에서는 window, 서버에서는 global을 의미한다.



- 특징

  - 전역 객체는 실행 컨텍스트에 컨트롤이 들어가기 이전에 생성되며 contstructor가 업시 때문에 `new` 연산자를 사용하여 새롭게 생성할 수 없다.
    - 즉 개발자가 전역 객체를 생성하는 것은 불가능하다.
  - 전역 객체는 전역 스코프를 갖게 된다.
  - 전역 객체의 자식 객체를 사용할 때 전역 객체의 기술은 생략할 수 있다.
    - 예를 들어 document 객체는 window의 자식 객체이기에 `window.document`와 같이 기술할 수 있으나 일반적으로 생략한다.
    - 그러나 사용자가 정의한 변수와 전역 객체의 자식 객체 이름이 충돌하는 경우, 명확히 전역 객체를 기술하여 혼동을 방지할 수 있다.

  ```javascript
  // 둘은 같은 문장이다.
  window.document.getElementById('foo').style.display = 'none'
  document.getElementById('foo').style.display = 'none'
  ```

  - 전역 객체는 전역 변수를 프로퍼티로 갖게 된다. 
    - 다시 말해 전역 변수는 전역 객체의 프로퍼티이다.

  ```javascript
  var gv = 'global variable'
  console.log(gv)			// global variable
  console.log(window.gv)	// global variable
  ```

  - 글로벌 영역에서 선언한 함수도 전역 객체의 프로퍼티로 접근할 수 있다.
    - 다시 말해 전역 함수는 전역 객체의 메소드다.

  ```javascript
  function gf(){
      console.log('global function')
  }
  
  gf()		// global function
  window.gf()	// global function
  ```

  - Standard Built-in Objects(표준 빌트인 객체)도 역시 전역 객체의 자식 객체이다. 
    - 전역 객체의 자식 객체를 사용할 때 전역 객체의 기술은 생략할 수 있으므로 표준 빌트인 객체도 전역 객체의 기술을 생략할 수 있다.

  ```javascript
  window.console.log('hello!')	// hello!
  console.log('hello!')			// hello!
  ```



## 전역 프로퍼티

- 애플리케이션 전역에서 사용하는 값들을 나타내기 위해 사용하는 것으로서 전역 객체의 프로퍼티이다.
  - 전역 프로퍼티는 간단한 값이 대부분이며 다른 프로퍼티나 메서드를 가지고 있지 않다.
  - 예를 들어 전역 프로퍼티인 undefined는 따로 메서드를 가지고 있지 않다.



- `Infinity`

  - 양/음의 무한대를 나타내는 숫자값 Infinity를 값으로 갖는다.

  ```javascript
  console.log(window.Infinity) // Infinity
  console.log(typeof Infinity) // number
  ```



- `NaN`

  - 숫자가 아님(Not a Number)을 나타내는 숫자값 NaN을 값으로 갖는다.
  - NaN 프로퍼티는 Number.NaN 프로퍼티와 같다.

  ```javascript
  console.log(window.NaN) 	// NaN
  
  console.log(Number('abc')) 	// NaN
  console.log(1 * 'str')  	// NaN
  console.log(typeof NaN)    	// number
  ```



- `undefined`

  - 원시타입 undefined를 값으로 갖는다.

  ```javascript
  console.log(window.undefined) // undefined
  
  var foo
  console.log(foo) // undefined
  console.log(typeof undefined) // undefined
  ```

  

## 전역 함수

- 애플리케이션 전역에서 호출할 수 있는 함수로서 전역 객체의 메서드이다.



- `eval()`

  - 매개변수에 전달된 문자열 구문 또는 표현식을 평가 또는 실행한다. 
  - 사용자로 부터 입력받은 콘텐츠(untrusted data)를 `eval()`로 실행하는 것은 보안에 매우 취약하므로 사용을 지양해야 한다.

  ```javascript
  var foo = eval('1 + 2')
  console.log(foo)		 // 3
  
  var x = 3
  var y = 3
  console.log(eval('x * y')) // 9
  ```



- `isFinite()`

  - 매개 변수에 전달된 값이 정상적인 유한수인지 검사하여 그 결과를 Boolean으로 반환한다. 
  - 매개변수에 전달된 값이 숫자가 아닌 경우, 숫자로 변환한 후 검사를 수행한다.
  - `null`은 0으로 변환된다.

  ```javascript
  console.log(isFinite(Infinity));  // false
  console.log(isFinite(NaN));       // false
  console.log(isFinite('Hello'));   // false
  console.log(isFinite(0));         // true
  console.log(isFinite('10'));      // true
  console.log(isFinite(null));      // true
  ```



- `isNaN()`

  - 매개 변수에 전달된 값이 `NaN`인지 검사하여 그 결과를 Boolean으로 반환한다. 
  - 매개변수에 전달된 값이 숫자가 아닌 경우, 숫자로 변환한 후 검사를 수행한다.
  - `undefined`, 빈 객체, 비어있지 않은 숫자가 아닌 문자열은 `NaN`으로 변환된다.

  ```javascript
  isNaN(NaN)       // true
  isNaN(undefined) // true
  isNaN({})        // true
  isNaN('blabla')  // true
  
  isNaN(true)      // false
  isNaN(null)      // false
  isNaN(37)        // false
  
  // strings
  isNaN('37')      // false: '37' → 37
  isNaN('37.37')   // false: '37.37' → 37.37
  isNaN('')        // false: '' → 0
  isNaN(' ')       // false: ' ' → 0
  
  // dates
  isNaN(new Date())             // false: new Date() → Number
  isNaN(new Date().toString())  // true:  String → NaN
  ```



- `parseFloat()`

  - 매개변수에 전달된 문자열을 부동소수점 숫자로 변환하여 반환한다.
  - 문자열의 첫 숫자만 반환되며 전후 공백은 무시된다.
  - 첫 문자를 숫자로 반환할 수 없다면 `NaN`을 반환한다.

  ```javascript
  parseFloat('3.14');     // 3.14
  parseFloat('10.00');    // 10
  parseFloat('34 45 66'); // 34
  parseFloat(' 60 ');     // 60
  parseFloat('28 years'); // 28
  parseFloat('He was 28') // NaN
  ```



- `parseInt()`

  - 매개변수에 전달된 문자열을 정수형 숫자로 해석하여 반환한다.
  - 진법을 나타내는 기수를 두 번째 매개변수로 받으며, 10진수가 기본값이다(첫 번째 인자를 해당 진수로 변환하여 해석한다). 
  - 반환값은 언제나 10진수이다(결과값을 10진수로 변환하여 반환한다.).
  - 두 번째 매개변수에 진법을 나타내는 기수를 지정하지 않아도 첫 번째 매개변수에 전달된 문자열이 "0x" 또는 "0X"로 시작하면 16진수로 해석하여 반환한다.
  - 첫 번째 매개변수에 전달된 문자열이 "0"으로 시작해도 8진수가 아닌 10진수로 해석한다.
  - 첫번째 매개변수에 전달된 문자열의 첫번째 문자가 해당 지수의 숫자로 변환될 수 없다면 `NaN`을 반환한다.
  - 하지만 첫번째 매개변수에 전달된 문자열의 두번째 문자부터 해당 진수를 나타내는 숫자가 아닌 문자(예를 들어 2진수의 경우, 2)와 마주치면 이 문자와 계속되는 문자들은 전부 무시되며 해석된 정수값만을 반환한다.
  - 첫번째 매개변수에 전달된 문자열에 공백이 있다면 첫번째 문자열만 해석하여 반환하며 전후 공백은 무시된다. 만일 첫번째 문자열을 숫자로 파싱할 수 없는 경우, NaN을 반환한다.

  ```javascript
  parseInt(12)			// 12
  parseInt(12.3)			// 12
  parseInt('12.345')		// 12
  parseInt('10',2)		// 2
  parseInt('0x10') 		// 16
  parseInt('Q123')		// NaN
  parseInt('20', 2)		// NaN
  parseInt('1Q23')		// 1
  parseInt('11 22 33'); 	// 11
  parseInt(' 28 ');     	// 28
  parseInt('28 years'); 	// 28
  ```



- `encodeURI()`, `decodeURI()`

  - `encodeURI()`는 매개변수로 전달된 URI(Uniform Resource Identifier)를 인코딩한다.
    - **인코딩**: URI의 문자들을 이스케이프 처리하는 것을 의미한다.
    - **이스케이프 처리**: 네트워크를 통해 정보를 공유할 때 어떤 시스템에서도 읽을 수 있는 **ASCII Character-set**로 변환하는 것이다. UTF-8 특수문자의 경우, 1문자당 1~3byte, UTF-8 한글 표현의 경우, 1문자당 3btye이다. 예를 들어 특수문자 공백(space)은 %20, 한글 ‘가’는 %EC%9E%90으로 인코딩된다.
    - 이스케이프 처리 이유: URI 문법 형식 표준 RFC3986에 따르면 URL은 ASCII Character-set으로만 구성되어야 하며 한글을 포함한 대부분의 외국어나 ASCII에 정의되지 않은 특수문자의 경우 URL에 포함될 수 없다. 따라서 URL 내에서 의미를 갖고 있는 문자(%, ?, #)나 URL에 올 수 없는 문자(한글, 공백 등) 또는 시스템에 의해 해석될 수 있는 문자(<, >)를 이스케이프 처리하여 야기될 수 있는 문제를 예방하기 위함이다.
    - 단, `알파벳, 0-9의 숫자,-_.!~*'()`등은 이스케이프 처리에서 제외된다.
  - `decodeURI()`는 매개변수로 전달된 URI를 디코딩한다.

  ```javascript
  var uri = 'http://example.com?address=대전&hobby=programmin&watching'
  var enc = encodeURI(uri)
  var dec = decodeURI(enc)
  console.log(enc)	// http://example.com?address=%EB%8C%80%EC%A0%84&hobby=programmin&watching
  console.log(dec)	// http://example.com?address=대전&hobby=programmin&watching
  ```



- `encodeURICompoent()`/`decodeURIComponent()`

  - `encodeURIComponent()`는 매개변수로 전달된 URI(Uniform Resource Identifier) component(구성 요소)를 인코딩한다.
    - `encodeURIComponent()`는 인수를 쿼리스트링의 일부라고 간주한다.
    - 따라서 `=,?,&`를 인코딩한다.
    - 반면 `encodeURI()`는 인수를 URI 전체라고 간주하며 파라미터 구분자인 `=,?,&`를 인코딩하지 않는다.
  - `decodeURIComponent()`는 매개변수로 전달된 URI component를 디코딩한다.

  ```javascript
  var uri = 'http://example.com?address=대전&hobby=programmin&watching'
  var encc = encodeURIComponent(uri)// http%3A%2F%2Fexample.com%3Faddress%3D%EB%8C%80%EC%A0%84%26hobby%3Dprogrammin%26watching
  
  var encc = decodeURIComponent(dec)// http://example.com?address=대전&hobby=programmin&watching
  ```





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
  ````



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
    -  `Date.prototype.getMinutes()`: 분(0 ~ 59)를 나타내는 정수를 반환한다.
    -  `Date.prototype.getSeconds()`: 초(0~59)를 나타내는 정수를 반환한다.
    -  `Date.prototype.getMilliseconds()` : 밀리초(0 ~ 999)를 나타내는 정수를 반환한다.

  ```javascript
  var d = new Date()
  console.log(d.getHours())			// 21
  console.log(d.getMinutes())			// 20
  console.log(d.getSeconds())			// 55
  console.log(d.getMilliseconds())	// 1
  ```

  - `Date.prototype.setHours()` / `Date.prototype.setMinutes()` / `Date.prototype.setSeconds()` / `Date.prototype.setMilliseconds()`
    -  `Date.prototype.setHours()`: 시간(0 ~ 23)를 나타내는 정수를 설정한다. 시간 이외 분, 초, 밀리초도 설정할 수 있다.
    -  `Date.prototype.setMinutes()`: 분(0 ~ 59)를 나타내는 정수를 설정한다. 분 이외 초, 밀리초도 설정할 수 있다.
    -  `Date.prototype.setSeconds()`: 초(0 ~ 59)를 나타내는 정수를 설정한다. 초 이외 밀리초도 설정할 수 있다.
    -  `Date.prototype.setMilliseconds()` : 밀리초(0 ~ 999)를 나타내는 정수를 설정한다.

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

