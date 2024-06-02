# 배열

- 배열(array)
  - 같은 타입의 여러 변수를 하나의 묶음으로 다루는 것을 배열이라 한다.
    - 중요한 것은 같은 타입이어야 한다는 것이며, 서로 다른 타입의 변수들로 구성된 배열은 만들 수 없다.
  - 배열은 각 저장공간이 메모리상에서 연속적으로 배치되어 있다.
    - 배열을 선언할 때 까지는 메모리에 데이터를 저장할 공간이 생기지 않는다.
    - 배열의 길이를 지정하여 배열을 생성하는 순간 메모리에 데이터를 연속적으로 저장할 공간을 할당한다.



- 배열의 선언과 생성

  - 배열의 선언
    - 원하는 타입의 변수를 선언하고 변수 또는 타입에 배열임을 의미하는 대괄호를 붙이면 된다.
    - 일반적으로는 타입 뒤에 붙인다.

  ```java
  타입[] 변수이름;
  ```

  - 배열의 생성
    - 배열을 생성할 때는 배열의 길이를 지정해야하며, 생성된 배열의 길이는 변경이 불가능하다.
    - 길이를 입력하지 않을 경우 길이가 0인 배열이 생성된다.

  ```java
  // 선언
  타입 [] 변수이름;
  // 생성
  변수이름 = new 타입[길이];
  ```

  - 선언과 생성을 동시에 할 수도 있다.

  ```java
  타입[] 변수이름 = new 타입[길이];
  ```



- 배열의 길이와 인덱스

  - 생성된 배열의 각 저장공간을 배열의 요소(element)라 하며, `배열이름[인덱스]`의 형식으로 배열의 요소에 접근할 수 있다.
    - Index는 배열의 요소마다 붙여진 일련번호로 각 요소를 구별하는데 사용된다.
    - Index는 0부터 시작한다.
  - 배열의 길이
    - 배열을 생성할 때 괄호 안에 배열의 길이를 적어줘야 하는데, 배열의 길이는 배열의 요소의 개수이다.
    - 배열의 길이의 최대값은 int type의 최대값이다.
    - 길이가 0인 배열도 생성하는 것이 가능하다.
    - `.length` 를 통해 배열의 길이를 알 수 있다.

  ```java
  int[] arr = new int [5];
  System.out.println(arr.length);	// 5
  ```

  - 배열의 길이 변경
    - 배열은 한 번 선언되고 나면 길이를 변경할 수 없다.
    - 따라서 배열의 길이를 변경하기 위해서는 더 큰 배열을 새로 생성한 후, 기존 배열의 내용을 새로운 배열에 복사해야한다.

  ```java
  int[] arr = new int[]{1, 2, 3, 4, 5};
  int[] longer_arr = new int[arr.length * 2];
  
  for(int i=0; i<arr.length; i++) {
      longer_arr[i] = arr[i];
  }
  
  arr = longer_arr;
  ```



- 배열의 초기화

  - 배열은 생성과 동시에 자동적으로 자신의 타입에 해당하는 기본값으로 초기화된다.
    - 따라서 배열을 사용하기 전에 따로 초기화를 해주지 않아도 된다.
    - 그러나 만약 원하는 값으로 초기화하려면 아래와 같이 해주면 된다.
    - 원래는 배열의 길이를 지정해야 하지만, 자동으로 중괄호 안의 값의 개수에 의해 배열의 길이가 결정되기에 배열의 길이는 지정하지 않아도 된다.

  ```java
  int[] numbers = new int[] {1,2,3,4,5};
  ```

  - 아래와 같이 `new 타입[]`을 생략하는 것도 가능하다.
    - 단, 이는 배열의 선언과 생성을 동시에 할 때만 가능하며, 선언과 생성을 따로 할 때는 불가능하다.

  ```java
  int[] numbers = {1,2,3,4,5};
  ```



- 문자형 배열

  - 배열의 타입이 String인 경우에도 int 배열의 선언과 생성 방법은 다르지 않다.
    - 초기화 방법 역시 동일하다.

  ```java
  String[] names = new String[3];
  // 초기화 방법도 동일하다.
  String[] name = new String[] {"Foo", "Bar", "Baz"};
  String[] name = {"Foo", "Bar", "Baz"};
  ```

  - char배열
    - 문자열은 문자를 연이어 늘어놓은 것을 의미하므로 문자배열인 char 배열과 같은뜻이다.
    - Java에서 문자열을 처리할 때 char 배열이 아닌 String class를 사용해서 문자열을 처리하는 이유는 String 클래스가 char 배열에 여러 가지 기능을 추가하여 확장한 것이기 때문이다.
    - 따라서 char 배열을 사용하는 것 보다 String class를 사용하는 것이 문자열을 다루기 더 편리하다.
    - 단, char 배열과 String의 중요한 차이 중 하나는 char 배열은 변경이 가능하지만 String은 변경이 불가능하다는 것이다.
    - String은 변경이 가능한 것 처럼 보일 뿐 사실은 변경이 발생할 때 마다 새로운 String 객체가 생성되는 것이다.
    - char 배열은 `println`을 통해 출력할 때 배열 내의 모든 char를 하나로 합쳐서 출력한다.

  - char 배열을 String으로, String을 char 배열로 변환하는 것이 가능하다.

  ```java
  public class Main {
      public static void main(String[] args) {
          String name = "John Doe";
          // String을 char배열로 변환
          // 출력 결과는 String을 출력한 것과 같아서 변환이 안됐다고 생각할 수 있으나 변환이 된 것이다.
          // 상기했듯 println은 char 배열을 출력할 때 모든 char를 하나로 합쳐서 출력한다.
          System.out.println(name.toCharArray());		// John Doe
          
          // char 배열을 String으로 변환
          char[] arr = {'a', 'b', 'c'};
          String str = new String(arr);s
      }
  }
  ```

  



- 배열과 관련된 method들

  - `Arrays.toString()`
    - 배열을 문자열로 변환한다.

  ```java
  import java.util.Arrays;
  
  public class Main {
      public static void main(String[] args) {
          int[] arr = new int[]{1, 2, 3, 4, 5};
          System.out.println(Arrays.toString(arr));	// [1, 2, 3, 4, 5]
      }
  }
  ```

  - `System.arraycopy()`
    - 배열을 효율적으로 복사해주는 method이다.
    - 첫 번째 인자로 source 배열, 두 번째 인자로 복사를 시작할 source 배열의 index, 세 번째 인자로 destination 배열, 네 번째 인자로 복사한 내용을 저장하기 시작할 destination 배열의 index, 다섯 번째 인자로 복사할 길이를 지정한다. 

  ```java
  import java.util.Arrays;
  
  public class Main {
      public static void main(String[] args) {
          int[] arr = new int[]{1, 2, 3, 4, 5};
          int[] longer_arr = new int[arr.length * 2];
          System.arraycopy(arr, 0, longer_arr, 0, arr.length);
          System.out.println(Arrays.toString(longer_arr));	// [1, 2, 3, 4, 5, 0, 0, 0, 0, 0]
      }
  }
  ```

  









# 클래스

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
  - 객체 변수는 도트 연산자 `.`을 통해 접근 가능하다.
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



- 접근제한자

  - 클래스 내에서 멤버의 접근을 제한하는 역할
  - 클래스는 필드(객체변수)와 메소드를 가진다. 클래스와 관련 없는 필드나 메소드는 막을 필요가 있다.
  - 캡슐화: 해당 클래스와 관련된 내용을 모아서 가지고 있는 것
  - 종류
    - public: 어떤 클래스든 접근할 수 있다.
    - protected: 자기 자신, 같은 패키지에 속한 클래스, 서로 다른 패키지의 상속받은 자식 클래스에는 접근할 수 있다.
    - private: 자기 자신만 접근할 수 있다.
    - default: 접근 제한자를 적지 않은 경우, 같은 패키지만 접근 가능

  ```java
  package first;
  
  public class Example {
  	public String pub = "pub";
  	protected String pro = "pro";
  	private String pri = "pri";
  	String def = "def";
  }
  
  
  //같은 패키지의 다른 클래스
  package first;
  
  public class Example2 {
  	public static void main(String[] args) {
  		Example ex1 = new Example();
  		System.out.println(ex1.pub); //pub
  		System.out.println(ex1.pro); //pro
  		//System.out.println(ex1.pri); //error가 발생
  		System.out.println(ex1.def); //def
  	}
  }
  
  
  //다른 패키지의 다른 클래스
  package com.eightcruz.javastudy;
  
  import first.Example;
  
  public class Hello {
  	public static void main(String[] args) {
  		Example ex1 = new Example();
  		System.out.println(ex1.pub); //pub
  //		System.out.println(ex1.pro); //error
  //		System.out.println(ex1.pri); //error
  //		System.out.println(ex1.def); //error
  	}
  }
  
  
  //다른 패키지의 다른 클래스에서 상속을 받은 경우
  package com.eightcruz.javastudy;
  
  import first.Example;
  
  public class Hello extends Example {
  	public static void main(String[] args) {
          //상속 받아서 상속 받은 클래스로 객체를 생성하면
  		Hello ex1 = new Hello();
  		System.out.println(ex1.pub); //pub
  		System.out.println(ex1.pro); //pro
  //		System.out.println(ex1.pri); //error
  //		System.out.println(ex1.def); //error
  	}
  }
  ```



## 추상 클래스

- 동물 이라고 했을 때 사람에 따라 강아지, 고양이, 사자, 호랑이 등 다양한 동물을 떠올릴 것이다. 이렇듯 구체적이지 않은 클래스를 추상 클래스라고 한다.



- 추상 클래스는 부모로서의 역할은 수행할수 있지만 객체는 생성할 수 없다.



- 클래스 내부의 메소드 중 하나라도 추상 메소드라면 해당 클래스는 추상 클래스가 된다.

  ```java
  //Bird.java
  package first;
  
  public abstract class Bird {
      
      // sing이라는 메소드는 새 마다 울음 소리가 다르므로 추상 메소드로 선언해야 한다. 
      // 클래스 내부의 메소드 중 하나라도 추상 메소드가 있으면 해당 클래스는 추상 클래스가 되어야 한다.
      // 따라서 이 클래스는 추상 클래스여야 한다.
      // 구체적으로 어떻게 울지 정할 수 없으므로 선언만 한다. ()가 붙으면 선언이 된 것으로 간주한다.
  	public abstract void sing();
      
      //추상 클래스라고 하더라도 추상 메소드가 아닌 메소드도 사용할 수 있다.
  	public void fly() {
  		System.out.println("날다");
  	}
  }
  ```
  
  ```java
  //Sparrow.java
  package first;
  
  public class Sparrow extends Bird {
  
  	@Override
      //부모 클래스에서 추상 메소드로 선언했으므로 상속 받은 클래스에서 구체적으로 내용을 입력해줘야 한다.
      //그렇지 않을 경우 에러가 발생한다.
  	public void sing() {
  		System.out.println("짹짹");
  	}
  	public static void main(String[] args) {
          //객체 생성 가능
  		Sparrow sp1 = new Sparrow();
  		sp1.sing();  //짹짹
  		sp1.fly();   //날다
  	}
  }
  ```






## 클래스 형변환

- 부모 클래스를 타입으로 가지는 자식 클래스의 인스턴스를 생성할 수 있다.

  - 이 때 부모가 가지고 있는 내용(메소드, 변수 등)만 사용 가능하며 비록 자식 클래스의 인스턴스라 할지라도 자식 클래스의 내용은 사용이 불가능하다.

  ```java
  //Car.java
  package first;
  
  public class Car {
  	//run 메소드
  	public void run() {
  		System.out.println("차가 달립니다.");
  	}
  }
  
  
  //Taxi.java
  package first;
  
  public class Taxi extends Car{
  	public void pickuppassenger() {
  		System.out.println("손님을 태웠습니다.");
  	}
  	public static void main(String[] args) {
  		//부모 타입으로 자식 클래스의 객체를 생성할 수 있다.
  		Car car1 = new Taxi();
  		//이 경우 부모가 가지고 있는 내용(메소드, 변수 등)만 사용 가능하다.
  		car1.run();   //차가 달립니다.
  		//비록 car1이 Taxi의 인스턴스라 할지라도 타입은 Car 타입이므로 아래 코드는 불가능하다.
  		//car1.pickuppassenger()
  	}
  }
  ```

  - 이 때 필요한 것이 형변환이다.

  ```java
  //Taxi.java
  package first;
  
  public class Taxi extends Car{
  	public void pickuppassenger() {
  		System.out.println("손님을 태웠습니다.");
  	}
  	public static void main(String[] args) {
  		Car car1 = new Taxi();
  		car1.run();
          //단순히 아래와 같이 할 수는 없다. Car 타입임에도 Taxi 타입인 변수에 담으려 하므로 에러가 발생
          //Taxi taxi1 = car1;
          //따라서 아래와 같이 형변환 후 담아야 한다.
          Taxi taxi1 = (Taxi)car1;
          
          //이제 아래와 같이 부모, 자식 클래스의 메소드를 모두 사용 가능하다.
          taxi1.run();   //차가 달립니다.
          taxi1.pickuppassenger() //손님을 태웠습니다.
  	}
  }
  ```





## 내부 클래스

- 내부 클래스: 클래스 안에 선언된 클래스



- 종류(4가지로 구분 가능)

  ```java
  package first;
  
  public class InnerClass {
      
      
      //1.중첩 클래스(인스턴스 클래스): 인스턴스 변수(필드)를 선언하는 위치에 선언하는 경우
  	class Inner1{
          //내부 클래스의 인스턴스 변수
  		int val = 1;
          //내부 클래스의 메소드
  		public void hello1() {
  			System.out.println("Inner Class1");
  		}
  	}
      
      
      
      //2.정적 중첩 클래스(스태틱 클래스): static 키워드를 사용, 필드를 선언할 때 스태틱으로 선언한 것과 유사하다고 생각하면 된다.
     	static class Inner2{
          int val = 2;
          //내부 클래스의 메소드
  		public void hello2() {
  			System.out.println("Inner Class2");
  		}
      }
      
      
      
      //3.지역 중첩 클래스(지역 클래스): 메소드 안에 클래스로 선언한 경우
      public void example(){
          class Inner2{
              int val = 3;
              //내부 클래스의 메소드
              public void hello3() {
                  System.out.println("Inner Class2");
              }
      	}
          //3) 지역 중첩 클래스 사용 방법: 메소드 안에서만 사용이 가능하다.
          Inner3 ic3 = new Inner3();
          System.out.println(ic3.val);
          ic3.hello3();
      }
      
      
      
      public static void main(String[] args) {
          
          //1) 중첩 클래스 사용 방법
  		InnerClass tmp = new InnerClass();
  		InnerClass.Inner1 ic1 = tmp.new Inner1(); 
  		System.out.println(ic1.val);   //1
  		ic1.hello1();  //Inner Class1
          
          //2)정적 중첩 클래스 사용 방법: 정적 클래스이기에 1번과 다른 방법으로 사용
          InnerClass.Inner2 ic2 = new InnerClass.Inner2();
          System.out.println(ic2.val);  //2
          ic2.hello2();  //Inner Class2
          
          //3) 지역 중첩 클래스 사용 방법: 메소드 안에서만 사용이 가능하므로 메소드를 실행시켜야 한다.
          InnerClass tmp2 = new InnerClass();
          tmp2.example(); //3 /n  Inner Class2 
  	}
  }
  
  ```



- 익명 중첩 클래스(익명 클래스)

  - 내부 클래스의 한 종류지만 내용이 길어 따로 분리
  - 부모 클래스를 상속받는 클래스를 굳이 만들 필요가 없을 경우에 사용한다.
  - 즉, 상속받는 클래스가 해당 클래스에서만 사용되고 다른 클래스에서는 사용되지 않는 경우에 사용한다.

  ```java
  //AbstClass.java
  package first;
  
  public abstract class AbstClass {
  	public abstract void example();
  }
  
  
  //InnerClass4.java
  package first;
  
  public class InnerClass4 extends AbstClass{
  	public void example() {
  		System.out.println("메세지 출력1");
  	}
  	
  	public static void main(String[] args) {
  		//아래는 기존의 방식
  		//AbstClass tmp = new InnerClass4();
  		//tmp.example();
  		
  		//익명 클래스는 위와 같은 방식으로 사용하지 않는다. 부모 클래스를 상속 받은 익명 클래스를 만들어서 사용한다.
          //생성자 다음에 중괄호 열고 닫고가 나오면, 해당 생성자 이름에 해당하는 클래스를 상속받는 이름없는 객체를 만든다는 것을 뜻한다.
          //중괄호 안에는 메소드를 구현하거나 메소드를 추가할 수 있다. 이렇게 생성된 이름 없는 객체를 tmp라는 참조변수가 참조하도록 하고, 
          //example()메소드를 호출하는 코드이다.
  		AbstClass tmp = new AbstClass() {
  			public void example() {
  				System.out.println("메세지 출력2");
  			}
  		};
  		tmp.example();
  	}
  }
  ```

  





# 메소드

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
  - 입력변수: 매개변수 혹은 인자라고 불린다.
    - 매개변수(Parameter, 인자): 전달된 인자를 받아들이는 변수
    - 인수(Argument): 어떤 함수를 호출시에 전달되는 값
  



- `this`: 메소드 내부에 사용된 `this`는 클래스에 의해서 생성된 객체를 지칭한다.

  - 아래 예시의 경우 메소드가 아닌 생성자이지만 `this`를 설명하는데는 지장이 없다.

  ```java
  //아래와 같은 코드의 경우 별 문제가 없지만
  package pract;
  
  public class method {
  	String name1= "이름";
  	
  	public method(String name2) {
  		name1=name2;
  	}
  	
  	public static void main(String[] args) {
  		method m1 = new method("이름2");
  		System.out.println(m1.name1); //이름2
  	}
  }
    
  //아래 코드의 경우 객체변수와 매개변수의 변수명이 같으므로 문제가 생긴다.
  package pract;
  
  public class method {
  	String name= "이름";
  	
  	public method(String name) {
  		name=name;  //이 줄에 사용 된 2개의 name은 모두 매개변수 name을 가리키게 된다.
          //즉 예시에 따르면 아래에서 이 메소드의 인자로 "이름2"를 받으므로
          //"이름2"="이름2"와 마찬가지인 코드다.
  		System.out.println(name); //이름2
  	}
  	
  	public static void main(String[] args) {
  		method m1 = new method("이름2");
          //따라서 객체변수 name은 바뀐 적이 없으므로 "이름"이 출력된다.
  		System.out.println(m1.name); //이름
  	}
  }
  
  //this를 사용하면 위와 같은 문제를 해결할 수 있다.
  package pract;
    
  public class method {
    	String name="이름1";
    	public method(String name) {
  		//this는 객체 자신을 가리키므로 아래 코드는 다음과 같다.
          //e1.name=name;
    		this.name=name;
    		System.out.println(name); //이름2
    	}
    	public static void main(String[] args) {
    		method m1 = new method("이름2");
        System.out.println(m1.name);  //이름2
    	}
  }
  ```




- 클래스에 정의된 메소드를 사용하기 위해서는 객체를 만들어야 한다.

  ```java
  package pract;
  
  public class animal {
  	String name;
      
      //setName이라는 메소드를 작성
      //void는 리턴값(출력)이없다는 의미이고, String iname은 iname이라는 문자열을 입력으로 받는 메소드라는 뜻이다.
  	public void setName(String iname) {
          //여기서 this는 Animal class에 의해 생성되어 이 함수를 실행시킨 객체인 cat을 가리킨다.
  		this.name=iname;
          //즉 아래 예시에 따라 아래 코드를 풀어쓰면 다음과 같다.
          //cat.name="Summer";
  	}
  	public static void main(String[] args) {
  		//객체 생성
  		animal cat = new animal();
  		cat.setName("Summer");
  		System.out.println(cat.name);  //Summer
  	}
  }
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
  
  - 기본적으로 클래스는 인스턴스가 생성되지 않은 상태(인스턴스화 되지 않은 상태)에서 사용할 수 없다. 붕어빵 틀만 있다고 붕어빵을 먹을 수 없는 것과 마찬가지다.
  - `static` 키워드는 인스턴스가 생성되지 않았어도 static한 메소드나 필드를 사용할 수 있게 해준다. 
    - main 메소드에는 `static` 키워드가 작성되어 있는데 클래스를 정의하고 인스턴스를 생성하지 않았음에도 main 메소드가 실행되었던 이유가 바로 이 때문이다. 예를 들어 아래에서 `method1` 이라는 메소드는 인스턴스를 생성해야 실행시킬 수 있지만 main메소드는 인스턴스가 없어도 실행이 된다.
  - static한 메소드 내에서 static하지 않은 필드(변수)는 사용할 수 없다. 
    - static한 메소드가 실행되는 시점에 해당 클래스가 인스턴스화되지 않았을 수 있기 때문이다.
    - static한 메소드에서 static하지 않은 변수를 사용하기 위해서는 객체를 생성 해야 한다. 
    - 이때 모든 객체가 static하지 않은 변수 를 공유하는 것이 아니라 각 객체별로 static하지 않은 변수를 저장하는 공간이 따로 생기게 된다. 
    - 이는 인스턴스가 생성될 때 각 인스턴스의 저장 공간에 생성되는 변수이므로 `인스턴스 변수`라고 부른다.
  - **garbage collection**의 관리 영역 밖에 존재하기에 Static영역에 있는 멤버들은 프로그램의 종료시까지 메모리가 할당된 채로 존재하게 된다. 
    - garbage collection: 프로그램이 동적으로 할당했던 메모리 영역 중에서 필요없게 된 영역을 해제하는 기능.
    - 그렇기에 Static을 너무 남발하게 되면 만들고자 하는 시스템 성능에 악영향을 줄 수 있다.
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
          System.out.println(globalVariable);   //에러가 발생(static한 메소드 내에서 static하지 않은 필드(변수)는 사용할 수 없다)
          System.out.println(localVariable);	  //에러가 발생
          System.out.println(staticVariable);   //에러 발생X(인스턴스를 생성하지 않아도 접근 가능)
          
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
  //반면에 method1에서 globalValue를 사용할 수 있는 이유는 method1은 static 메소드가 아니기 때문이다.
  ```








# 상속

- 클래스 상속

  - `extends` 키워드를 사용
  - `자식클래스 extends 부모클래스`
  - 이클립스에서는 상속 받을 클래스 생성시에 `Superclass`에서 상속 받을 클래스를 선택할 수 있다.
  - 단일상속만 가능하다.

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

  - `IS-A`(혹은 kind of 관계)
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
  - `@Overrride` 어노테이션을 붙이는 것과 안 붙이는 것의 차이
      - 어노테이션을 붙인 메서드가 부모 메서드를 오버라이드 하지 않으면 컴파일시 오류가 발생한다.
      - 이런 기능이 생긴 이유는 오버라이딩하던 부모 클래스가 변경되었을 경우 자식 클래스는 이를 알 수 있는 방법이 없다.
      - 따라서 오버라이딩이 아닌 새로운 메서드의 선언이 되어버린다.
      - 이런 현상을 방지하기 위해 어노테이션을 추가한 것이다.
  
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

  - 매개변수의 수, 매개변수의 타입이 다른 경우 동일한 이름으로 메소드를 여러 개 정의할 수 있다.
  - 즉, 입력항목이 다른 경우 동일한 이름의 메소드를 만들 수 있다.
  - 매개변수의 이름이 달라도 매개변수의 수,매개변수의 타입이 같다면 오버로딩이 불가능
  
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



- super

  - 부모 객체를 나타내는 키워드, 나를 가리키는 키워드가 this라면 부모를 가리키는 키워드는 super이다. 또한 `super()`는 부모의 생성자를 실행시키는 것이다.
  - super키워드는 자식 클래스에서 부모의 메서드나 필드를 사용할 때에도 사용 가능하다.
    - 예를 들어 부모 클래스에 run이라는 메소드가 있다면 자식 클래스에서는 이를 `super.run()`으로 실행 가능하다.
  - 자식 생성자가 실행 될 때 부모 생성자도 함께 실행된다.

  ```java
  //Car.java
  package first;
  
  public class Car {
  	public Car() {
  		System.out.println("Car의 기본 생성자");
  	}
  }
  
  //Taxi.java
  package first;
  
  //Car 클래스를 상속
  public class Taxi extends Car{
  	public Taxi() {
  		System.out.println("Taxi의 기본생성자");
  	}
  	public static void main(String[] args) {
          // Taxi의 객체가 생성되면 아래 out과 같은 메세지가 출력된다.
          // 즉 Taxi의 기본생성자 뿐 아니라 Car의 기본생성자도 함께 실행된다.
          // 또한 Car의 기본생성자가 먼저 실행된다.
  		Taxi taxi1 = new Taxi();
  	}
  }
  
  out
  Car의 기본 생성자  
  Taxi의 기본생성자
  
  //즉 Taxi.java의 코드는 사실 다음과 같다.
  package first;
  
  public class Taxi extends Car{
  	public Taxi() {
          super(); //이 코드가 생략된 것이다.
  		System.out.println("Taxi의 기본생성자");
  	}
  	public static void main(String[] args) {
  		Taxi taxi1 = new Taxi();
  	}
  }
  ```

  - 자동으로 실행됨에도 알아야 하는 이유는 다음과 같다.
    - 자식 생성자가 실행될 경우 컴파일러가 자동으로 실행하는 것은 부모 생성자의 기본생성자 뿐이다.
    - 따라서 부모의 생성자가 기본 생성자가 아닐 경우에 컴파일러가 자동으로 부모 생성자를 호출하지 못하게 되어 에러가 발생한다.
    - 따라서 생성자를 직접 호출해야 한다.

  ```java
  //Car.java
  package first;
  
  public class Car {
      //만일 부모의 생성자의 디폴트 생성자(기본생성자)를 없애고 아래와 같이 수정할 경우
  	public Car(String name) {
  		System.out.println("Car의 기본 생성자");
  	}
  }
  
  
  //Taxi.java
  //아래 코드는 실행되지 않는다.
  package first;
  
  public class Taxi extends Car{
  	public Taxi() {
  		System.out.println("Taxi의 기본생성자");
  	}
  	public static void main(String[] args) {
  		Taxi taxi1 = new Taxi();
  	}
  }
  
  
  //따라서 아래와 같이 수정해줘야 한다.
  //Taxi.java
  package first;
  
  public class Taxi extends Car{
  	public Taxi() {
          super("택시")
  		System.out.println("Taxi의 기본생성자");
  	}
  	public static void main(String[] args) {
  		Taxi taxi1 = new Taxi();
  	}
  }
  ```



- 오버로딩과 오버라이딩

  |                | 오버로딩  | 오버라이딩 |
  | -------------- | --------- | ---------- |
  | 메서드 이름    | 동일      | 동일       |
  | 매개변수, 타입 | 다름      | 동일       |
  | 반환 타입      | 상관 없음 | 동일       |

  



# 생성자

- 메소드명이 클래스명과 동일하고 리턴 자료형이 없는 메소드를 생성자(Constructor)라고 말한다.

  - 즉, 생성자는 다음의 규칙을 따른다
    - 클래스명과 메소드명이 동일하다.
    - 리턴타입을 정의하지 않는다.
  - 생성자의 특징
    - 생성자는 자바 클래스의 멤버가 아니다.
    - 상속되지 않는다.
    - 상속 받은 클래스를 생성하면, 상속한 클래스의 생성자도 호출된다.
    - 오버라이딩의 대상이 될 수 없다.
    - 일반적인 메소드 호출 방법으로 호출할 수 없다.
  - `new`
    - 생성자는 객체가 생성될 때 호출된다.
    - 객체가 생성될 때는 `new`라는 키워드로 객체가 만들어질 때이다.
    - 즉, 생성자는 `new`라는 키워드가 사용될 때 호출된다.
  - 생성자를 만드는 이유는 객체를 생성할 때 필드를 초기화 하기 위함이다. 
    - 예를 들어 만일 동물 객체를 생성할 때 이름이라는 필드를 사용자가 지정한 이름으로 초기화 하여 생성하고자 할 때 사용한다. 
  
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

  - `this` 와 생성자 오버로딩
    - `this` 바로 뒤에 `()`를 붙이면 자신의 생성자를 호출한다.
  
  ```java
  package first;
  
  public class Example {
  	String name;
  	int number;
  	
  	//매개변수 입력 없이 생성할 경우 이름은 미정으로, 숫자는 0000으로 초기화 하고자 작성한 생성자
  	public Example() {
  		this.name = "미정";
  		this.number = 0000;
  	}
  	
  	//매개변수를 입력 받았을 경우 매개변수로 초기화 하고자 하는 생성자
  	public Example(String name, int number) {
  		this.name = name;
  		this.number = number;
  	}
      
  }
  
  
  //위에서 두 생성자는 내용이 거의 겹치는데 굳이 유사한 코드를 반복작성하지 않고 this를 사용하면 아래와 같이 작성이 가능하다.
  package first;
  
  public class Example {
  	String name;
  	int number;
  	
      //생성자1번
  	public Example() {
  		this("미정",0000); //이를 통해 입력 타입과 갯수가 맞는 아래 생성자 2번이 호출, 실행된다.
  	}
  	
      //생성자2번
  	public Example(String name, int number) {
  		this.name = name;
  		this.number = number;
  	}
      
  	public static void main(String[] args) {
  		Example e1 = new Example();
  		System.out.println(e1.name);    //미정
  		System.out.println(e1.number);  //0000
  	}
  }  
  ```





# 패키지

- 패키지
  - 서로 관련 있는 클래스 또는 인터페이스들을 묶어 놓은 묶음
  - 클래스들이 필요할 때만 사용될 수 있도록 할 수 있고, 다른 그룹에 속한 클래스와 발생할 수 있는 클래스 이름간 충돌을 막아줌으로써 클래스의 관리를 편하게 해준다.
  - 패키지 이름은 대부분 도메인 이름을 거꾸로 적은 후 프로젝트 이름을 붙여 사용, 패키지가 있는 클래스를 사용할 때는 `import`사용
  - 도메인을 거꾸로 적기에 `.`을 사용하게 되는데 `.`으로 분절된 바로 첫 글자로 숫자는 올 수 없다.



- 생성 방법

  - src디렉토리에서 `new`선택 -  `Package` 선택

  - 패키지 이름 작성

    - 예를 들어 도메인 명이 `javastudy.eightcruz.com`이면 `com.eightcruz.javastudy`와 같이 작성
    - 생성된 패키지 파일 우클릭 후 클래스 생성

    ```java
    package com.eightcruz.javastudy;  //package이름
    
    public class Hello {
    
    }
    ```



- 다른 디렉토리에서 사용하는 방법

  - `import` 를 써야 한다.
  - 패키지의 특정 클래스가 아닌 모든 클래스를 쓰고자 한다면 `package이름.*`으로 작성한다.
  - `ctrl`+`shift`+`o`를 누르면 작성한 코드 중 import 해야 하는 import문이 자동으로 작성된다.

  ```java
  package first;   //first 디렉토리(다른 디렉토리)에서 사용하려면
  
  import com.eightcruz.javastudy.Hello;  //import 해야 한다.
  //아래와 같이 쓰면 Hello 클래스 뿐 아니라 package의 모든 클래스를 전부 import하겠다는 뜻이다.
  //import com.eightcruz.javastudy.*;
  
  public class PackageExample {
  	Hello h1 = new Hello();
      //만일 import 하지 않았을 경우 아래와 같이 작성해야 한다.
      //com.eightcruz.javastudy.Hello hello = new com.eightcruz.javastudy.Hello()
  }
  ```

  



# 인터페이스

- 인터페이스: 서로 관계가 없는 물체들이 상호 작용을 하기 위해서 사용하는 장치나 시스템



- 사용 이유

  - 개에게는 사과를, 고양이에게는 바나나를 먹이로 준다고 가정하고 이를 코드로 표현하면 다음과 같다.

  ```java
  //Animal.java
  package first;
  
  public class Animal {
  	String name;
  	public void setName(String name) {
  		this.name=name;
  	}
  }
  
  //Dog.java
  public class Dog extends Animal{
      
  }
  
  //Cat.java
  public class Cat extends Animal{
      
  }
  
  //Zookeeper.java
  package first;
  
  public class Zookeeper{
    
    //입력값의 자료형 타입이 다를 경우 메소드 명을 동일하게 사용할 수 있다(메소드 오버로딩)
    //class는 하나의 자료형이 될 수 있다.
    //아래 예시에서 첫 번재 feed 메소드는 Dog이라는 자료형(클래스인 자료형)을 입력값으로 받고, 두 번째 feed 메소드는 Cat이라는 자료형(클래스인 자료형)을 입력값으로 받으므로 서로 다른 타입의 자료형을 받으므로 메소드 오버로딩이 가능하다.
    public void feed(Dog dog){
        System.out.println("사과를 먹였습니다.");
    }
    public void feed(Cat cat) {
  	  System.out.println("바나나를 먹였습니다.");
    }
    public static void main(String[] args) {
  	  Zookeeper zk1 = new Zookeeper();
  	  Dog d1 = new Dog();
  	  Cat c1 = new Cat();
  	  zk1.feed(d1);   //사과를 먹였습니다.
  	  zk1.feed(c1);   //바나나를 먹였습니다.
    }
  }
  ```

  - 만일 개, 고양이 뿐 아니라 먹여야 할 동물이 수 백가지라면 수 백개의 메소드를 일일이 작성해야 할 것이다.

  ```java
  //Zookeeper.java
  //...전략
  public void feed(Snake snake){
      System.out.println("수박을 먹였습니다.");
  }
  public void feed(Parrot parrot) {
      System.out.println("키위를 먹였습니다.");
  }
  //...후략
  ```

  - 이럴 때 인터페이스를 사용하면 훨씬 간편하게 작성이 가능하다.
    - 인터페이스의 메소드에는 입출력에 대한 정의만 있고 내용은 없는데 메소드의 내용은 인터페이스를 `implements`한 클래스들에 구현한다.

  ```java
  //ZooAnimals.java
  package first;
  
  //class가 아닌 interface를 사용
  public interface ZooAnimal{
      //동물 별로 다른 먹이를 주기 위한 메소드
      //다른 메소드와 달리 입출력에 대한 정의만 있고 내용은 없다(추상 메소드와 유사).
  	public String getFood();
  }
  
  //Dog, Cat 클래스도 아래와 같이 변경
  //Dog.java
  public class Dog extends Animal implements ZooAnimal{
      //인터페이스에서 정의하지 않은 메소드의 내용을 정의(추상 메소드와 유사하게 implements 해놓고 작성하지 않으면 에러가 발생한다.)
      public String getFood(){
          return "사과";
      }
  }
  
  //Cat.java
  public class Cat extends Animal implements ZooAnimal{
      //인터페이스에서 다 정의하지 않은 메소드의 내용을 정의
      public String getFood(){
          return "바나나";
      }
  }
  
  //Zookeeper.java
  package first;
  
  public class Zookeeper{
  	public void feed(ZooAnimal zooanimal) {
          // feed() 메소드는 ZooAnimal 자료형 타입을 매개변수로 받는다.
          // 그러나 Dog, Cat 클래스의 인스턴스를 인자로 넘겼음에도 에러가 발생하지 않는다.
  	    System.out.println(zooanimal.getFood()+"를 먹였습니다.");
  	}
    public static void main(String[] args) {
  	  Zookeeper zk1 = new Zookeeper();
  	  Dog d1 = new Dog();
  	  Cat c1 = new Cat();
  	  zk1.feed(d1);  //사과를 먹였습니다.
  	  zk1.feed(c1);  //바나나를 먹였습니다.
    }
  }
  ```
  
  - 이제 변경된 class에서 선언된 객체들(d1,c1)은 각기 Dog, Cat라는 class의 객체이게도 하지만 ZooAnimal라는 interface의 객체이기도 하다. 
  - 따라서 위 처럼 ZooAnimal을 자료형 타입으로 사용가능하다.
    - 이와 같이 객체가 한 개 이상의 자료형 타입을 갖게 되는 특성을 다형성(폴리모피즘)이라 한다.
  - 만일 새로운 동물을 추가하고 싶을 경우 새로운 동물 클래스를 작성할 때 아래와 같이 하기만 하면 된다.
  
  ```java
  //Snake.java
  package first;
  
  public class Snake extends Animal {
  	public String getFood(){
          return "수박";
      }
  }
  
  //Parrot.java
  package first;
  
  public class Parrot extends Animal {
  	public String getFood(){
          return "키위";
    }
  }
  ```
  
  - 위의 예시를 통해 알 수 있는 인터페이스의 핵심은 필요한 메소드의 갯수가 줄었다는 점이 **아니라** `ZooKeeper` class가 동물들의 종류에 의존적인 클래스에서 동물들의 종류와 무관한 **독립적인 클래스**가 되었다는 점이다. 바로 이 점이 인터페이스를 사용하는 이유이다.



- 인터페이스는 USB포트와 유사하다.
  - 만일 USB포트가 없을 경우 컴퓨터(위 예시에서 ZooKeeper)에는 컴퓨터에 연결 할 수 있는 각종 기기들(마우스, 키보드, 외장하드 등, 위 예시에서 각종 동물들)을 컴퓨터와 연결할 수 있는 단자를 모두 구비해야 할 것이다. 
  - 이런 상황에서는 컴퓨터에 연결 할 수 있는 기기가 늘어날수록  컴퓨터 역시 이에 맞춰서 단자를 늘리며 변화해야 한다(즉, 컴퓨터는 주변 기기에 독립적이지 못하고 주변 기기에 의존적으로 변화해야 한다).
  - 그러나 모든 기기들이 규격화된 USB 포트를 사용할 경우 컴퓨터는 USB 단자만 있으면 되고 어떤 기기들이 새로 만들어졌는지 신경쓸 필요가 없어진다(독립적).



- 다형성(Polymorphism)

  - 객체지향 프로그래밍의 특징 중 하나
  - 객체가 한 개 이상의 자료형 타입을 갖게 되는 특성을 말한다.

  ```java
  //Bouncer.java, Dog, Cat등은 위에서 작성한 코드와 동일
  package first;
  
  public class Bouncer {
  	//Animal 자료형임에도 Dog나 Cat 객체를 인자로 받을 수 있는 이유는 두 클래스가 Animal을 상속받기 때문이다.
      //자식클래스에 의해서 만들어진 객체는 언제나 부모 클래스의 자료형으로 사용할 수가 있다.
  	//즉 다음과 같은 코딩이 가능하다.
  	//Animal dog1 = new Dog();
  	//Animal cat1 = new Cat();
  	public void barkAnimal(Animal animal) {
      	//만일 입력받은 Animal 클래스의 객체가 Dog 클래스의 객체면 멍멍을 출력
          if (animal instanceof Dog) {
              System.out.println("멍멍");
            //만일 입력받은 Animal 클래스의 객체가 Cat 클래스의 객체면 야옹을 출력
          } else if (animal instanceof Cat) {
              System.out.println("야옹");
          }
      }
  
      public static void main(String[] args) {
          Tiger dog1 = new Dog();
          Lion cat1 = new Cat();
  
          Bouncer bouncer= new Bouncer();
          bouncer.barkAnimal(dog1);
          bouncer.barkAnimal(cat1);
      }
  }
  ```

  - 위 예시에서 Snake, Parrot등이 추가되면 메소드 역시 아래와 같이 바뀌게 된다.
    - 동물이 하나씩 증가할 때마다 이런 식으로 증가시키는 것은 비효율적이다.
    - 따라서 이를 인터페이스로 작성할 필요가 있다.

  ```java
  public void barkAnimal(Animal animal) {
      if (animal instanceof Dog) {
          System.out.println("멍멍");
      } else if (animal instanceof Cat) {
          System.out.println("야옹");
      } else if (animal instanceof Snake) {
          System.out.println("쉭쉭");
      } else if (animal instanceof Parrot) {
          System.out.println("짹짹");
      }
  }
  ```

  - 인터페이스를 적용하기 위해 코드를 수장하면 다음과 같다.

  ```java
  //Barkable.java파일 생성
  public interface Barkable {
      public void bark();
  }
  
  //Dog.java
  package first;
  
  //인터페이스는 아래에서 알 수 있듯이 ,로 구분하여 여러 개를 implements 할 수 있다.
  public class Dog extends Animal implements ZooAnimal, Barkable{
      public String getFood(){
          return "사과";
      }
      
      //아래 코드를 추가
      public void bark() {
          System.out.println("멍멍");
      }
  }
  
  //Cat.java
  package first;
  
  public class Cat extends Animal implements ZooAnimal, Barkable{
      public String getFood(){
          return "바나나";
      }
      
      //아래 코드를 추가
      public void bark() {
          System.out.println("야옹");
      }
  }
  
  
  //Bouncer.java의 barkAnimal메소드는 아래와 같이 수정
  //Tiger의 객체와 Lion의 객체는 Animal의 객체이기도 하고 ZooAnimal의 객체이기도 하다.
  //따라서 아래 메소드의 인자의 자료형을 Animal에서 Barkable로 바꿔서 사용할 수 있다.
  public void barkAnimal(Barkable animal) {
      animal.bark();
  }
  ```

  - 지금까지 살펴본 바에 따르면 Dog 클래스의 객체는 Dog의 객체이면서, Animal의 객체이고, Barkable의 객체며, ZooAnimal의 객체이기도하다. 
    - 이와 같이 하나의 객체가 여러개의 자료형 타입을 갖는 것을 다형성이라한다.
    - 따라서 아래와 같이 여러 자료형으로 표현할 수 있다.

  ```java
  Tiger tiger1 = new Dog();
  Animal animal1 = new Dog();
  ZooAniaml zooAniaml1 = new Dog();
  Barkable barkable1 = new Dog();
  ```

  - 단, 각기 다른 클래스로 선언된 객체들은 사용할 수 있는 메소드가 서로 다르다.
    - ZooAniaml 인터페이스의 객체인 zooAniaml1은 ZooAniaml 에 선언된 getFood메소드만 호출이 가능하고 bark메소드는 호출할 수 없다.
    - 각기 다른 클래스로 선언된 객체들이 자신이 생성된 클래스가 아닌 다른 클래스의 메소드를 사용하게 하고자 한다면 아래 두 방법중 하나를 사용하면 된다.
    - 두 번째 방법이 가능한 이유는 인터페이스는 일반 클래스와 달리 `extends` 를 이용하여 여러개의 인터페이스를 동시에 상속 받을 수 있기 때문이다(일반 클래스는 단일 상속만 가능하다.).

  ```java
  //BarkableZooAniaml.java
  //방법1.사용하고자 하는 메소드를 모두 합해 새로운 인터페이스를 생성
  public interface BarkableZooAniaml  {
      public void bark();
      public String getFood();
  }
  
  //BarkableZooAniaml.java
  //방법2. 사용하고자 하는 메소드가 있는 인터페이스를 상속 받아 생성
  public interface BarkablePredator extends Predator, Barkable {
  }
  
  
  
  //위 두 방식 중 한 방식으로 인터페이스 생성 후 각 동물 클래스를 아래와 같이 수정
  //Dog.java
  public class Dog extends Animal implements BarkableZooAniaml {
      public String getFood() {
          return "사과";
      }
  
      public void bark() {
          System.out.println("멍멍");
      }
  }
  
  //Cat.java
  package first;
  
  public class Cat extends Animal implements BarkableZooAniaml{
      public String getFood(){
          return "바나나";
      }
      
      //아래 코드를 추가
      public void bark() {
          System.out.println("야옹");
      }
  }
  ```

  - 자식 인터페이스로 생성한 객체의 자료형은 부모 인터페이스로 사용하는 것이 가능하다.
    - 예를 들어 위에서 Bouncer 클래스의 barkAnimal 메소드의 입력 자료형이 Barkable이더라도 BarkablePredator를 구현한 Dog 클래스의 객체를 인자로 전달 할 수 있다. 
    - 자식 클래스의 객체 자료형을 부모 클래스의 자료형으로 사용가능하다는 점과 동일하다.



- default 메소드와 static 메소드

  - JAVA 8부터 적용되는 개념
  - 본래 인터페이스 파일에 작성하는 메소드는 추상 클래스에 작성하는 메소드와 마찬가지로 간략하게 적고 실제 메소드의 내용은 해당 인터페이스를 사용하는 클래스에 작성했다. 
  - 그러나, 인터페이스에서 `default` 또는`static` 키워드를 사용하면 메소드의 내용까지 인터페이스에 작성이가능하다. 
  - 이 경우 굳이 클래스에 해당 메소드를 다시 구현할 필요가 없다. 

  ```java
  //Calculator.java
  package first;
  
  public interface Calculator {
      //기존 방식
  	public int plus(int a , int b);
  	public int minus(int a, int b);
  	
      //default 키워드를 사용하여 인터페이스 내부에 메소드의 내용까지 구현
  	default int exec(int a, int b) {
  		return a+b;
  	}
      
      //static 키워드를 사용하여 인터페이스 내부에 메소드의 내용까지 구현
      public static int exec2(int a, int b) {
  		return a+b;
  	}
  }
  
  
  
  //Cal.java
  //class파일 생성시 interface를 추가 할 때 Calculator.java를 추가하고 생성하면 기본적인 코드가 작성된 채로 생성된다.
  package first;
  
  public class Cal implements Calculator {
  	
      
      //아래 두 메소드와 달리 default, static으로 구현한 메소드는 다시 구현하지 않아도 사용이 가능하다.
  	@Override
  	public int plus(int a, int b) {
  		// TODO Auto-generated method stub
  		return a+b;
  	}
  
  	@Override
  	public int minus(int a, int b) {
  		// TODO Auto-generated method stub
  		return a-b;
  	}
  	public static void main(String[] args) {
          
          //default 메소드 실행 방법
  		Calculator cal1 = new Cal();
  		System.out.println(cal1.plus(1,2)); //3
  		System.out.println(cal1.exec(1,2)); //3
          
          
          //satatic 메소드는 위와 같은 방법으로 실행시킬 수 없다.
          //cal1.exec2(1,2)  //error 발생
          
          //static 메소드는 아래와 같이 인터페이스명.메소드명()형식으로 사용이 가능하다.
          System.out.println(Calculator.exec2(1,2)); //3
  	}
  }
  ```

  - default 키워드가 사용된 메소드의 경우 오버라이딩도 가능하다(static 키워드가 사용된 메소드는 불가능)

  ```java
  package first;
  
  public class Cal implements Calculator {
  
  	@Override
  	public int plus(int a, int b) {
  		// TODO Auto-generated method stub
  		return a+b;
  	}
  
  	@Override
  	public int minus(int a, int b) {
  		// TODO Auto-generated method stub
  		return a-b;
  	}
  	
  	public int exec(int a, int b) {
  		return a*b;
  	}
  	
  	public int exec2(int a, int b) {
  		return a/b;
  	}
  	
  	public static void main(String[] args) {
  		Calculator cal1 = new Cal();
          //오버라이딩 적용되어 3*2가 실행
  		System.out.println(cal1.exec(3,2));  //6
  		
          //오버라이딩 적용되지 않아 9+3이 실행
  		System.out.println(Calculator.exec2(9,3));  //12
  	}
  }
  ```

  

  