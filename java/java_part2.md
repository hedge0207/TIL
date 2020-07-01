#  객체지향 프로그래밍

## 클래스

- Java는 객체 지향 언어로 클래스에 대해 이해하는 것이 중요하다.



- 하나의 .java 파일 내에는 여러개의 클래스를 선언할 수 있다. 단, 파일명과 클래스명이 일치할 경우 일치하는 클래스에 `public`을 붙여주는 것이 관례다.



- 클래스: 객체를 만들기 위한 틀

  - 붕어빵을 예로 들면, 붕어빵이 객체라면 붕어빵 틀이 클래스라고 할 수 있다.

  - 클래스를 생성 후 `new` 키워드를 통해 객체(인스턴스)를 생성 
    - 만일 dog이라는 인스턴스를 생성한다고 하면 dog에는 사실 인스턴스 그 자체가 아닌 생성된 인스턴스를 가리키고 있는 주소가 저장되어 있다.
  - 클래스에 의해 만들어진 객체를 인스턴스라고 한다.
    - 아래 예시를 보았을 때 'dog은 인스턴스'라는 표현보다는 'dog은 객체'라는 표현이 자연스럽다.
    - 'dog은 Animal의 객체'라는 표현보다는 'dog은 Animal의 인스턴스'라는 표현이 자연스럽다.

  ```java
  //클래스 생성
  public class Animal {
    
  }
    
  //객체 생성
  Animal dog = new Animal()
  ```



- 객체 변수(필드라고도 부른다)

  - 클래스에 선언된 변수를 객체 변수라고 부른다.
  - 혹은 인스턴스 변수, 멤버 변수, 속성이라고도 부른다.
  - 객체 변수는 도트 연산자 `.`를 통해 접근 가능하다.
  - 객체 변수는 공유되지 않는다. 즉 개별 객체 마다 객체 변수의 값이 독립적으로 유지된다. 예를 들어 cat, dog이라는 두 인스턴스가 있을 경우 name이라는 객체 변수를 각기 Summer, Spring이라는 다른 이름으로 가지고 있다.

  ```java
  //클래스 생성
  package first;
  
  public class Animal {
      //name이라는 객체 변수 추가
  	String name;
  }
  
  
  //객체 생성
  Animal dog = new Animal();
  dog.name="Spring";
  System.out.println(dog.name); //Spring
  ```





## 메소드

- 메소드

  ```java
  //기본형
  
  //입력변수를 매개변수 혹은 인자라고도 부른다.
  public 리턴자료형 메소드명(입력자료형1 입력변수1, 입력자료형2 입력변수2, ...) {
      ...    
      return 리턴값;  // 리턴자료형이 void 인 경우에는 return 문이 필요없다.
  }
  ```

  - 클래스 내에 구현된 함수를 메소드라고 한다. 
  - Java는 클래스를 떠나 존재하는 것이 있을 수 없기에 자바에는 함수가 따로 존재하지 않고 메소드만 존재한다고 볼 수 있다.
  - 사용하는 이유는 다른 언어와 마찬가지로 반복 작업을 보다 편하게 하기 위해서이다.
  - 객체 변수와 마찬가지로 도트 연산자를 통해 접근이 가능하다.
  - `this`: 메소드 내부에 사용된 `this`는 클래스에 의해서 생성된 객체를 지칭한다.
  - 입력변수: 매개변수 혹은 인자라고 불린다.
    - 매개변수(Parameter): 전달된 인자를 받아들이는 변수
    - 인자(Argument): 어떤 함수를 호출시에 전달되는 값
  - 클래스에 정의된 메소드를 사용하기 위해서는 객체를 만들어야 한다.

  ```java
  package first;
  
  public class Animal {
  	String name;
      
      //setName이라는 메소드를 작성
      //void는 리턴값(출력)이없다는 의미이고, String name은 name이라는 문자열을 입력으로 받는 메소드라는 뜻이다.
  	public void setName(String iname) {
          //여기서 this는 Animal class에 의해 생성되어 이 함수를 실행시킨 객체인 cat을 가리킨다.
  		this.name=iname;
          //즉 아래 예시에 따라 아래 코드를 풀어쓰면 다음과 같다.
          //cat.name="Summer";
  	}
  }
  
  //객체 생성
  Animal cat = new Animal();
  cat.setName("Summer");
  System.out.println(cat.name);  //Summer
  ```

  - 리턴값이 있을 경우의 메소드

  ```java
  public class Example {
      //sum이라는 메소드는 두 개의 int형 데이터를 입력값으로 받아 그 둘의 합을 int형으로 리턴한다.
      //리턴 값이 없을 경우 void를 쓰지만, 있을 경우 리턴값의 자료형(아래의 경우 int)을 적는다.
      public int sum(int a, int b) {
          return a+b;
      }
  
      public static void main(String[] args) {
          int a = 1;
          int b = 2;
  		
          //Example 클래스의 객체를 하나 생성하고
          Example ex1 = new Example();
          //sum 메소드를 실행시키면 그 결과값이 c에 담기게 된다.
          int c = ex1.sum(a, b);
  
          System.out.println(c); //3
      }
  }
  ```



- return만 단독으로 써서 메소드를 즉시 빠져나가는 방법

  - 파이썬과 달리 이러한 방법은 리턴 자료형이 void인 메소드에서만 사용할 수 있다. 
  - 리턴자료형이 명시되어 있는 메소드에서 return 문만 작성하면 컴파일 시 오류가 발생한다.

  ```java
  public void say_nick(String nickname) {
      if ("바보".equals(nickname)) {
          return;  //return문만 작성
      }
      System.out.println("나의 별명은 "+nickname+" 입니다.");
  }
  ```



- 메소드 내에서 선언된 변수의 효력 범위

  - 로컬변수: 메소드 내에서만 쓰이는 변수

  ```java
  class Example {
      //plus라는 메소드 내에서의 a와
      public void plus(int a) {
          a++;
      }
  
      //main 메소드에서의 a는 서로 다른 변수이다.
      public static void main(String[] args) {
          int a = 1;
          Example ex2 = new Example();
          ex2.plus(a);
          System.out.println(a);  //1
      }
  }
  ```

  - 객체를 넘길 경우
    - 위와 마찬가지로 메인 메소드와 동일한 이름의 객체를 조작
    - 위와는 다르게 객체 ex의 객체변수인 a의 값이 실제로 변한 것을 볼 수 있다.
    - 단, 객체 변수를 넘길 경우에는 객체변수는 변화하지 않는다. 객체 변수를 넘긴 것이지 객체 자체를 넘긴 것은 아니므로 값이 변화하지 않는다.
    - 메소드의 입력 파라미터가 값이 아닌 객체일 경우 메소드 내의 객체는 전달 받은 객체 그 자체로 수행된다.
    - 메소드의 입력항목이 값인지 객체인지를 구별하는 기준은 입력항목의 자료형이 primitive 자료형인지 아닌지에 따라 나뉜다.

  ```java
  public class Example {
  
      int a;  // 객체변수 a를 선언
  	
      //메소드
      public void plus(Example ex) {  //main메소드에 쓰인 ex와 동일한 이름으로 인자를 받아온다.
          ex.a++;
      }
  	
      //메인 메소드
      public static void main(String[] args) {
          Example ex = new Example();
          ex.a = 1;
          ex.plus(ex);
          System.out.println(ex.a); //2
      }
  }
  
  
  
  //this를 사용하여 아래와 같이 쓸 수도 있다.
  public class Example {
  
      int a;
  	
      //메소드
      public void plus() {  //굳이 인자를 적지 않고
          //this를 활용
          this.a++;
      }
  	
      //메인 메소드
      public static void main(String[] args) {
          Example ex = new Example();
          ex.a = 1;
          ex.plus(); //인자를 넘기지 않는다.
          System.out.println(ex.a); //2
      }
  }
  
  
  
  //객체 변수를 넘길 경우
  package first;
  
  public class Example {
  
      int a;  // 객체변수 a를 선언
  	
      //메소드
      public void plus(int a) { //객체 변수를 인자로 받는다.
          a++;
      }
  	
      //메인 메소드
      public static void main(String[] args) {
          Example ex = new Example();
          ex.a = 1;
          ex.plus(ex.a);  //객체변수를 넘긴다.
          System.out.println(ex.a); //1
      }
  }
  ```

  - `static`
    - 기본적으로 클래스는 인스턴스가 생성되지 않은 상태(인스턴스화 되지 않은 상태)에서 사용할 수 없다. 붕어빵 틀이 있다고 붕어빵을 먹을 수 없는 것과 마찬가지다.
    - main 메소드에는 `static` 키워드가 작성되어 있는데 클래스를 정의하고 인스턴스를 생성하지 않았음에도 main 메소드가 실행되었던 이유가 바로 이 때문이다. 예를 들어 아래에서 `method1` 이라는 메소드는 인스턴스를 생성해야 실행시킬 수 있지만 main메소드는 인스턴스가 없어도 실행이 된다.
    - `static` 키워드는 인스턴스가 생성되지 않았어도 static한 메소드나 필드를 사용할 수 있게 해준다. 
    - static한 메소드 내에서 static하지 않은 필드(변수)는 사용할 수 없다. static한 메소드가 실행되는 시점에 해당 클래스가 인스턴스화되지 않았을 수 있기 때문이다.
    - static한 메소드에서 static하지 않은 변수를 사용하기 위해서는 객체를 생성 해야 한다. 이때 모든 객체가 static하지 않은 변수 를 공유하는 것이 아니라 각 객체별로 static하지 않은 변수를 저장하는 공간이 따로 생기게 된다. 이는 인스턴스가 생성될 때 각 인스턴스의 저장 공간에 생성되는 변수이므로 `인스턴스 변수`라고 부른다.
    - 반면에 static한 변수는 모든 객체에 별도의 저장공간에 저장되지 않고, 따라서 모든 객체가 공유한다. 이렇게 모든 객체가 값을 공유하는 static한 변수를 `클래스 변수`라고 부른다.

  ```java
  package first;
  
  public class Example {
  
      int globalVariable=1;  // 객체변수
      static int staticVariable=3; //static Value
  	
      //메소드
      public void method1(int value) {
          int localVariable=2; //로컬변수
          System.out.println(globalVariable); //에러 발생X
          System.out.println(localVariable);	 //에러 발생X
          System.out.println(value);		 //에러 발생X
      }
  	
      //메인 메소드
      public static void main(String[] args) {
          System.out.println(globalVariable);   //에러가 발생
          System.out.println(localVariable);	  //에러가 발생
          System.out.println(staticVariable);   //에러 발생X
          
          //static한 메소드에서 static하지 않은 변수를 사용하는 방법
          Example variable1 = new Example();
          System.out.println(variable1.globalVariable); //에러 발생X
          
          Example variable2 = new Example();
          System.out.println(variable2.globalVariable); //에러 발생X
          
          //variable1과 variable2의 전역변수(static하지 않은 변수, 인스턴스 변수)에 각기 다른 값을 넣어보면 
          variable1.globalVariable=123;
          variable2.globalVariable=456;
          
          //각기 다르게 저장된 것을 확인할 수 있다.
          System.out.println(variable1.globalVariable);  //123
          System.out.println(variable2.globalVariable);  //456
          //만일 두 인스턴스가 동일한 globalVariable(static하지 않은 변수)을 공유한다면 variable1도 456이 출력되어야 할 것이나 그렇지 않았다.
          //따라서 각 인스턴스는 static하지 않은 변수를 각기 별도의 저장공간에 저장하고 있다는 것을 알 수 있다.
          
          
          //반면에 static 변수(클래스 변수)는
          variable1.staticVariable = 789;
          variable2.staticVariable = 101112;
          
          //객체 간에 서로 공유하는 것을 알 수 있다.
          System.out.println(variable1.staticVariable); //101112
          System.out.println(variable2.staticVariable); //101112
          
          //또한 클래스 변수는 클래스명로 접근해서 사용할 수 있다.
          System.out.println(Example.staticVariable); //101112
              
      }
  }
  
  //Example이라는 같은 클래스 안에 있음에도 main 메소드에서 globalValue를 사용할 수 없는 이유는 main 메소드에 static 키워드가 정의되어 있기 때문이다.
  //반면에 method1에서 에러가 발생하지 않는 이유는 method1은 static 메소드가 아니기 때문이다.
  ```

  



## 상속

- 클래스 상속

  - `extends` 키워드를 사용
  - `자식클래스 extends 부모클래스`

  ```java
  //animal.java
  public class Animal {
      String name;
  
      public void setName(String name) {
          this.name = name;
      }
  }
  
  
  //Dog.java
  //상속 기본 틀
  public class Dog extends Animal {
  
  }
  
  //아래와 같이 부모 클래스의 객체 변수와 메소드를 사용 가능하다.
  public class Dog extends Animal {
      
      //상속 받지 않고 추가적으로 정의한 메소드 sleep
      public void sleep() {
          System.out.println(this.name+" zzz");
      }
  
      public static void main(String[] args) {
          Dog dog = new Dog();
          
          //Animal 클래스에서 상속받은 setName 메소드와 객체변수 name 
          dog.setName("poppy");
          System.out.println(dog.name);
          dog.sleep();
      }
  }
  
  
  
  //자바에서 만드는 모든 클래스는 Object라는 클래스를 상속받게 되어 있다. 따라서 엄밀히 말하면 Animal 클래스도 아래와 같다. 다만 Object 클래스를 상속받는 것이 너무도 당연하므로 아래와 같이 적지는 않는다.
  public class Animal extends Object {
      String name;
  
      public void setName(String name) {
          this.name = name;
      }
  }
  ```

  - `IS-A`
    - 하위 클래스가 상위 클래스에서 상속을 받을 경우 하위 클래스는 상위 클래스에 포함된다고 할 수 있다.
    - 자바에서는 이 관계를 `IS-A`관계라고 표현한다.
    - 아래의 예시에서는 `Dog is a Animal`과 같이 말할 수 있다.
    - 이러한 관계에 있을 때 자식 객체는 부모 클래스를 자료형인 것처럼 사용할 수 있다.
    - 그러나 부모 클래스로 만들어진 객체는 자식 클래스를 자료형으로는 사용할 수 없다.
    - 상기했듯 모든 클래스는 Object라는 클래스를 상속받게 되어 있다.  따라서 모든 객체는 Object 자료형으로 사용할 수 있다. 

  ```java
  //자식 객체는 부모 클래스의 자료형인 것처럼 사용할 수 있지만
  Animal dog = new Dog();
  
  //아래와 같이 할 수는 없다.
  Dog dog = new Animal();
  
  //Animal dog = new Dog();는 "개로 만든 객체는 동물 자료형이다."로 읽을 수 있다.
  //Dog dog = new Animal();는 "동물로 만든 객체는 개 자료형이다."로 읽을 수 있다.
  //그러나 동물로 만든 객체는 고양이일 수도 있고, 호랑이일 수도 있다. 따라서 Dog dog = new Animal();와 같이 쓸 수는 없다.
  
  
  //모든 객체는 Object라는 클래스를 상속 받으므로 아래와 같은 코드가 가능하다.
  Object animal = new Animal();
  Object dog = new Dog();
  ```

  

- 메소드 오버라이딩

  - 부모클래스의 메소드를 자식클래스가 동일한 형태로 또다시 구현하는 행위
  - 상속 받은 클래스에 상속한 클래스와 동일한 형태(입출력이 동일)의 메소드를 구현하면 상속 받은 클래스의 메소드가 상속한 클래스의 메소드보다 더 높은 우선 순위를 갖게 된다.

  ```java
  //housedog.java
  //위에서 정의한 Dog 클래스를 상속
  
  //상속 받은 그대로 아래 클래스를 실행시키면 "Spring zzz"가 출력될 것이다.
  public class HouseDog extends Dog {
      public static void main(String[] args) {
          HouseDog houseDog = new HouseDog();
          houseDog.setName("Spring");
          houseDog.sleep();
      }
  }
  
  
  //아래와 같이 클래스를 수정하면  "Spring zzz in house"가 출력될 것이다.
  public class HouseDog extends Dog {
      public void sleep() {
          System.out.println(this.name+" zzz in house");
      } 
  
      public static void main(String[] args) {
          HouseDog houseDog = new HouseDog();
          houseDog.setName("Spring");
          houseDog.sleep();  //Spring zzz in house
      }
  }
  ```



- 메소드 오버로딩

  -  입력항목이 다른 경우 동일한 이름의 메소드를 만드는 것

  ```java
  public class HouseDog extends Dog {
      //이 메소드와
      public void sleep() {
          System.out.println(this.name+" zzz in house");
      } 
  	
      //이 메소드는 이름이 완전히 같지만 입력항목이 다르므로 동일한 이름으로 생성할 수 있다.
      public void sleep(int hour) {
          System.out.println(this.name+" zzz in house for " + hour + " hours");
      } 
  
      public static void main(String[] args) {
          HouseDog houseDog = new HouseDog();
          houseDog.setName("Spring");
          houseDog.sleep();    //Spring zzz in house
          houseDog.sleep(3);   //Spring zzz in house for 3 hours
      }
  }
  ```



- 다중 상속

  - 클래스가 동시에 하나 이상의 클래스를 상속 받는 것, Java는 다중 상속을 지원하지 않는다.
  - 만일 다중 상속을 지원한다면 아래와 같은 문제가 생긴다. 따라서 이러한 문제를 없애기 위해 Java는 다중상속을 지원하지 않는다.

  ```java
  //아래 코드는 실행되지 않는 코드이다.
  
  class A {
      public void msg() {
          System.out.println("A message");
      }
  }
  
  class B {
      public void msg() {
          System.out.println("B message");
      }
  }
  
  class C extends A, B {
      public void static main(String[] args) {
          C test = new C();
          test.msg();  //이 메소드는 A클래스의 메소드인지, B클래스의 메소드인지 불명확하다.
      }
  }
  ```





## 생성자

- 메소드명이 클래스명과 동일하고 리턴 자료형이 없는 메소드를 생성자(Constructor)라고 말한다.

  - 즉, 생성자는 다음의 규칙을 따른다
    - 클래스명과 메소드명이 동일하다.
    - 리턴타입을 정의하지 않는다.
  - `new`
    - 생성자는 객체가 생성될 때 호출된다.
    - 객체가 생성될 때는 `new`라는 키워드로 객체가 만들어질 때이다.
    - 즉, 생성자는 `new`라는 키워드가 사용될 때 호출된다.

  ```java
  //Animal, Dog, 클래스는 위에서 작성한 것과 동일, HouseDog클래스는 아래와 같이 main 메소드 수정
  public class HouseDog extends Dog {
      public void sleep() {
          System.out.println(this.name+" zzz in house");
      } 
  
      public void sleep(int hour) {
          System.out.println(this.name+" zzz in house for " + hour + " hours");
      } 
  
      public static void main(String[] args) {
          HouseDog dog = new HouseDog();
          System.out.println(dog.name); //name객체 변수에 아무 값도 설정하지 않았으므로 null이 출력
      }
  }
  
  
  //위 상황에서 객체 변수에 값을 설정해야만 객체가 생성될 수 있도록 강제하는 방법
  public class HouseDog extends Dog {
      
      //아래 메소드를 추가(생성자)
      public HouseDog(String name) {
          this.setName(name);
      } 
      
      public void sleep() {
          System.out.println(this.name+" zzz in house");
      } 
  
      public void sleep(int hour) {
          System.out.println(this.name+" zzz in house for " + hour + " hours");
      } 
  
      public static void main(String[] args) {
          HouseDog dog = new HouseDog("Spring"); 
          //생성자를 작성했으므로 아래와 같이 객체를 생성할 경우 오류가 발생한다(아래 default 생성자 참고).
          //HouseDog dog = new HouseDog();
          System.out.println(dog.name); //Spring
      }
  }
  ```



- default 생성자

  - 생성자의 입력 항목이 없고 생성자 내부에 아무 내용이 없는 생성자를 default 생성자라고 부른다.

  - 디폴트 생성자를 구현하면 해당 클래스의 인스턴스가 만들어질 때 디폴트 생성자가 실행된다.
  - 클래스에 생성자가 하나도 없을 경우 컴파일러는 자동으로 디폴트 생성자를 추가한다.
  - 작성된 생성자가 하나라도 있다면 컴파일러는 디폴트 생성자를 추가하지 않는다.
    - 위 예시에서 `HouseDog dog = new HouseDog();`라는 코드가 에러를 발생시키는 이유가 바로 이 때문으로 이 코드는 default 생성자를 사용한 것이다.
    - 개발자가 생성자를 만든 후에는 컴파일러는 default 생성자를 추가하지 않고 따라서 위 코드는 생성자가 존재하지 않게 되어 에러가 발생한다.

  ```java
  //즉 본래 HouseDog 클래스에는 아래와 같이 컴파일러가 추가한 default 생성자가 존재했다.
  
  public class HouseDog extends Dog {
      //default 생성자
      public HouseDog() {
      }
      
  	//...중략...
      public static void main(String[] args) {
          //따라서 이 코드에서는 아래와 같이 생성이 가능했으나
          HouseDog dog = new HouseDog();
          System.out.println(dog.name); //null
      }
  }
  
  
  //아래와 같이 직접 생성자를 작성한 경우에는
  public class HouseDog extends Dog {
  	//직접 작성한 생성자
      public HouseDog(String name) {
          this.setName(name);
      } 
      
  	//...중략...
      public static void main(String[] args) {
          //더 이상 default 생성자가 없으므로 아래와 같이 생성은 불가능하고
          //HouseDog dog = new HouseDog();
          
          //새로 작성한 양식에 맞춰서 생성해줘야 한다.
          HouseDog dog = new HouseDog("Spring");
          System.out.println(dog.name); //Spring
      }
  }
  ```



- 생성자 오버로딩

  - 하나의 클래스에 여러개의 입력항목이 다른 생성자를 만들 수 있다.

  ```java
  public class HouseDog extends Dog {
      
      //생성자1
      public HouseDog(String name) {
          this.setName(name);
      }
  	
      //생성자2
      public HouseDog(int type) {
          if (type == 1) {
              this.setName("Summer");
          } else if (type == 2) {
              this.setName("Autumn");
          }
      }
  
      public static void main(String[] args) {
          //생성자1
          HouseDog happy = new HouseDog("Spring");
          //생성자2
          HouseDog yorkshire = new HouseDog(1);
          System.out.println(Spring.name);  //Spring
          System.out.println(Summer.name);  //Summer
      }
  }
  ```

  









