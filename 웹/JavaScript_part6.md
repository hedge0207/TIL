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
  - 프로토타입인 이같은 문제를 해결해준다.

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

  ```javascript
  // 부모 생성자 함수
  var Parent = (function () {
    // constructor
    function Parent(name) {
      this.name = name
    }
  
    // 메소드
    Parent.prototype.sayHi = function () {
      console.log('Hi! ' + this.name)
    }
  
    // 생성자를 반환한다.
    return Parent;
  }())
  
  // 자식 생성자 함수
  var Child = (function () {
    // constructor
    function Child(name) {
      this.name = name
    }
  
    // 자식 생성자 함수의 프로토타입 객체를 부모 생성자 함수의 인스턴스로 교체.
    Child.prototype = new Parent()
  
    // 메소드 오버라이드
    Child.prototype.sayHi = function () {
      console.log('안녕하세요! ' + this.name)
    }
  
    // sayBye 메소드는 Parent 생성자함수의 인스턴스에 위치된다
    Child.prototype.sayBye = function () {
      console.log('안녕히가세요! ' + this.name)
    }
  
    // 생성자를 반환한다.
    return Child
  }())
  
  var child = new Child('Cha')
  console.log(child)  // Parent { name: 'Cha' }
  
  console.log(Child.prototype) // Parent { name: undefined, sayHi: [Function], sayBye: [Function] }
  
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
    - 프로토타입 객체(`new Parent()`객체)는 내부 프로퍼티로 constructor를 가지며 이는 생성자 함수를 가리킨다. 
    - 하지만 의사 클래스 패턴 상속은 프로토타입 객체를 인스턴스로 교체하는 과정에서 constructor의 연결이 깨지게 된다. 
    - 즉, `child` 객체를 생성한 것은 `Child` 생성자 함수이지만 `child.constructor`의 출력 결과는 `Child` 생성자 함수가 아닌 `Parent` 생성자 함수를 나타낸다. 
    - 이는 `child` 객체의 프로토타입 객체인 `new Parent()` 객체는 `constructor`가 없기 때문에 프로토타입 체인에 의해 `Parent.prototype`의 constructor를 참조했기 때문이다.

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
    // Constructor
    function Parent(name) {
      this.name = name
    }
  
    // method
    Parent.prototype.sayHi = function () {
      console.log('Hi! ' + this.name)
    };
  
    // return constructor
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